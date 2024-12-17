from pydantic import BaseModel, validator, ValidationError
from datetime import datetime

class EventData(BaseModel):
    event_time: str
    event_type: str
    product_id: str
    category_id: str
    category_code: str
    brand: str
    price: str
    user_id: str
    user_session: str

    @validator('event_time')
    def validate_event_time(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S UTC')
        except ValueError:
            raise ValueError(f"Invalid event_time format: {value}")
        return value

    @validator('event_type')
    def validate_event_type(cls, value):
        if not value:
            raise ValueError(f"event_type can not be empty")
        return value

    @validator('product_id', 'category_id', 'user_id')
    def validate_numeric_ids(cls, value):
        if not value.isdigit():
            raise ValueError(f"{value} must be a numeric string")
        return value

    @validator('price')
    def validate_price(cls, value):
        try:
            price = float(value)
            if price <= 0:
                raise ValueError(f"Invalid price: {value}")
        except ValueError:
            raise ValueError(f"Invalid price format: {value}")
        return value

    @validator('brand')
    def validate_brand(cls, value):
        if not value:
            raise ValueError("brand cannot be empty")
        return value

    @validator('category_code')
    def validate_category_code(cls, value):
        if not value:
            raise ValueError("category_code cannot be empty")
        return value

    @validator('user_session')
    def validate_user_session(cls, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError(f"Invalid user_session: {value}")
        return value

# Hàm validate dữ liệu
def validate_data(data):
    try:
        event_data = EventData(**data)  # Sử dụng Pydantic để validate
        return True
    except ValidationError as e:
        print(f"Validation failed: {e}")
        return False
