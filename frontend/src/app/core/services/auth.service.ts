import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, throwError } from 'rxjs';

// Data Contracts
export interface LoginRequest {
  username: string;  // Backend expects 'username' field (email goes here)
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  role: string;
  is_active: boolean;
  created_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);

  // Reactive State with Signals
  private tokenSignal = signal<string | null>(this.getStoredToken());
  private currentUserSignal = signal<User | null>(null);

  // Public Computed Signals
  public isLoggedIn = computed(() => !!this.tokenSignal());
  public currentUser = computed(() => this.currentUserSignal());
  public userRole = computed(() => this.currentUserSignal()?.role || null);

  constructor() {
    // Auto-load user if token exists
    if (this.tokenSignal()) {
      this.loadCurrentUser();
    }
  }

  // ==================== AUTHENTICATION ====================

  /**
   * Login with email and password
   * Backend expects FormData with 'username' and 'password' fields (OAuth2 spec)
   */
  login(email: string, password: string): Observable<AuthResponse> {
    const formData = new FormData();
    formData.append('username', email);  // FastAPI OAuth2 uses 'username'
    formData.append('password', password);

    return this.http.post<AuthResponse>('/api/auth/login', formData).pipe(
      tap(response => {
        this.setToken(response.access_token);
        localStorage.setItem('user_role', response.role);
        this.loadCurrentUser();
      }),
      catchError(error => {
        console.error('Login failed:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Register new user account
   */
  register(username: string, email: string, password: string): Observable<User> {
    const payload: RegisterRequest = { username, email, password };
    
    return this.http.post<User>('/api/auth/register', payload).pipe(
      catchError(error => {
        console.error('Registration failed:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Logout - Clear all auth data
   */
  logout(): void {
    this.clearAuth();
    this.router.navigate(['/login']);
  }

  // ==================== USER MANAGEMENT ====================

  /**
   * Load current user profile from backend
   */
  private loadCurrentUser(): void {
    this.http.get<User>('/api/auth/me').subscribe({
      next: (user) => {
        this.currentUserSignal.set(user);
      },
      error: (error) => {
        console.error('Failed to load user:', error);
        // Token might be expired or invalid
        if (error.status === 401) {
          this.clearAuth();
        }
      }
    });
  }

  /**
   * Manually refresh user data
   */
  refreshUser(): Observable<User> {
    return this.http.get<User>('/api/auth/me').pipe(
      tap(user => this.currentUserSignal.set(user))
    );
  }

  // ==================== TOKEN MANAGEMENT ====================

  /**
   * Get current JWT token
   */
  getToken(): string | null {
    return this.tokenSignal();
  }

  /**
   * Set and persist JWT token
   */
  private setToken(token: string): void {
    localStorage.setItem('access_token', token);
    this.tokenSignal.set(token);
  }

  /**
   * Get token from localStorage
   */
  private getStoredToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Clear all authentication data
   */
  private clearAuth(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    this.tokenSignal.set(null);
    this.currentUserSignal.set(null);
  }

  // ==================== UTILITY METHODS ====================

  /**
   * Check if user has specific role
   */
  hasRole(role: string): boolean {
    return this.userRole() === role;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.isLoggedIn();
  }
}
