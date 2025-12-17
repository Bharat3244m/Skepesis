# Skepesis - Architecture Documentation

## 📐 Project Overview

**Skepesis** is an adaptive learning platform that analyzes cognitive patterns, confidence levels, and curiosity behaviors to provide personalized insights.

### Design Philosophy
- **Minimal**: Clean, distraction-free interface
- **Intelligent**: Data-driven insights without overwhelming users
- **Calm**: Soft colors, ample spacing, smooth interactions
- **Professional**: Production-ready, scalable architecture

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI 0.124+ (async Python web framework)
- SQLAlchemy 2.0.45 (ORM)
- Pydantic 2.12.5 (data validation)
- SQLite (database)
- Uvicorn 0.38.0 (ASGI server)

**Frontend:**
- Jinja2 3.1.6 (server-side templates)
- Vanilla JavaScript (no frameworks)
- Pure CSS (no preprocessors)
- Inter font via Google Fonts

**External APIs:**
- Open Trivia Database (question import)

### Directory Structure

```
skepesis/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── question.py      # Question entity
│   │   ├── attempt.py       # Learning session entity
│   │   └── response.py      # User response entity
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── question.py      # Question DTOs
│   │   ├── attempt.py       # Attempt DTOs
│   │   └── response.py      # Response DTOs
│   │
│   ├── crud/                # Database operations
│   │   ├── question.py      # Question CRUD
│   │   ├── attempt.py       # Attempt CRUD
│   │   └── response.py      # Response CRUD
│   │
│   ├── routers/             # API endpoints
│   │   ├── questions.py     # Question endpoints
│   │   ├── attempts.py      # Attempt endpoints
│   │   ├── responses.py     # Response endpoints
│   │   ├── students.py      # Student endpoints
│   │   └── trivia.py        # External API integration
│   │
│   ├── services/            # Business logic
│   │   └── curiosity.py     # Metacognitive analysis
│   │
│   └── templates/           # Jinja2 HTML templates
│       ├── base.html        # Base layout
│       ├── index.html       # Landing page
│       ├── quiz.html        # Quiz interface
│       ├── results.html     # Insights page
│       ├── dashboard.html   # Progress tracking
│       └── attempt_details.html  # Session breakdown
│
├── app/
│   ├── static/
│   │   └── css/
│   │       └── style.css    # All application styles
│
├── run.py                   # Application runner
├── requirements.txt        # Python dependencies
└── skepesis.db            # SQLite database
```

---

## 🎨 Design System

### Color Palette

```css
/* Brand */
--color-primary: #6366F1;        /* Indigo */
--color-primary-hover: #4F46E5;
--color-primary-light: #818CF8;

/* Neutrals */
--color-bg: #FAFAFA;             /* Off-white background */
--color-surface: #FFFFFF;        /* White cards/panels */
--color-surface-raised: #F5F5F5; /* Elevated surfaces */
--color-border: #E5E5E5;         /* Standard borders */

/* Text */
--color-text: #1A1A1A;           /* Primary text */
--color-text-secondary: #525252; /* Secondary text */
--color-text-tertiary: #737373;  /* Tertiary text */

/* Semantic */
--color-success: #10B981;        /* Green */
--color-warning: #F59E0B;        /* Orange */
--color-error: #EF4444;          /* Red */
```

### Typography

- **Font Family**: Inter (400, 500, 600 weights)
- **Base Size**: 16px
- **Line Height**: 1.7 (body), 1.2-1.3 (headings)
- **Scale**: h1 (2.5rem) → h6 (1rem)

### Spacing Scale

Based on 4px base unit:
- space-1: 4px
- space-2: 8px
- space-3: 12px
- space-4: 16px (base)
- space-6: 24px
- space-8: 32px
- space-12: 48px
- space-16: 64px

### Components

Reusable UI components with consistent styling:

**Buttons:**
- `.btn-primary` - Primary CTA
- `.btn-secondary` - Secondary actions
- `.btn-large` - Hero sections
- `.btn-icon` - Icon-only buttons

**Badges:**
- `.badge.success` - Completed/Correct
- `.badge.warning` - Needs attention
- `.badge.info` - In progress

**Cards:**
- `.card` - Base card
- `.feature-card` - Landing features
- `.stat-card` - Statistics
- `.score-card` - Results scores
- `.attempt-card` - Session history
- `.insight-card` - Analysis cards
- `.pattern-card` - Learning patterns
- `.question-item` - Question breakdown

**States:**
- `.empty-state` - No data available
- `.error-state` - Error occurred
- `.loader` - Loading animation

---

## 📊 Data Models

### Question
```python
{
    "id": int,
    "text": str,
    "category": str,
    "difficulty": str,
    "option_a": str,
    "option_b": str,
    "option_c": str,
    "option_d": str,
    "correct_answer": str  # A, B, C, or D
}
```

