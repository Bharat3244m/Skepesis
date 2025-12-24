import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  standalone: true,
  selector: 'app-login',
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="page-wrapper" style="display: flex; align-items: center; justify-content: center;">

      <div class="panel" style="width: 100%; max-width: 400px; padding: var(--space-8);">

        <div class="text-center mb-4">
          <h2 class="section-title">Welcome Back</h2>
          <p class="section-subtitle">Sign in to continue learning</p>
        </div>

        <div *ngIf="error" class="error-state" style="padding: var(--space-4); margin-bottom: var(--space-4);">
          {{ error }}
        </div>

        <form (ngSubmit)="onSubmit()">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-input"
              [(ngModel)]="email"
              name="email"
              required
              placeholder="student@example.com">
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <input
              type="password"
              class="form-input"
              [(ngModel)]="password"
              name="password"
              required>
          </div>

          <button type="submit" [disabled]="loading" class="btn btn-primary btn-block" style="width: 100%; margin-top: var(--space-4);">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <div style="text-align: center; margin-top: var(--space-6);">
          <p class="text-muted">
            Don't have an account?
            <a routerLink="/register" style="font-weight: 600;">Register here</a>
          </p>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  email = '';
  password = '';
  loading = false;
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  onSubmit() {
    this.loading = true;
    this.error = '';

    this.auth.login(this.email, this.password).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.error = 'Invalid credentials';
        this.loading = false;
      }
    });
  }
}
