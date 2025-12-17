# Skepesis

> **A smart adaptive learning platform that analyzes cognitive patterns, confidence levels, and curiosity behaviors to provide personalized insights.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Overview

Skepesis is a metacognitive learning platform that goes beyond traditional quizzes by analyzing **how** you think, not just **what** you know. It tracks confidence patterns, identifies knowledge gaps, and provides personalized strategies based on your learning style.

### ✨ Key Features

- **🧠 Metacognitive Analysis**: Understand your confidence patterns and learning style
- **📊 Curiosity Score**: Quantifies your willingness to explore uncertain territory
- **🎯 Adaptive Insights**: Personalized feedback based on confidence vs. correctness
- **📈 Progress Tracking**: Visual dashboard with history and analytics
- **🔍 Question-Level Breakdown**: Detailed analysis of each response
- **🎨 Modern UI**: Clean, minimal, distraction-free interface

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd skepesis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python seed_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   ```
   http://localhost:8000
   ```

That's it! The platform is now running locally.

---

## 🎯 How It Works

### 1. Take a Quiz
- Enter your name and select quiz parameters
- Answer questions with 1-5 confidence levels
- One question at a time, distraction-free

### 2. Get Insights
- View comprehensive results and cognitive patterns
- See confidence vs. correctness analysis
- Identify overconfidence and underconfidence patterns
- Receive personalized learning strategies

### 3. Track Progress
- Dashboard with all attempt history
- View by cards or table layout
- Dive into question-by-question breakdowns
- Filter by correct/incorrect/confidence levels

---

## 🏗️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database (easily replaceable with PostgreSQL)

### Frontend
- **Jinja2**: Template engine for server-side rendering
- **Vanilla JavaScript**: No frameworks, lightweight and fast
- **Pure CSS**: Custom design system, no preprocessors
- **Inter Font**: Clean, modern typography

### External APIs
- **Open Trivia Database**: Question import functionality

---

## 📂 Project Structure

```
skepesis/
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── database.py          # Database configuration
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic validation schemas
│   ├── crud/                # Database operations
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── templates/           # Jinja2 HTML templates
│
├── app/
│   ├── static/
│   │   └── css/
│   │       └── style.css    # Application styles (3,400+ lines)
│
├── run.py                   # Application runner
├── seed_db.py              # Database seeding script
├── requirements.txt        # Python dependencies
│
└── Documentation/
    ├── ARCHITECTURE.md      # Architecture overview
    ├── COMPONENTS.md        # UI component library
    └── DEVELOPMENT.md       # Development guide
```

---

## 🎨 Design Philosophy

Skepesis follows a **minimal, clean, modern** design language inspired by:
- **Notion**: Clean information hierarchy
- **Linear**: Sharp, purposeful UI
- **Vercel**: Subtle elegance
- **Stripe**: Professional clarity

### Design Principles

1. **Minimal**: No clutter, every element has a purpose
2. **Calm**: Soft colors, generous spacing, smooth transitions
3. **Intelligent**: Data-driven insights without overwhelming users
4. **Accessible**: WCAG AAA compliant, keyboard navigable
5. **Responsive**: Mobile-first, scales gracefully

### Color Palette

