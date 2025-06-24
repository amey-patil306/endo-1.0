# Endometriosis RAG Explanation System - Phase 3

A Retrieval-Augmented Generation (RAG) system that provides clear, empathetic explanations of endometriosis ML predictions using medical knowledge and the Llama API.

## 🎯 Overview

This system combines:
- **Vector Database**: Medical knowledge stored in ChromaDB with semantic search
- **LLM Integration**: Llama 2 via Hugging Face API for natural language generation
- **RAG Pipeline**: Retrieves relevant medical context and generates personalized explanations
- **Fallback System**: Provides structured responses when AI is unavailable

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd rag-system
pip install -r requirements.txt
```

### 2. Initialize Vector Store

```bash
python vector_store.py
```

This will:
- Load medical documents from `medical_knowledge/` folder
- Create embeddings using sentence-transformers
- Store in ChromaDB for fast retrieval

### 3. Run the RAG API

```bash
python rag_api.py
```

The RAG API will be available at: `http://localhost:8001`

### 4. Test the System

```bash
python test_rag_system.py
```

## 📚 System Architecture

```
User Query + ML Prediction
           ↓
    [Vector Search] → Medical Knowledge Base
           ↓
    [Context Retrieval] → Relevant Medical Info
           ↓
    [Prompt Construction] → Combine Query + Prediction + Context
           ↓
    [Llama API] → Generate Explanation
           ↓
    [Response Formatting] → Structured Output
```

## 🔧 API Endpoints

### Core Endpoints

- **POST** `/explain` - Generate comprehensive explanations
- **POST** `/ask` - Answer specific questions
- **GET** `/search` - Search medical knowledge base
- **GET** `/recommendations/{risk_level}` - Get structured recommendations

### Health & Testing

- **GET** `/health` - System health check
- **POST** `/test-explanation` - Test with dummy data

## 📊 Usage Examples

### Generate Explanation

```bash
curl -X POST "http://localhost:8001/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What does my 78% probability mean?",
    "prediction_result": {
      "prediction": 1,
      "prediction_label": "Endometriosis",
      "confidence": 0.78,
      "probabilities": {
        "no_endometriosis": 0.22,
        "endometriosis": 0.78
      },
      "risk_level": "High"
    },
    "use_fallback": false
  }'
```

### Ask Specific Question

```bash
curl -X POST "http://localhost:8001/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the treatment options for endometriosis?",
    "prediction_result": {
      "prediction": 1,
      "prediction_label": "Endometriosis",
      "confidence": 0.75,
      "probabilities": {
        "no_endometriosis": 0.25,
        "endometriosis": 0.75
      },
      "risk_level": "High"
    }
  }'
```

## 🧠 Medical Knowledge Base

The system includes comprehensive medical information:

### Documents Included:
- **endometriosis_overview.txt**: General medical information
- **symptom_explanations.txt**: Detailed symptom descriptions
- **prediction_interpretation.txt**: How to understand ML results
- **support_resources.txt**: Resources and next steps

### Knowledge Categories:
- Symptoms and their medical explanations
- Diagnosis processes and procedures
- Treatment options and management
- Support resources and lifestyle advice
- Risk interpretation and next steps

## 🤖 LLM Integration

### Llama API Configuration
- **Model**: meta-llama/Llama-2-7b-chat-hf
- **API**: Hugging Face Inference API
- **Token**: `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`

### Prompt Engineering
The system uses carefully crafted prompts that:
- Combine user queries with medical context
- Include prediction results and risk levels
- Generate empathetic, non-alarming responses
- Provide actionable next steps

### Fallback System
When the LLM API is unavailable:
- Pre-written, medically-reviewed responses
- Risk-level specific recommendations
- Structured guidance based on prediction results

## 📱 Frontend Integration

### React Component Example

