import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    is_dev = os.environ.get("ENVIRONMENT", "production").lower() == "development"
    print(f"🚀 Starting WordRhythm Server on port {port} (Dev mode: {is_dev})")
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=is_dev)
