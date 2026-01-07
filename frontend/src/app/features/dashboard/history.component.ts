import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router'; // Added RouterModule for routerLink in HTML
import { ApiService } from '../../core/services/api'; // Import API Service

// Updated interface to include ID (needed for navigation)
interface QuizSession {
  id: string; // Added ID
  userName: string;
  date: string;
  score: number;
  questions: number;
  curiosity: number;
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  searchTerm: string = '';
  allSessions: QuizSession[] = []; // Data now comes from API
  sessions: QuizSession[] = [];

  constructor(
    private router: Router,
    private api: ApiService // Inject API Service
  ) {}

  ngOnInit() {
    // specific call to fetch real data
    this.api.getAttempts().subscribe({
      next: (data) => {
        // Map Backend Data (snake_case) to Your Interface (camelCase)
        this.allSessions = data.map((item: any) => ({
          id: item.id,
          userName: item.student_name, // Map student_name -> userName
          date: new Date(item.started_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          score: item.total_questions > 0 
            ? Math.round((item.correct_answers / item.total_questions) * 100) 
            : 0, // Calculate percentage score
          questions: item.total_questions,
          curiosity: Math.round(item.curiosity_score || 0)
        }));

        // Initialize the view
        this.sessions = [...this.allSessions];
      },
      error: (err) => console.error('Error loading history:', err)
    });
  }

  search() {
    if (!this.searchTerm.trim()) {
      this.sessions = [...this.allSessions];
      return;
    }

    this.sessions = this.allSessions.filter(s => 
      s.userName.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  viewSessionDetails(sessionId: string) {
    // Now uses the actual ID from the clicked session
    this.router.navigate(['/attempt', sessionId]);
  }
}