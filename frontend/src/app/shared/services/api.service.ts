import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AttemptStats {
  accuracy: number;
  curiosity: number;
  confidence: number;
  alignment: number;
}

export interface AttemptDetail {
  id: number;
  student_name: string;
  started_at: string;
  completed_at: string | null;
  total_questions: number;
  correct_answers: number;
  average_confidence: number;
  curiosity_score: number;
}

export interface QuestionResponse {
  id: number;
  attempt_id: number;
  question_id: number;
  question_text: string;
  user_answer: string;
  is_correct: boolean;
  confidence_level: number;
  time_spent: number;
  category: string;
  difficulty: string;
  correct_answer?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  private apiUrl = environment?.apiUrl || 'http://127.0.0.1:8080/api';

  // Get attempt details
  getAttempt(attemptId: number): Observable<AttemptDetail> {
    return this.http.get<AttemptDetail>(`${this.apiUrl}/attempts/${attemptId}`);
  }

  // Get all responses for an attempt
  getAttemptResponses(attemptId: number): Observable<QuestionResponse[]> {
    return this.http.get<QuestionResponse[]>(`${this.apiUrl}/responses/attempt/${attemptId}`);
  }

  // Get AI insights for an attempt
  getAttemptInsights(attemptId: number): Observable<{ attempt_id: number, student_name: string, ai_insights: string }> {
    return this.http.get<{ attempt_id: number, student_name: string, ai_insights: string }>(`${this.apiUrl}/attempts/${attemptId}/insights`);
  }
}
