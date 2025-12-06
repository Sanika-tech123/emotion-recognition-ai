"""
Emotion Recognition Model Evaluation Script
Tests model accuracy, precision, recall, and generates confusion matrix
"""

import requests
import json
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

API_URL = "http://localhost:8000"

# Test samples with ground truth labels
TEXT_TEST_DATA = [
    # Happiness
    ("I'm so happy and excited about this!", "Happiness"),
    ("This is absolutely wonderful!", "Happiness"),
    ("I love this so much!", "Happiness"),
    ("Best day ever!", "Happiness"),
    
    # Sadness
    ("I'm so sad and depressed", "Sadness"),
    ("This makes me feel terrible", "Sadness"),
    ("I can't stop crying", "Sadness"),
    
    # Anger
    ("This makes me so angry!", "Anger"),
    ("I'm furious about this!", "Anger"),
    ("Why don't you just listen to me?!", "Anger"),
    ("This is absolutely infuriating!", "Anger"),
    
    # Fear
    ("I'm terrified of what might happen", "Fear"),
    ("This scares me so much", "Fear"),
    ("I'm really afraid", "Fear"),
    
    # Surprise
    ("Wow, I didn't expect that!", "Surprise"),
    ("That's so surprising!", "Surprise"),
    ("I can't believe it!", "Surprise"),
    
    # Neutral
    ("The meeting is at 3pm", "Neutral"),
    ("I went to the store", "Neutral"),
    ("It is what it is", "Neutral"),
    
    # Disgust
    ("That's absolutely disgusting", "Disgust"),
    ("This is revolting", "Disgust"),
]

def test_text_model():
    """Test text emotion recognition model"""
    print("=" * 60)
    print("TEXT MODEL EVALUATION")
    print("=" * 60)
    
    true_labels = []
    predicted_labels = []
    
    for text, true_emotion in TEXT_TEST_DATA:
        try:
            response = requests.post(
                f"{API_URL}/predict/text",
                json={"text": text},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()["data"]
                predicted = data["label"]
                confidence = data["score"]
                
                true_labels.append(true_emotion)
                predicted_labels.append(predicted)
                
                match = "✓" if predicted == true_emotion else "✗"
                print(f"{match} Text: '{text[:50]}...'")
                print(f"  True: {true_emotion} | Predicted: {predicted} ({confidence*100:.1f}%)")
            else:
                print(f"✗ Error: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Connection Error: {e}")
    
    # Calculate metrics
    if true_labels and predicted_labels:
        accuracy = accuracy_score(true_labels, predicted_labels)
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels, predicted_labels, average='weighted', zero_division=0
        )
        
        print("\n" + "=" * 60)
        print("TEXT MODEL METRICS")
        print("=" * 60)
        print(f"Accuracy:  {accuracy*100:.2f}%")
        print(f"Precision: {precision*100:.2f}%")
        print(f"Recall:    {recall*100:.2f}%")
        print(f"F1 Score:  {f1*100:.2f}%")
        
        # Confusion Matrix
        unique_labels = sorted(list(set(true_labels + predicted_labels)))
        cm = confusion_matrix(true_labels, predicted_labels, labels=unique_labels)
        
        print("\nConfusion Matrix:")
        plot_confusion_matrix(cm, unique_labels, "Text Model Confusion Matrix")
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
    
    return None

def plot_confusion_matrix(cm, labels, title):
    """Generate and save confusion matrix visualization"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    filename = title.lower().replace(" ", "_") + ".png"
    plt.savefig(filename)
    print(f"✓ Saved confusion matrix to {filename}")
    plt.close()

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API is running and healthy")
            return True
        else:
            print("✗ API returned error")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to API: {e}")
        print(f"  Make sure backend is running at {API_URL}")
        return False

def main():
    """Run all evaluation tests"""
    print("\n" + "=" * 60)
    print("EMOTION RECOGNITION MODEL EVALUATION")
    print("=" * 60 + "\n")
    
    # Check API health
    if not test_api_health():
        print("\nPlease start the backend server first:")
        print("  cd backend")
        print("  uvicorn main:app --host 0.0.0.0 --port 8000")
        return
    
    print()
    
    # Test text model
    text_metrics = test_text_model()
    
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)
    
    if text_metrics:
        print("\n📊 Summary:")
        print(f"  Text Model Accuracy: {text_metrics['accuracy']*100:.1f}%")
        print(f"  Text Model F1 Score: {text_metrics['f1']*100:.1f}%")
        print("\n✓ Check generated confusion matrix images for detailed analysis")

if __name__ == "__main__":
    main()
