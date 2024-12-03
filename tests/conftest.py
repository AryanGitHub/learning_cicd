from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from app import config
import pytest
from app.database import get_db
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base as TestBase
from sqlalchemy.ext.declarative import declarative_base
from fastapi import status
from app import schema




#postgresql://username:password@localhost:port/database_name
POSTGRES_TEST_DB_CONNECTION_URL = config.settings.db_protocol+config.settings.db_username+ ":" + config.settings.db_password + "@" + config.settings.db_hostname + ":" + str(config.settings.db_port) + "/" + config.settings.db_name+"_test"
test_engine = create_engine(POSTGRES_TEST_DB_CONNECTION_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture()
def test_db_session():
    TestBase.metadata.drop_all(test_engine)
    TestBase.metadata.create_all(test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client (test_db_session):
    def override_session():
        return test_db_session
    app.dependency_overrides[get_db]=override_session
    return TestClient(app)

@pytest.fixture()
def a_test_user (client):
    response = client.post("/users", json={	"username": "test","email": "test@test.com","password": "pass"})
    assert(response.status_code == status.HTTP_201_CREATED)
    new_user = schema.user_response(**response.json())
    response = response.json()
    response["password"] = "pass"
    return response