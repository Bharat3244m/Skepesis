"""
Scoring Service

Handles score calculations and performance metrics
"""
from typing import List
from app.models.response import Response
from app.logger import get_logger

logger = get_logger(__name__)


class ScoringError(Exception):
    """Custom exception for scoring errors"""
    pass


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
        
        Raises:
            ScoringError: If calculation fails
        """
        if not responses:
            return 0.0
        
        try:
            total_score = 0.0
            
            for response in responses:
                base_score = 100 if response.is_correct else 0
                
                # Confidence bonus/penalty
                confidence_factor = 0
                confidence_level = response.confidence_level or 0
                
                if response.is_correct and confidence_level > 70:
                    # Bonus for being confident and correct
                    confidence_factor = 10
                elif not response.is_correct and confidence_level > 70:
                    # Penalty for overconfidence
                    confidence_factor = -15
                elif response.is_correct and confidence_level < 40:
                    # Small bonus for correct despite low confidence
                    confidence_factor = 5
                
                total_score += base_score + confidence_factor
            
            # Normalize to 0-100
            max_possible = len(responses) * 110  # Max with bonuses
            return min(100, (total_score / max_possible) * 100) if max_possible > 0 else 0.0
        except Exception as e:
            logger.error(f"Error calculating weighted score: {e}")
            raise ScoringError(f"Failed to calculate weighted score: {e}") from e
    
    @staticmethod
    def calculate_percentile(score: float, all_scores: List[float]) -> int:
        """
        Calculate percentile ranking
        
        Returns: Percentile (0-100)
        
        Raises:
            ScoringError: If calculation fails
        """
        try:
            if not all_scores:
                return 50
            
            below = sum(1 for s in all_scores if s < score)
            return int((below / len(all_scores)) * 100)
        except Exception as e:
            logger.error(f"Error calculating percentile: {e}")
            raise ScoringError(f"Failed to calculate percentile: {e}") from e
