import os
from deepface import DeepFace
import pandas as pd

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]

print(models[2])


def find_face_in_image(target_image, image_folder, result_file):
    # Ensure the result file is empty or create it if it doesn't exist
    with open(result_file, 'w') as f:
        f.write('')

    try:
        # Perform face recognition
        
        dfs = DeepFace.find(img_path=target_image, db_path=image_folder, model_name = models[2], detector_backend='retinaface')
        if not dfs.empty:
            # Save results to a file
            with open(result_file, 'a') as f:
                f.write(f"Matches for {target_image}:\n")
                f.write(f"{dfs}\n\n")

        print(f"Face recognition completed. Results saved to {result_file}")
    except Exception as e:
        print(f"Error processing {target_image}: {e}")

if __name__ == "__main__":
    target_image = "find.jpg"  # Path to the specific image you want to recognize
    image_folder = "downloaded_images_2023"  # Folder where your images are stored
    result_file = "face_recognition_results.txt"  # File to save the results

    find_face_in_image(target_image, image_folder, result_file)
