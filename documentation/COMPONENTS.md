# Skepesis - Design System & Components

## Overview

This document describes the complete design system and all reusable UI components in the Skepesis platform. Each component is built with pure CSS (no frameworks) and follows our design system principles.

---

## 📐 Design Principles

1. **Modularity**: Each component is self-contained with clear dependencies
2. **Consistency**: All components use design system tokens (colors, spacing, shadows)
3. **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation
4. **Responsiveness**: Mobile-first, scales gracefully across devices
5. **Simplicity**: Minimal markup, clear class names, no magic

---

## 🎨 Design System Tokens

### Colors

#### Brand
```css
--color-primary: #6366F1;         /* Indigo - CTAs, links */
--color-primary-hover: #4F46E5;   /* Hover state */
--color-primary-light: #818CF8;   /* Disabled state */
--color-primary-subtle: rgba(99, 102, 241, 0.08);  /* Backgrounds */
```

#### Neutrals
```css
--color-bg: #FAFAFA;              /* Page background */
--color-surface: #FFFFFF;         /* Cards */
--color-surface-raised: #F5F5F5;  /* Elevated elements */
--color-border: #E5E5E5;          /* Borders */
--color-border-subtle: #F0F0F0;   /* Inner dividers */
```

#### Text
```css
--color-text: #1A1A1A;            /* Primary text */
--color-text-secondary: #525252;  /* Secondary text */
--color-text-tertiary: #737373;   /* Tertiary text */
```

#### Semantic
```css
--color-success: #10B981;         /* Green - Correct */
--color-warning: #F59E0B;         /* Orange - Warning */
--color-error: #EF4444;           /* Red - Error */
```

### Spacing

```css
--space-1: 0.25rem;  /* 4px  - Tight spacing */
--space-2: 0.5rem;   /* 8px  - Compact */
--space-3: 0.75rem;  /* 12px - Form controls */
--space-4: 1rem;     /* 16px - Base unit (default) */
--space-6: 1.5rem;   /* 24px - Card padding */
--space-8: 2rem;     /* 32px - Section spacing */
--space-12: 3rem;    /* 48px - Large breaks */
--space-16: 4rem;    /* 64px - Page spacing */
```

### Border Radius

```css
--radius-sm: 0.375rem;  /* 6px  - Buttons, badges */
--radius-md: 0.5rem;    /* 8px  - Cards, inputs */
--radius-lg: 0.75rem;   /* 12px - Large containers */
```

### Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.06);        /* Minimal */
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);        /* Standard */
--shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);       /* High */
```

### Transitions

```css
--transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);  /* All interactions */
```

### Typography

**Font Family:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Font Sizes:**
```css
h1: 2.5rem;   /* 40px */
h2: 2rem;     /* 32px */
h3: 1.5rem;   /* 24px */
h4: 1.25rem;  /* 20px */
h5: 1.125rem; /* 18px */
h6: 1rem;     /* 16px */
body: 1rem;   /* 16px */
small: 0.875rem;  /* 14px */
```

**Font Weights:**
- 400: Regular (body text)
- 500: Medium (labels, UI elements)
- 600: Semibold (headings, emphasis)

**Line Heights:**
- Body: 1.7
- Headings: 1.2-1.3

### Breakpoints

```css
/* Mobile (default): < 640px */

/* Tablet */
@media (min-width: 640px) { }

