import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AppService {
  apiBase = '/api';

  constructor(private http: HttpClient) {}

  get<T>(endpoint: string) {
    return this.http.get<T>(`${this.apiBase}${endpoint}`);
  }

  post<T>(endpoint: string, data: any) {
    return this.http.post<T>(`${this.apiBase}${endpoint}`, data);
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }
}
