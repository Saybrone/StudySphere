# StudySphere
An open platform for students to share their knowledge and collaborate.

<img src="static/Logo.png" alt="StudySphere" width="300">

# Table of Contents
- [Project Structure](#Project-Structure)
- [Problem & Objective](#Problem-Objective)
- [Key Features](Key-Features)
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
# Key Features  <a class="anchor" id="Key-Features"></a>
- **Dashboard** — clean overview of user activity  
- **Note Creation** — write and save notes instantly  
- **File Attachments** — upload documents to your notes  
- **Secure Authentication** — login/signup with encrypted credentials  
- **Search System** — find notes by keywords in title or content  
- **Production Ready Architecture** — ready to support many users  
- **Cloud-Based Storage** — powered by NeonDB & FastAPI

# Problem & Objective <a class="anchor" id="Problem-Objective"></a>
While studying students face issues like:

- Unorganized notes on different devices
- No lesson notes on internet
- Hard-to-search study material 
- No platform to share notes with close and long distance


**StudySphere aims to solve these by:**
- Creating an open platform where students can upload notes
- Providing a clean UI to orginize notes
- Allowing students to reach and share every registered note

The initial goal is to create a modern, light, scalable platform for student collaboration and study material organization.

# How It Works/Tech Stack <a class="anchor" id="Tech"></a>

<img src="Flowchart.jpg" alt="Flowchart.jpg" width="3000">

## Tech Stack
- Python 3.13
- HTML
- CSS
- FastAPI
- SqlAlchemy
- NeonDB
- PostgreSQL




# Backend <a class="anchor" id="Backend"></a>

The backend is designed to be fast, secure, and scalable, using FastAPI.

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

To deploy StudySphere:

### 0. Set A NeonDB project
### 1. Configure environment variables
.env:
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host/db
```
### 2. Install dependencies  
run: ```pip install -r requirements.txt```

### 3. Run FastAPI  
run: ```python -m uvicorn main:app --host 0.0.0.0 --port 8000```

## If you want to try Full Website, use already deployed model:
Important: Because it is free trial of render, notes will be deleted after server sleeps

**[Try Now](https://studysphere-0jqu.onrender.com/)**

  https://studysphere-0jqu.onrender.com/

## FutureGoals <a class="anchor" id="FutureGoals"></a>

Planned improvements:
- Better UI animations  
- Creating view pages for notes  
- Tasks & reminders system  
- Private Note sharing between users  
- Real-time chat between students  
- Profile customization  
- AI assistant to help stundents while reading notes
- **Full Deployment using Amazon VPS hosting**
  
## Impact <a class="anchor" id="Impact"></a>

StudySphere aims to:
- Help students stay organized  
- Improve knowledge sharing  
- Reduce friction in note-taking  
- Provide a modern academic workspace  
- Support and encourage collaboration at education 

The platform is built with education and accessibility as its core.


## License

```
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
