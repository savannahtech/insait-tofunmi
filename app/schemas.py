from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The question to be answered"
    )

    @property
    def truncated_question(self) -> str:
        """Returns a truncated version of the question for logging"""
        return self.question[:50] + "..." if len(self.question) > 50 else self.question



class QuestionResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 10

class ErrorResponse(BaseModel):
    error: str
    details: str



class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse] = Field(..., description="List of questions and answers")
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")

