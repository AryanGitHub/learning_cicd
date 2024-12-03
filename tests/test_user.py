
from fastapi import status
from app import schema
from app import models
from app.tokenAuth import ALGORITHM , SECRET


def test_root (client):
    data = client.get("/")
    assert(data.json().get("message")=="working")
    assert(data.status_code==status.HTTP_200_OK)

def test_create_user(client,test_db_session):
    response = client.post("/users", json={	"username": "Mohit","email": "Rohit@gmail.com","password": "pass"})
    assert (response.status_code == status.HTTP_201_CREATED)

    new_user = schema.user_response(**response.json())
    users_from_db = test_db_session.query(models.user).filter(models.user.user_id == new_user.user_id).first()

    assert(new_user.username == "Mohit" )
    assert(new_user.email == "Rohit@gmail.com")
    assert(new_user.username == users_from_db.username)
    assert(new_user.email == users_from_db.email)

def test_get_user_from_username (a_test_user,client , test_db_session ):
    data = client.get(f"users/username/{a_test_user.get("username")}")
    user_response = schema.user_response(**data.json())
    a_test_user = schema.user_response(**a_test_user)
    assert(data.status_code==status.HTTP_200_OK)
    users_from_db = test_db_session.query(models.user).filter(models.user.user_id == a_test_user.user_id).first()

    assert(user_response.username == a_test_user.username)
    assert(a_test_user.username == users_from_db.username)

    assert(user_response.email == a_test_user.email)
    assert(a_test_user.email == users_from_db.email)

    assert(user_response.user_id == a_test_user.user_id)
    assert(a_test_user.user_id == users_from_db.user_id)

    assert(user_response.created_at == a_test_user.created_at)
    assert(a_test_user.created_at == users_from_db.created_at)

def test_login (a_test_user , client):
    response = client.post("/login" , data={"username": a_test_user.get("username"), "password": a_test_user.get("password")} )
    assert(response.status_code == status.HTTP_200_OK)
    authToken = schema.authToken_response(**response.json())
    assert (authToken.token_type == "bearer")
    from jose import jwt
    user = jwt.decode(response.json()["access_token"], SECRET, algorithms=[ALGORITHM])
    assert(user["username"] == a_test_user["username"])

    


