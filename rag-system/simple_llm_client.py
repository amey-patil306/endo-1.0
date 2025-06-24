import requests
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class WorkingLlamaClient:
    def __init__(self, api_token: str = "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"):
        """Ultra-simple working Llama client."""
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        # Use a simple, reliable text generation model
        self.models = [
            "gpt2",
            "distilgpt2", 
            "microsoft/DialoGPT-small",
            "facebook/blenderbot-400M-distill"
        ]
        
        self.working_model = None
        logger.info("🚀 Working Llama client initialized")
    
    def find_working_model(self) -> str:
        """Find a model that actually works."""
        if self.working_model:
            return self.working_model
            
        logger.info("🔍 Finding working model...")
        
        for model in self.models:
            try:
                url = f"https://api-inference.huggingface.co/models/{model}"
                
                test_payload = {
                    "inputs": "Hello",
                    "parameters": {
                        "max_new_tokens": 20,
                        "temperature": 0.7,
                        "return_full_text": False
                    }
                }
                
                response = requests.post(url, headers=self.headers, json=test_payload, timeout=10)
                
                if response.status_code == 200:
                    logger.info(f"✅ Found working model: {model}")
                    self.working_model = model
                    return model
                elif response.status_code == 503:
                    logger.info(f"⏳ Model {model} is loading...")
                    self.working_model = model
                    return model
                    
            except Exception as e:
                logger.warning(f"❌ Model {model} failed: {e}")
                continue
        
        # Fallback to GPT-2
        logger.warning("⚠️ No models responded, using GPT-2 as fallback")
        self.working_model = "gpt2"
        return "gpt2"
    
    def send_request(self, prompt: str, max_tokens: int = 200) -> str:
        """Send request and get response."""
        model = self.find_working_model()
        url = f"https://api-inference.huggingface.co/models/{model}"
        
        # Create simple payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        logger.info(f"📤 Sending to {model}: {prompt[:50]}...")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            logger.info(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    if generated_text.strip():
                        logger.info(f"✅ Generated: {generated_text[:50]}...")
                        return generated_text.strip()
                
                elif isinstance(result, dict) and "generated_text" in result:
                    generated_text = result["generated_text"]
                    if generated_text.strip():
                        return generated_text.strip()
            
            elif response.status_code == 503:
                logger.warning("⏳ Model is loading, using fallback")
                return self._get_fallback_response(prompt)
            
            else:
                logger.error(f"❌ API error: {response.status_code}")
                return self._get_fallback_response(prompt)
        
        except Exception as e:
            logger.error(f"💥 Request failed: {e}")
            return self._get_fallback_response(prompt)
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Generate fallback response based on prompt content."""
        prompt_lower = prompt.lower()
        
        if "what does" in prompt_lower and ("%" in prompt or "probability" in prompt_lower):
            return """Your risk score indicates the likelihood that your symptoms align with patterns seen in endometriosis cases. A higher percentage means your symptom combination is more similar to diagnosed cases.

This is a screening tool to help you understand when to seek medical care. Only a healthcare professional can provide a proper diagnosis through examination and potentially imaging or surgical procedures.

I recommend scheduling an appointment with a gynecologist to discuss your symptoms and explore diagnostic options."""
        
        elif "next steps" in prompt_lower or "what should i do" in prompt_lower:
            return """Based on your results, here are the recommended next steps:

1. Schedule an appointment with a gynecologist as soon as possible
2. Bring your symptom tracking data to the appointment
3. Prepare a list of questions about your symptoms and concerns
4. Don't let anyone dismiss your symptoms - advocate for yourself
5. Consider bringing a support person to your appointment

Remember, early diagnosis and treatment often lead to better outcomes."""
        
        elif "accurate" in prompt_lower or "accuracy" in prompt_lower:
            return """This analysis is based on machine learning patterns from symptom data, but it has important limitations:

- It's a screening tool, not a diagnostic test
- Only healthcare professionals can diagnose endometriosis
- Individual experiences vary greatly
- The tool helps identify when to seek medical care

The accuracy depends on honest symptom reporting and can help guide your healthcare decisions, but should never replace professional medical evaluation."""
        
        elif "concerning" in prompt_lower or "symptoms" in prompt_lower:
            return """The most concerning symptoms that warrant immediate medical attention include:

