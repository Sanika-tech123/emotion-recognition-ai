from transformers import pipeline

def debug_text():
    model_name = "SamLowe/roberta-base-go_emotions"
    print(f"Loading {model_name}...")
    classifier = pipeline("text-classification", model=model_name, top_k=None)
    
    text = "Why don’t you just listen to me for once?!"
    print(f"\nAnalyzing: '{text}'")
    
    results = classifier(text)[0]
    
    print("\nRaw Scores:")
    for res in sorted(results, key=lambda x: x['score'], reverse=True):
        print(f"{res['label']}: {res['score']:.4f}")

if __name__ == "__main__":
    debug_text()
