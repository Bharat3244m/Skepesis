import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { QuizComponent } from './features/quiz/quiz.component';
import { AnalysisComponent } from './features/analysis/analysis.component';
import { CuriosityComponent } from './features/curiosity/curiosity.component';
import { HistoryComponent } from './features/dashboard/history.component';
// Correct nested paths:
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { ProfileComponent } from './features/profile/profile.component';
import { AttemptDetailsComponent } from './features/analysis/attempt-details/attempt-details.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'quiz', component: QuizComponent },
  { path: 'results/:id', component: AnalysisComponent },
  { path: 'attempt/:id', component: AttemptDetailsComponent },
  { path: 'curiosity', component: CuriosityComponent },
  { path: 'dashboard', component: HistoryComponent },
  { path: 'profile', component: ProfileComponent },
  { path: '**', redirectTo: '' }
];