import { Routes } from '@angular/router';
import { LayoutComponent } from './shared/layout/layout';

export const routes: Routes = [
  // 1. PUBLIC LANDING PAGE (Root Path)
  // This puts the UI you want on the Home Page
  {
    path: '',
    component: LayoutComponent,
    children: [
      {
        path: '',
        loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent)
      }
    ]
  },

  // 2. Auth Pages (Login/Register)
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register').then(m => m.RegisterComponent)
  },

  // 3. Protected Dashboard (User Only)
  {
    path: 'dashboard',
    component: LayoutComponent,
    children: [
      {
        path: '',
        loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.DashboardComponent)
      }
    ]
  },

  // 4. Other Protected Pages
  {
    path: 'profile',
    component: LayoutComponent,
    children: [
      {
        path: '',
        loadComponent: () => import('./pages/profile/profile').then(m => m.ProfileComponent)
      }
    ]
  },
  {
    path: 'quiz',
    component: LayoutComponent,
    children: [
      {
        path: '',
        loadComponent: () => import('./features/quiz/quiz').then(m => m.QuizComponent)
      }
    ]
  },

  // Fallback
  { path: '**', redirectTo: '' }
];
