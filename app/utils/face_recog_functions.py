import tempfile
import os
from deepface import DeepFace
from PIL import Image
import io

model_name = "Facenet512"

# Load the DeepFace model once
deepface_model = DeepFace.build_model(model_name)  # Build model only once


def find_face_in_image(file_stream: io.BytesIO, image_folder: str) -> str:
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
        
        # Use DeepFace to find the face in the temporary file
        dfs = DeepFace.find(img_path=temp_file_name, db_path=image_folder, model_name=model_name, detector_backend='retinaface', refresh_database=False, distance_metric='euclidean_l2')
        
        # Clean up the temporary file
        os.remove(temp_file_name)
        
        if isinstance(dfs, list) and dfs:
            dfs = dfs[0]
            
        print(dfs)
        
        if not dfs.empty:
            if dfs['distance'].min() < 0.7:
                
                best_match_index = dfs['distance'].idxmin()
                best_match = dfs.loc[best_match_index]
                
                # Extract the ID from the file path
                detected_name = best_match['identity']
                # Extract the ID number (assuming it's the part before the file extension)
                id_number = os.path.basename(detected_name).split('.')[0]  # Adjust this line if needed
                
                return id_number
            
            else:
                # Get the top 3 matches
                top_3_matches = dfs.nsmallest(3, 'distance')
                top_3_names = [
                    os.path.basename(match['identity']).split('.')[0] for _, match in top_3_matches.iterrows()
                ]
                return ' '.join(top_3_names)
        else:
            # No face detected in the image
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None
