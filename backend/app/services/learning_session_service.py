from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, List

from app.models.attempt import Attempt
from app.models.response import Response
from app.services.scoring import ScoringService
from app.services.curiosity import CuriosityAnalyzer
from app.services.llm import get_llm_service
from app.schemas.response import ResponseCreate # You need to ensure this schema exists

class LearningSessionService:
    
    @staticmethod
    async def start_attempt(db: AsyncSession, student_email: str) -> Attempt:
        attempt = Attempt(student_name=student_email)
        db.add(attempt)
        await db.commit()
        await db.refresh(attempt)
        return attempt

    @staticmethod
    async def submit_response(
        db: AsyncSession,
        attempt_id: int,
        payload: ResponseCreate
    ) -> Response:
        
        # Calculate correctness immediately
        is_correct = (
            payload.correct_answer is not None
            and payload.user_answer.strip().upper() == payload.correct_answer.strip().upper()
        )

        response = Response(
            attempt_id=attempt_id,
            question_id=payload.question_id,
            user_answer=payload.user_answer,
            is_correct=is_correct,
            confidence_level=payload.confidence_level,
            time_spent=payload.time_spent,
            question_text=payload.question_text,
            category=payload.category,
            difficulty=payload.difficulty
        )

        db.add(response)
        
        # Update attempt stats (Async)
        q = await db.execute(select(Attempt).where(Attempt.id == attempt_id))
        attempt = q.scalars().first()
        if attempt:
            attempt.total_questions += 1
            if is_correct:
                attempt.correct_answers += 1
        
        await db.commit()
        await db.refresh(response)
        return response

    @staticmethod
    async def generate_insights(db: AsyncSession, attempt_id: int) -> str:
        """
        Orchestrates the LLM to analyze the student's attempt.
        """
        # 1. Fetch Attempt with Responses (Eager Load)
        # Note: In async, we must explicitly load relationships or use select().options(selectinload(...))
        stmt = select(Attempt).where(Attempt.id == attempt_id)
        result = await db.execute(stmt)
        attempt = result.scalars().first()
        
        if not attempt:
            return "Attempt not found."

        # Fetch responses manually if relationship loading is tricky in your setup
        r_stmt = select(Response).where(Response.attempt_id == attempt_id)
        r_result = await db.execute(r_stmt)
        responses = r_result.scalars().all()

        # 2. Logic Analysis (CPU bound, fast enough to run sync)
        summary = CuriosityAnalyzer.get_cognitive_insights(responses)
        
        # 3. LLM Generation (IO bound - await this!)
        llm = get_llm_service()
        prompt = f"Analyze this student's cognitive performance based on this data: {summary}"
        
        # Using the async generate method from your llm.py
        insight_text = await llm.generate(prompt)
        
        return insight_text
    
    @staticmethod
    async def complete_attempt(db: AsyncSession, attempt: Attempt) -> Attempt:
        from datetime import datetime
        
        # 1. Calculate Scores (CPU bound, sync is fine here)
        responses = attempt.responses
        
        # Calculate scores using your existing logic
        accuracy = ScoringService.calculate_accuracy(responses) if hasattr(ScoringService, 'calculate_accuracy') else 0.0
        curiosity = CuriosityAnalyzer.calculate_curiosity_score(responses)
        
        # 2. Update DB (Async)
        attempt.completed_at = datetime.utcnow()
        attempt.curiosity_score = curiosity
        # attempt.score = accuracy # if you have a score column
        
        await db.commit()
        await db.refresh(attempt)
        return attempt
    
    @staticmethod
    async def get_responses_for_attempt(db: AsyncSession, attempt_id: int) -> List[Response]:
        """Fetch all responses for a given attempt ID."""
        from sqlalchemy.future import select
        
        query = select(Response).where(Response.attempt_id == attempt_id).order_by(Response.created_at)
        result = await db.execute(query)
        return result.scalars().all()