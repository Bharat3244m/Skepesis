import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { QuizComponent } from './features/quiz/quiz.component';
import { AnalysisComponent } from './features/analysis/analysis.component';
import { CuriosityComponent } from './features/curiosity/curiosity.component';
import { HistoryComponent } from './features/dashboard/history.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { ProfileComponent } from './features/profile/profile.component';
import { AttemptDetailsComponent } from './features/analysis/attempt-details/attempt-details.component';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  
  // Protected routes - require authentication
  { path: 'quiz', component: QuizComponent, canActivate: [authGuard] },
  { path: 'results/:id', component: AnalysisComponent, canActivate: [authGuard] },
  { path: 'attempt/:id', component: AttemptDetailsComponent, canActivate: [authGuard] },
  { path: 'curiosity', component: CuriosityComponent, canActivate: [authGuard] },
  { path: 'dashboard', component: HistoryComponent, canActivate: [authGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
  
  { path: '**', redirectTo: '' }
];