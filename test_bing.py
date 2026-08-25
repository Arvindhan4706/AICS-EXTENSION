from apps.ml_engine.predict import analyze_target_url
import json

try:
    res = analyze_target_url('https://www.bing.com/search?q=google')
    print(json.dumps(res, indent=2))
except Exception as e:
    import traceback
    traceback.print_exc()
