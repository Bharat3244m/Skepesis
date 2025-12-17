"""
Open Trivia Database API Integration
Fetches questions from https://opentdb.com/
"""
import httpx
import html
import random
from typing import List, Optional, Dict, Any
from app.schemas.question import QuestionCreate

class TriviaAPIService:
    """Service to fetch questions from Open Trivia Database"""
    
    BASE_URL = "https://opentdb.com/api.php"
    
    @staticmethod
    def decode_html_entities(text: str) -> str:
        """Decode HTML entities in text"""
        if not text:
            return text
        return html.unescape(text)
    
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
                
                if data.get("response_code") != 0:
                    raise ValueError(f"API error: response_code {data.get('response_code')}")
                
                questions = []
                for item in data.get("results", []):
                    question = TriviaAPIService._convert_to_question(item)
                    questions.append(question)
                
                return questions
                
        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch questions from API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing API response: {str(e)}")
    
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
        except Exception as e:
            raise Exception(f"Failed to fetch categories: {str(e)}")
