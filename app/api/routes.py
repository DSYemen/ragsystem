from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.loaders.file_loader import load_and_process_file, is_supported_file
from app.loaders.web_loader import load_from_url
from app.database.vector_store import add_to_vector_store, search_vector_store
from app.processors.text_processor import process_query
from app.config import settings
from typing import List
import aiohttp
from app.utils.logging import logger
from app.utils.error_handling import handle_exceptions
from app.utils.rate_limiter import rate_limiter



router = APIRouter()

@router.post("/upload")
@handle_exceptions
async def upload_file(file: UploadFile = File(...)):
    if not is_supported_file(file.filename):
        logger.warning(f"محاولة تحميل ملف غير مدعوم: {file.filename}")
        raise HTTPException(status_code=400, detail="نوع الملف غير مدعوم")
    
    content = await file.read()
    documents = load_and_process_file(content, file.filename)
    add_to_vector_store(documents)
    logger.info(f"تمت معالجة وإضافة الملف: {file.filename}")
    return {"message": "تمت معالجة الملف وإضافته إلى قاعدة البيانات المتجهية"}


@router.post("/load-from-url")
async def load_url(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="فشل في تحميل المحتوى من الرابط")
                content = await response.text()
        documents = load_from_url(url)
        add_to_vector_store(documents)
        return {"message": "تم تحميل المحتوى من الرابط ومعالجته وإضافته إلى قاعدة البيانات المتجهية"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search")
async def search(query: str, k: int = Query(5, ge=1, le=20)):
    try:
        results = search_vector_store(query, k=k)
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
@handle_exceptions
async def query(query: str):
    rate_limiter()
    result = process_query(query)
    logger.info(f"تم معالجة الاستعلام: {query[:50]}...")
    return {"result": result}