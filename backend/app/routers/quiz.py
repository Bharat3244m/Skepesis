from fastapi import APIRouter, HTTPException, Query
import httpx
import html
import random

router = APIRouter()

@router.get("/generate")
async def generate_quiz(
    amount: int = 10,
    category: int = None,
    difficulty: str = None,
    type: str = "multiple"
):
    # Base URL for Open Trivia DB
    url = "https://opentdb.com/api.php"
    
    params = {
        "amount": amount,
        "type": type
    }
    
    # Only add if not 'any'
    if category and category != 0: 
        params["category"] = category
    if difficulty and difficulty != "any":
        params["difficulty"] = difficulty

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data["response_code"] != 0:
                raise HTTPException(status_code=400, detail="Could not retrieve questions from Trivia API")
            
            # Clean up the data (decode HTML entities & shuffle answers)
            cleaned_questions = []
            for idx, q in enumerate(data["results"]):
                # Combine correct and incorrect answers
                all_options = q["incorrect_answers"] + [q["correct_answer"]]
                random.shuffle(all_options)
                
                cleaned_questions.append({
                    "id": idx,
                    "text": html.unescape(q["question"]),
                    "category": html.unescape(q["category"]),
                    "difficulty": q["difficulty"],
                    "options": [html.unescape(opt) for opt in all_options],
                    "correct_answer": html.unescape(q["correct_answer"])
                })
                
            return cleaned_questions

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))