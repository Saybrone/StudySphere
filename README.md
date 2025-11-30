# StudySphere
An open platform for students to share their knowledge and collaborate.

<img src="static/Logo.png" alt="StudySphere" width="300">

# Table of Contents
- [Project Structure](#Project-Structure)
- [Problem & Objective](#Problem-Objective)
- [Features](#Features)
- [How It Works/Tech Stack](#Tech)
- [Backend](#Backend)
  - [FastAPI](#FastAPI)
  - [SQL Alchemy](#SQL-Alchemy)
  - [NeonDB](#NeonDB)
- [Frontend](#Frontend)
  - [Dashboard](#Dashboard)
  - [MyNotes/Search Notes](#MyNotes-SearchNotes)
  - [Authentication](#Authentication)
- [Deployment](#Deployment)
- [Future Goals](#FutureGoals)
- [Impact](#Impact)
- [License](#license)

# Project Structure <a class="anchor" id="Project-Structure"></a>
```
StudySphere/
├── app/
│ ├── main.py
│ ├── models.py
│ └── database.py  
├── templates/
│ ├── Dashboard.html
│ ├── login.html
│ ├── my_notes.html
│ ├── search_notes.html
│ └── signup.html 
├── static/
│ ├── Authentication.css
│ ├── Logo.png
│ ├── dashboard.css
│ ├── mynotes.css
│ └── searchnotes.css                    
├── requirements.txt                            
├── LICENSE                 
└── README.md             
```
# Problem & Objective <a class="anchor" id="Problem-Objective"></a>

Students face issues like:
- Notes scattered across devices  
- No collaboration-friendly platform  
- Hard-to-search study material  
- Manual file management  

**StudySphere solves this by:**
- Centralized note creation  
- File attachments  
- Smart search  
- Clean dashboard  
- Secure user authentication  

The goal is to create a modern, light, scalable platform for student collaboration and study material organization.


# Backend <a class="anchor" id="Backend"></a>

The backend is designed to be fast, secure, and scalable, using by FastAPI.

## FastAPI <a class="anchor" id="FastAPI"></a>

FastAPI provides:
- High performance  
- Request validation  
- Async support  
- Static file + template integration  
- Easy routing  

Backend includes:
- Authentication with JWT cookies  
- Secure password hashing  
- File upload system  
- Search filtering  
- User session handling  

## SQLAlchemy <a class="anchor" id="SQL-Alchemy"></a>

Used for:
- Database model definitions  
- Table creation  
- Managing relations  

### Models: 
- **User**
  - id  
  - username  
  - email  
  - password (hashed)

- **Note**
  - id  
  - title  
  - content  
  - file_path  
  - user_id  
  - created_at  

Notes are linked to the user, and files are removed automatically when a note is deleted.


## NeonDB <a class="anchor" id="NeonDB"></a>

NeonDB is the PostgreSQL cloud database used in production.

Benefits:
- Serverless auto-scaling  
- High availability  
- Always-free tier  
- PostgreSQL-compatible  

Local development uses SQLite; production uses NeonDB via environment variables.


# Frontend <a class="anchor" id="Frontend"></a>

Frontend uses **HTML + CSS (Glassmorphic design)** and is rendered with Jinja2 templates.

Design focus:
- Smooth, modern UI  
- Soft glass panels  
- Card-based layout  
- Mobile-friendly  
- Consistent buttons


## Dashboard <a class="anchor" id="Dashboard"></a>

Dashboard includes:
- Navigation to notes  
- Buttons for:
  - My Notes  
  - Create Note  
  - Search Notes  
- Glass-style containers  
- Email-based greeting  
- Logout button  


## MyNotes / Search Notes <a class="anchor" id="MyNotes-SearchNotes"></a>

### MyNotes
Features:
- Add a note  
- Add file attachments  
- Modern “Attach File” button  
- View all notes belonging to the user  
- Download attached files  
- Delete notes (with auto file deletion)  
- Glassmorphic layout with cards  


### Search Notes
- Instant filtering  
- Matching notes appear as the user types  
- Responsive note grid  


## Authentication <a class="anchor" id="Authentication"></a>

Authentication includes:
- User signup  
- Secure login  
- JWT-based session stored in `httponly` cookies  
- Logout clears token  
- Unauthorized users are blocked from:
  - Dashboard  
  - MyNotes  
  - Search  
  - Note creation  
  - Note deletion  

Passwords are:
- SHA-256 cleaned  
- Argon2 hashed  
- Safely stored  


# Deployment

