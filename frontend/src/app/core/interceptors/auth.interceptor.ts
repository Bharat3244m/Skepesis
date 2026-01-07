import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

/**
 * Functional HTTP Interceptor for JWT Authentication
 * 
 * Features:
 * - Automatically attaches Authorization header with JWT token
 * - Handles 401 Unauthorized errors by logging out user
 * - Skips token for public endpoints (login, register)
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  // List of public endpoints that don't need authentication
  const publicEndpoints = ['/api/auth/login', '/api/auth/register'];
  const isPublicEndpoint = publicEndpoints.some(endpoint => req.url.includes(endpoint));

  // Clone request and add Authorization header if:
  // 1. Token exists
  // 2. Not a public endpoint
  let authReq = req;
  if (token && !isPublicEndpoint) {
    authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  // Handle response and catch 401 errors
  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !isPublicEndpoint) {
        // Token expired or invalid - auto logout
        console.warn('Unauthorized access - logging out');
        authService.logout();
      }
      return throwError(() => error);
    })
  );
};
