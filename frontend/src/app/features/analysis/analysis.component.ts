import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-analysis',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit {
  // Mocking the data structure from your screenshot for perfect UI matching
  metrics = {
    accuracy: 20,
    confidence: 65,
    calibration: 27,
    avgTime: 6.6
  };

  matrix = {
    highCorrect: 0,
    highIncorrect: 3,
    lowCorrect: 1,
    lowIncorrect: 1
  };

  ngOnInit() {
    // Logic to calculate summary text based on matrix
  }

  getCalibrationText(): string {
    return `Mixed calibration: ${this.matrix.highIncorrect} overconfident errors, ${this.matrix.lowCorrect} underconfident success.`;
  }
}