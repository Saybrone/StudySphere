from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .models import User, Note
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import hashlib
import os
from jose import JWTError, jwt
from fastapi.staticfiles import StaticFiles
import os


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
os.makedirs("uploads", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

Base.metadata.create_all(bind=engine)


def get_db(): 
    db = SessionLocal() 
    try: yield db 
    finally: db.close()
def get_current_user(
    access_token: str = Cookie(None), 
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def safe_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()



def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return RedirectResponse("/login-page")

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
    return RedirectResponse("/login-page", status_code=303)

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
def dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "Dashboard.html",
        {"request": request, "email": user.email}
    )


@app.get("/my-notes", response_class=HTMLResponse)
def my_notes_page(request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == user.id).all()
    return templates.TemplateResponse(
        "my_notes.html",
        {"request": request, "email": user.email, "notes": notes}
    )


@app.post("/notes/create")
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_path = None

    if file:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = f"{upload_dir}/{user.id}_{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

    note = Note(
        title=title,
        content=content,
        user_id=user.id,
        file_path=file_path
    )

    db.add(note)
    db.commit()

    return RedirectResponse("/my-notes", status_code=303)

@app.post("/notes/delete/{note_id}")
def delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.file_path:
        print(note.file_path)
        file_full_path = note.file_path
        if os.path.exists(file_full_path):
            os.remove(file_full_path)
            print("Ok")
        else:
            print("not Ok")
    db.delete(note)
    db.commit()
    return RedirectResponse("/my-notes", status_code=303)

@app.get("/notes/search", response_class=HTMLResponse)
def search_notes(
    request: Request,
    q: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not q or q.strip() == "":
        results = db.query(Note).all()

    else:
        search_term = f"%{q}%"
        results = db.query(Note).filter(
            (Note.title.ilike(search_term)) |
            (Note.content.ilike(search_term))
        ).all()

    return templates.TemplateResponse(
        "search_notes.html",
        {
            "request": request,
            "results": results,
            "query": q if q else ""
        }
    )
