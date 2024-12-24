import pytest
from unittest.mock import patch, MagicMock
from tests.factories import QuestionAnswerFactory
from app import create_app, db
from app.models import QuestionAnswer

from unittest.mock import patch, Mock
from openai import (
    OpenAIError,
    APIError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    InternalServerError,
)
from app.services.openai_service import get_openai_answer

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["OPENAI_API_KEY"] = "test-key"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        
    # Cleanup
    # with app.app_context():
    #     db.drop_all()


def test_ask_endpoint_success(client, mocker):
    """Test the /ask endpoint for a successful response."""
    mock_response = {
        "choices": [
            {"message": {"content": "Mocked Answer"}}
        ]
    }
    mocker.patch(
        'openai.ChatCompletion.create',
        return_value=mock_response
    )
    
    response = client.post('/api/v1/ask', json={'question': 'What is Flask?'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['question'] == 'What is Flask?'
    

def test_ask_endpoint_validation_error(client):
    """Test the /ask endpoint with missing question."""
    response = client.post('/api/v1/ask', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid input data' in data['details']


def test_ask_endpoint_openai_error(client, mocker):
    """Test the /ask endpoint when OpenAI service fails."""
    mocker.patch(
        'openai.ChatCompletion.create',
        side_effect=Exception("OpenAI service error")
    )
    
    response = client.post('/api/v1/ask', json={'question': 'x' * 50000})
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'String should have at most 500 characters' in str(data['details'])


def test_ask_endpoint_db(client, mocker):
    """Test the /ask endpoint when database save succeds."""
    mock_response = {
        "choices": [
            {"message": {"content": "Mocked Answer"}}
        ]
    }
    mocker.patch(
        'openai.ChatCompletion.create',
        return_value=mock_response
    )
    
    mocker.patch(
        'app.dal.question_dal.save_question_answer',
        return_value=None
    )
    
    response = client.post('/api/v1/ask', json={'question': 'What is Flask?'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'error' not in data
    answer = data['answer']
    db_record = QuestionAnswer.query.get(data['id'])
    assert db_record is not None
    assert db_record.question == 'What is Flask?'
    assert db_record.answer == answer
    assert db_record.created_at is not None



def test_ask_endpoint_invalid_json(client):
    """Test the /ask endpoint with an invalid JSON payload."""
    response = client.post('/api/v1/ask', data="Invalid JSON")
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'An unexpected error occurred' in data['details']


def test_ask_endpoint_unsupported_method(client):
    """Test the /ask endpoint with an unsupported HTTP method."""
    response = client.get('/api/v1/ask')
    assert response.status_code == 405
    data = response.get_json()
    assert 'error' in data
    assert 'The method is not allowed for this endpoint' in data['message']



