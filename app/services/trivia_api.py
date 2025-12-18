"""
Open Trivia Database API Integration
Fetches questions from https://opentdb.com/
"""
import httpx
import html
import random
from typing import List, Optional, Dict, Any
from app.schemas.question import QuestionCreate
from app.logger import get_logger

logger = get_logger(__name__)


class TriviaAPIError(Exception):
    """Custom exception for Trivia API errors"""
    pass


class TriviaAPIService:
    """Service to fetch questions from Open Trivia Database"""
    
    BASE_URL = "https://opentdb.com/api.php"
    
    @staticmethod
    def decode_html_entities(text: str) -> str:
        """Decode HTML entities in text"""
        if not text:
            return text
        try:
            return html.unescape(text)
        except Exception as e:
            logger.warning(f"Failed to decode HTML entities: {e}")
            return text
    
    @staticmethod
    async def fetch_questions(
        amount: int = 10,
        category: Optional[int] = None,
        difficulty: Optional[str] = None,
        question_type: str = "multiple"
    ) -> List[QuestionCreate]:
        """
        Fetch questions from Open Trivia Database API
        
        Args:
            amount: Number of questions (1-50)
            category: Category ID (optional)
            difficulty: easy, medium, or hard (optional)
            question_type: multiple or boolean
            
        Returns:
            List of QuestionCreate objects
            
        Raises:
            TriviaAPIError: If API request fails or returns invalid data
        """
        params = {
            "amount": min(amount, 50),  # API limit is 50
            "type": question_type
        }
        
        if category:
            params["category"] = category
        if difficulty:
            params["difficulty"] = difficulty
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(TriviaAPIService.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                
                response_code = data.get("response_code")
                if response_code != 0:
                    error_messages = {
                        1: "Not enough questions available for the specified criteria",
                        2: "Invalid parameter in API request",
                        3: "Token not found (session issue)",
                        4: "Token empty (all questions exhausted)"
                    }
                    error_msg = error_messages.get(response_code, f"Unknown API error code: {response_code}")
                    logger.warning(f"Trivia API returned error: {error_msg}")
                    raise TriviaAPIError(error_msg)
                
                questions = []
                for item in data.get("results", []):
                    try:
                        question = TriviaAPIService._convert_to_question(item)
                        questions.append(question)
                    except Exception as e:
                        logger.warning(f"Failed to convert question: {e}")
                        continue
                
                if not questions:
                    raise TriviaAPIError("No valid questions could be parsed from API response")
                
                return questions
                
        except httpx.TimeoutException as e:
            logger.error(f"Timeout fetching questions from Trivia API: {e}")
            raise TriviaAPIError("Trivia API request timed out") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Trivia API: {e}")
            raise TriviaAPIError(f"Trivia API returned HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            logger.error(f"Network error fetching questions: {e}")
            raise TriviaAPIError(f"Failed to connect to Trivia API: {str(e)}") from e
        except TriviaAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing API response: {e}")
            raise TriviaAPIError(f"Error processing API response: {str(e)}") from e
    
    @staticmethod
    def _convert_to_question(item: Dict[str, Any]) -> QuestionCreate:
        """Convert Open Trivia DB format to our Question format"""
        
        # Decode HTML entities
        question_text = TriviaAPIService.decode_html_entities(item.get("question", ""))
        correct_answer = TriviaAPIService.decode_html_entities(item.get("correct_answer", ""))
        incorrect_answers = [
            TriviaAPIService.decode_html_entities(ans) 
            for ans in item.get("incorrect_answers", [])
        ]
        
        # Map difficulty
        difficulty_map = {
            "easy": "beginner",
            "medium": "intermediate",
            "hard": "advanced"
        }
        difficulty = difficulty_map.get(item.get("difficulty", "easy"), "beginner")
        
        # Create category name (clean up the API category)
        category = item.get("category", "General Knowledge")
        category = category.replace("Entertainment: ", "").replace("Science: ", "")
        
        # Determine question type
        question_type = "true_false" if item.get("type") == "boolean" else "multiple_choice"
        
        # For multiple choice, randomize options and assign to A, B, C, D
        if question_type == "multiple_choice":
            all_options = [correct_answer] + incorrect_answers
            random.shuffle(all_options)
            
            # Find which option is correct
            correct_key = chr(65 + all_options.index(correct_answer))  # A, B, C, or D
            
            # Pad options if less than 4
            while len(all_options) < 4:
                all_options.append("")
            
            return QuestionCreate(
                text=question_text,
                question_type=question_type,
                difficulty=difficulty,
                category=category,
                correct_answer=correct_key,
                option_a=all_options[0] if len(all_options) > 0 else "",
                option_b=all_options[1] if len(all_options) > 1 else "",
                option_c=all_options[2] if len(all_options) > 2 else "",
                option_d=all_options[3] if len(all_options) > 3 else "",
                explanation=f"Source: Open Trivia Database"
            )
        else:
            # True/False questions
            return QuestionCreate(
                text=question_text,
                question_type=question_type,
                difficulty=difficulty,
                category=category,
                correct_answer="A" if correct_answer.lower() == "true" else "B",
                option_a="True",
                option_b="False",
                option_c="",
                option_d="",
                explanation=f"Source: Open Trivia Database"
            )
    
    @staticmethod
    async def get_categories() -> Dict[int, str]:
        """Fetch available categories from API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get("https://opentdb.com/api_category.php")
                response.raise_for_status()
                data = response.json()
                
                categories = {}
                for cat in data.get("trivia_categories", []):
                    categories[cat["id"]] = cat["name"]
                
                return categories
        except httpx.TimeoutException as e:
            logger.error(f"Timeout fetching categories: {e}")
            raise TriviaAPIError("Trivia API request timed out") from e
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching categories: {e}")
            raise TriviaAPIError(f"Failed to fetch categories: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error fetching categories: {e}")
            raise TriviaAPIError(f"Failed to fetch categories: {str(e)}") from e