```javascript
const ExplanationComponent = ({ predictionResult, userQuery }) => {
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);

  const getExplanation = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_query: userQuery,
          prediction_result: predictionResult,
          use_fallback: false
        })
      });
      
      const result = await response.json();
      setExplanation(result);
    } catch (error) {
      console.error('Error getting explanation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="explanation-container">
      {loading ? (
        <div>Generating explanation...</div>
      ) : explanation ? (
        <div>
          <h3>Understanding Your Results</h3>
          <p>{explanation.explanation}</p>
          
          <h4>Recommendations</h4>
          <ul>
            {explanation.recommendations.map((rec, index) => (
              <li key={index}>
                <strong>[{rec.category}]</strong> {rec.action}
                <p>{rec.description}</p>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <button onClick={getExplanation}>Get Explanation</button>
      )}
    </div>
  );
};
```

## 🔒 Security & Privacy

### Data Handling
- No personal health data is stored permanently
- Queries are processed in real-time
- Medical context is retrieved from curated sources
- API responses don't include sensitive information

### API Security
- CORS configured for frontend domains
- Rate limiting recommended for production
- Input validation and sanitization
- Error handling without exposing system details

## 🚀 Deployment Options

### Option 1: Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python vector_store.py  # Initialize vector store

EXPOSE 8001
CMD ["uvicorn", "rag_api:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Option 2: Cloud Deployment

**Render/Railway/Fly.io:**
1. Push code to GitHub
2. Set environment variables
3. Configure build: `pip install -r requirements.txt && python vector_store.py`
4. Set start command: `uvicorn rag_api:app --host 0.0.0.0 --port $PORT`

## 📈 Performance Optimization

### Vector Store Optimization
- Chunk size: 500 characters with 50 overlap
- Embedding model: all-MiniLM-L6-v2 (fast, good quality)
- ChromaDB persistence for fast startup

### LLM Optimization
- Temperature: 0.7 for balanced creativity/accuracy
- Max tokens: 400 for concise responses
- Timeout: 30 seconds with fallback

### Caching Strategy
- Vector search results cached per session
- Common questions pre-computed
- Fallback responses for instant delivery

## 🧪 Testing & Validation

### Automated Tests
- Health checks for all components
- End-to-end workflow testing
- Fallback system validation
- Medical accuracy verification

### Manual Testing Scenarios
- High/moderate/low risk predictions
- Various user query types
- Edge cases and error conditions
- Response quality and empathy

## 📞 Troubleshooting

### Common Issues

**Vector Store Not Loading**
```bash
# Reinitialize vector store
python vector_store.py
```

**LLM API Errors**
- Check Hugging Face API token
- Verify model availability
- Test with fallback responses

**Slow Response Times**
- Check vector store performance
- Monitor API response times
- Consider caching strategies

### Debug Mode
```bash
# Run with debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" rag_api.py
```

## 🔮 Future Enhancements

### Planned Features
- Multi-language support
- Personalized recommendations based on user history
- Integration with medical databases
- Voice-based interaction
- Mobile app integration

### Advanced RAG Features
- Multi-modal inputs (images, voice)
- Temporal reasoning for symptom progression
- Integration with wearable device data
- Collaborative filtering for similar cases

## 📋 Integration Checklist

- [ ] RAG API running and healthy
- [ ] Vector store initialized with medical knowledge
- [ ] LLM API token configured
- [ ] Frontend integration completed
- [ ] Error handling implemented
- [ ] User testing conducted
- [ ] Medical review completed
- [ ] Deployment configured
- [ ] Monitoring set up
- [ ] Documentation updated

## 🎯 Success Metrics

- **User Engagement**: Time spent reading explanations
- **Clarity**: User feedback on explanation quality
- **Actionability**: Users following recommendations
- **Medical Accuracy**: Healthcare provider validation
- **System Performance**: Response times and availability

---

This RAG system transforms complex ML predictions into clear, actionable guidance, helping users understand their health data and make informed decisions about seeking medical care.