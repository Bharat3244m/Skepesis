export interface Option {
  id: string; // e.g., 'A', 'B'
  text: string;
}

export interface Question {
  id: number;
  text: string;
  category: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  options: Option[];
  correctAnswer?: string; // Hidden during the quiz
}

export interface UserResponse {
  questionId: number;
  selectedOption: string;
  confidence: number;
  timeTaken: number;
}