from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta, datetime
from typing import Optional

from database import get_db
from models import User
import schemas
import utils

# JWT Secret key và thuật toán
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 PasswordBearer: endpoint để lấy token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# API đăng ký người dùng mới
@router.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra xem username đã tồn tại hay chưa
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Băm mật khẩu trước khi lưu vào DB
    hashed_password = utils.get_password_hash(user.password)
    new_user = User(first_name=user.first_name, sur_name=user.sur_name, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# API login, trả về access token
@router.post("/login")
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()

    # Kiểm tra username và mật khẩu
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Tạo token JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Lấy thông tin người dùng hiện tại dựa trên token
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Xác thực token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Lấy thông tin người dùng từ DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"first_name": user.first_name,"sur_name":user.sur_name, "email": user.email}
