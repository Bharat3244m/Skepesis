import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-home',
  imports: [CommonModule, RouterModule],
  template: `
    <section class="hero">
      <div class="container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-12); align-items: center;">

          <div class="hero-content">
            <div class="status-pill info" style="margin-bottom: var(--space-4);">
              <span class="status-dot"></span>
              v2.0 Now Live
            </div>

            <h1 class="hero-title">
              Learning that <br>
              <span class="gradient-text">Adapts to You</span>
            </h1>

            <p class="hero-subtitle">
              Stop wasting time on what you already know. Skepesis uses metacognitive analysis to predict learning gaps before you even see them.
            </p>

            <div class="hero-cta">
              <a routerLink="/register" class="btn btn-primary btn-large">
                Get Started Free
              </a>
              <a routerLink="/login" class="btn btn-secondary btn-large">
                Live Demo
              </a>
            </div>

            <div class="hero-stats">
              <div class="hero-stat">
                <div class="hero-stat-value">12k+</div>
                <div class="hero-stat-label">Active Learners</div>
              </div>
              <div class="hero-stat">
                <div class="hero-stat-value">85%</div>
                <div class="hero-stat-label">Retention Rate</div>
              </div>
              <div class="hero-stat">
                <div class="hero-stat-value">24/7</div>
                <div class="hero-stat-label">AI Tutor</div>
              </div>
            </div>
          </div>

          <div class="hero-visual">
            <div class="data-grid">
              <div class="data-point" style="--delay: 0s">
                <div class="metric-value">A+</div>
                <div class="metric-label">Physics Mastery</div>
                <div style="margin-top: 10px; height: 4px; background: #e2e8f0; border-radius: 2px;">
                  <div style="width: 90%; height: 100%; background: var(--color-success); border-radius: 2px;"></div>
                </div>
              </div>

              <div class="data-point" style="--delay: 0.1s">
                <div class="metric-value">0.8s</div>
                <div class="metric-label">Avg Response</div>
              </div>

              <div class="data-point" style="--delay: 0.2s; grid-column: span 2;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                  <span class="metric-label">Learning Curve</span>
                  <span class="status-pill success">Optimal</span>
                </div>
                <svg viewBox="0 0 100 20" style="width: 100%; height: 40px; stroke: var(--color-primary); fill: none; stroke-width: 2;">
                  <path d="M0,20 C20,20 20,10 40,10 C60,10 60,0 100,0" />
                </svg>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <div class="features-header">
          <span class="features-badge">Core Engine</span>
          <h2 class="section-title">Cognitive Architecture</h2>
          <p class="section-subtitle">
            Most platforms test memory. Skepesis tests understanding.
          </p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3 class="feature-title">Metacognition</h3>
            <p class="feature-description">
              We ask "How confident are you?" before every answer to detect the Dunning-Kruger effect and calibration gaps.
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">Dynamic Difficulty</h3>
            <p class="feature-description">
              The AI adjusts question complexity in real-time, keeping you in the "Zone of Proximal Development."
            </p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Gap Analysis</h3>
            <p class="feature-description">
              Our dashboard doesn't just show scores; it visualizes the specific concepts holding you back.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="how-it-works">
      <div class="container">
        <div class="how-header">
          <h2 class="section-title">How It Works</h2>
        </div>

        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <h3 class="step-title">Take a Quiz</h3>
            <p class="step-description">Answer adaptive questions tailored to your level.</p>
          </div>
          <div class="step-card">
            <div class="step-number">2</div>
            <h3 class="step-title">Rate Confidence</h3>
            <p class="step-description">Tell us how sure you are about your answer.</p>
          </div>
          <div class="step-card">
            <div class="step-number">3</div>
            <h3 class="step-title">AI Analysis</h3>
            <p class="step-description">We detect if you're guessing or truly mastering it.</p>
          </div>
          <div class="step-card">
            <div class="step-number">4</div>
            <h3 class="step-title">Growth</h3>
            <p class="step-description">Receive a custom study plan to close your gaps.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container">
        <div class="cta-card">
          <h2 class="cta-title">Ready to upgrade your brain?</h2>
          <p class="cta-description">
            Join thousands of students using Skepesis to learn faster and retain more.
          </p>
          <a routerLink="/register" class="btn btn-primary btn-large" style="background: white; color: var(--color-primary);">
            Create Free Account
          </a>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container">
        <div class="footer-text">&copy; 2025 Skepesis Inc.</div>
        <p class="footer-tagline">Designed for lifelong learners.</p>
      </div>
    </footer>
  `
})
export class HomeComponent {}
