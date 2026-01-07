import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

/**
 * Functional Auth Guard
 * 
 * Protects routes that require authentication.
 * Redirects unauthenticated users to /login
 * 
 * Usage in routes:
 * { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] }
 */
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  // Store the attempted URL for redirecting after login
  const returnUrl = state.url;
  console.log(`Access denied. Redirecting to login. Return URL: ${returnUrl}`);

  // Redirect to login with return URL
  router.navigate(['/login'], { 
    queryParams: { returnUrl } 
  });
  
  return false;
};

/**
 * Role-based Guard Factory
 * 
 * Usage:
 * { path: 'admin', component: AdminComponent, canActivate: [roleGuard(['TEACHER', 'ADMIN'])] }
 */
export function roleGuard(allowedRoles: string[]): CanActivateFn {
  return (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (!authService.isAuthenticated()) {
      router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
      return false;
    }

    const userRole = authService.userRole();
    if (userRole && allowedRoles.includes(userRole)) {
      return true;
    }

    // User doesn't have required role
    console.warn(`Access denied. Required roles: ${allowedRoles.join(', ')}`);
    router.navigate(['/']);
    return false;
  };
}
