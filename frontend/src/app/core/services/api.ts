import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // We use a relative path because the proxy handles the rest
  private baseUrl = '/api'; 

  constructor(private http: HttpClient) {}

  // Generic GET method
  get<T>(endpoint: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${endpoint}`);
  }

  // Generic POST method
  post<T>(endpoint: string, data: any): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${endpoint}`, data);
  }

  // Specific: Get All Attempts
  getAttempts() {
    return this.get<any[]>('attempts/');
  }

  // Specific: Get Single Attempt Details
  getAttemptDetails(id: string) {
    return this.get<any>(`attempts/${id}`);
  }
  
  // Specific: Get Responses for an Attempt
  getAttemptResponses(id: string) {
    return this.get<any>(`attempts/${id}/responses`);
  }

  // Quiz/Trivia endpoints
  getTriviaCategories() {
    return this.get<{ categories: { [key: string]: string } }>('trivia/categories');
  }

  generateQuiz(amount: number = 10, category?: number, difficulty?: string) {
    let endpoint = `quiz/generate?amount=${amount}&type=multiple`;
    if (category) endpoint += `&category=${category}`;
    if (difficulty && difficulty !== 'any') endpoint += `&difficulty=${difficulty}`;
    return this.get<any[]>(endpoint);
  }

  // Create a new attempt (start a quiz session)
  createAttempt(studentEmail: string) {
    return this.post<any>('attempts/', { student_name: studentEmail });
  }

  // Submit a response
  submitResponse(payload: {
    attempt_id: number;
    question_id: number;
    question_text: string;
    user_answer: string;
    confidence_level: number;
    time_spent: number;
    category: string;
    difficulty: string;
    correct_answer: string;
  }) {
    return this.post<any>('responses/', payload);
  }

  // Complete an attempt
  completeAttempt(attemptId: number) {
    return this.post<any>(`attempts/${attemptId}/complete`, {});
  }
}