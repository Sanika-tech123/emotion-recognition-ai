import sys
import os
sys.path.append(os.getcwd())

try:
    print("Importing speech_model...")
    from backend.models.speech_model import speech_model
    print("Import successful.")
    
    if speech_model.model is None:
        print("ERROR: speech_model.model is None!")
    else:
        print("SUCCESS: speech_model.model is loaded.")
        
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
