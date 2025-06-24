#!/usr/bin/env python3
"""
Simple test script for the direct Llama API integration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_client import SimpleLlamaClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_simple_llama():
    """Test the simplified Llama API client."""
    print("🧪 Testing Simple Llama API Client")
    print("=" * 50)
    
    # Initialize client
    client = SimpleLlamaClient()
    
    # Test 1: Simple question
    print("\n🤖 Test 1: Simple Medical Question")
    print("-" * 40)
    
    simple_question = "What is endometriosis?"
    print(f"📝 Question: {simple_question}")
    
    response = client.send_request(simple_question, max_tokens=150)
    print(f"📤 Response: {response}")
    
    if len(response) > 50 and "error" not in response.lower():
        print("✅ Simple question test PASSED")
    else:
        print("❌ Simple question test FAILED")
        return False
    
    # Test 2: Medical explanation
    print("\n🏥 Test 2: Medical Explanation Generation")
    print("-" * 45)
    
    sample_prediction = {
        "prediction_label": "Endometriosis",
        "confidence": 0.75,
        "risk_level": "High",
        "probabilities": {"endometriosis": 0.75, "no_endometriosis": 0.25}
    }
    
    user_query = "What does my 75% risk score mean?"
    print(f"📝 User query: {user_query}")
    
    explanation = client.generate_explanation(user_query, sample_prediction, [])
    print(f"📤 Explanation: {explanation}")
    
    if len(explanation) > 100 and "error" not in explanation.lower():
        print("✅ Medical explanation test PASSED")
    else:
        print("❌ Medical explanation test FAILED")
        return False
    
    # Test 3: Question answering
    print("\n❓ Test 3: Question Answering")
    print("-" * 35)
    
    question = "What are the next steps I should take?"
    print(f"📝 Question: {question}")
    
    answer = client.answer_question(question, sample_prediction)
    print(f"📤 Answer: {answer}")
    
    if len(answer) > 30:
        print("✅ Question answering test PASSED")
    else:
        print("❌ Question answering test FAILED")
        return False
    
    print("\n🎉 All tests PASSED! Simple Llama API is working.")
    print("\n📋 Next steps:")
    print("1. Start the RAG API: python rag_api.py")
    print("2. Test in your React app")
    print("3. Ask questions and generate explanations")
    
    return True

if __name__ == "__main__":
    try:
        success = test_simple_llama()
        if success:
            sys.exit(0)
        else:
            print("\n❌ Tests failed. Check the logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)