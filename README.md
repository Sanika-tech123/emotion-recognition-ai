# AI-Powered Real-Time Speech & Text Emotion Recognition System

## Overview
This project is a full-stack AI application that detects emotions from:
- **Text**: Using RoBERTa (Go Emotions) - 28 emotion categories
- **Speech**: Using Wav2Vec2 - 8 emotion categories

Both models map to **10 target emotions**: Happiness, Sadness, Anger, Fear, Surprise, Disgust, Neutral, Love/Affection, Confusion, and Stress/Anxiety.

The system features a professional **Streamlit** frontend with animated gradients and glassmorphism design, backed by a robust **FastAPI** backend.

## Features
- **Real-time Text Analysis**: Detects emotions from natural language
- **Real-time Speech Analysis**: Record your voice or upload `.wav` files
- **Automatic Emotion Mapping**: Maps 28 text + 8 speech emotions to 10 categories
- **Auto Neutral Filtering**: Automatically suppresses neutral bias
- **Interactive Visualizations**: Radar charts and confidence metrics
- **Professional UI**: Animated gradient background with glassmorphism effects

## Model Performance

### Accuracy Metrics
- **Text Model**: ~70% accuracy on 10-emotion classification
  - Base Model: `SamLowe/roberta-base-go_emotions` (28 classes)
  - Mapped to 10 target emotions
- **Speech Model**: ~75% accuracy on 10-emotion classification
  - Base Model: `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition` (8 classes)
  - Mapped to 10 target emotions

### Important Notes
- Emotion recognition is inherently subjective
- State-of-the-art research typically achieves 60-80% accuracy on multi-class emotion tasks
- These models are **pre-trained** and do not require custom training
- For higher accuracy (90%+), fine-tuning on domain-specific data would be required

### Testing Accuracy
Run the evaluation script to measure performance:
```bash
python test_accuracy.py
```
This generates:
- Accuracy, Precision, Recall, F1 scores
- Confusion matrix visualization
- Performance breakdown by emotion

## Prerequisites
- Python 3.8+
- Internet connection (for downloading models on first run)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Start the Backend
```bash
cd backend
# Windows (PowerShell)
$env:TF_USE_LEGACY_KERAS=1; uvicorn main:app --host 0.0.0.0 --port 8000

# Linux/Mac
export TF_USE_LEGACY_KERAS=1 && uvicorn main:app --host 0.0.0.0 --port 8000
```
*The API will start at `http://127.0.0.1:8000`*

> **Note**: First run downloads models (~1GB total). Wait for "Application startup complete".

### 3. Start the Frontend
Open a **new** terminal:
```bash
streamlit run frontend/streamlit_app.py
```
*Opens automatically at `http://localhost:8501`*

## Architecture
- **Backend**: FastAPI, PyTorch, Transformers (HuggingFace), Librosa, SoundFile
- **Frontend**: Streamlit, Plotly, Streamlit-Audiorec
- **Models**:
  - Text: `SamLowe/roberta-base-go_emotions`
  - Speech: `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition`

## Project Structure
```
project2/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── models/
│       ├── text_model.py       # RoBERTa text classifier
│       └── speech_model.py     # Wav2Vec2 speech classifier
├── frontend/
│   └── streamlit_app.py        # Streamlit UI
└── test_accuracy.py            # Model evaluation script
```

## Usage Examples

### Text Analysis
```python
# Send request to API
response = requests.post(
    "http://localhost:8000/predict/text",
    json={"text": "I'm so happy and excited!"}
)
# Returns: {"label": "Happiness", "score": 0.92, "all_scores": {...}}
```

### Audio Analysis
Upload `.wav` file or record directly in the UI. The system automatically:
1. Converts to mono if stereo
2. Resamples to 16kHz
3. Normalizes amplitude
4. Predicts emotion

## Troubleshooting
- **Connection Error**: Ensure backend is running on port 8000
- **Slow Processing**: First prediction loads models into memory (~5s), subsequent predictions are fast
- **Audio Errors**: Use `.wav` format, 16kHz recommended
- **Import Errors**: Run `pip install -r backend/requirements.txt`

## Limitations
1. **Subjective Nature**: Emotions are inherently subjective and context-dependent
2. **Sarcasm/Irony**: Models may misinterpret sarcastic or ironic text
3. **Background Noise**: Speech model performance degrades with noisy audio
4. **Cultural Differences**: Models trained primarily on English data
5. **Missing Emotions**: Some emotions (Love, Confusion, Stress) have limited representation in speech model

## Future Improvements
- Fine-tune models on custom labeled data
- Add multilingual support
- Implement ensemble methods for higher accuracy
- Add real-time streaming audio analysis
- Support more audio formats (mp3, m4a, etc.)
cd C:\Users\Shree\Desktop\project2\backend
$env:TF_USE_LEGACY_KERAS=1; uvicorn main:app --host 0.0.0.0 --port 8000
## License
This project uses pre-trained models from HuggingFace under their respective licenses.

## How to Run test_accuracy.py


Application startup complete
Uvicorn running on http://0.0.0.0:8000

# Navigate to project
cd C:\Users\Shree\Desktop\project2
python test_accuracy.py


# Navigate to project root
cd C:\Users\Shree\Desktop\project2

# Start Streamlit
streamlit run frontend/streamlit_app.py
