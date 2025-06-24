import requests
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SimpleLlamaClient:
    def __init__(self, api_token: str = "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"):
        """Simple Llama API client that just sends payloads and gets responses."""
        self.api_token = api_token
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Use a simple, reliable model
        self.model = "microsoft/DialoGPT-medium"
        self.api_url = f"{self.base_url}/{self.model}"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"🚀 Simple Llama client initialized")
        logger.info(f"🔗 API URL: {self.api_url}")
        logger.info(f"🔑 Token: {self.api_token[:10]}...")
    
    def send_request(self, prompt: str, max_tokens: int = 300) -> str:
        """Send a direct request to Llama API and return the response."""
        
        # Create simple payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        logger.info(f"📤 Sending request to Llama API...")
        logger.info(f"📝 Prompt: {prompt[:100]}...")
        logger.info(f"🎯 Max tokens: {max_tokens}")
        
        try:
            # Send the request
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload, 
                timeout=30
            )
            
            logger.info(f"📡 Response status: {response.status_code}")
            
            # Handle different response codes
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Success! Response type: {type(result)}")
                
                # Extract the generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    logger.info(f"📄 Generated text length: {len(generated_text)}")
                    
                    if generated_text.strip():
                        return generated_text.strip()
                    else:
                        return "I apologize, but I couldn't generate a proper response. Please try again."
                
                elif isinstance(result, dict) and "generated_text" in result:
                    generated_text = result["generated_text"]
                    return generated_text.strip()
                
                else:
                    logger.warning(f"⚠️ Unexpected response format: {result}")
                    return "I received an unexpected response format. Please try again."
            
            elif response.status_code == 503:
                logger.warning("⏳ Model is loading...")
                return "The AI model is currently loading. Please try again in a moment."
            
            elif response.status_code == 404:
                logger.error("❌ Model not found")
                return "The AI model is not available. Please try again later."
            
            elif response.status_code == 401:
                logger.error("❌ Authentication failed")
                return "Authentication failed. Please check the API configuration."
            
            elif response.status_code == 429:
                logger.error("❌ Rate limit exceeded")
                return "Too many requests. Please wait a moment and try again."
            
            else:
                logger.error(f"❌ HTTP error: {response.status_code}")
                logger.error(f"📄 Response: {response.text}")
                return f"Service temporarily unavailable (Error {response.status_code}). Please try again."
        
        except requests.exceptions.Timeout:
            logger.error("⏰ Request timed out")
            return "The request timed out. Please try again."
        
        except requests.exceptions.ConnectionError:
            logger.error("🌐 Connection error")
            return "Unable to connect to the AI service. Please check your internet connection."
        
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
    
    def generate_explanation(self, user_query: str, prediction_result: Dict, medical_context: List[str]) -> str:
        """Generate explanation for endometriosis prediction."""
        
        # Create a focused prompt
        risk_level = prediction_result.get('risk_level', 'Unknown')
        probability = prediction_result.get('probabilities', {}).get('endometriosis', 0)
        
        prompt = f"""You are a helpful medical assistant. A user has received an endometriosis risk assessment.

User's Question: {user_query}

Assessment Results:
- Risk Level: {risk_level}
- Probability: {probability:.0%}

Please provide a clear, supportive explanation that:
1. Explains what the results mean in simple terms
2. Gives practical next steps
3. Emphasizes consulting healthcare professionals
4. Is reassuring but informative

Keep your response under 200 words and be empathetic."""

        logger.info("🧠 Generating medical explanation...")
        return self.send_request(prompt, max_tokens=250)
    
    def answer_question(self, question: str, prediction_result: Dict) -> str:
        """Answer a specific question about endometriosis."""
        
        risk_level = prediction_result.get('risk_level', 'Unknown')
        probability = prediction_result.get('probabilities', {}).get('endometriosis', 0)
        
        prompt = f"""You are a medical information assistant. Answer this question about endometriosis:

Question: {question}

Context: The user has a {risk_level.lower()} risk assessment with {probability:.0%} probability.

Provide a helpful, accurate answer in 2-3 sentences. Always recommend consulting healthcare professionals for medical advice."""

        logger.info(f"❓ Answering question: {question}")
        return self.send_request(prompt, max_tokens=150)

# Fallback responses (same as before)
FALLBACK_RESPONSES = {
    "high_risk": """Based on your symptom pattern, the model suggests a higher likelihood of endometriosis. This means your symptoms align with patterns commonly seen in diagnosed cases.

**What this means:** Your combination of symptoms creates a pattern often associated with endometriosis.

**Important next steps:**
- Schedule an appointment with a gynecologist as soon as possible
- Keep detailed records of your symptoms
- Don't let anyone dismiss your concerns
- Consider bringing support to medical appointments

**Remember:** This is a screening tool, not a diagnosis. Only a healthcare provider can properly diagnose endometriosis.""",
    
    "moderate_risk": """Your symptom pattern shows some features that could be associated with endometriosis, but the picture isn't entirely clear.

**What this means:** Some symptoms align with endometriosis patterns, but other factors might explain your experience.

**Recommended next steps:**
- Schedule a consultation with a gynecologist
- Continue tracking your symptoms
- Discuss your family history with your doctor
- Don't delay seeking care if symptoms affect your quality of life

**Keep in mind:** Many conditions can cause similar symptoms. A healthcare provider can help determine the most likely causes.""",
    
    "low_risk": """Based on your symptom pattern, the model suggests a lower likelihood of endometriosis, though this doesn't completely rule out the condition.

**What this means:** Your symptoms don't strongly match typical endometriosis patterns, but every person's experience is unique.

**Still important:**
- Continue monitoring your symptoms
- Maintain regular gynecological check-ups
- Consult a healthcare provider if symptoms worsen
- Trust your body and advocate for your health"""
}

def get_fallback_response(risk_level: str, user_query: str = "") -> str:
    """Get fallback response when API is unavailable."""
    risk_key = risk_level.lower() + "_risk"
    return FALLBACK_RESPONSES.get(risk_key, FALLBACK_RESPONSES["moderate_risk"])

# For backward compatibility
class LlamaAPIClient(SimpleLlamaClient):
    """Alias for backward compatibility."""
    pass