import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  errorMessage = '';
  isLoading = false;

  onSubmit(): void {
    this.errorMessage = '';

    // Validation
    if (!this.username || !this.email || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    if (this.password.length < 6) {
      this.errorMessage = 'Password must be at least 6 characters';
      return;
    }

    this.isLoading = true;

    this.authService.register(this.username, this.email, this.password).subscribe({
      next: () => {
        // Auto-login after successful registration
        this.authService.login(this.email, this.password).subscribe({
          next: () => {
            this.router.navigate(['/dashboard']);
          },
          error: () => {
            // If auto-login fails, redirect to login page
            this.router.navigate(['/login']);
          }
        });
      },
      error: (err) => {
        this.isLoading = false;
        if (err.status === 400) {
          this.errorMessage = err.error?.detail || 'Email already registered';
        } else if (err.status === 0) {
          this.errorMessage = 'Cannot connect to server. Please ensure the backend is running.';
        } else {
          this.errorMessage = err.error?.detail || 'Registration failed. Please try again.';
        }
      }
    });
  }
}
