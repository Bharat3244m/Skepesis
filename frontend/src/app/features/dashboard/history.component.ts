import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface QuizSession {
  userName: string;
  date: string;
  score: number;
  questions: number;
  curiosity: number;
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  searchTerm: string = '';
  
  // Mocking the data from your "bharat" session screenshot
  allSessions: QuizSession[] = [
    {
      userName: 'bharat',
      date: 'Jan 1',
      score: 20,
      questions: 5,
      curiosity: 33
    }
  ];

  sessions: QuizSession[] = [];

  ngOnInit() {
    // Initially show all sessions
    this.sessions = [...this.allSessions];
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
}