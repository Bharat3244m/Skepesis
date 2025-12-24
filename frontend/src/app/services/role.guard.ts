import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from './auth';
import { Router } from '@angular/router';

export function roleGuard(allowed: string[]): CanActivateFn {
  return () => {
    const auth = inject(AuthService);
    const router = inject(Router);

    if (auth.hasRole(allowed)) {
      return true;
    }

    router.navigate(['/dashboard']);
    return false;
  };
}
