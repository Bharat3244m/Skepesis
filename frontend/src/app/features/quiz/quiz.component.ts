import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Question, UserResponse } from '../../models/quiz';
import { ApiService } from '../../core/services/api';

@Component({
  selector: 'app-quiz',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.scss']
})
export class QuizComponent implements OnInit, OnDestroy {
  // State
  questions: Question[] = [];
  currentIdx = 0;
  selectedOptionId: string | null = null;
  currentConfidence = 50;
  
  // Quiz settings
  categories: { [key: string]: string } = {};
  selectedCategory: number = 0;
  selectedDifficulty: string = 'any';
  questionCount: number = 10;
  
  // Metrics
  startTime!: number;
  timerInterval: any;
  secondsElapsed = 0;
  responses: UserResponse[] = [];
  
  // Session
  attemptId: number | null = null;
  loading = false;
  quizStarted = false;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  get currentQuestion(): Question {
    return this.questions[this.currentIdx];
  }

  ngOnInit() {
    // Load categories
    this.api.getTriviaCategories().subscribe({
      next: (data) => {
        this.categories = data.categories;
      },
      error: (err) => console.error('Failed to load categories:', err)
    });
  }

  startQuiz() {
    this.loading = true;
    
    // Create attempt first
    this.api.createAttempt('student@example.com').subscribe({
      next: (attempt) => {
        this.attemptId = attempt.id;
        
        // Then fetch questions
        this.api.generateQuiz(
          this.questionCount,
          this.selectedCategory || undefined,
          this.selectedDifficulty
        ).subscribe({
          next: (questions) => {
            this.questions = questions.map((q: any) => ({
              id: q.id,
              text: q.text,
              category: q.category,
              difficulty: q.difficulty,
              options: q.options.map((opt: string, idx: number) => ({
                id: String.fromCharCode(65 + idx), // A, B, C, D
                text: opt
              })),
              correctAnswer: q.correct_answer
            }));
            
            this.quizStarted = true;
            this.loading = false;
            this.startTimer();
            this.startTime = Date.now();
          },
          error: (err) => {
            console.error('Failed to load questions:', err);
            this.loading = false;
            alert('Failed to load quiz questions. Please try again.');
          }
        });
      },
      error: (err) => {
        console.error('Failed to create attempt:', err);
        this.loading = false;
        alert('Failed to start quiz session. Please try again.');
      }
    });
  }

  startTimer() {
    this.timerInterval = setInterval(() => this.secondsElapsed++, 1000);
  }

  formatTime(): string {
    const mins = Math.floor(this.secondsElapsed / 60);
    const secs = this.secondsElapsed % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  selectOption(id: string) {
    this.selectedOptionId = id;
  }

  onConfidenceChange(value: number) {
    this.currentConfidence = value;
  }

  nextQuestion() {
    if (!this.attemptId) return;
    
    const timeTaken = Math.floor((Date.now() - this.startTime) / 1000);
    const selectedOption = this.currentQuestion.options.find(opt => opt.id === this.selectedOptionId);
    
    // Submit response to backend
    const payload = {
      attempt_id: this.attemptId,
      question_id: this.currentQuestion.id,
      question_text: this.currentQuestion.text,
      user_answer: selectedOption?.text || '',
      confidence_level: this.currentConfidence,
      time_spent: timeTaken,
      category: this.currentQuestion.category,
      difficulty: this.currentQuestion.difficulty,
      correct_answer: this.currentQuestion.correctAnswer || ''
    };

    this.api.submitResponse(payload).subscribe({
      next: () => {
        const response: UserResponse = {
          questionId: this.currentQuestion.id,
          selectedOption: this.selectedOptionId!,
          confidence: this.currentConfidence,
          timeTaken: timeTaken
        };

        this.responses.push(response);

        if (this.currentIdx < this.questions.length - 1) {
          this.currentIdx++;
          this.selectedOptionId = null;
          this.currentConfidence = 50;
          this.startTime = Date.now();
        } else {
          this.finishQuiz();
        }
      },
      error: (err) => {
        console.error('Failed to submit response:', err);
        alert('Failed to save your answer. Please try again.');
      }
    });
  }

  finishQuiz() {
    if (!this.attemptId) return;
    
    this.loading = true;
    
    // Complete the attempt
    this.api.completeAttempt(this.attemptId).subscribe({
      next: () => {
        // Navigate to analysis page
        this.router.navigate(['/attempt', this.attemptId]);
      },
      error: (err) => {
        console.error('Failed to complete quiz:', err);
        // Still navigate even if completion fails
        this.router.navigate(['/attempt', this.attemptId]);
      }
    });
  }

  ngOnDestroy() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  }
}