from typing import Optional
from ninja import Schema

class FaqSchema(Schema):
    id: int
    question: str
    answer: str


class FaqCreationSchema(Schema):
    question: str
    answer: str


class FaqUpdateSchema(Schema):
    question: Optional[str] = ''
    answer: Optional[str] = ''


class FaqDeleteSchema(Schema):
    is_deleted: bool