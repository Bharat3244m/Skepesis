import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-attempt-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './attempt-details.component.html',
  styleUrls: ['./attempt-details.component.scss']
})
export class AttemptDetailsComponent implements OnInit {
  constructor() {}
  ngOnInit(): void {}

  getPattern(isCorrect: boolean, confidence: number): string {
    if (isCorrect && confidence >= 75) return '💪 Confident & Correct';
    if (isCorrect && confidence < 50) return '✨ Lucky or Underconfident';
    if (!isCorrect && confidence >= 75) return '⚠️ Overconfident';
    if (!isCorrect && confidence < 50) return '🎲 Guessing';
    return '🎯 Calibrated';
  }
}