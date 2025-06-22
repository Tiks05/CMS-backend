# CMS-backend · Content Management System Backend

[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

📘 CMS-backend is a scalable and modular backend service for an article management system built with Flask + SQLAlchemy 2.x. Inspired by the official design of Tomato Novel (番茄小说), this backend supports multi-role access control, article publishing, nested comments, file uploads, and more. It is designed to work seamlessly with [CMS-frontend](https://github.com/Tiks05/CMS-frontend) built with Vue3 + TypeScript.

## ✨ Features

- 🌐 RESTful API design with modular routing via Flask Blueprints
- 🔐 JWT-based authentication and role-based authorization
- 📝 Article CRUD with categorization, pagination, and attachment support
- 💬 Infinite-level nested comment system with reply tagging
- 🗂️ Structured file uploads with automatic folder classification
- ⚙️ Clean and maintainable architecture with clear separation of concerns
- 🔄 MySQL database support with SQLAlchemy 2.x and Alembic migrations

## 🛠 Tech Stack

| Layer            | Technology                 |
|------------------|----------------------------|
| Language         | Python 3.12+               |
| Framework        | Flask                      |
| ORM              | SQLAlchemy 2.x             |
| Validation       | Pydantic                   |
| Authentication   | Flask-JWT-Extended + bcrypt|
| Database         | MySQL                      |
| File Handling    | Flask + Werkzeug           |
| Configuration    | dotenv (.env)              |
| Deployment Ready | Gunicorn / Docker (optional) |

## 📁 Project Structure

CMS-backend/
├── app/
│   ├── controllers/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── static/uploads/
├── migrations/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Tiks05/CMS-backend.git
cd CMS-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your DB credentials and JWT secret
```

### 5. Initialize the database

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Run the application

```bash
python run.py
```

## 🧩 Planned Enhancements

- [x] JWT auth system
- [x] Role-based access control
- [x] Article publishing and editing
- [x] Nested comments
- [ ] Favorites, likes, and read tracking
- [ ] Admin moderation dashboard
- [ ] Swagger/OpenAPI Docs
- [ ] Docker containerization

## 📄 License

MIT License © 2025 [Tiks](https://github.com/Tiks05)

## 🙌 Acknowledgements

- Inspired by [Tomato Novel](https://fanqienovel.com/)
- Developed as part of a university-level UI/UX system design course
