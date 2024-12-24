from app import db
from app.models import QuestionAnswer
from sqlalchemy import desc
from flask import current_app



def save_question_answer(question, answer):
    qa = QuestionAnswer(question=question, answer=answer)
    db.session.add(qa)
    db.session.commit()
    return qa


def get_all_questions(page=1, per_page=10):
    pagination = QuestionAnswer.query\
        .order_by(desc(QuestionAnswer.created_at))\
        .paginate(page=page, per_page=per_page)
    
    return pagination.items, pagination.total
