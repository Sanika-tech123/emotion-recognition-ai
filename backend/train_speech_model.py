import os
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from models.speech_model import SpeechEmotionModel

# Configuration
DATASET_PATH = "datasets" # User should place RAVDESS/TESS here
MODEL_SAVE_PATH = "model_weights.h5"

def load_data(dataset_path):
    features = []
    labels = []
    
    print(f"Scanning {dataset_path} for audio files...")
    
    # Example logic for RAVDESS (Actor_01/03-01-01-01-01-01-01.wav)
    # Filename identifiers: Modality-Vocal-Emotion-Intensity-Statement-Repetition-Actor
    # Emotion: 01=neutral, 02=calm, 03=happy, 04=sad, 05=angry, 06=fearful, 07=disgust, 08=surprised
    
    emotion_map = {
        '01': 'neutral', '02': 'calm', '03': 'happy', '04': 'sad',
        '05': 'angry', '06': 'fearful', '07': 'disgust', '08': 'surprised'
    }

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                
                # Simple parsing logic for RAVDESS
                parts = file.split("-")
                if len(parts) == 7:
                    emotion_code = parts[2]
                    emotion = emotion_map.get(emotion_code)
                    if emotion:
                        # Extract features
                        try:
                            audio, sr = librosa.load(file_path, res_type='kaiser_fast')
                            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
                            mfccs_processed = np.mean(mfccs.T, axis=0)
                            
                            features.append(mfccs_processed)
                            labels.append(emotion)
                        except Exception as e:
                            print(f"Error processing {file}: {e}")

    return np.array(features), np.array(labels)

def train():
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset directory '{DATASET_PATH}' not found. Please create it and add RAVDESS/TESS datasets.")
        return

    X, y = load_data(DATASET_PATH)
    
    if len(X) == 0:
        print("No data found.")
        return

    print(f"Data loaded: {len(X)} samples")

    # Encode labels
    lb = LabelEncoder()
    y = to_categorical(lb.fit_transform(y))
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Reshape for CNN (Batch, Steps, Channels)
    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)
    
    # Initialize model
    speech_model = SpeechEmotionModel(model_path=None) # Don't load existing weights
    model = speech_model.model
    
    # Train
    print("Starting training...")
    model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test))
    
    # Save
    model.save_weights(MODEL_SAVE_PATH)
    print(f"Model weights saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()
