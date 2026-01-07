import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfidenceSliderComponent } from '../../shared/components/confidence-slider/confidence-slider.component';
import { Question, UserResponse } from '../../models/quiz';

@Component({
  selector: 'app-quiz',
  standalone: true,
  imports: [CommonModule, ConfidenceSliderComponent],
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.scss']
})
export class QuizComponent implements OnInit, OnDestroy {
  // State
  questions: Question[] = []; // This will be populated by your API later
  currentIdx = 0;
  selectedOptionId: string | null = null;
  currentConfidence = 50;
  
  // Metrics
  startTime!: number;
  timerInterval: any;
  secondsElapsed = 0;
  responses: UserResponse[] = [];

  get currentQuestion(): Question {
    return this.questions[this.currentIdx];
  }

  ngOnInit() {
    this.startTimer();
    this.startTime = Date.now();
    // Mock data to match your screenshot
    this.questions = [{
      id: 1,
      text: 'What was the name of the first Bulgarian personal computer?',
      category: 'COMPUTERS',
      difficulty: 'Advanced',
      options: [
        { id: 'A', text: 'Pravetz 8D' },
        { id: 'B', text: 'IZOT 1030' },
        { id: 'C', text: 'Pravetz 82' },
        { id: 'D', text: 'IMKO-1' }
      ]
    }];
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
    const timeTaken = Math.floor((Date.now() - this.startTime) / 1000);
    
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
      this.startTime = Date.now(); // Reset start time for next question
    } else {
      this.finishQuiz();
    }
  }

  finishQuiz() {
    console.log('Quiz Complete! Data for Analysis:', this.responses);
    // Logic to navigate to /analysis will go here next
  }

  ngOnDestroy() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  }
}