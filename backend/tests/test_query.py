import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.retrieval import retrieval_service

client = TestClient(app)

# Mock the retrieval service so we don't need a real Chroma DB for basic routing tests
class MockRetrieverService:
    def retrieve(self, query):
        return []

retrieval_service.retrieve = MockRetrieverService().retrieve

# Also mock generation
from app.services.generation import generation_service
class MockGenerationService:
    def generate_answer(self, question, docs, vision_context=""):
        return "Mock answer", ["mock_source.pdf"]

generation_service.generate_answer = MockGenerationService().generate_answer

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query_endpoint_happy_path():
    response = client.post("/query", data={"question": "What is a corner?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "Mock answer"

def test_query_endpoint_missing_question():
    # Sending empty body should cause a 422 Unprocessable Entity
    response = client.post("/query", data={})
    assert response.status_code == 422
