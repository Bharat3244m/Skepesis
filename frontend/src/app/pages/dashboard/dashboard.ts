import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  standalone: true,
  selector: 'app-dashboard',
  imports: [CommonModule, RouterModule],
  template: `
    <div class="dashboard-container">

      <header class="dashboard-header">
        <div class="breadcrumb">
          <span class="breadcrumb-current">Overview</span>
        </div>
        <h1 class="dashboard-title">
          Cognitive <span class="text-primary">Overview</span>
        </h1>
        <p class="dashboard-subtitle">
          Welcome back, {{ user?.username || 'Student' }}. Your metacognitive calibration is improving.
        </p>
      </header>

      <div class="dashboard-stats">

        <div class="metric-card featured">
          <span class="metric-indicator"></span>
          <div class="metric-value">
            85<span class="metric-unit">%</span>
          </div>
          <span class="metric-label">Confidence Calibration</span>
        </div>

        <div class="metric-card">
          <div class="metric-value">
            12
          </div>
          <span class="metric-label">Active Streaks</span>
        </div>

        <div class="metric-card">
          <div class="metric-value">
            B2
          </div>
          <span class="metric-label">Knowledge Level</span>
        </div>

        <div class="metric-card">
          <div class="metric-value">
            450
          </div>
          <span class="metric-label">Points Earned</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: var(--space-8);">

        <div class="main-column">

          <div class="section-header">
            <h2 class="section-title">Learning Profile</h2>
          </div>

          <div class="learning-style-card loaded mb-4">
            <div class="style-indicator">
              <span class="style-icon-inner">👁️</span>
            </div>
            <div class="style-content">
              <h3 class="style-name">Visual Learner</h3>
              <p class="style-description">
                You retain 40% more information when concepts are presented with diagrams.
              </p>
            </div>
          </div>

          <div class="section-header">
            <h2 class="section-title">Recent Activity</h2>
          </div>

          <div class="recent-grid">
            <a routerLink="/quiz" class="recent-card">
              <div class="recent-card-header">
                <div class="recent-avatar">Ph</div>
                <div class="recent-info">
                  <span class="recent-name">Physics: Quantum Mechanics</span>
                  <span class="recent-date">2 hours ago</span>
                </div>
              </div>
              <div class="recent-card-stats">
                <div class="recent-stat">
                  <span class="recent-stat-value success">92%</span>
                  <span class="recent-stat-label">Score</span>
                </div>
                <div class="recent-stat">
                  <span class="recent-stat-value">High</span>
                  <span class="recent-stat-label">Confidence</span>
                </div>
              </div>
            </a>

            <a routerLink="/quiz" class="recent-card">
              <div class="recent-card-header">
                <div class="recent-avatar" style="background: var(--color-warning);">Hi</div>
                <div class="recent-info">
                  <span class="recent-name">History: World War II</span>
                  <span class="recent-date">Yesterday</span>
                </div>
              </div>
              <div class="recent-card-stats">
                <div class="recent-stat">
                  <span class="recent-stat-value warning">78%</span>
                  <span class="recent-stat-label">Score</span>
                </div>
                <div class="recent-stat">
                  <span class="recent-stat-value">Med</span>
                  <span class="recent-stat-label">Confidence</span>
                </div>
              </div>
            </a>
          </div>

        </div>

        <div class="sidebar-column">

          <div class="panel">
            <h3 class="panel-title mb-3">Quick Actions</h3>

            <a routerLink="/quiz" class="btn btn-primary btn-block mb-2" style="justify-content: center;">
              Start Daily Quiz
            </a>

            <a routerLink="/profile" class="btn btn-secondary btn-block" style="justify-content: center;">
              View Full Report
            </a>
          </div>

          <div class="panel mt-4">
            <h3 class="panel-title mb-3">Weekly Growth</h3>

            <div class="simple-chart">
              <div class="chart-bar-group">
                <div class="chart-bar-container">
                  <div class="chart-bar" style="height: 40%;"></div>
                </div>
                <span class="chart-label">M</span>
              </div>
              <div class="chart-bar-group">
                <div class="chart-bar-container">
                  <div class="chart-bar" style="height: 60%;"></div>
                </div>
                <span class="chart-label">T</span>
              </div>
              <div class="chart-bar-group">
                <div class="chart-bar-container">
                  <div class="chart-bar" style="height: 85%;"></div>
                </div>
                <span class="chart-label">W</span>
              </div>
              <div class="chart-bar-group">
                <div class="chart-bar-container">
                  <div class="chart-bar" style="height: 70%; background: var(--color-accent);"></div>
                </div>
                <span class="chart-label">T</span>
              </div>
            </div>

            <div class="trend-indicator improving">
              <span class="trend-text">+12%</span>
              <span class="trend-detail">vs last week</span>
            </div>

          </div>

        </div>
      </div>
    </div>
  `
})
export class DashboardComponent implements OnInit {
  user: any;

  constructor(private auth: AuthService) {}

  ngOnInit() {
    this.auth.user$.subscribe(u => this.user = u);
  }
}
