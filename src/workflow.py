"""
Main healthcare workflow
"""
from typing import Dict, Any
from .config import HealthcareConfig
from .chains import (
    GuardrailChain,
    IntentClassifierChain,
    SymptomCheckerChain,
    GovernmentSchemeChain,
    MentalWellnessChain,
    YogaChain,
    AyushChain,
    HospitalLocatorChain
)

class HealthcareWorkflow:
    """Main workflow orchestrator for hybrid RAG/Search system"""
    
    def __init__(self, config: HealthcareConfig):
        self.config = config
        
        # Initialize all chains, PASSING THE CORRECT TOOL to each one.
        self.guardrail = GuardrailChain(config.llm)
        self.classifier = IntentClassifierChain(config.llm)
        self.symptom_chain = SymptomCheckerChain(config.llm)
        
        # --- THIS IS THE CRITICAL FIX ---
        
        # Agents using WEB SEARCH get config.search_tool
        self.gov_scheme_chain = GovernmentSchemeChain(config.llm, config.search_tool)
        self.mental_wellness_chain = MentalWellnessChain(config.llm, config.search_tool)
        self.hospital_chain = HospitalLocatorChain(config.llm, config.search_tool)
        
        # Agents using RAG get config.rag_retriever
        self.ayush_chain = AyushChain(config.llm, config.rag_retriever)
        self.yoga_chain = YogaChain(config.llm, config.rag_retriever) # This was the line causing the error
        
        # --- END OF FIX ---

    def run(self, user_input: str, query_for_classification: str) -> Dict[str, Any]:
        """Execute the workflow"""
        
        # Step 1: Safety check
        print("🛡️  [STEP 1/3] Running Safety Guardrail Check...")
        safety_check = self.guardrail.check(query_for_classification)
        if not safety_check.get("is_safe", True):
            return {"status": "blocked", "reason": safety_check.get("reason")}
        print("   ✓ Content is safe\n")
        
        # Step 2: Classify intent
        print("🎯 [STEP 2/3] Classifying Intent...")
        classification = self.classifier.run(query_for_classification)
        intent = classification.get("classification")
        print(f"   → Intent: {intent}\n")
        
        # Step 3: Route to appropriate chain (using the clean user_input)
        print(f"🔗 [STEP 3/3] Executing Chain for '{intent}'...")
        result = {"intent": intent, "reasoning": classification.get("reasoning"), "output": None}
        
        if intent == "government_scheme_support":
            result["output"] = self.gov_scheme_chain.run(user_input)
            
        elif intent == "mental_wellness_support":
            result["output"] = self.mental_wellness_chain.run(user_input)
            # Yoga is RAG-based, so it will use the RAG retriever
            result["yoga_recommendations"] = self.yoga_chain.run(user_input)
            
        elif intent == "ayush_support":
            result["output"] = self.ayush_chain.run(user_input)
            
        elif intent == "symptom_checker":
            result.update(self._handle_symptoms(user_input))
            
        elif intent == "facility_locator_support":
            result["output"] = self.hospital_chain.run(user_input)
            
        else:
            result["output"] = "I couldn't understand your request. Please try rephrasing."
        
        print("   ✓ Chain execution complete\n")
        return result
    
    def _handle_symptoms(self, user_input: str) -> Dict[str, Any]:
        """Handle symptom checking with multi-agent follow-up"""
        symptom_data = self.symptom_chain.run(user_input)
        result = {"symptom_assessment": symptom_data.model_dump()}
        
        if symptom_data.is_emergency:
            hospital_query = f"Find nearest emergency hospitals for: {', '.join(symptom_data.symptoms)}"
            result["output"] = {
                "emergency": True,
                "message": "⚠️ URGENT: Seek immediate medical attention. Call emergency services.",
            }
            result["hospital_locator"] = self.hospital_chain.run(hospital_query)
        else:
            symptom_text = f"Patient has {', '.join(symptom_data.symptoms)} with severity {symptom_data.severity}/10"
            result["output"] = {"emergency": False, "message": "Based on your symptoms, here are some recommendations:"}
            # All follow-up recommendations for symptoms will use the RAG system
            result["ayurveda_recommendations"] = self.ayush_chain.run(f"Provide ayurvedic remedies for: {symptom_text}")
            result["yoga_recommendations"] = self.yoga_chain.run(f"Suggest yoga for: {symptom_text}")
            result["general_guidance"] = self.mental_wellness_chain.run(f"Provide wellness advice for: {symptom_text}")
        
        return result