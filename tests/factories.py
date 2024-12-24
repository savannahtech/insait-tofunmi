import factory
from app.models import QuestionAnswer
from datetime import datetime
from app import db

class QuestionAnswerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = QuestionAnswer
        sqlalchemy_session = db.session  # Use the SQLAlchemy session

    id = factory.Sequence(lambda n: n + 1)
    question = factory.Faker("sentence")
    answer = factory.Faker("paragraph")
    created_at = factory.LazyFunction(datetime.utcnow)