/* Desktop */
@media (min-width: 1024px) { }
```

---

## 🔘 Buttons

### Primary Button
**Usage**: Main call-to-action, primary user actions  
**Class**: `.btn-primary`

```html
<button class="btn-primary">Start Learning</button>
```

**Variants**:
- `.btn-primary.btn-large` - Hero sections, landing page CTAs
- `.btn-primary:disabled` - Disabled state (reduced opacity, no pointer events)

**Styling**:
- Background: `--color-primary`
- Hover: `--color-primary-hover`
- Padding: `--space-3 --space-6` (12px 24px)
- Border radius: `--radius-sm`
- Transition: `--transition`

---

### Secondary Button
**Usage**: Secondary actions, cancel buttons  
**Class**: `.btn-secondary`

```html
<button class="btn-secondary">Cancel</button>
```

**Styling**:
- Background: Transparent
- Border: 1px solid `--color-border`
- Color: `--color-text`
- Hover: Background `--color-surface-raised`

---

### Icon Button
**Usage**: Icon-only actions (close, delete, edit)  
**Class**: `.btn-icon`

```html
<button class="btn-icon" aria-label="Close">×</button>
```

**Styling**:
- Size: 32×32px
- Border radius: 50% (circular)
- Hover: Background `--color-surface-raised`

---

## 🏷️ Badges

### Standard Badge
**Usage**: Status indicators, labels, tags  
**Class**: `.badge`

```html
<span class="badge">General Knowledge</span>
```

**Variants**:
- `.badge.success` - Green, for completed/correct states
- `.badge.warning` - Orange, for warnings/attention needed
- `.badge.info` - Blue, for neutral information
- `.badge.primary` - Indigo, for highlighted items

**Styling**:
- Padding: `--space-1 --space-3` (4px 12px)
- Border radius: `--radius-sm`
- Font size: 0.875rem (14px)
- Font weight: 500

---

## 🃏 Cards

### Base Card
**Usage**: Container for grouped content  
**Class**: `.card`

```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here.</p>
</div>
```

**Styling**:
- Background: `--color-surface`
- Border: 1px solid `--color-border`
- Border radius: `--radius-md`
- Padding: `--space-6` (24px)
- Shadow: `--shadow-sm`

---

### Feature Card
**Usage**: Landing page features, benefits  
**Class**: `.feature-card`

```html
<div class="feature-card">
  <div class="feature-icon">🧠</div>
  <h3>Metacognitive Analysis</h3>
  <p>Understand your confidence patterns.</p>
</div>
```

**Styling**:
- Extends: `.card`
- Hover: Slight lift (translateY -2px), shadow-md
- Transition: `--transition`
- Icon size: 48px, centered

---

### Stat Card
**Usage**: Dashboard statistics, key metrics  
**Class**: `.stat-card`

```html
<div class="stat-card">
  <div class="stat-value">87%</div>
  <div class="stat-label">Average Score</div>
</div>
```

**Styling**:
- Extends: `.card`
- Value: Font size 2rem, font weight 600
- Label: Color `--color-text-secondary`, font size 0.875rem

---

### Score Card
**Usage**: Results page scores  
**Class**: `.score-card`

```html
<div class="score-card">
  <div class="score-icon">🎯</div>
  <div class="score-value">15 / 20</div>
  <div class="score-label">Questions Correct</div>
</div>
```

**Styling**:
- Extends: `.card`
- Centered content
- Icon: 64px font size
- Value: 1.75rem, font weight 600
- Label: `--color-text-secondary`

---

### Attempt Card
**Usage**: Dashboard attempt history (card view)  
**Class**: `.attempt-card`

```html
<div class="attempt-card">
  <div class="attempt-header">
    <span class="badge success">Completed</span>
    <span class="attempt-date">2 hours ago</span>
  </div>
  <div class="attempt-stats">
    <div class="stat-item">
      <span class="stat-label">Score</span>
      <span class="stat-value">85%</span>
    </div>
    <!-- More stats -->
  </div>
</div>
```

**Styling**:
- Extends: `.card`
- Header: Flexbox, space-between alignment
- Stats: Grid layout, 2 columns
- Hover: Pointer cursor, shadow lift

---

### Insight Card
**Usage**: Results page insights  
**Class**: `.insight-card`

**Variants**:
- `.insight-card.overconfident` - Warning style
- `.insight-card.underconfident` - Info style
- `.insight-card.well-calibrated` - Success style
- `.insight-card.guessing` - Neutral style

```html
<div class="insight-card overconfident">
  <div class="insight-icon">⚠️</div>
  <h4>Overconfidence Detected</h4>
  <p>3 questions where you were very confident but incorrect.</p>
</div>
```

**Styling**:
- Background: Subtle color based on variant (8% opacity semantic color)
- Border left: 3px solid semantic color
- Icon: Large (48px)

---

### Pattern Card
**Usage**: Results page learning patterns  
**Class**: `.pattern-card`

```html
<div class="pattern-card">
  <div class="pattern-icon">🎯</div>
  <h4>Pattern Name</h4>
  <p>3 questions</p>
</div>
```

**Styling**:
- Compact size
- Icon: 40px
- Centered text
- Hover: Scale(1.02)

---

### Question Item
**Usage**: Attempt details question breakdown  
**Class**: `.question-item`

```html
<div class="question-item">
  <div class="question-header">
    <span class="badge">Science</span>
    <span class="badge success">Correct</span>
  </div>
  <h4>Question text goes here?</h4>
  <div class="question-answers">
    <div class="answer-option correct">
      <span class="answer-label">A</span>
      <span>Correct Answer</span>
      <span class="answer-marker">✓</span>
    </div>
    <div class="answer-option user-selected">
      <span class="answer-label">B</span>
      <span>Your Answer</span>
      <span class="answer-marker">Your choice</span>
    </div>
  </div>
