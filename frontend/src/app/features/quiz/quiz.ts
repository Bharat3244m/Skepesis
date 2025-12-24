import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http'; // Import HttpClient

@Component({
  standalone: true,
  selector: 'app-quiz',
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page-wrapper quiz-page">

      <div class="setup-container" *ngIf="gameState === 'setup'">
        <div class="panel setup-card">
          <div class="text-center mb-4">
            <h2 class="section-title">New Session</h2>
            <p class="text-muted">Configure your learning parameters</p>
          </div>

          <form (ngSubmit)="startQuiz()">
            <div class="form-group">
              <label class="form-label">Category</label>
              <div class="select-wrapper">
                <select [(ngModel)]="config.category" name="category" class="form-input custom-select">
                  <option [ngValue]="null">Any Category</option>
                  <option *ngFor="let cat of categories" [value]="cat.id">{{ cat.name }}</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Difficulty</label>
              <div class="select-wrapper">
                <select [(ngModel)]="config.difficulty" name="difficulty" class="form-input custom-select">
                  <option value="any">Any Difficulty</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Questions</label>
              <input type="number" [(ngModel)]="config.amount" name="amount" class="form-input" min="1" max="50">
            </div>

            <div class="mt-4">
              <button type="submit" [disabled]="isLoading" class="btn btn-primary btn-block btn-large">
                {{ isLoading ? 'Loading Quiz...' : 'Start Session' }}
              </button>
            </div>

            <p *ngIf="error" class="text-danger text-center mt-2">{{ error }}</p>
          </form>
        </div>
      </div>

      <div class="quiz-container" *ngIf="gameState === 'active'">

        <div class="quiz-header">
          <div class="quiz-meta">
            <span class="badge info">{{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
            <span class="badge warning">{{ questions[currentQuestionIndex].difficulty | titlecase }}</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" [style.width.%]="((currentQuestionIndex + 1) / questions.length) * 100"></div>
          </div>
        </div>

        <div class="question-card">
          <h2 class="question-text" [innerHTML]="questions[currentQuestionIndex].text"></h2>

          <div class="options-grid">
            <button
              *ngFor="let option of questions[currentQuestionIndex].options"
              (click)="selectAnswer(option)"
              class="option-btn">
              {{ option }}
            </button>
          </div>
        </div>

        <button (click)="quitQuiz()" class="btn-link text-muted mt-4">Quit Session</button>
      </div>

    </div>
  `,
  styles: [`
    /* Reuse previous setup styles */
    .quiz-page {
      background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .setup-container { width: 100%; max-width: 480px; }
    .setup-card {
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(12px);
      padding: 30px;
      border-radius: 24px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* Active Quiz Styles */
    .quiz-container { width: 100%; max-width: 640px; }

    .question-card {
      background: white;
      padding: 40px;
      border-radius: 24px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.08);
      text-align: center;
      margin-top: 20px;
    }

    .question-text {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--color-text);
      margin-bottom: 30px;
    }

    .options-grid {
      display: grid;
      gap: 12px;
    }

    .option-btn {
      padding: 16px;
      border: 2px solid #e2e8f0;
      background: white;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      text-align: left;
    }

    .option-btn:hover {
      border-color: var(--color-primary);
      background: var(--color-primary-subtle);
    }

    .progress-track {
      height: 6px;
      background: #e2e8f0;
      border-radius: 3px;
      margin-top: 15px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: var(--color-primary);
      transition: width 0.3s ease;
    }

    .text-danger { color: #dc2626; }
    .mt-2 { margin-top: 0.5rem; }
  `]
})
export class QuizComponent {
  // State
  gameState: 'setup' | 'active' | 'result' = 'setup';
  isLoading = false;
  error = '';

  // Data
  questions: any[] = [];
  currentQuestionIndex = 0;

  // Config
  config = {
    category: null,
    difficulty: 'any',
    amount: 10
  };

  // Categories (Shortened list for brevity, keep your full list)
  categories = [
    { id: 9, name: 'General Knowledge' },
    { id: 18, name: 'Science: Computers' },
    { id: 21, name: 'Sports' },
    { id: 23, name: 'History' },
    { id: 27, name: 'Animals' }
  ];

  constructor(private http: HttpClient) {}

  startQuiz() {
    this.isLoading = true;
    this.error = '';

    // Build Query Params
    let params: any = { amount: this.config.amount };
    if (this.config.category) params.category = this.config.category;
    if (this.config.difficulty !== 'any') params.difficulty = this.config.difficulty;

    // Call Backend
    this.http.get<any[]>('http://localhost:8000/api/quiz/generate', { params })
      .subscribe({
        next: (data) => {
          if (data.length > 0) {
            this.questions = data;
            this.gameState = 'active';
            this.currentQuestionIndex = 0;
          } else {
            this.error = 'No questions found for these settings.';
          }
          this.isLoading = false;
        },
        error: (err) => {
          this.error = 'Failed to load quiz. Check backend connection.';
          this.isLoading = false;
          console.error(err);
        }
      });
  }

  selectAnswer(answer: string) {
    // Logic to handle answer selection goes here
    // For now, just move to next question
    if (this.currentQuestionIndex < this.questions.length - 1) {
      this.currentQuestionIndex++;
    } else {
      alert("Quiz Finished!");
      this.gameState = 'setup';
    }
  }

  quitQuiz() {
    this.gameState = 'setup';
    this.questions = [];
  }
}
