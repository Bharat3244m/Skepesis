import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-curiosity',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './curiosity.component.html',
  styleUrls: ['./curiosity.component.scss']
})
export class CuriosityComponent {
  query: string = '';

  // This matches the (click)="handleAnalysis()" in your HTML template
  handleAnalysis() {
    if (this.query.trim().length < 10) return;
    console.log('Analyzing:', this.query);
    // Logic for API call will go here later
  }
}