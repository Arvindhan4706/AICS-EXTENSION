from apps.ml_engine.predict import analyze_target_url
import json

try:
    res = analyze_target_url('http://localhost:3005/')
    print(json.dumps(res, indent=2))
except Exception as e:
    print('ERROR:', str(e))
