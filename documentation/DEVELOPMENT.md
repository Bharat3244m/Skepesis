# Skepesis - Development Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed
- pip package manager
- Basic knowledge of FastAPI, SQLAlchemy, and Jinja2

### Initial Setup

1. **Clone & Navigate**
```bash
cd /home/bharat/Documents/skepesis
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
python seed_db.py
```

5. **Run Development Server**
```bash
python run.py
```

Server will start at: `http://localhost:8000`

---

## 📁 Project Structure Explained

```
skepesis/
│
├── app/                           # Main application package
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, routes, startup/shutdown
│   ├── config.py                  # Environment config, settings
│   ├── database.py                # SQLAlchemy session, connection
│   │
│   ├── models/                    # Database models (ORM)
│   │   ├── __init__.py
│   │   ├── question.py            # Question entity
│   │   ├── attempt.py             # Attempt entity
│   │   └── response.py            # Response entity
│   │
│   ├── schemas/                   # Pydantic schemas (validation, serialization)
│   │   ├── __init__.py
│   │   ├── question.py            # QuestionCreate, QuestionRead
│   │   ├── attempt.py             # AttemptCreate, AttemptRead
│   │   └── response.py            # ResponseCreate, ResponseRead
│   │
│   ├── crud/                      # Database operations (Create, Read, Update, Delete)
│   │   ├── __init__.py
│   │   ├── question.py            # get_questions(), create_question()
│   │   ├── attempt.py             # get_attempts(), create_attempt()
│   │   └── response.py            # create_response(), get_responses()
│   │
│   ├── routers/                   # API endpoints (organized by resource)
│   │   ├── __init__.py
│   │   ├── questions.py           # /api/questions/*
│   │   ├── attempts.py            # /api/attempts/*
│   │   ├── responses.py           # /api/responses/*
│   │   ├── students.py            # /api/students/*
│   │   └── trivia.py              # /api/trivia/* (external API)
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   └── curiosity.py           # calculate_curiosity_score()
│   │
│   └── templates/                 # Jinja2 HTML templates
│       ├── base.html              # Base layout (header, footer)
│       ├── index.html             # Landing page
│       ├── quiz.html              # Quiz interface
│       ├── results.html           # Results & insights
│       ├── dashboard.html         # Attempt history
│       └── attempt_details.html   # Question breakdown
│
├── app/
│   ├── static/                    # Static assets (CSS, JS, images)
│   │   └── css/
│   │       └── style.css          # All application styles (3,400+ lines)
│
├── run.py                         # Application entry point
├── requirements.txt               # Python dependencies
├── skepesis.db                    # SQLite database (auto-generated)
│
└── Documentation/
    ├── ARCHITECTURE.md            # Project architecture overview
    ├── COMPONENTS.md              # UI component library
    └── DEVELOPMENT.md             # This file
```

---

## 🔧 Development Workflow

### Adding a New Feature

#### 1. Database Model (if needed)
**File**: `app/models/new_model.py`

```python
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
```

#### 2. Pydantic Schema
**File**: `app/schemas/new_model.py`

```python
from pydantic import BaseModel
from datetime import datetime

class NewModelBase(BaseModel):
    name: str

class NewModelCreate(NewModelBase):
    pass

class NewModelRead(NewModelBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # SQLAlchemy ORM mode
```

#### 3. CRUD Operations
**File**: `app/crud/new_model.py`

```python
from sqlalchemy.orm import Session
from app.models.new_model import NewModel
from app.schemas.new_model import NewModelCreate

def create_new_model(db: Session, model: NewModelCreate):
    db_model = NewModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_new_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NewModel).offset(skip).limit(limit).all()
```

#### 4. API Router
**File**: `app/routers/new_model.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import new_model as crud
from app.schemas.new_model import NewModelCreate, NewModelRead

router = APIRouter(prefix="/api/new-model", tags=["new-model"])

@router.post("/", response_model=NewModelRead)
def create_new_model(model: NewModelCreate, db: Session = Depends(get_db)):
    return crud.create_new_model(db, model)

@router.get("/", response_model=list[NewModelRead])
def list_new_models(db: Session = Depends(get_db)):
    return crud.get_new_models(db)
```

#### 5. Register Router
**File**: `app/main.py`

```python
from app.routers import new_model

app.include_router(new_model.router)
```

#### 6. Template (if needed)
**File**: `app/templates/new_page.html`

```html
{% extends "base.html" %}

{% block title %}New Page{% endblock %}

{% block content %}
<div class="container">
  <h1>New Page</h1>
  <!-- Your content -->
</div>
{% endblock %}
```

#### 7. Add Route in main.py

```python
@app.get("/new-page")
async def new_page(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})
```

---

## 🎨 Styling Guidelines

### Using Design Tokens

Always use CSS variables from the design system:

```css
/* ✅ Good */
.my-component {
  background: var(--color-surface);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  color: var(--color-text);
  transition: var(--transition);
}

/* ❌ Bad */
.my-component {
  background: #FFFFFF;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  color: #1A1A1A;
  transition: 150ms ease;
}
```

### Component Naming Convention

Follow BEM-inspired naming:

```css
/* Block */
.component { }

/* Element */
.component-header { }
.component-body { }
.component-footer { }

/* Modifier */
.component--large { }
.component--success { }
```

### Adding New Components

1. Define component in `static/css/style.css`
2. Add section comment header
3. Use design tokens
4. Document in `COMPONENTS.md`