</div>
```

**Styling**:
- Extends: `.card`
- Answer options: Flexbox with visual markers
- Correct: Green left border
- Incorrect: Red left border
- User selected: Highlighted background

---

## 📋 Forms

### Input Field
**Usage**: Text inputs, email, number fields  
**Class**: `.form-group` (wrapper), `.form-input` (input)

```html
<div class="form-group">
  <label for="name">Your Name</label>
  <input type="text" id="name" class="form-input" placeholder="Enter your name">
</div>
```

**Styling**:
- Padding: `--space-3 --space-4` (12px 16px)
- Border: 1px solid `--color-border`
- Border radius: `--radius-md`
- Focus: Border color `--color-primary`, shadow

---

### Select Dropdown
**Usage**: Dropdown selections  
**Class**: `.form-select`

```html
<select class="form-select">
  <option value="">All Categories</option>
  <option value="science">Science</option>
</select>
```

**Styling**:
- Same as `.form-input`
- Custom arrow icon (background SVG)

---

### Range Slider
**Usage**: Confidence input (1-5)  
**Class**: `.confidence-slider`

```html
<input type="range" min="1" max="5" value="3" class="confidence-slider">
```

**Styling**:
- Custom track: Height 8px, rounded
- Custom thumb: 24×24px circle
- Track fill: Primary color gradient
- Smooth transitions

---

## 📊 Data Display

### Table
**Usage**: Tabular data (dashboard table view)  
**Class**: `.table-container`, `.data-table`

```html
<div class="table-container">
  <table class="data-table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Score</th>
      </tr>
    </thead>
    <tbody>
      <tr class="clickable" onclick="location.href='/attempt/1'">
        <td>Jan 15, 2025</td>
        <td>85%</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Styling**:
- Container: Overflow-x auto (responsive)
- Header: Background `--color-surface-raised`, bold text
- Rows: Border bottom `--color-border-subtle`
- Hover: Background `--color-surface-raised` (on clickable rows)
- Min-width on cells for readability

---

### Progress Bar
**Usage**: Quiz progress, confidence visualization  
**Class**: `.progress-bar` (container), `.progress-fill` (fill)

```html
<div class="progress-bar">
  <div class="progress-fill" style="width: 60%"></div>
</div>
```

**Styling**:
- Container: Height 8px, background `--color-border`, rounded
- Fill: Background `--color-primary`, transition width
- Variants: `.success`, `.warning`, `.error` for colored fills

---

## 🔔 Feedback Components

### Empty State
**Usage**: No data available  
**Class**: `.empty-state`

```html
<div class="empty-state">
  <div class="empty-icon">📚</div>
  <h3>No Attempts Yet</h3>
  <p>Start your first quiz to see your learning progress.</p>
  <button class="btn-primary">Start Quiz</button>
</div>
```

**Styling**:
- Centered content (text-align center)
- Icon: 80px font size, muted color
- Spacing: Large gaps between elements
- Max-width: 400px

---

### Error State
**Usage**: Error occurred  
**Class**: `.error-state`

```html
<div class="error-state">
  <div class="error-icon">⚠️</div>
  <h3>Something Went Wrong</h3>
  <p>Failed to load data. Please try again.</p>
  <button class="btn-secondary" onclick="location.reload()">Retry</button>
</div>
```

**Styling**:
- Similar to `.empty-state`
- Icon: Warning color
- Focused on recovery actions

---

### Loader
**Usage**: Loading states  
**Class**: `.loader`

```html
<div class="loader"></div>
```

**Styling**:
- Animated spinning circle
- Size: 40px
- Border: 4px, primary color
- Animation: Rotate 360deg, 1s infinite

---

## 🎛️ Interactive Components

### Filter Tabs
**Usage**: Attempt details filters  
**Class**: `.filter-tabs`, `.filter-tab`

```html
<div class="filter-tabs">
  <button class="filter-tab active" data-filter="all">
    All <span class="tab-count">20</span>
  </button>
  <button class="filter-tab" data-filter="correct">
    Correct <span class="tab-count">15</span>
  </button>
</div>
```

