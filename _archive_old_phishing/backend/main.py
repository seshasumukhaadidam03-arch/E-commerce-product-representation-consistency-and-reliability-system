import os
import sys
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

# Add root folder to python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.feature_extractor import PhishingFeatureExtractor

app = FastAPI(
    title="AI Phishing Detection & Prevention System API",
    description="Inference API to check if a website is a phishing attempt.",
    version="1.0.0"
)

# Enable CORS for Chrome Extension requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the chrome extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths for loading the serialized model
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.pkl")

# Shared feature extractor instance
extractor = PhishingFeatureExtractor(timeout=1.5)

model_data = None

def load_model():
    global model_data
    if os.path.exists(MODEL_PATH):
        try:
            model_data = joblib.load(MODEL_PATH)
            print(f"Successfully loaded trained model from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model from {MODEL_PATH}: {e}")
            model_data = None
    else:
        print(f"Model file not found at {MODEL_PATH}. Running in fallback heuristic mode.")

@app.on_event("startup")
def startup_event():
    load_model()

class URLCheckRequest(BaseModel):
    url: str

class URLCheckResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    method: str
    features: dict

def fallback_heuristics(url: str, features: dict) -> dict:
    """
    Fallback heuristic checker if the machine learning model is not yet trained.
    Returns simulated classification and confidence.
    """
    is_phishing = False
    confidence = 0.5
    reasons = []
    
    # 1. Suspicious keywords in domain
    if features.get('has_suspicious_keyword', 0) == 1:
        is_phishing = True
        confidence += 0.25
        reasons.append("suspicious_keyword")
        
    # 2. IP Address as domain name
    if features.get('is_ip', 0) == 1:
        is_phishing = True
        confidence += 0.3
        reasons.append("ip_in_domain")
        
    # 3. No SSL
    if features.get('is_ssl', 1) == 0:
        confidence += 0.15
        reasons.append("no_ssl")
        if confidence >= 0.7:
            is_phishing = True
            
    # 4. Too many subdomains
    if features.get('qty_subdomains', 0) > 3:
        confidence += 0.1
        reasons.append("excessive_subdomains")
        if confidence >= 0.7:
            is_phishing = True
            
    # Normalize confidence
    confidence = min(max(confidence, 0.5), 0.95)
    
    return {
        "is_phishing": is_phishing,
        "confidence": confidence,
        "method": f"heuristic_fallback({','.join(reasons) if reasons else 'safe'})"
    }

@app.post("/api/v1/check", response_model=URLCheckResponse)
async def check_url(payload: URLCheckRequest):
    url = payload.url
    
    # Extract features from the URL
    try:
        features = extractor.extract_all(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature extraction failed: {str(e)}")
        
    # Check if we should use the ML model or fallback heuristics
    global model_data
    if model_data is None:
        # Reload attempt in case it was trained since startup
        load_model()
        
    if model_data is not None:
        try:
            model = model_data['model']
            feature_cols = model_data['feature_cols']
            
            # Convert features dict to DataFrame with matching columns
            df_features = pd.DataFrame([features])
            
            # Fill missing columns with -1 and keep only the trained columns in correct order
            for col in feature_cols:
                if col not in df_features.columns:
                    df_features[col] = -1
            df_features = df_features[feature_cols]
            
            # Perform inference
            prediction = int(model.predict(df_features)[0])
            probabilities = model.predict_proba(df_features)[0]
            confidence = float(probabilities[prediction])
            
            return URLCheckResponse(
                url=url,
                is_phishing=prediction == 1,
                confidence=confidence,
                method="machine_learning",
                features=features
            )
        except Exception as e:
            print(f"Inference error: {e}. Falling back to heuristics.")
            
    # Fallback path if model not trained or fails
    heuristics_result = fallback_heuristics(url, features)
    return URLCheckResponse(
        url=url,
        is_phishing=heuristics_result['is_phishing'],
        confidence=heuristics_result['confidence'],
        method=heuristics_result['method'],
        features=features
    )

@app.get("/api/v1/status")
async def get_status():
    global model_data
    return {
        "status": "online",
        "model_loaded": model_data is not None,
        "model_file_exists": os.path.exists(MODEL_PATH)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
