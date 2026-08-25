import os
import sys

# Add the apps/backend directory to the path so modules resolve correctly
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "apps", "backend"))

# Load the FastAPI app
from main import app