- **Primary**: Indigo (#6366F1) - CTAs, links, focus states
- **Background**: Off-white (#FAFAFA) - Calm, easy on eyes
- **Surface**: Pure white (#FFFFFF) - Cards, panels
- **Text**: Near-black (#1A1A1A) - High contrast, readable
- **Semantic**: Green (success), Amber (warning), Red (error)

---

## 📊 Features Deep Dive

### Metacognitive Analysis

Skepesis analyzes four key areas:

1. **Curiosity Score** (0-100)
   - Willingness to take risks on uncertain questions
   - High confidence on difficult questions = higher curiosity
   - Time spent on questions indicates engagement

2. **Learning Style Badge**
   - **Exploratory**: High curiosity, explores unknown territory
   - **Analytical**: Careful, methodical approach
   - **Calibrated**: Excellent self-awareness
   - **Confident**: Strong conviction in knowledge

3. **Confidence Patterns**
   - **Overconfidence**: High confidence + incorrect answer
   - **Underconfidence**: Low confidence + correct answer
   - **Well-Calibrated**: Confidence matches performance
   - **Guessing**: Very low confidence responses

4. **Knowledge Gaps**
   - Category-level accuracy analysis
   - Identifies weak areas for improvement
   - Suggests growth opportunities

For a detailed guide on metacognitive features, see [METACOGNITION.md](METACOGNITION.md).

---

## 🛠️ Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python run.py
```

Server runs on `http://localhost:8000` with hot-reload enabled.

### API Documentation

FastAPI provides interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Database Management

```bash
# View database structure
sqlite3 skepesis.db
.schema

# Reset database
rm skepesis.db
# Restart the application to re-initialize and seed the database
```

### Adding Questions

1. **Via API**: Use `/api/questions/` endpoint
2. **Via Trivia Import**: Use `/api/trivia/import` endpoint

---

## 📝 API Endpoints

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/random` - Get random questions
- `GET /api/questions/categories` - List categories
- `POST /api/questions/` - Create question

### Attempts
- `GET /api/attempts/` - List all attempts
- `GET /api/attempts/{id}` - Get attempt details
- `POST /api/attempts/` - Create attempt
- `POST /api/attempts/{id}/complete` - Mark complete
- `GET /api/attempts/{id}/insights` - Get cognitive insights
- `GET /api/attempts/{id}/responses` - Get question breakdown

### Responses
- `POST /api/responses/` - Submit answer

### Trivia
- `GET /api/trivia/categories` - List external categories
- `POST /api/trivia/import` - Import questions

---

## 🧪 Testing

### Manual Testing

Use the FastAPI interactive docs at `/docs` to test API endpoints.

### Browser Testing

Tested and compatible with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Responsive Testing

Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

---

## 🚀 Deployment

### Production Considerations

1. **Database**: Replace SQLite with PostgreSQL
   ```python
   # app/config.py
   DATABASE_URL = "postgresql://user:password@localhost/skepesis"
   ```

2. **Environment Variables**
   ```bash
   export SECRET_KEY="your-secret-key"
   export DATABASE_URL="postgresql://..."
   export DEBUG="False"
   ```

3. **Web Server**: Use Nginx or Caddy as reverse proxy

4. **ASGI Server**: Use Gunicorn with Uvicorn workers
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

5. **Security**
   - Enable HTTPS
   - Configure CORS for your domain
   - Set up rate limiting
   - Add authentication (if needed)

### Docker Deployment

```bash
# Build image
docker build -t skepesis .

# Run container
docker run -p 8000:8000 skepesis
```

---

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Complete architecture overview
- **[COMPONENTS.md](COMPONENTS.md)**: Design system & UI component library
- **[DEVELOPMENT.md](DEVELOPMENT.md)**: Development guide and best practices
- **[METACOGNITION.md](METACOGNITION.md)**: Detailed guide on learning analysis features

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Read the [DEVELOPMENT.md](DEVELOPMENT.md) guide
2. Follow code style guidelines
3. Write clear commit messages
4. Test your changes thoroughly
5. Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **FastAPI** team for the excellent framework
- **Open Trivia Database** for free question API
- **Inter font** by Rasmus Andersson
- Design inspiration from **Notion**, **Linear**, **Vercel**, and **Stripe**

---

## 📧 Contact

For questions, feedback, or support:
- Create an issue on GitHub
- Email: contact@skepesis.com

---

## 🗺️ Roadmap

### v1.1 (Planned)
- [ ] User authentication
- [ ] Personal progress tracking
- [ ] Custom question creation UI
- [ ] Spaced repetition algorithm

### v2.0 (Future)
- [ ] AI-powered question generation
- [ ] Collaborative learning sessions
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard

---

**Built with ❤️ for curious learners**

**Version**: 1.0.0  
**Last Updated**: December 2025
