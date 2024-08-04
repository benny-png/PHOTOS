from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

class FaceRecognitionResult(Base):
    __tablename__ = "face_recognition_results"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)
    detected_name = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
