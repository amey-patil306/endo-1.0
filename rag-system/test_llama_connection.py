#!/usr/bin/env python3
"""
Quick test to verify Hugging Face API connection and find working models.
"""

import requests
import json

def test_models():
    """Test multiple models to find one that works."""
    print("🧪 Testing Hugging Face API Connection...")
    print("=" * 50)
    
    # Your token
    api_token = "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"
    
    # Models to test (in order of preference)
    models_to_test = [
        "microsoft/DialoGPT-medium",
        "facebook/blenderbot-400M-distill", 
        "microsoft/DialoGPT-small",
        "gpt2",
        "distilgpt2"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    print(f"🔑 Using token: {api_token[:10]}...")
    print(f"🎯 Testing {len(models_to_test)} models...")
    
    working_models = []
    
    for i, model in enumerate(models_to_test, 1):
        print(f"\n🧪 Test {i}/{len(models_to_test)}: {model}")
        print("-" * 40)
        
        url = f"https://api-inference.huggingface.co/models/{model}"
        
        # Test payload
        test_payload = {
            "inputs": "Hello, can you respond?",
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            print(f"📡 Sending request to: {url}")
            response = requests.post(url, headers=headers, json=test_payload, timeout=15)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS! Model is working")
                print(f"📄 Response type: {type(result)}")
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    print(f"🎯 Generated: {generated_text[:100]}...")
                    working_models.append(model)
                elif isinstance(result, dict):
                    print(f"📦 Response: {result}")
                    working_models.append(model)
                
            elif response.status_code == 503:
                print("⏳ Model is loading (this is normal)")
                print("🔄 This model should work once loaded")
                working_models.append(model)
                
            elif response.status_code == 404:
                print("❌ Model not found")
                
            elif response.status_code == 401:
                print("❌ Authentication failed - check your token")
                break
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"📄 Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out")
        except Exception as e:
            print(f"💥 Exception: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 FINAL RESULTS")
    print("=" * 50)
    
    if working_models:
        print(f"✅ Found {len(working_models)} working models:")
        for i, model in enumerate(working_models, 1):
            print(f"  {i}. {model}")
        
        print(f"\n🎯 Recommended model: {working_models[0]}")
        print("\n📋 Next steps:")
        print("1. The system will automatically use the first working model")
        print("2. Start the RAG API: python rag_api.py")
        print("3. Test explanations in your React app")
        
        return True
    else:
        print("❌ No working models found")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify your Hugging Face token is valid")
        print("3. Try again in a few minutes (models may be loading)")
        
        return False

def test_specific_model(model_name):
    """Test a specific model with a medical question."""
    print(f"\n🏥 Testing medical response with {model_name}")
    print("-" * 50)
    
    api_token = "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"
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    medical_prompt = "What is endometriosis and what are its main symptoms?"
    
    payload = {
        "inputs": medical_prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                print(f"✅ Medical response generated:")
                print(f"📄 {generated_text}")
                return True
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_models()
    
    if success:
        # Test the first working model with a medical question
        working_models = [
            "microsoft/DialoGPT-medium",
            "facebook/blenderbot-400M-distill", 
            "microsoft/DialoGPT-small",
            "gpt2"
        ]
        
        for model in working_models:
            if test_specific_model(model):
                break