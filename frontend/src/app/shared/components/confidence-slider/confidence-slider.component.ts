import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-confidence-slider',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './confidence-slider.component.html',
  styleUrls: ['./confidence-slider.component.scss']
})
export class ConfidenceSliderComponent {
  confidenceValue: number = 50;
  @Output() valueChange = new EventEmitter<number>();

  get label(): string {
    if (this.confidenceValue < 33) return 'Low';
    if (this.confidenceValue < 67) return 'Medium';
    return 'High';
  }

  onInput() {
    this.valueChange.emit(this.confidenceValue);
  }
}