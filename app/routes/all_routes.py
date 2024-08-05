from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.face_recog_functions import find_face_in_image
from app.database.database import get_db, FaceRecognitionResult
from io import BytesIO

face_recog_router = APIRouter()

@face_recog_router.post("/recognize-face/")
async def recognize_face(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read the file into memory
        file_content = await file.read()
        file_stream = BytesIO(file_content)
        
        # Use the original filename for `image_path`
        image_path = file.filename

        # Process the file in-memory
        detected_name = find_face_in_image(file_stream, "app/files/downloaded_images_2023")
        
        if detected_name is None:
            return {"not_found": "Face not found 🔍. Please ensure the image has a clear view of the face."}
        
        if "Error" in detected_name:
            # If there is an error message returned from find_face_in_image, raise an HTTP exception
            raise HTTPException(status_code=500, detail=detected_name)
        
        detected_names = detected_name.split()
        
        if len(detected_names) == 1:
            # Save result to database with the original filename as image_path
            result = FaceRecognitionResult(image_path=image_path, detected_name=detected_name)
            db.add(result)
            db.commit()
            db.refresh(result)
            return {"detected_name": detected_name}
        
        if len(detected_names) > 1:
            return {
                "low_confidence": "Low confidence in recognition. Top matches are:",
                "detected_names": detected_names
            }

    except Exception as e:
        # Handle exceptions and return error response
        raise HTTPException(status_code=500, detail=f"500: {str(e)}")
