from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import shutil
import os
from models.text_model import text_model
from models.speech_model import speech_model

app = FastAPI(title="AI Emotion Recognition API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v) > 5000:
            raise ValueError('Text too long (max 5000 characters)')
        return v.strip()

@app.get("/")
async def root():
    return {"message": "AI Emotion Recognition API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models": {
            "text": "loaded" if text_model.classifier else "error",
            "speech": "loaded" if speech_model.model else "error"
        }
    }

@app.post("/predict/text")
async def predict_text(request: TextRequest):
    """Predict emotion from text"""
    try:
        result = text_model.predict(request.text)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return {"status": "success", "data": result}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Text prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/audio")
async def predict_audio(file: UploadFile = File(...)):
    """Predict emotion from audio file"""
    temp_file = None
    
    try:
        # Validate file type
        if not file.filename.endswith('.wav'):
            raise HTTPException(
                status_code=400, 
                detail="Only .wav files are supported. Please convert your audio to WAV format."
            )
        
        # Validate file size (max 50MB)
        if file.size and file.size > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 50MB)")
        
        temp_file = f"temp_{file.filename}"
        
        print(f"Received audio file: {file.filename}, Content-Type: {file.content_type}")
        
        # Save uploaded file
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate file exists and has content
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Predict
        result = speech_model.predict(temp_file)
        
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
             
        return {"status": "success", "data": result}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up on error
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        
        print(f"Audio prediction error: {e}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500, 
            detail=f"Audio processing failed: {str(e)}"
        )
