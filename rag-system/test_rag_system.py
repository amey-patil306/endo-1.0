import requests
import json
import time

# API base URL
RAG_API_URL = "http://127.0.0.1:8001"
PREDICTION_API_URL = "http://127.0.0.1:8000"

def test_rag_health():
    """Test RAG API health check."""
    print("=== Testing RAG API Health ===")
    try:
        response = requests.get(f"{RAG_API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_explanation_generation():
    """Test explanation generation with various scenarios."""
    print("\n=== Testing Explanation Generation ===")
    
    test_cases = [
        {
            "name": "High Risk Case",
            "prediction": {
                "prediction": 1,
                "prediction_label": "Endometriosis",
                "confidence": 0.85,
                "probabilities": {
                    "no_endometriosis": 0.15,
                    "endometriosis": 0.85
                },
                "risk_level": "High"
            },
            "query": "I got an 85% probability result. What does this mean? Should I be worried?"
        },
        {
            "name": "Moderate Risk Case",
            "prediction": {
                "prediction": 0,
                "prediction_label": "No Endometriosis",
                "confidence": 0.55,
                "probabilities": {
                    "no_endometriosis": 0.55,
                    "endometriosis": 0.45
                },
                "risk_level": "Moderate"
            },
            "query": "My result shows 45% chance of endometriosis. What should I do next?"
        },
        {
            "name": "Low Risk Case",
            "prediction": {
                "prediction": 0,
                "prediction_label": "No Endometriosis",
                "confidence": 0.80,
                "probabilities": {
                    "no_endometriosis": 0.80,
                    "endometriosis": 0.20
                },
                "risk_level": "Low"
            },
            "query": "I have a low risk result but I'm still experiencing pain. What could this mean?"
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        
        request_data = {
            "user_query": case["query"],
            "prediction_result": case["prediction"],
            "use_fallback": False  # Try AI first, fallback if needed
        }
        
        try:
            response = requests.post(f"{RAG_API_URL}/explain", json=request_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Query: {case['query']}")
                print(f"Risk Level: {result['risk_level']}")
                print(f"Explanation: {result['explanation'][:200]}...")
                print(f"Number of Recommendations: {len(result['recommendations'])}")
                
                # Show top recommendations
                for i, rec in enumerate(result['recommendations'][:2]):
                    priority = rec.get('priority', 'normal')
                    print(f"  {i+1}. [{rec['category']}] {rec['action']} ({priority})")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Request failed: {e}")

def test_question_answering():
    """Test specific question answering."""
    print("\n=== Testing Question Answering ===")
    
    questions = [
        "What are the main symptoms of endometriosis?",
        "How is endometriosis diagnosed?",
        "What treatment options are available?",
        "Can endometriosis affect fertility?",
        "What lifestyle changes can help with symptoms?"
    ]
    
    sample_prediction = {
        "prediction": 1,
        "prediction_label": "Endometriosis",
        "confidence": 0.75,
        "probabilities": {
            "no_endometriosis": 0.25,
            "endometriosis": 0.75
        },
        "risk_level": "High"
    }
    
    for question in questions:
        print(f"\nQuestion: {question}")
        
        request_data = {
            "question": question,
            "prediction_result": sample_prediction
        }
        
        try:
            response = requests.post(f"{RAG_API_URL}/ask", json=request_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Answer: {result['answer'][:150]}...")
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Request failed: {e}")

def test_knowledge_search():
    """Test medical knowledge search."""
    print("\n=== Testing Knowledge Search ===")
    
    search_queries = [
        "endometriosis pain management",
        "fertility and endometriosis",
        "diagnosis process",
        "treatment options"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: {query}")
        
        try:
            response = requests.get(f"{RAG_API_URL}/search", params={"query": query, "limit": 2})
            
            if response.status_code == 200:
                result = response.json()
                print(f"Found {result['total_found']} results")
                
                for i, doc in enumerate(result['results']):
                    print(f"  {i+1}. Source: {doc['source']}")
                    print(f"     Content: {doc['content'][:100]}...")
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Search failed: {e}")

def test_integrated_workflow():
    """Test complete workflow: Prediction -> Explanation."""
    print("\n=== Testing Integrated Workflow ===")
    
    # Sample symptom data for prediction
    sample_symptoms = {
        "Irregular_Missed_periods": 1,
        "Cramping": 1,
        "Menstrual_clots": 1,
        "Pain_Chronic_pain": 1,
        "Extreme_Bloating": 1,
        "Depression": 1,
        "Ovarian_cysts": 1,
        "Painful_urination": 0,
        "Hip_pain": 1,
        "Migraines": 1,
        # Set remaining symptoms to 0
        "Infertility": 0,
        "Diarrhea": 0,
        "Long_menstruation": 0,
        "Vomiting_constant_vomiting": 0,
        "Leg_pain": 0,
        "Fertility_Issues": 0,
        "Pain_after_Intercourse": 0,
        "Digestive_GI_problems": 0,
        "Anaemia_Iron_deficiency": 0,
        "Vaginal_Pain_Pressure": 0,
        "Cysts_unspecified": 0,
        "Abnormal_uterine_bleeding": 0,
        "Hormonal_problems": 0,
        "Feeling_sick": 0,
        "Abdominal_Cramps_during_Intercourse": 0,
        "Insomnia_Sleeplessness": 0,
        "Loss_of_appetite": 0
    }
    
    try:
        # Step 1: Get prediction
        print("Step 1: Getting ML prediction...")
        pred_response = requests.post(f"{PREDICTION_API_URL}/predict", json=sample_symptoms)
        
        if pred_response.status_code != 200:
            print(f"Prediction API not available: {pred_response.status_code}")
            print("Using dummy prediction data...")
            prediction_result = {
                "prediction": 1,
                "prediction_label": "Endometriosis",
                "confidence": 0.82,
                "probabilities": {
                    "no_endometriosis": 0.18,
                    "endometriosis": 0.82
                },
                "risk_level": "High"
            }
        else:
            prediction_result = pred_response.json()
        
        print(f"Prediction: {prediction_result['prediction_label']} ({prediction_result['confidence']:.1%} confidence)")
        
        # Step 2: Generate explanation
        print("\nStep 2: Generating explanation...")
        user_query = "I just got my results and I'm scared. Can you explain what this means and what I should do?"
        
        explanation_request = {
            "user_query": user_query,
            "prediction_result": prediction_result,
            "use_fallback": False
        }
        
        exp_response = requests.post(f"{RAG_API_URL}/explain", json=explanation_request)
        
        if exp_response.status_code == 200:
            explanation = exp_response.json()
            
            print(f"\nUser Query: {user_query}")
            print(f"Risk Level: {explanation['risk_level']}")
            print(f"\nExplanation:\n{explanation['explanation']}")
            print(f"\nKey Recommendations:")
            
            for rec in explanation['recommendations'][:3]:
                priority = rec.get('priority', 'normal')
                print(f"- [{rec['category']}] {rec['action']} ({priority})")
                print(f"  {rec['description']}")
        else:
            print(f"Explanation generation failed: {exp_response.status_code}")
            
    except Exception as e:
        print(f"Integrated workflow test failed: {e}")

def test_fallback_responses():
    """Test fallback responses when AI is unavailable."""
    print("\n=== Testing Fallback Responses ===")
    
    test_prediction = {
        "prediction": 1,
        "prediction_label": "Endometriosis",
        "confidence": 0.75,
        "probabilities": {
            "no_endometriosis": 0.25,
            "endometriosis": 0.75
        },
        "risk_level": "High"
    }
    
    request_data = {
        "user_query": "What does my high risk result mean?",
        "prediction_result": test_prediction,
        "use_fallback": True  # Force fallback response
    }
    
    try:
        response = requests.post(f"{RAG_API_URL}/explain", json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            print("Fallback response generated successfully:")
            print(f"Explanation: {result['explanation'][:200]}...")
            print(f"Recommendations: {len(result['recommendations'])} items")
        else:
            print(f"Fallback test failed: {response.status_code}")
            
    except Exception as e:
        print(f"Fallback test error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Endometriosis RAG Explanation System")
    print("=" * 60)
    
    # Test health first
    if not test_rag_health():
        print("❌ RAG API is not healthy. Make sure it's running:")
        print("   python rag-system/rag_api.py")
        exit(1)
    
    # Run all tests
    test_explanation_generation()
    test_question_answering()
    test_knowledge_search()
    test_fallback_responses()
    test_integrated_workflow()
    
    print("\n✅ All RAG system tests completed!")
    print("\n📋 Next Steps:")
    print("1. Integrate RAG API with your React frontend")
    print("2. Add explanation component to display results")
    print("3. Test with real user data")
    print("4. Deploy both prediction and explanation APIs")