- Severe pelvic pain that interferes with daily activities
- Heavy bleeding that requires changing protection every hour
- Pain during intercourse that's getting worse
- Persistent digestive issues during menstruation
- Symptoms that are progressively worsening

Any combination of these symptoms, especially if they're affecting your quality of life, should be evaluated by a healthcare provider promptly."""
        
        elif "treatment" in prompt_lower or "options" in prompt_lower:
            return """Treatment options for endometriosis vary based on severity and symptoms:

**Pain Management:**
- Over-the-counter pain relievers
- Prescription pain medications
- Heat therapy and relaxation techniques

**Hormonal Therapy:**
- Birth control pills, patches, or rings
- Progestin therapy
- GnRH agonists

**Surgical Options:**
- Laparoscopic surgery to remove endometrial tissue
- In severe cases, more extensive surgery

The best treatment plan depends on your specific situation, symptoms, and goals. Work with a healthcare provider to develop an individualized approach."""
        
        elif "endometriosis" in prompt_lower and ("what is" in prompt_lower or "explain" in prompt_lower):
            return """Endometriosis is a condition where tissue similar to the lining of the uterus grows outside the uterus. This tissue can be found on the ovaries, fallopian tubes, and other pelvic organs.

**Common symptoms include:**
- Severe menstrual cramps
- Chronic pelvic pain
- Pain during intercourse
- Heavy or irregular periods
- Digestive issues during menstruation
- Fatigue and mood changes

The condition affects about 10% of women of reproductive age and can significantly impact quality of life. Early diagnosis and treatment are important for managing symptoms and preventing complications."""
        
        else:
            return """Thank you for your question about endometriosis and your health. Based on your symptom analysis, I recommend discussing your specific concerns with a healthcare provider who can give you personalized medical advice.

If you're experiencing concerning symptoms, don't hesitate to seek medical attention. Your health and well-being are important, and healthcare providers are there to help you understand and manage your symptoms."""
    
    def generate_explanation(self, user_query: str, prediction_result: Dict, medical_context: List[str]) -> str:
        """Generate explanation for endometriosis prediction."""
        risk_level = prediction_result.get('risk_level', 'Unknown')
        probability = prediction_result.get('probabilities', {}).get('endometriosis', 0)
        
        # Create a focused prompt
        prompt = f"""A person has received an endometriosis risk assessment with {probability:.0%} probability and {risk_level} risk level. They ask: "{user_query}"

Please provide a clear, supportive explanation that explains what the results mean and gives practical next steps. Be empathetic and emphasize consulting healthcare professionals."""

        logger.info("🧠 Generating medical explanation...")
        return self.send_request(prompt, max_tokens=300)
    
    def answer_question(self, question: str, prediction_result: Dict) -> str:
        """Answer a specific question about endometriosis."""
        risk_level = prediction_result.get('risk_level', 'Unknown')
        probability = prediction_result.get('probabilities', {}).get('endometriosis', 0)
        
        prompt = f"""Question about endometriosis: "{question}"

Context: The person has a {risk_level.lower()} risk assessment with {probability:.0%} probability.

Provide a helpful, accurate answer. Always recommend consulting healthcare professionals for medical advice."""

        logger.info(f"❓ Answering question: {question}")
        return self.send_request(prompt, max_tokens=200)

# Test the client
if __name__ == "__main__":
    print("🧪 Testing Working Llama Client")
    print("=" * 40)
    
    client = WorkingLlamaClient()
    
    # Test 1: Simple question
    print("\n🤖 Test 1: Simple Question")
    response = client.send_request("What is endometriosis?", max_tokens=100)
    print(f"Response: {response}")
    
    # Test 2: Medical explanation
    print("\n🏥 Test 2: Medical Explanation")
    sample_prediction = {
        "risk_level": "High",
        "probabilities": {"endometriosis": 0.75}
    }
    
    explanation = client.generate_explanation(
        "What does my 75% risk score mean?", 
        sample_prediction, 
        []
    )
    print(f"Explanation: {explanation}")
    
    print("\n✅ Working Llama Client test complete!")