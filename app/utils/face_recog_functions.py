import tempfile
import os
from deepface import DeepFace
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

model_name = "Facenet512"

# Load the DeepFace model once
try:
    deepface_model = DeepFace.build_model(model_name)
    logger.info(f"DeepFace model '{model_name}' loaded successfully.")
except Exception as e:
    logger.error(f"Error loading DeepFace model: {str(e)}")
    deepface_model = None

def find_face_in_image(file_stream: io.BytesIO, image_folder: str) -> str:
    if deepface_model is None:
        return "Error: DeepFace model is not loaded properly."
    
    temp_file_name = None
    try:
        # Create a temporary file to hold the in-memory image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file_name = temp_file.name
            
        # Save the in-memory file stream to the temporary file
        image = Image.open(file_stream)
        
        # Convert image to RGB if it is not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image.save(temp_file_name, format='JPEG')
        logger.debug(f"Image saved to temporary file: {temp_file_name}")
        
        # Use DeepFace to find the face in the temporary file
        logger.debug(f"Starting DeepFace.find with parameters: img_path={temp_file_name}, db_path={image_folder}, model_name={model_name}")
        dfs = DeepFace.find(img_path=temp_file_name, db_path=image_folder, model_name=model_name, detector_backend='retinaface', enforce_detection=False, align=True, normalization='base')
        
        if isinstance(dfs, list) and dfs:
            dfs = dfs[0]
        
        if not dfs.empty:
            if dfs['distance'].min() < 0.7:
                best_match_index = dfs['distance'].idxmin()
                best_match = dfs.loc[best_match_index]
                
                # Extract the ID from the file path
                detected_name = best_match['identity']
                # Extract the ID number (assuming it's the part before the file extension)
                id_number = os.path.basename(detected_name).split('.')[0]
                
                logger.info(f"Face detected with high confidence. ID: {id_number}")
                return id_number
            else:
                # Get the top 3 matches
                top_3_matches = dfs.nsmallest(3, 'distance')
                top_3_names = [
                    os.path.basename(match['identity']).split('.')[0] for _, match in top_3_matches.iterrows()
                ]
                logger.info(f"Face detected with low confidence. Top 3 matches: {', '.join(top_3_names)}")
                return ' '.join(top_3_names)
        else:
            logger.info("No face detected in the image")
            return None
    except Exception as e:
        logger.exception(f"Error processing image: {str(e)}")
        return f"Error processing image: {str(e)}"
    finally:
        # Clean up the temporary file
        if temp_file_name and os.path.exists(temp_file_name):
            os.remove(temp_file_name)
            logger.debug(f"Temporary file removed: {temp_file_name}")
