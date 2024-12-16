import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise import accuracy
import numpy as np
import dask.dataframe as dd

# Đường dẫn đến file CSV
file_path = 'data/2019-Nov.csv' # CẦN THAY THẾ SANG LẤY DỮ LIỆU TỪ API
chunksize = 100000  # Số dòng trong mỗi chunk

# Khởi tạo các biến toàn cục
missing_values = None

try:
    # không cần chia nữa, chia ở bước ingestion rồi

    # Đọc và xử lý từng chunk sử dụng Dask
    ddf = dd.read_csv(file_path, blocksize=chunksize) # CẦN THAY THẾ SANG LẤY DỮ LIỆU TỪ API

    # parquet -> data frame
    # pd.read_parquet('example_pa.parquet', engine='pyarrow')

    # Task 1: Làm sạch dữ liệu: xử lý giá trị thiếu
    ddf = ddf.fillna({'category_code': 'Unknown', 'brand': 'Unknown', 'event_type': 'Unknown'})
    ddf['price'] = ddf['price'].fillna(ddf['price'].quantile(0.5))  # Thay thế giá trị thiếu bằng median ước lượng

    # Task 2: Loại bỏ giá trị không hợp lệ
    ddf = ddf[ddf['price'] > 0]  # Loại bỏ các hàng có giá trị giá <= 0

    # Mã hóa categorical (OneHotEncoder thay vì LabelEncoder)
    one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    categorical_cols = ['category_code', 'brand', 'event_type']
    categorical_data = ddf[categorical_cols].compute()
    one_hot_encoded = one_hot_encoder.fit_transform(categorical_data)
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_cols))

    # Kết hợp dữ liệu được mã hóa vào DataFrame ban đầu
    ddf = ddf.drop(columns=categorical_cols)
    ddf = dd.concat([dd.from_pandas(one_hot_df, npartitions=ddf.npartitions), ddf.reset_index(drop=True)], axis=1)

    # Chuẩn hóa các cột số
    if 'price' in ddf.columns:
        scaler = StandardScaler()
        ddf['price'] = dd.from_array(scaler.fit_transform(ddf['price'].compute().values.reshape(-1, 1)))


#TRAINING DỮ LIỆU - ĐƯA RA GỢI Ý SẢN PHẨM

    # Chia dữ liệu và đánh giá mô hình
    if 'price' in ddf.columns:
        X = ddf.drop(columns=['price']).compute()  # Dữ liệu đầu vào
        y = ddf['price'].compute()  # Nhãn

        # Chia tập train-test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("\nTập dữ liệu đã được chia cho train-test.")
        print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

        # Ví dụ: Tính RMSE cho baseline (trung bình giá)
        baseline_pred = [y_train.mean()] * len(y_test)
        rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
        print(f"\nBaseline RMSE: {rmse:.4f}")

    # Collaborative Filtering using Surprise
    if 'user_id' in ddf.columns and 'product_id' in ddf.columns:
        print("\nĐang xây dựng mô hình Collaborative Filtering...")
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ddf[['user_id', 'product_id', 'rating']].compute(), reader)
        trainset, testset = surprise_train_test_split(data, test_size=0.2)

        svd = SVD()
        svd.fit(trainset)

        predictions = svd.test(testset)
        print("RMSE for Collaborative Filtering:", accuracy.rmse(predictions))

    # Content-based Filtering using Cosine Similarity
    if 'category_code' in ddf.columns and 'brand' in ddf.columns:
        print("\nĐang xây dựng mô hình Content-based Filtering...")

        # Kết hợp các cột mô tả sản phẩm để tạo ra một chuỗi mô tả hoàn chỉnh
        ddf['description'] = ddf['category_code'] + ' ' + ddf['brand']

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(ddf['description'].compute())

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Chức năng gợi ý sản phẩm tương tự
        def get_recommendations(product_id, cosine_sim=cosine_sim):
            idx = ddf.index[ddf['product_id'] == product_id].compute().tolist()[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]  # Lấy 10 sản phẩm tương tự
            product_indices = [i[0] for i in sim_scores]
            return ddf['product_id'].iloc[product_indices].compute()

#ĐÂY LÀ OUTPUT

        # Ví dụ: Gợi ý sản phẩm tương tự cho một sản phẩm
        sample_product_id = ddf['product_id'].iloc[0].compute()
        recommendations = get_recommendations(sample_product_id)
        print(f"\nGợi ý sản phẩm tương tự cho sản phẩm {sample_product_id}:\n", recommendations)