**Styling**:
- Horizontal flex layout
- Active: Primary color text, bottom border
- Inactive: Secondary text, no border
- Hover: Primary light background
- Count badge: Muted, small

---

### View Toggle
**Usage**: Dashboard cards/table view switch  
**Class**: `.view-toggle`

```html
<div class="view-toggle">
  <button class="toggle-btn active" data-view="cards">Cards</button>
  <button class="toggle-btn" data-view="table">Table</button>
</div>
```

**Styling**:
- Button group (border radius on ends only)
- Active: Primary background, white text
- Inactive: Transparent, border, secondary text
- Smooth transitions

---

### Modal
**Usage**: Quiz start, confirmations  
**Class**: `.modal-overlay`, `.modal`

```html
<div class="modal-overlay">
  <div class="modal">
    <div class="modal-header">
      <h2>Start New Quiz</h2>
      <button class="btn-icon" onclick="closeModal()">×</button>
    </div>
    <div class="modal-body">
      <!-- Modal content -->
    </div>
    <div class="modal-footer">
      <button class="btn-secondary">Cancel</button>
      <button class="btn-primary">Start</button>
    </div>
  </div>
</div>
```

**Styling**:
- Overlay: Fixed position, rgba backdrop
- Modal: Centered, max-width 500px, shadow-lg
- Header: Border bottom
- Footer: Border top, flex layout

---

## 🧭 Navigation

### Header
**Usage**: Global navigation  
**Class**: `.header`

```html
<header class="header">
  <div class="container">
    <div class="nav-brand">
      <a href="/">Skepesis</a>
    </div>
    <nav class="nav-links">
      <a href="/dashboard">Dashboard</a>
    </nav>
  </div>
</header>
```

**Styling**:
- Background: `--color-surface`
- Border bottom: `--color-border`
- Sticky positioning (optional)
- Flexbox layout, space-between

---

### Footer
**Usage**: Global footer  
**Class**: `.footer`

```html
<footer class="footer">
  <div class="container">
    <p>&copy; 2025 Skepesis. Adaptive Learning Platform.</p>
  </div>
</footer>
```

**Styling**:
- Background: `--color-surface-raised`
- Border top: `--color-border`
- Padding: `--space-8`
- Centered text

---

## 📱 Responsive Behavior

### Breakpoints

```css
/* Mobile: < 640px (default) */
/* Tablet: 640px - 1024px */
@media (min-width: 640px) { ... }

/* Desktop: > 1024px */
@media (min-width: 1024px) { ... }
```

### Mobile Adaptations

1. **Grid Layouts**: 1 column → 2 columns → 3+ columns
2. **Typography**: Slightly smaller font sizes
3. **Spacing**: Reduced padding/margins
4. **Tables**: Horizontal scroll in container
5. **Navigation**: Hamburger menu (if implemented)
6. **Modals**: Full-width on mobile, centered on desktop

---

## ♿ Accessibility

### Focus States
All interactive elements have visible focus indicators:
```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Color Contrast
All text meets WCAG AAA standards:
- Primary text: 16.6:1 ratio
- Secondary text: 8.3:1 ratio
- Tertiary text: 5.8:1 ratio

### Semantic HTML
- Use `<button>` for actions (not `<div onclick>`)
- Use `<a>` for navigation
- Use proper heading hierarchy (h1 → h6)
- Use `<form>` for user input

### ARIA Labels
```html
<button aria-label="Close modal">×</button>
<input aria-describedby="error-message">
<div role="alert" aria-live="polite">Success!</div>
```

---

## 🎨 Customization

### Using Design Tokens

All components use CSS variables for easy theming:

```css
/* Override in :root or specific component */
.custom-button {
  background: var(--color-primary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}
```

### Component Composition

Combine classes for variations:

```html
<!-- Large primary button -->
<button class="btn-primary btn-large">Get Started</button>

<!-- Success badge with icon -->
<span class="badge success">
  <span class="badge-icon">✓</span>
  Completed
</span>
```

---

## 📖 Usage Guidelines

1. **Be Consistent**: Use the same component for the same purpose across pages
2. **Keep It Simple**: Don't over-nest components
3. **Use Semantic HTML**: Choose the right element for the job
4. **Test Responsiveness**: Check mobile, tablet, desktop views
5. **Consider Accessibility**: Add ARIA labels, test keyboard navigation
6. **Document Changes**: Update this file when adding/modifying components

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Maintained by**: Skepesis Team
