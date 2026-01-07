export interface CognitiveMetrics {
  accuracy: number;
  confidence: number;
  calibration: number;
  avgTime: number;
}

export interface CalibrationMatrix {
  highCorrect: number;    // Calibrated
  highIncorrect: number;  // Overconfident
  lowCorrect: number;     // Lucky/Underconfident
  lowIncorrect: number;   // Calibrated
}