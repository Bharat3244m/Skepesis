import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { ApiService, AttemptDetail, QuestionResponse } from '../../../shared/services/api.service';

interface SessionDisplay {
  id: number;
  student: string;
  date: string;
  time: string;
  status: string;
  questions_count: number;
  stats: {
    accuracy: number;
    curiosity: number;
    confidence: number;
    alignment: number;
  };
}

interface ResponseDisplay {
  id: number;
  text: string;
  user_answer: string;
  correct_answer?: string;
  is_correct: boolean;
  confidence: number;
  category: string;
  time: number;
}

@Component({
  selector: 'app-attempt-details',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './attempt-details.component.html',
  styleUrls: ['./attempt-details.component.scss']
})
export class AttemptDetailsComponent implements OnInit {
  private apiService = inject(ApiService);
  private route = inject(ActivatedRoute);

  attemptId: string | null = null;
  activeFilter = 'all';
  loading = true;
  error: string | null = null;

  // Session Data
  session: SessionDisplay = {
    id: 0,
    student: '',
    date: '',
    time: '',
    status: 'Loading...',
    questions_count: 0,
    stats: {
      accuracy: 0,
      curiosity: 0,
      confidence: 0,
      alignment: 0
    }
  };

  allResponses: ResponseDisplay[] = [];
  filteredResponses: ResponseDisplay[] = [];

  constructor() {}

  ngOnInit(): void {
    this.attemptId = this.route.snapshot.paramMap.get('id');
    if (this.attemptId) {
      this.loadAttemptData(parseInt(this.attemptId, 10));
    }
  }

  private loadAttemptData(id: number): void {
    this.loading = true;
    this.error = null;

    console.log(`Loading attempt ${id}...`);

    // Load both attempt details and responses
    Promise.all([
      this.apiService.getAttempt(id).toPromise(),
      this.apiService.getAttemptResponses(id).toPromise()
    ])
      .then(([attempt, responses]) => {
        console.log('Attempt data loaded:', attempt, responses);
        if (attempt && responses) {
          this.session = this.mapAttemptToSession(attempt, responses);
          this.allResponses = this.mapResponsesToDisplay(responses);
          this.filteredResponses = this.allResponses;
        }
        this.loading = false;
      })
      .catch(err => {
        console.error('Error loading attempt data:', err);
        
        // More specific error messages
        if (err.status === 404) {
          this.error = `Session #${id} not found. It may have been deleted or doesn't exist.`;
        } else if (err.status === 0) {
          this.error = 'Cannot connect to the server. Please ensure the backend is running on http://127.0.0.1:8080';
        } else if (err.status === 401 || err.status === 403) {
          this.error = 'You do not have permission to view this session.';
        } else {
          this.error = `Failed to load session details. Error: ${err.message || 'Unknown error'}`;
        }
        
        this.loading = false;
      });
  }

  private mapAttemptToSession(attempt: AttemptDetail, responses: QuestionResponse[]): SessionDisplay {
    const startedAt = new Date(attempt.started_at);
    const accuracy = attempt.total_questions > 0 
      ? Math.round((attempt.correct_answers / attempt.total_questions) * 100) 
      : 0;

    // Calculate alignment (confidence calibration)
    const alignment = this.calculateAlignment(responses);

    return {
      id: attempt.id,
      student: attempt.student_name.split('@')[0], // Extract name from email
      date: this.formatDate(startedAt),
      time: this.formatTime(startedAt),
      status: attempt.completed_at ? 'COMPLETED' : 'IN PROGRESS',
      questions_count: attempt.total_questions,
      stats: {
        accuracy: accuracy,
        curiosity: Math.round(attempt.curiosity_score),
        confidence: Math.round(attempt.average_confidence),
        alignment: alignment
      }
    };
  }

  private mapResponsesToDisplay(responses: QuestionResponse[]): ResponseDisplay[] {
    return responses.map(r => ({
      id: r.id,
      text: r.question_text,
      user_answer: r.user_answer,
      correct_answer: r.correct_answer,
      is_correct: r.is_correct,
      confidence: r.confidence_level,
      category: r.category,
      time: r.time_spent
    }));
  }

  private calculateAlignment(responses: QuestionResponse[]): number {
    if (responses.length === 0) return 0;

    let alignedCount = 0;
    responses.forEach(r => {
      const isHighConfidence = r.confidence_level >= 70;
      // Aligned if: (high confidence AND correct) OR (low confidence AND incorrect)
      if ((isHighConfidence && r.is_correct) || (!isHighConfidence && !r.is_correct)) {
        alignedCount++;
      }
    });

    return Math.round((alignedCount / responses.length) * 100);
  }

  private formatDate(date: Date): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
  }

  private formatTime(date: Date): string {
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be 12
    const minutesStr = minutes < 10 ? '0' + minutes : minutes.toString();
    return `${hours}:${minutesStr} ${ampm}`;
  }

  setFilter(filter: string) {
    this.activeFilter = filter;
    if (filter === 'all') {
      this.filteredResponses = this.allResponses;
    } else if (filter === 'correct') {
      this.filteredResponses = this.allResponses.filter(r => r.is_correct);
    } else if (filter === 'incorrect') {
      this.filteredResponses = this.allResponses.filter(r => !r.is_correct);
    }
  }

  // Visual Helper: Curiosity Pattern
  getPattern(isCorrect: boolean, confidence: number): { label: string, class: string, icon: string } {
    if (isCorrect && confidence >= 75) return { label: 'Confident & Correct', class: 'pattern-optimal', icon: '💪' };
    if (isCorrect && confidence < 50) return { label: 'Underconfident', class: 'pattern-info', icon: '✨' };
    if (!isCorrect && confidence >= 75) return { label: 'Overconfident', class: 'pattern-danger', icon: '⚠️' };
    if (!isCorrect && confidence < 50) return { label: 'Guessing', class: 'pattern-neutral', icon: '🎲' };
    return { label: 'Calibrated', class: 'pattern-success', icon: '🎯' };
  }

  getAccuracyColor(acc: number): string {
    if (acc >= 70) return 'var(--color-success)';
    if (acc >= 50) return 'var(--color-warning)';
    return '#DC2626';
  }
}