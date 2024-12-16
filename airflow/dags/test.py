from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import dvc.api
import pandas as pd
import dask.dataframe as dd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Dataset as SurpriseDataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise import accuracy
import numpy as np

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Config paths
data_raw = "data/2019-Nov.csv"
data_processed = "processed_data/output.csv"

with DAG(
    dag_id="data_processing_pipeline",
    default_args=default_args,
    description="DAG for processing large datasets and recommendation models with DVC and S3",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["data-processing"],
) as dag:

    def process_raw_data():
        try:
            # Load and process raw data
            ddf = dd.read_csv(data_raw, blocksize=100000)

            # Clean missing data
            ddf = ddf.fillna({'category_code': 'Unknown', 'brand': 'Unknown', 'event_type': 'Unknown'})
            ddf['price'] = ddf['price'].fillna(ddf['price'].quantile(0.5))
            ddf = ddf[ddf['price'] > 0]  # Remove invalid price rows

            # One-hot encoding
            one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            categorical_cols = ['category_code', 'brand', 'event_type']
            categorical_data = ddf[categorical_cols].compute()
            one_hot_encoded = one_hot_encoder.fit_transform(categorical_data)
            one_hot_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_cols))

            # Combine with original DataFrame
            ddf = ddf.drop(columns=categorical_cols)
            ddf = dd.concat([dd.from_pandas(one_hot_df, npartitions=ddf.npartitions), ddf.reset_index(drop=True)], axis=1)

            # Normalize price
            scaler = StandardScaler()
            ddf['price'] = dd.from_array(scaler.fit_transform(ddf['price'].compute().values.reshape(-1, 1)))

            # Save processed data
            ddf.compute().to_csv(data_processed, index=False)
            print("Data processing completed and saved.")

        except Exception as e:
            print(f"Error in process_raw_data: {e}")

    def train_models():
        try:
            # Load processed data
            df = pd.read_csv(data_processed)

            # Train-test split
            X = df.drop(columns=['price'])  # Input features
            y = df['price']  # Target variable
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Baseline RMSE
            baseline_pred = [y_train.mean()] * len(y_test)
            rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
            print(f"Baseline RMSE: {rmse:.4f}")

            # Collaborative Filtering
            if 'user_id' in df.columns and 'product_id' in df.columns:
                reader = Reader(rating_scale=(1, 5))
                data = SurpriseDataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
                trainset, testset = surprise_train_test_split(data, test_size=0.2)

                svd = SVD()
                svd.fit(trainset)

                predictions = svd.test(testset)
                print("Collaborative Filtering RMSE:", accuracy.rmse(predictions))

        except Exception as e:
            print(f"Error in train_models: {e}")

    def version_data():
        try:
            # DVC versioning and push to S3
            import subprocess
            dvc_command = [
                "dvc", "add", data_processed,
                "&&", "dvc", "push"
            ]
            subprocess.run(" ".join(dvc_command), shell=True, check=True)
            print("Data versioned and pushed to S3.")
        except Exception as e:
            print(f"Error in version_data: {e}")

    # Define tasks
    process_task = PythonOperator(
        task_id="process_raw_data",
        python_callable=process_raw_data,
    )

    train_task = PythonOperator(
        task_id="train_models",
        python_callable=train_models,
    )

    version_task = PythonOperator(
        task_id="version_data",
        python_callable=version_data,
    )

    # Task dependencies
    process_task >> train_task >> version_task
