from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_input = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def save_transcript(session_id, user_input, bot_response):
    db = SessionLocal()
    transcript = Transcript(session_id=session_id, user_input=user_input, bot_response=bot_response)
    db.add(transcript)
    db.commit()
    db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