Example:

```css
/* ============ My New Component ============ */

.my-component {
  /* Layout */
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  
  /* Box model */
  padding: var(--space-6);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  
  /* Visual */
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
  
  /* Animation */
  transition: var(--transition);
}

.my-component:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.my-component-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text);
}

.my-component-description {
  color: var(--color-text-secondary);
  line-height: 1.6;
}
```

---

## 🧪 Testing

### Manual Testing Checklist

#### New Feature Testing
- [ ] Feature works on Chrome, Firefox, Safari
- [ ] Responsive on mobile (< 640px)
- [ ] Responsive on tablet (640px - 1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] Keyboard navigation works
- [ ] Focus states visible
- [ ] Screen reader accessible (test with NVDA/VoiceOver)
- [ ] Error states handled gracefully
- [ ] Loading states show feedback
- [ ] Empty states provide guidance

#### API Testing
Use FastAPI's interactive docs: `http://localhost:8000/docs`

1. Navigate to endpoint
2. Click "Try it out"
3. Fill in parameters
4. Execute request
5. Verify response

### Database Testing

```python
# In Python shell
from app.database import SessionLocal, engine
from app.models.question import Question

# Create session
db = SessionLocal()

# Query test
questions = db.query(Question).all()
print(f"Total questions: {len(questions)}")

# Close session
db.close()
```

---

## 🐛 Debugging

### Common Issues

#### 1. "ModuleNotFoundError"
**Cause**: Virtual environment not activated  
**Solution**: 
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. "Table doesn't exist"
**Cause**: Database not initialized  
**Solution**:
```bash
# Delete old database
rm skepesis.db

# Re-seed
python seed_db.py
```

#### 3. "Port already in use"
**Cause**: Previous server still running  
**Solution**:
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in run.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### 4. "Template not found"
**Cause**: Incorrect template path  
**Solution**: Check `app/templates/` directory structure

#### 5. CSS not loading
**Cause**: Static files not mounted  
**Solution**: Verify in `app/main.py`:
```python
app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

### Logging

Add logging for debugging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/debug")
def debug_endpoint(db: Session = Depends(get_db)):
    logger.info("Debug endpoint called")
    questions = db.query(Question).all()
    logger.info(f"Found {len(questions)} questions")
    return {"count": len(questions)}
```

---

## 📦 Dependencies

### Core Dependencies

```txt
fastapi==0.124.0          # Web framework
uvicorn[standard]==0.38.0  # ASGI server
sqlalchemy==2.0.45        # ORM
pydantic==2.12.5          # Data validation
jinja2==3.1.6             # Template engine
python-multipart==0.0.20  # Form handling
httpx==0.28.1             # HTTP client
```

### Adding New Dependencies

1. Install package:
```bash
pip install package-name
```

2. Update requirements:
```bash
pip freeze > requirements.txt
```

3. Document in `ARCHITECTURE.md` if significant

---

## 🚀 Deployment

### Production Checklist

- [ ] Update `DATABASE_URL` in `app/config.py` (use PostgreSQL, not SQLite)
- [ ] Set `DEBUG = False` in config
- [ ] Use environment variables for secrets
- [ ] Enable CORS for production domain
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure logging to file/service
- [ ] Add error tracking (Sentry, Rollbar)
- [ ] Set up database backups
- [ ] Enable API rate limiting
- [ ] Minify CSS (optional)
- [ ] Set up CI/CD pipeline
- [ ] Configure web server (Nginx, Caddy)

### Example Production Config

```python
# app/config.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skepesis.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG = os.getenv("DEBUG", "False") == "True"
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

settings = Settings()
```

### Docker Deployment (Optional)

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./skepesis.db:/app/skepesis.db
    environment:
      - DATABASE_URL=sqlite:///./skepesis.db
```

Run:
```bash
docker-compose up -d
```

---

## 🔄 Version Control

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes, commit often
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Merge to main
git checkout main
git merge feature/new-feature
```

### Commit Message Convention

```
feat: Add user authentication
fix: Resolve quiz scoring bug
docs: Update API documentation
style: Format CSS for readability
refactor: Simplify curiosity calculation
test: Add unit tests for CRUD operations
chore: Update dependencies
```

---

## 📚 Additional Resources

### FastAPI
- [Official Docs](https://fastapi.tiangolo.com/)
- [Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Guide](https://docs.pydantic.dev/)

### SQLAlchemy
- [Official Docs](https://docs.sqlalchemy.org/)
- [ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

### Jinja2
- [Template Designer Docs](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### CSS
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

---

## 💡 Best Practices

1. **Keep functions small**: One function, one purpose
2. **Use type hints**: Makes code self-documenting
3. **Write docstrings**: Explain complex logic
4. **Handle errors**: Use try/except, return meaningful errors
5. **Validate input**: Use Pydantic schemas for all API inputs
6. **Use design tokens**: Never hardcode colors/spacing
7. **Test responsively**: Check mobile/tablet/desktop views
8. **Commit often**: Small, focused commits with clear messages
9. **Document changes**: Update relevant .md files
10. **Review before merge**: Check code quality, test thoroughly

---

## 🤝 Contributing

1. Read this document thoroughly
2. Follow code style guidelines
3. Test your changes
4. Update documentation
5. Submit clear commit messages
6. Request review from team

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Maintained by**: Skepesis Team
