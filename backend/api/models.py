from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.expression import text
from zoneinfo import ZoneInfo

from .database import Base

tz = ZoneInfo("Africa/Accra")

class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, nullable=False)
    system = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
    response_time = Column(Float, nullable=False)
    relevance = Column(String, nullable=False)
    system_tokens = Column(Integer, nullable=False)
    completion_tokens = Column(Integer, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    eval_prompt_tokens = Column(Integer, nullable=False)
    eval_completion_tokens = Column(Integer, nullable=False)
    eval_total_tokens = Column(Integer, nullable=False)
    openai_cost = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    feedbacks = relationship("Feedbacks", back_populates="conversation", cascade="all, delete-orphan")


class Feedbacks(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"))
    feedback = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    conversation = relationship("Conversations", back_populates="feedbacks")


