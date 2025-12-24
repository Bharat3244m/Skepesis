import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  standalone: true,
  selector: 'app-profile',
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container" style="padding-top: var(--space-8); padding-bottom: var(--space-12);">

      <div style="margin-bottom: var(--space-8); display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <h1 class="section-title" style="margin-bottom: 4px; font-size: 2rem;">Student Profile</h1>
          <p class="section-subtitle" style="margin: 0;">Manage your account and viewing learning preferences.</p>
        </div>
        <span class="status-pill success">
          <span class="status-dot"></span> Online
        </span>
      </div>

      <div class="profile-grid">

        <aside class="profile-sidebar">

          <div class="panel" style="text-align: center; padding: var(--space-8) var(--space-6);">
            <div class="avatar-large">
              {{ getInitials(user?.username) }}
            </div>

            <h2 class="profile-name">{{ user?.username || 'User' }}</h2>
            <p class="text-muted" style="font-size: 0.9rem;">{{ user?.email }}</p>

            <div style="margin: var(--space-4) 0;">
              <span class="status-pill info">{{ user?.role || 'Student' }}</span>
            </div>

            <div class="divider"></div>

            <div style="text-align: left;">
              <div class="meta-row">
                <span class="meta-icon">📅</span>
                <div>
                  <div class="meta-label">Joined</div>
                  <div class="meta-value">Dec 19, 2025</div>
                </div>
              </div>
              <div class="meta-row">
                <span class="meta-icon">📍</span>
                <div>
                  <div class="meta-label">Region</div>
                  <div class="meta-value">Asia/Kolkata</div>
                </div>
              </div>
            </div>

            <div class="divider"></div>

            <button class="btn btn-primary btn-block">Edit Profile</button>
          </div>

          <div class="panel" style="margin-top: var(--space-4); border-color: rgba(220, 38, 38, 0.2);">
            <h4 style="font-size: 0.85rem; color: #DC2626; margin-bottom: var(--space-3); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;">Danger Zone</h4>
            <button class="btn-link" style="color: #DC2626; padding: 0; font-size: 0.85rem;">Delete Account</button>
          </div>

        </aside>

        <main class="profile-content">

          <div class="stats-row">
            <div class="metric-card featured">
              <span class="metric-indicator"></span>
              <div class="metric-value">87</div>
              <span class="metric-label">Curiosity Score</span>
            </div>

            <div class="metric-card">
              <div class="metric-value" style="color: var(--color-success);">5 <span style="font-size: 1rem; color: var(--color-text-tertiary);">days</span></div>
              <span class="metric-label">Current Streak</span>
            </div>

            <div class="metric-card">
              <div class="metric-value">14</div>
              <span class="metric-label">Total Sessions</span>
            </div>
          </div>

          <div class="panel">
            <div class="panel-header" style="display: flex; justify-content: space-between; align-items: center;">
              <h3 class="panel-title">Learning Context</h3>
              <button class="btn-link" style="font-size: 0.85rem;">Update</button>
            </div>

            <div class="context-grid">
              <div class="context-item">
                <span class="context-label">Primary Goal</span>
                <span class="context-value">Mastery</span>
              </div>
              <div class="context-item">
                <span class="context-label">Field of Interest</span>
                <span class="context-value">General Science</span>
              </div>
              <div class="context-item">
                <span class="context-label">Weekly Commitment</span>
                <span class="context-value">5 Hours</span>
              </div>
              <div class="context-item">
                <span class="context-label">Skill Level</span>
                <span class="context-value">Intermediate</span>
              </div>
            </div>
          </div>

          <div class="feature-card" style="display: flex; align-items: center; gap: var(--space-6); background: var(--color-surface);">
            <div class="feature-icon" style="background: var(--color-primary-subtle); width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border-radius: 12px; font-size: 2rem;">
              ⚛️
            </div>
            <div>
              <h3 class="feature-title" style="margin-bottom: 4px;">Current Focus: Physics</h3>
              <p class="feature-description" style="margin: 0;">
                You are currently exploring Quantum Mechanics. Your next recommended topic is <strong>Wave-Particle Duality</strong>.
              </p>
            </div>
            <button class="btn btn-secondary" style="margin-left: auto;">Continue</button>
          </div>

        </main>
      </div>
    </div>
  `,
  styles: [`
    /* GRID SYSTEM */
    .profile-grid {
      display: grid;
      grid-template-columns: 320px 1fr; /* Sidebar fixed, content flexible */
      gap: var(--space-8);
      align-items: start;
    }

    /* AVATAR STYLING */
    .avatar-large {
      width: 120px;
      height: 120px;
      background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
      color: white;
      font-size: 3rem;
      font-weight: 700;
      border-radius: 50%; /* Circle */
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto var(--space-5);
      box-shadow: var(--shadow-md);
    }

    .profile-name {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-text);
      margin-bottom: var(--space-1);
    }

    /* META DATA (Sidebar) */
    .meta-row {
      display: flex;
      gap: var(--space-3);
      margin-bottom: var(--space-4);
      align-items: flex-start;
    }
    .meta-icon { font-size: 1.25rem; opacity: 0.7; }
    .meta-label { font-size: 0.75rem; color: var(--color-text-tertiary); text-transform: uppercase; font-weight: 600; }
    .meta-value { font-size: 0.9rem; color: var(--color-text); font-weight: 500; }

    .divider {
      height: 1px;
      background: var(--color-border-subtle);
      margin: var(--space-6) 0;
    }

    /* STATS ROW */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--space-4);
      margin-bottom: var(--space-6);
    }

    /* CONTEXT GRID */
    .context-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-6);
    }
    .context-item { display: flex; flex-direction: column; gap: 4px; }
    .context-label { font-size: 0.8rem; color: var(--color-text-tertiary); font-weight: 500; }
    .context-value { font-size: 1rem; color: var(--color-text); font-weight: 600; }

    /* RESPONSIVE */
    @media (max-width: 900px) {
      .profile-grid { grid-template-columns: 1fr; } /* Stack on tablet/mobile */
      .stats-row { grid-template-columns: 1fr; }
      .context-grid { grid-template-columns: 1fr; }
      .feature-card { flex-direction: column; text-align: center; }
      .feature-card button { margin: var(--space-4) 0 0 0; }
    }
  `]
})
export class ProfileComponent implements OnInit {
  user: any;

  constructor(private auth: AuthService) {}

  ngOnInit() {
    this.auth.user$.subscribe(u => this.user = u);
  }

  getInitials(name: string): string {
    return name ? name.substring(0, 2).toUpperCase() : 'SK';
  }
}
