import os
import joblib
import sys

# Add the project root to sys.path so we can import apps
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps.ml_engine.models.ensemble import CyberShieldEnsemble

def pretrain():
    print("Initializing ensemble model...")
    model = CyberShieldEnsemble()
    
    print("Training models on local datasets...")
    model.train_on_dataset()
    
    print("Models trained successfully. Saving to disk...")
    # Ensure directory exists
    os.makedirs('apps/ml_engine/models/pretrained', exist_ok=True)
    
    joblib.dump(model.rf_model, 'apps/ml_engine/models/pretrained/rf_model.pkl')
    joblib.dump(model.gb_model, 'apps/ml_engine/models/pretrained/gb_model.pkl')
    joblib.dump(model.dt_model, 'apps/ml_engine/models/pretrained/dt_model.pkl')
    
    print("Pre-training complete! Models saved to apps/ml_engine/models/pretrained/")

if __name__ == '__main__':
    pretrain()
