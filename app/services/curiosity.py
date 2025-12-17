"""
Curiosity Analysis Service

Primary Goal: Help learners understand HOW they learn, not just WHAT they learn.

Analyzes user confidence levels and response patterns to infer:
- Curiosity patterns and exploratory behavior
- Learning gaps and knowledge calibration
- Cognitive behavior and metacognitive awareness
- Thinking patterns and decision-making style
"""
from typing import List, Dict, Any
from app.models.response import Response

class CuriosityAnalyzer:
    """Analyzes user responses to determine curiosity and learning patterns.
    
    Focused on metacognitive insights and actionable self-awareness.
    """
    
    @staticmethod
    def calculate_curiosity_score(responses: List[Response]) -> float:
        """
        Calculate curiosity score based on confidence-correctness patterns.
        
        High curiosity indicators:
        - Low confidence + Correct answer (exploring despite uncertainty)
        - High confidence + Incorrect answer (overconfidence, needs recalibration)
        
        Returns: Score from 0-100
        """
        if not responses:
            return 0.0
        
        curiosity_points = 0.0
        
        for response in responses:
            conf = response.confidence_level
            
            # Pattern 1: Low confidence but correct (curious learner)
            if response.is_correct and conf < 50:
                curiosity_points += (50 - conf) / 50 * 25
            
            # Pattern 2: High confidence but incorrect (overconfident, learning opportunity)
            if not response.is_correct and conf > 70:
                curiosity_points += (conf - 70) / 30 * 20
            
            # Pattern 3: Medium confidence (thoughtful consideration)
            if 40 <= conf <= 60:
                curiosity_points += 10
        
        # Normalize to 0-100
        max_possible = len(responses) * 30
        return min(100, (curiosity_points / max_possible) * 100) if max_possible > 0 else 0
    
    @staticmethod
    def identify_learning_gaps(responses: List[Response]) -> Dict[str, Any]:
        """
        Identify areas where the student needs improvement.
        
        Returns: Dictionary with gap analysis
        """
        gaps = {
            "overconfident_errors": [],
            "underconfident_successes": [],
            "consistent_mistakes": [],
            "low_confidence_responses": [],
            "knowledge_areas": {},
            "difficulty_analysis": {}
        }
        
        # Track confidence totals per category for averaging
        category_confidence_totals = {}
        
        for response in responses:
            conf = response.confidence_level
            # Use the stored category directly from response
            question_category = response.category or "General"
            question_difficulty = response.difficulty or "medium"
            
            # Overconfident on wrong answers
            if not response.is_correct and conf > 70:
                gaps["overconfident_errors"].append({
                    "question_id": response.question_id,
                    "confidence": conf,
                    "category": question_category,
                    "question_text": response.question_text
                })
            
            # Underconfident on correct answers
            if response.is_correct and conf < 40:
                gaps["underconfident_successes"].append({
                    "question_id": response.question_id,
                    "confidence": conf,
                    "category": question_category,
                    "question_text": response.question_text
                })
            
            # Low confidence responses (potential guessing)
            if conf < 30:
                gaps["low_confidence_responses"].append({
                    "question_id": response.question_id,
                    "confidence": conf,
                    "is_correct": response.is_correct,
                    "category": question_category
                })
            
            # Track by category
            if question_category not in gaps["knowledge_areas"]:
                gaps["knowledge_areas"][question_category] = {
                    "correct": 0,
                    "total": 0,
                    "avg_confidence": 0,
                    "avg_time": 0
                }
                category_confidence_totals[question_category] = {"confidence": 0, "time": 0}
            
            gaps["knowledge_areas"][question_category]["total"] += 1
            category_confidence_totals[question_category]["confidence"] += conf
            category_confidence_totals[question_category]["time"] += response.time_spent
            if response.is_correct:
                gaps["knowledge_areas"][question_category]["correct"] += 1
            
            # Track by difficulty
            if question_difficulty not in gaps["difficulty_analysis"]:
                gaps["difficulty_analysis"][question_difficulty] = {
                    "correct": 0,
                    "total": 0,
                    "avg_confidence": 0
                }
            gaps["difficulty_analysis"][question_difficulty]["total"] += 1
            if response.is_correct:
                gaps["difficulty_analysis"][question_difficulty]["correct"] += 1
        
        # Calculate averages for knowledge areas
        for cat, totals in category_confidence_totals.items():
            total_questions = gaps["knowledge_areas"][cat]["total"]
            if total_questions > 0:
                gaps["knowledge_areas"][cat]["avg_confidence"] = round(
                    totals["confidence"] / total_questions, 1
                )
                gaps["knowledge_areas"][cat]["avg_time"] = round(
                    totals["time"] / total_questions, 1
                )
        
        return gaps
    
    @staticmethod
    def get_confidence_accuracy_alignment(responses: List[Response]) -> float:
        """
        Measure how well confidence levels align with correctness.
        
        Perfect alignment: High confidence when correct, low when incorrect
        Returns: Score from 0-100
        """
        if not responses:
            return 0.0
        
        alignment_score = 0.0
        
        for response in responses:
            if response.is_correct:
                # Should have high confidence
                alignment_score += response.confidence_level
            else:
                # Should have low confidence
                alignment_score += (100 - response.confidence_level)
        
        return alignment_score / len(responses)
    
    @staticmethod
    def analyze_learning_patterns(responses: List[Response]) -> Dict[str, Any]:
        """
        Analyze HOW the learner learns - their thinking patterns and approach.
        """
        if not responses:
            return {}
        
        # Analyze response speed patterns
        avg_time = sum(r.time_spent for r in responses) / len(responses)
        time_variance = sum(abs(r.time_spent - avg_time) for r in responses) / len(responses)
        
        # Determine thinking speed
        if avg_time < 15:
            thinking_speed = "quick"
            speed_insight = "You process information rapidly and make fast decisions."
        elif avg_time < 30:
            thinking_speed = "moderate"
            speed_insight = "You take a balanced approach, considering options carefully."
        else:
            thinking_speed = "deliberate"
            speed_insight = "You're thorough and take time to analyze each question deeply."
        
        # Analyze confidence patterns
        high_conf_responses = [r for r in responses if r.confidence_level > 70]
        low_conf_responses = [r for r in responses if r.confidence_level < 40]
        
        # Risk-taking behavior
        risk_behavior = "calculated"
        if len(high_conf_responses) > len(responses) * 0.7:
            risk_behavior = "bold"
        elif len(low_conf_responses) > len(responses) * 0.5:
            risk_behavior = "cautious"
        
        # Learning approach
        approach = "balanced"
        approach_insight = "You blend intuition with analysis effectively."
        
        if time_variance < 5 and avg_time < 20:
            approach = "intuitive"
            approach_insight = "You rely on gut instinct and pattern recognition."
        elif time_variance < 5 and avg_time > 25:
            approach = "systematic"
            approach_insight = "You follow a consistent, methodical thinking process."
        elif time_variance > 10:
            approach = "adaptive"
            approach_insight = "You adjust your strategy based on question difficulty."
        
        return {
            "thinking_speed": thinking_speed,
            "speed_insight": speed_insight,
            "avg_time_per_question": round(avg_time, 1),
            "risk_behavior": risk_behavior,
            "learning_approach": approach,
            "approach_insight": approach_insight,
            "consistency_score": round(100 - (time_variance / avg_time * 100) if avg_time > 0 else 0, 1)
        }
    
    @staticmethod
    def generate_learning_moments(responses: List[Response]) -> List[Dict[str, Any]]:
        """
        Identify key learning moments - breakthrough insights and growth opportunities.
        """
        moments = []
        
        # Low confidence success - "Hidden mastery"
        for idx, r in enumerate(responses):
            if r.is_correct and r.confidence_level < 30:
                moments.append({
                    "type": "hidden_mastery",
                    "title": "💎 Hidden Mastery",
                    "description": f"Question #{idx + 1}: You knew more than you thought! Trust your knowledge.",
                    "lesson": "Your intuition is stronger than you realize."
                })
        
        # High confidence error - "Calibration moment"
        for idx, r in enumerate(responses):
            if not r.is_correct and r.confidence_level > 80:
                moments.append({
                    "type": "calibration_moment",
                    "title": "🎯 Calibration Moment",
                    "description": f"Question #{idx + 1}: High confidence met unexpected outcome.",
                    "lesson": "A chance to refine your understanding and check assumptions."
                })
        
        # Consistent accuracy with varying confidence - "Growing self-awareness"
        correct_with_varied_conf = [r for r in responses if r.is_correct]
        if len(correct_with_varied_conf) >= 3:
            conf_range = max(r.confidence_level for r in correct_with_varied_conf) - min(r.confidence_level for r in correct_with_varied_conf)
            if conf_range > 40:
                moments.append({
                    "type": "self_awareness",
                    "title": "🧠 Growing Self-Awareness",
                    "description": "Your confidence varied but you stayed accurate.",
                    "lesson": "You're learning to distinguish between certainty and correctness."
                })
        
        return moments[:5]  # Limit to top 5 moments
    
    @staticmethod
    def generate_reflection_prompts(responses: List[Response], insights: Dict[str, Any]) -> List[str]:
        """
        Generate personalized reflection questions to encourage metacognition.
        """
        prompts = []
        
        # Based on accuracy
        if insights.get("accuracy", 0) > 80:
            prompts.append("What strategies helped you succeed? How can you apply them to new topics?")
        else:
            prompts.append("Which questions made you pause? What would you do differently next time?")
        
        # Based on confidence alignment
        alignment = insights.get("confidence_accuracy_alignment", 0)
        if alignment < 60:
            prompts.append("When you felt confident, what made you so sure? Were there warning signs you missed?")
        elif alignment > 85:
            prompts.append("You have strong self-awareness! How did you develop this calibration?")
        
        # Based on curiosity
        if insights.get("curiosity_score", 0) > 70:
            prompts.append("You show exploratory learning! How does uncertainty feel when you're learning?")
        
        # Based on learning approach
        patterns = insights.get("learning_patterns", {})
        if patterns.get("thinking_speed") == "quick":
            prompts.append("You're a fast thinker! Would slowing down reveal new insights?")
        elif patterns.get("thinking_speed") == "deliberate":
            prompts.append("You're thorough! Does your careful approach ever hold you back?")
        
        return prompts[:3]  # Limit to 3 most relevant prompts
    
    @staticmethod
    def get_cognitive_insights(responses: List[Response]) -> Dict[str, Any]:
        """
        Generate comprehensive cognitive behavior insights focused on HOW learners learn.
        """
        if not responses:
            return {}
        
        curiosity_score = CuriosityAnalyzer.calculate_curiosity_score(responses)
        gaps = CuriosityAnalyzer.identify_learning_gaps(responses)
        alignment = CuriosityAnalyzer.get_confidence_accuracy_alignment(responses)
        learning_patterns = CuriosityAnalyzer.analyze_learning_patterns(responses)
        learning_moments = CuriosityAnalyzer.generate_learning_moments(responses)
        
        # Calculate accuracy
        correct_count = sum(1 for r in responses if r.is_correct)
        accuracy = (correct_count / len(responses)) * 100
        
        # Average confidence
        avg_confidence = sum(r.confidence_level for r in responses) / len(responses)
        
        # Determine learning style with narrative
        learning_style = "analytical"
        style_narrative = "You approach learning systematically and thoughtfully."
        
        if curiosity_score > 70:
            learning_style = "exploratory"
            style_narrative = "You're a curious explorer who thrives on discovery and uncertainty."
        elif alignment > 80:
            learning_style = "calibrated"
            style_narrative = "You have exceptional self-awareness about your knowledge."
        elif avg_confidence > 75:
            learning_style = "confident"
            style_narrative = "You trust your abilities and make bold decisions."
        
        # Generate improvement suggestions
        suggestions = []
        if curiosity_score < 40:
            suggestions.append("Try exploring topics where you're less certain - growth happens at the edge of comfort.")
        if alignment < 70:
            suggestions.append("Practice metacognition: pause before answering to assess 'How sure am I really?'")
        if learning_patterns.get("consistency_score", 0) < 60:
            suggestions.append("Your approach varies widely - experiment with a more consistent strategy.")
        if accuracy < 60:
            suggestions.append("Focus on understanding concepts deeply rather than memorizing answers.")
        
        # Generate reflection prompts
        reflection_prompts = CuriosityAnalyzer._generate_reflection_prompts(
            learning_style, gaps, learning_patterns, alignment
        )
        
        # Calculate additional metrics for richer insights
        total_time = sum(r.time_spent for r in responses)
        avg_time = total_time / len(responses) if responses else 0
        
        # Time spent analysis
        correct_times = [r.time_spent for r in responses if r.is_correct]
        incorrect_times = [r.time_spent for r in responses if not r.is_correct]
        avg_correct_time = sum(correct_times) / len(correct_times) if correct_times else 0
        avg_incorrect_time = sum(incorrect_times) / len(incorrect_times) if incorrect_times else 0
        
        # Confidence distribution
        low_conf = len([r for r in responses if r.confidence_level < 40])
        mid_conf = len([r for r in responses if 40 <= r.confidence_level <= 70])
        high_conf = len([r for r in responses if r.confidence_level > 70])
        
        # Performance by confidence level
        high_conf_correct = len([r for r in responses if r.confidence_level > 70 and r.is_correct])
        high_conf_total = len([r for r in responses if r.confidence_level > 70])
        low_conf_correct = len([r for r in responses if r.confidence_level < 40 and r.is_correct])
        low_conf_total = len([r for r in responses if r.confidence_level < 40])
        
        high_conf_accuracy = (high_conf_correct / high_conf_total * 100) if high_conf_total > 0 else 0
        low_conf_accuracy = (low_conf_correct / low_conf_total * 100) if low_conf_total > 0 else 0
        
        # Calibration score - how well confidence predicts correctness
        calibration_score = CuriosityAnalyzer._calculate_calibration_score(responses)
        
        insights = {
            "curiosity_score": round(curiosity_score, 2),
            "accuracy": round(accuracy, 2),
            "avg_confidence": round(avg_confidence, 2),
            "confidence_accuracy_alignment": round(alignment, 2),
            "calibration_score": round(calibration_score, 2),
            "learning_style": learning_style,
            "style_narrative": style_narrative,
            "learning_patterns": learning_patterns,
            "learning_moments": learning_moments,
            "total_responses": len(responses),
            "correct_responses": correct_count,
            "gaps": gaps,
            "improvement_suggestions": suggestions,
            "reflection_prompts": reflection_prompts,
            # Time analysis
            "time_stats": {
                "total_time": total_time,
                "avg_time_per_question": round(avg_time, 1),
                "avg_time_correct": round(avg_correct_time, 1),
                "avg_time_incorrect": round(avg_incorrect_time, 1)
            },
            # Confidence analysis
            "confidence_distribution": {
                "low": low_conf,
                "medium": mid_conf,
                "high": high_conf
            },
            "confidence_performance": {
                "high_confidence_accuracy": round(high_conf_accuracy, 1),
                "low_confidence_accuracy": round(low_conf_accuracy, 1),
                "high_conf_questions": high_conf_total,
                "low_conf_questions": low_conf_total
            }
        }
        
        # Add reflection prompts
        insights["reflection_prompts"] = CuriosityAnalyzer.generate_reflection_prompts(responses, insights)
        
        return insights
    
    @staticmethod
    def _generate_reflection_prompts(
        learning_style: str, 
        gaps: Dict[str, Any],
        learning_patterns: Dict[str, Any],
        alignment: float
    ) -> List[Dict[str, str]]:
        """Generate personalized reflection prompts to encourage metacognition."""
        prompts = []
        
        # Universal prompts
        prompts.append({
            "question": "What surprised you most about your performance today?",
            "purpose": "Builds awareness of expectations vs. reality"
        })
        
        # Style-specific prompts
        if learning_style == "exploratory":
            prompts.append({
                "question": "When you felt uncertain but answered correctly, what knowledge or intuition were you drawing on?",
                "purpose": "Validates implicit knowledge and builds confidence"
            })
            prompts.append({
                "question": "How can you balance exploration with consolidating what you already know?",
                "purpose": "Encourages strategic learning"
            })
        
        elif learning_style == "confident":
            prompts.append({
                "question": "On questions you missed, what made you feel so confident?",
                "purpose": "Reveals blind spots and calibration opportunities"
            })
            prompts.append({
                "question": "How might you slow down to check your assumptions before answering?",
                "purpose": "Promotes metacognitive monitoring"
            })
        
        elif learning_style == "calibrated":
            prompts.append({
                "question": "What strategies help you accurately assess your knowledge level?",
                "purpose": "Reinforces effective metacognitive practices"
            })
            prompts.append({
                "question": "How can you apply this self-awareness to learning new topics?",
                "purpose": "Transfers skills to new contexts"
            })
        
        # Alignment-based prompts
        if alignment < 60:
            prompts.append({
                "question": "Before answering, try asking yourself: 'Would I bet money on this answer?' Why or why not?",
                "purpose": "Sharpens confidence calibration"
            })
        
        # Pattern-based prompts
        thinking_speed = learning_patterns.get("thinking_speed", "")
        if thinking_speed == "quick":
            prompts.append({
                "question": "What would change if you took 10 more seconds on each question?",
                "purpose": "Explores the value of deliberation"
            })
        elif thinking_speed == "deliberate":
            prompts.append({
                "question": "Are you overthinking, or is thorough analysis your strength?",
                "purpose": "Validates processing style while checking for inefficiency"
            })
        
        # Gap-based prompts
        overconfident = gaps.get("overconfident_errors", [])
        if len(overconfident) > 2:
            prompts.append({
                "question": "What patterns do you notice in the topics where you were overconfident?",
                "purpose": "Identifies systematic misconceptions"
            })
        
        return prompts[:5]  # Return top 5 most relevant prompts

    @staticmethod
    def _calculate_calibration_score(responses: List[Response]) -> float:
        """
        Calculate how well calibrated a student's confidence is.
        
        Perfect calibration: When confident at 70%, you're correct 70% of the time.
        Score of 100 means perfect calibration.
        """
        if not responses:
            return 0.0
        
        # Group responses by confidence buckets
        buckets = {
            "low": {"responses": [], "expected": 20},      # 0-40% confidence
            "medium": {"responses": [], "expected": 55},   # 40-70% confidence  
            "high": {"responses": [], "expected": 85}      # 70-100% confidence
        }
        
        for r in responses:
            if r.confidence_level < 40:
                buckets["low"]["responses"].append(r)
            elif r.confidence_level <= 70:
                buckets["medium"]["responses"].append(r)
            else:
                buckets["high"]["responses"].append(r)
        
        total_error = 0
        num_buckets_with_data = 0
        
        for bucket_name, bucket_data in buckets.items():
            bucket_responses = bucket_data["responses"]
            if len(bucket_responses) >= 1:
                actual_accuracy = sum(1 for r in bucket_responses if r.is_correct) / len(bucket_responses) * 100
                expected_accuracy = bucket_data["expected"]
                # Calculate error - lower is better
                error = abs(actual_accuracy - expected_accuracy)
                total_error += error
                num_buckets_with_data += 1
        
        if num_buckets_with_data == 0:
            return 50.0
        
        avg_error = total_error / num_buckets_with_data
        # Convert to a 0-100 score where 100 is perfect
        calibration_score = max(0, 100 - avg_error)
        return calibration_score