### Attempt (Learning Session)
```python
{
    "id": int,
    "student_name": str,
    "started_at": datetime,
    "completed_at": datetime | None,
    "total_questions": int,
    "correct_answers": int,
    "curiosity_score": float,
    "average_confidence": float,
    "confidence_alignment": float
}
```

### Response
```python
{
    "id": int,
    "attempt_id": int,
    "question_id": int,
    "user_answer": str,
    "is_correct": bool,
    "confidence": int,  # 0-100
    "time_taken": int   # seconds
}
```

---

## 🔄 User Flow

1. **Landing Page** (`/`)
   - Value proposition
   - Feature overview
   - Quick start CTA

2. **Quiz Setup** (Modal)
   - Enter name
   - Select question count
   - Choose category (optional)
   - Creates attempt record

3. **Quiz Interface** (`/quiz?attempt_id={id}`)
   - One question at a time
   - 4 multiple choice options
   - 1-5 confidence slider
   - Progress tracking
   - Keyboard shortcuts (1-4, Enter)

4. **Results & Insights** (`/results/{attempt_id}`)
   - Score summary
   - Curiosity score
   - Learning style badge
   - Confidence vs correctness patterns
   - Knowledge area breakdown
   - Reflection prompts
   - Personalized strategies

5. **Dashboard** (`/dashboard`)
   - All attempts history
   - Cards or Table view toggle
   - Summary statistics
   - Quick access to insights

6. **Attempt Details** (`/attempt/{attempt_id}`)
   - Question-by-question breakdown
   - Filter by correct/incorrect/confidence
   - Curiosity patterns per question
   - Performance metadata

---

## 🧠 Metacognitive Analysis

The platform analyzes:

1. **Curiosity Score**
   - Willingness to explore uncertain territory
   - Confidence calibration
   - Question engagement time

2. **Learning Style**
   - Exploratory: High curiosity, explores unknown
   - Analytical: Methodical, careful consideration
   - Calibrated: Excellent self-awareness
   - Confident: Strong conviction in knowledge

3. **Confidence Patterns**
   - Overconfidence: High confidence + incorrect
   - Underconfidence: Low confidence + correct
   - Well-calibrated: Confidence matches performance
   - Guessing: Very low confidence responses

4. **Knowledge Gaps**
   - Category-level accuracy analysis
   - Identifies weak areas
   - Suggests growth opportunities

---

## 🔧 API Endpoints

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

### Trivia (External)
- `GET /api/trivia/categories` - List external categories
- `POST /api/trivia/import` - Import questions
- `POST /api/trivia/preview` - Preview before import

---

## 🚀 Deployment Considerations

### Performance
- Static assets served efficiently
- Minimal JavaScript (< 5KB per page)
- Single CSS file (optimized for production)
- Database indexing on foreign keys

### Scalability
- Stateless API design
- RESTful endpoints
- Modular component structure
- Separation of concerns (MVC pattern)

### Security
- Input validation via Pydantic
- SQL injection prevention via ORM
- CORS configuration ready
- Environment-based configuration

### Monitoring
- Structured logging
- Error tracking ready
- API endpoint monitoring
- Database query optimization

---

## 📝 Code Style Guidelines

### Python
- PEP 8 compliant
- Type hints throughout
- Async/await for I/O operations
- Docstrings for public functions

### CSS
- BEM-inspired naming (`.component-element--modifier`)
- CSS variables for theming
- Mobile-first responsive design
- Grouped by feature/page

### JavaScript
- ES6+ syntax
- Async/await for API calls
- Descriptive variable names
- Error handling for all network requests

### HTML
- Semantic markup
- Accessible (ARIA labels where needed)
- SEO-friendly structure
- Minimal inline styles

---

## 🧪 Testing Strategy

### Current State
- Manual testing via browser
- API testing via FastAPI docs (`/docs`)

### Recommended Additions
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Load testing for scalability

---

## 📦 Future Enhancements

1. **User Accounts**
   - Authentication/Authorization
   - Personal progress tracking
   - Multi-device sync

2. **Advanced Analytics**
   - Longitudinal progress tracking
   - Spaced repetition recommendations
   - Difficulty adaptation

3. **Content Management**
   - Custom question creation
   - Question tagging system
   - Multimedia support

4. **Social Features**
   - Leaderboards
   - Shared learning sessions
   - Collaborative challenges

5. **AI Integration**
   - Personalized question generation
   - Natural language feedback
   - Adaptive difficulty tuning

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Inter Font](https://rsms.me/inter/)
- [Open Trivia Database](https://opentdb.com/)

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Maintained by**: Skepesis Team
