"""
Skepesis Application Runner
"""
import uvicorn

if __name__ == "__main__":
    # Run the application
    print("\n🚀 Starting Skepesis...")
    print("📍 Access the app at: http://127.0.0.1:8080")
    print("📊 API docs at: http://127.0.0.1:8080/docs\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
