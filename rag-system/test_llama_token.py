#!/usr/bin/env python3
"""
Test script to verify your Llama API token is working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_client import LlamaAPIClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_llama_api():
    """Test the Llama API with your specific token."""
    print("🧪 Testing Llama API with your token...")
    print("=" * 60)
    
    # Initialize client with your token
    client = LlamaAPIClient(api_token="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")
    
    # Test 1: Connection test
    print("\n🔍 Test 1: Connection Test")
    print("-" * 30)
    connection_ok = client.test_connection()
    if connection_ok:
        print("✅ Connection test PASSED")
    else:
        print("❌ Connection test FAILED")
        return False
    
    # Test 2: Simple response generation
    print("\n🤖 Test 2: Simple Response Generation")
    print("-" * 40)
    simple_prompt = "Explain what endometriosis is in simple terms."
    
    print(f"📝 Prompt: {simple_prompt}")
    print("⏳ Generating response...")
    
    response = client.generate_response(simple_prompt, max_length=200)
    
    print(f"📤 Response length: {len(response)} characters")
    print(f"📄 Response preview: {response[:100]}...")
    
    if len(response) > 50 and "error" not in response.lower():
        print("✅ Simple response test PASSED")
    else:
        print("❌ Simple response test FAILED")
        print(f"Full response: {response}")
        return False
    
    # Test 3: Medical explanation generation
    print("\n🏥 Test 3: Medical Explanation Generation")
    print("-" * 45)
    
    sample_prediction = {
        "prediction_label": "Endometriosis",
        "confidence": 0.75,
        "risk_level": "High",
        "probabilities": {"endometriosis": 0.75, "no_endometriosis": 0.25}
    }
    
    medical_context = [
        "Endometriosis is a condition where tissue similar to the uterine lining grows outside the uterus.",
        "Common symptoms include pelvic pain, heavy periods, and pain during intercourse."
    ]
    
    user_query = "What does my 75% risk score mean?"
    
    print(f"📝 User query: {user_query}")
    print("⏳ Generating medical explanation...")
    
    explanation = client.generate_explanation(user_query, sample_prediction, medical_context)
    
    print(f"📤 Explanation length: {len(explanation)} characters")
    print(f"📄 Explanation preview: {explanation[:150]}...")
    
    if len(explanation) > 100 and "error" not in explanation.lower():
        print("✅ Medical explanation test PASSED")
    else:
        print("❌ Medical explanation test FAILED")
        print(f"Full explanation: {explanation}")
        return False
    
    print("\n🎉 All tests PASSED! Your Llama API token is working correctly.")
    print("\n📋 Next steps:")
    print("1. Start the RAG API server: python rag_api.py")
    print("2. Test the full system in your React app")
    print("3. Generate predictions and ask for explanations")
    
    return True

if __name__ == "__main__":
    try:
        success = test_llama_api()
        if success:
            sys.exit(0)
        else:
            print("\n❌ Tests failed. Please check your token and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)