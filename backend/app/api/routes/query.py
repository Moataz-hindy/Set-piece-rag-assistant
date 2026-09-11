from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from app.schemas.query import QueryResponse
from app.services.retrieval import retrieval_service
from app.services.generation import generation_service
from app.services.vision import analyze_tactical_geometry
import shutil
import tempfile

router = APIRouter()

# Note: Since the real YOLOv8 requires heavy dependencies (ultralytics, torch, cv2)
# we are simulating the YOLO extraction part here to keep the demo clean.
# In a real environment, you would run model.predict(image_path) here.

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    question: str = Form(...),
    image: UploadFile = File(None)
):
    vision_context = ""
    
    if image:
        # Mocking YOLOv8 detection logic for demonstration
        # We would normally save the image, pass it to YOLOv8, and get the boxes.
        # Here we just use our mock results from the vision service.
        mock_results = [
            {"class": "ball", "box": (100, 100, 20, 20)}, 
            {"class": "player", "box": (120, 110, 50, 150)}, 
            {"class": "player", "box": (80, 90, 50, 150)}, 
            {"class": "goalkeeper", "box": (900, 500, 60, 160)}, 
            {"class": "player", "box": (880, 480, 50, 150)}, 
            {"class": "player", "box": (920, 490, 50, 150)}, 
        ]
        vision_context = analyze_tactical_geometry(mock_results)

    try:
        # 1. Retrieve
        docs = retrieval_service.retrieve(question)
        
        # 2. Generate
        answer, sources = generation_service.generate_answer(
            question=question, 
            docs=docs, 
            vision_context=vision_context
        )
        
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}
