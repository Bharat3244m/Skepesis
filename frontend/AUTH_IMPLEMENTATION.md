# JWT Authentication System - Implementation Guide

## 🎯 Architecture Overview

This authentication system uses **Angular Signals** for reactive state management and **Functional Guards/Interceptors** for modern Angular 18+ patterns.

## 📁 File Structure

```
src/app/
├── core/
│   ├── guards/
│   │   └── auth.guard.ts          # Functional route guard
│   ├── interceptors/
│   │   └── auth.interceptor.ts    # HTTP interceptor
│   └── services/
│       └── auth.service.ts        # Main auth service (Signals)
└── features/
    └── auth/
        ├── login/
        │   ├── login.component.ts       # Reactive Forms
        │   ├── login.component.html
        │   └── login.component.scss
        └── register/
            ├── register.component.ts
            ├── register.component.html
            └── register.component.scss
```

## 🔐 Authentication Flow

### 1. Login Process
```typescript
// User submits login form
email: "test@example.com"
password: "password123"

// Frontend sends FormData (OAuth2 spec)
POST /api/auth/login
Body: FormData {
  username: "test@example.com",  // Note: 'username' field!
  password: "password123"
}

// Backend responds
Response: {
  access_token: "eyJhbGciOiJIUzI1NiIs...",
  token_type: "bearer",
  role: "STUDENT"
}

// Service stores token
localStorage.setItem('access_token', token)
tokenSignal.set(token)

// Service loads user profile
GET /api/auth/me
Headers: { Authorization: "Bearer eyJhbG..." }

Response: {
  id: 1,
  email: "test@example.com",
  username: "teststudent",
  role: "STUDENT",
  is_active: true
}
```

### 2. Protected Route Access
```typescript
// User navigates to /dashboard
authGuard checks isAuthenticated()
  ├─ true  → Allow access
  └─ false → Redirect to /login?returnUrl=/dashboard
```

### 3. Auto-Logout on 401
```typescript
// Any API call returns 401
authInterceptor catches error
  → Calls authService.logout()
  → Clears localStorage
  → Redirects to /login
```

## 🚀 Quick Start

### 1. Test Login
```bash
# Navigate to login page
http://localhost:4200/login

# Use test credentials
Email: test@example.com
Password: password123
```

### 2. Access Protected Routes
After login, these routes are accessible:
- `/dashboard` - User history
- `/quiz` - Take quiz
- `/attempt/:id` - View attempt details
- `/profile` - User profile
- `/curiosity` - Curiosity analysis

### 3. Check Auth State
```typescript
// In any component
import { AuthService } from '@core/services/auth.service';

export class MyComponent {
  private authService = inject(AuthService);
  
  // Reactive signals
  isLoggedIn = this.authService.isLoggedIn();
  currentUser = this.authService.currentUser();
  userRole = this.authService.userRole();
}
```

## 📊 API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/login` | POST | ❌ | Login with credentials |
| `/api/auth/register` | POST | ❌ | Create new account |
| `/api/auth/me` | GET | ✅ | Get current user |
| `/api/attempts` | GET | ✅ | List user attempts |
| `/api/quiz/generate` | GET | ✅ | Generate quiz |

## 🔧 Configuration

### App Config (already set up)
```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withFetch(),
      withInterceptors([authInterceptor])  // ✅ Auto-adds Bearer token
    )
  ]
};
```

### Protected Routes
```typescript
// app.routes.ts
{ 
  path: 'dashboard', 
  component: DashboardComponent, 
  canActivate: [authGuard]  // ✅ Requires login
}
```

### Role-Based Protection
```typescript
import { roleGuard } from '@core/guards/auth.guard';

{ 
  path: 'admin', 
  component: AdminComponent, 
  canActivate: [roleGuard(['TEACHER', 'ADMIN'])] 
}
```

## 🎨 Usage Examples

### In Components
```typescript
// Using signals (reactive)
export class DashboardComponent {
  private authService = inject(AuthService);
  
  // Auto-updates when auth state changes
  isLoggedIn = this.authService.isLoggedIn();
  user = this.authService.currentUser();
  
  logout() {
    this.authService.logout(); // Auto-redirects to /login
  }
}
```

### In Templates
```html
<!-- Show/hide based on auth -->
<div *ngIf="authService.isLoggedIn()">
  Welcome, {{ authService.currentUser()?.username }}!
</div>

<!-- Role-based display -->
<button *ngIf="authService.hasRole('TEACHER')">
  View Student Reports
</button>
```

## 🧪 Testing

### Manual Testing
1. **Register new user:**
   - Go to `/register`
   - Fill form and submit
   - Should auto-login and redirect to dashboard

2. **Login existing user:**
   - Go to `/login`
   - Enter credentials
   - Should redirect to `/dashboard` (or returnUrl)

3. **Protected routes:**
   - Try accessing `/quiz` without login
   - Should redirect to `/login?returnUrl=/quiz`
   - After login, should redirect back to `/quiz`

4. **Token expiry:**
   - Login successfully
   - Manually delete `access_token` from localStorage
   - Make any API call
   - Should auto-logout and redirect to `/login`

### Backend Requirements
Ensure backend is running on `http://127.0.0.1:8080`:
```bash
cd backend
uvicorn app.main:app --reload --port 8080
```

## 🐛 Troubleshooting

### "401 Unauthorized" errors
- Check if token exists: `localStorage.getItem('access_token')`
- Verify backend is running on port 8080
- Check browser console for CORS errors

### Infinite redirect loops
- Clear localStorage: `localStorage.clear()`
- Check if route guard logic is correct
- Verify `returnUrl` is not `/login`

### Form validation not showing
- Ensure `ReactiveFormsModule` is imported
- Check if form controls are touched: `form.markAllAsTouched()`

## 🎓 Key Concepts

1. **Signals** - Reactive primitive for state management (replaces BehaviorSubject)
2. **Functional Guards** - Modern `CanActivateFn` instead of class-based guards
3. **Functional Interceptors** - `HttpInterceptorFn` for cleaner code
4. **Reactive Forms** - Type-safe form validation with `FormBuilder`
5. **OAuth2 Password Flow** - Backend expects FormData with 'username' field

## ✨ Features

- ✅ JWT token storage and automatic injection
- ✅ Auto-logout on 401 errors
- ✅ Protected routes with guards
- ✅ Role-based access control
- ✅ Return URL support after login
- ✅ Reactive state with Signals
- ✅ Form validation with user-friendly errors
- ✅ Loading states and error handling

---

**Next Steps:**
1. Test login/register flow
2. Navigate to protected routes
3. Check browser DevTools → Network tab for Authorization headers
4. Enjoy your secure app! 🎉
