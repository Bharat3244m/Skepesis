import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  showModal = false; // Controls visibility
  studentName = '';
  category = '';
  questionCount = 10;

  constructor(private router: Router) {}

  startQuiz() {
    this.router.navigate(['/quiz'], { 
      queryParams: { 
        name: this.studentName, 
        count: this.questionCount, 
        category: this.category 
      } 
    });
  }
}