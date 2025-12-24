import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { tap, catchError, map } from 'rxjs/operators';

// Match the backend User schema
export interface User {
  email: string;
  username: string;
  role: string;
  access_token?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // Hardcoded to localhost:8000 as per your backend setup
  private apiUrl = 'http://localhost:8000/api/auth';

  // State management
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadUserFromStorage();
  }

  // --- 1. Login (Fixes OAuth2 Form Data requirement) ---
  login(email: string, password: string): Observable<any> {
    // FastAPI's OAuth2PasswordRequestForm expects form-data, not JSON
    const formData = new FormData();
    formData.append('username', email); // OAuth2 standard uses 'username' field for email
    formData.append('password', password);

    return this.http.post<User>(`${this.apiUrl}/login`, formData).pipe(
      tap(response => this.handleAuthSuccess(response)),
      catchError(this.handleError)
    );
  }

  // --- 2. Register (Fixes your "Expected 1 argument" error) ---
  register(username: string, email: string, password: string): Observable<any> {
    const payload = { username, email, password };
    return this.http.post(`${this.apiUrl}/register`, payload).pipe(
      catchError(this.handleError)
    );
  }

  // --- 3. Logout ---
  logout() {
    // Call backend to clear cookies
    this.http.post(`${this.apiUrl}/logout`, {}).subscribe();
    // Clear local state
    localStorage.removeItem('user_data');
    this.userSubject.next(null);
  }

  // --- Helper Methods ---

  private handleAuthSuccess(response: any) {
    // Decode token or use returned user data
    const user: User = {
      email: response.sub || '', // Adjust based on your actual API response structure
      username: 'User',          // You might want to fetch the real profile after login
      role: response.role,
      access_token: response.access_token
    };

    // Save to local storage for persistence across refreshes
    localStorage.setItem('user_data', JSON.stringify(user));
    this.userSubject.next(user);
  }

  private loadUserFromStorage() {
    const stored = localStorage.getItem('user_data');
    if (stored) {
      try {
        this.userSubject.next(JSON.parse(stored));
      } catch {
        localStorage.removeItem('user_data');
      }
    }
  }

  isAuthenticated(): boolean {
    return this.userSubject.value !== null;
  }

  getRole(): string {
    return this.userSubject.value?.role || '';
  }

  hasRole(allowedRoles: string[]): boolean {
    const currentRole = this.getRole();
    return !allowedRoles || allowedRoles.length === 0 || allowedRoles.includes(currentRole);
  }

  private handleError(error: HttpErrorResponse) {
    let msg = 'Unknown error occurred';
    if (error.error && error.error.detail) {
      msg = error.error.detail; // FastAPI error message
    }
    return throwError(() => new Error(msg));
  }
}