except FileNotFoundError:
    print(f"Không tìm thấy file: {file_path}")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split as surprise_train_test_split
from surprise import accuracy
import numpy as np
import dask.dataframe as dd

# Đường dẫn đến file CSV
file_path = 'data/2019-Nov.csv' # CẦN THAY THẾ SANG LẤY DỮ LIỆU TỪ API
chunksize = 100000  # Số dòng trong mỗi chunk

# Khởi tạo các biến toàn cục
missing_values = None

try:
    # Đọc và xử lý từng chunk sử dụng Dask
    ddf = dd.read_csv(file_path, blocksize=chunksize) # CẦN THAY THẾ SANG LẤY DỮ LIỆU TỪ API

    # Làm sạch dữ liệu: xử lý giá trị thiếu
    ddf = ddf.fillna({'category_code': 'Unknown', 'brand': 'Unknown', 'event_type': 'Unknown'})
    ddf['price'] = ddf['price'].fillna(ddf['price'].quantile(0.5))  # Thay thế giá trị thiếu bằng median ước lượng

    # Loại bỏ giá trị không hợp lệ
    ddf = ddf[ddf['price'] > 0]  # Loại bỏ các hàng có giá trị giá <= 0

    # Mã hóa categorical (OneHotEncoder thay vì LabelEncoder)
    one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    categorical_cols = ['category_code', 'brand', 'event_type']
    categorical_data = ddf[categorical_cols].compute()
    one_hot_encoded = one_hot_encoder.fit_transform(categorical_data)
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_cols))

    # Kết hợp dữ liệu được mã hóa vào DataFrame ban đầu
    ddf = ddf.drop(columns=categorical_cols)
    ddf = dd.concat([dd.from_pandas(one_hot_df, npartitions=ddf.npartitions), ddf.reset_index(drop=True)], axis=1)

    # Chuẩn hóa các cột số
    if 'price' in ddf.columns:
        scaler = StandardScaler()
        ddf['price'] = dd.from_array(scaler.fit_transform(ddf['price'].compute().values.reshape(-1, 1)))


#TRAINING DỮ LIỆU - ĐƯA RA GỢI Ý SẢN PHẨM

    # Chia dữ liệu và đánh giá mô hình
    if 'price' in ddf.columns:
        X = ddf.drop(columns=['price']).compute()  # Dữ liệu đầu vào
        y = ddf['price'].compute()  # Nhãn

        # Chia tập train-test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("\nTập dữ liệu đã được chia cho train-test.")
        print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

        # Ví dụ: Tính RMSE cho baseline (trung bình giá)
        baseline_pred = [y_train.mean()] * len(y_test)
        rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
        print(f"\nBaseline RMSE: {rmse:.4f}")

    # Collaborative Filtering using Surprise
    if 'user_id' in ddf.columns and 'product_id' in ddf.columns:
        print("\nĐang xây dựng mô hình Collaborative Filtering...")
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ddf[['user_id', 'product_id', 'rating']].compute(), reader)
        trainset, testset = surprise_train_test_split(data, test_size=0.2)

        svd = SVD()
        svd.fit(trainset)

        predictions = svd.test(testset)
        print("RMSE for Collaborative Filtering:", accuracy.rmse(predictions))

    # Content-based Filtering using Cosine Similarity
    if 'category_code' in ddf.columns and 'brand' in ddf.columns:
        print("\nĐang xây dựng mô hình Content-based Filtering...")

        # Kết hợp các cột mô tả sản phẩm để tạo ra một chuỗi mô tả hoàn chỉnh
        ddf['description'] = ddf['category_code'] + ' ' + ddf['brand']

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(ddf['description'].compute())

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Chức năng gợi ý sản phẩm tương tự
        def get_recommendations(product_id, cosine_sim=cosine_sim):
            idx = ddf.index[ddf['product_id'] == product_id].compute().tolist()[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]  # Lấy 10 sản phẩm tương tự
            product_indices = [i[0] for i in sim_scores]
            return ddf['product_id'].iloc[product_indices].compute()

#ĐÂY LÀ OUTPUT

        # Ví dụ: Gợi ý sản phẩm tương tự cho một sản phẩm
        sample_product_id = ddf['product_id'].iloc[0].compute()
        recommendations = get_recommendations(sample_product_id)
        print(f"\nGợi ý sản phẩm tương tự cho sản phẩm {sample_product_id}:\n", recommendations)


except FileNotFoundError:
    print(f"Không tìm thấy file: {file_path}")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
