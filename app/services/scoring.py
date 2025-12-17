"""
Scoring Service

Handles score calculations and performance metrics
"""
from typing import List
from app.models.response import Response

class ScoringService:
    """Calculate various performance scores"""
    
    @staticmethod
    def calculate_weighted_score(responses: List[Response]) -> float:
        """
        Calculate weighted score considering:
        - Correctness (primary factor)
        - Confidence alignment (bonus/penalty)
        - Time efficiency (bonus)
        
        Returns: Score from 0-100
        """
        if not responses:
            return 0.0
        
        total_score = 0.0
        
        for response in responses:
            base_score = 100 if response.is_correct else 0
            
            # Confidence bonus/penalty
            confidence_factor = 0
            if response.is_correct and response.confidence_level > 70:
                # Bonus for being confident and correct
                confidence_factor = 10
            elif not response.is_correct and response.confidence_level > 70:
                # Penalty for overconfidence
                confidence_factor = -15
            elif response.is_correct and response.confidence_level < 40:
                # Small bonus for correct despite low confidence
                confidence_factor = 5
            
            total_score += base_score + confidence_factor
        
        # Normalize to 0-100
        max_possible = len(responses) * 110  # Max with bonuses
        return min(100, (total_score / max_possible) * 100)
    
    @staticmethod
    def calculate_percentile(score: float, all_scores: List[float]) -> int:
        """Calculate percentile ranking"""
        if not all_scores:
            return 50
        
        below = sum(1 for s in all_scores if s < score)
        return int((below / len(all_scores)) * 100)
