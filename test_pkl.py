from deepface import DeepFace

model_path = "/root/PHOTOS/app/files/downloaded_images_2023/ds_model_facenet512_detector_retinaface_aligned_normalization_base_expand_0.pkl"

try:
    model = DeepFace.build_model('Facenet512')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
