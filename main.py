from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="نظام RAG للبحث الدلالي",
    description="نظام للتعامل مع المستندات وإجراء بحث دلالي باستخدام تقنيات Langchain",
    version="0.2.0",
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تحديد النطاقات المسموح بها هنا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "مرحبًا بك في نظام RAG للبحث الدلالي"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": app.version}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)