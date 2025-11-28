from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .models import User
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import hashlib
import os
from jose import JWTError, jwt
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

Base.metadata.create_all(bind=engine)



def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")

def safe_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return RedirectResponse("/dashboard")

@app.get("/login-page", response_class=HTMLResponse)
def open_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup-page", response_class=HTMLResponse)
def open_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    safe = safe_password(password)
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = pwd_context.hash(safe)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

@app.post("/login")
def login(
    
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    clean_password = safe_password(password)
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(clean_password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/login-page")
    response.delete_cookie("access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, access_token: str = Cookie(None)):
    if not access_token:
        return RedirectResponse("/login-page")

    try:
        user_email = get_current_user(access_token)
    except:
        return RedirectResponse("/login-page")

    return templates.TemplateResponse("Dashboard.html", {"request": request, "email": user_email})
