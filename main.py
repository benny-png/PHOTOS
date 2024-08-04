from fastapi import FastAPI
from app.routes.all_routes import face_recog_router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

app.include_router(face_recog_router)

@app.on_event("startup")
async def startup_event():
    from app.database.database import Base
    Base.metadata.create_all(bind=engine)
