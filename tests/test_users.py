from app import schemas
from jose import jwt 
from app.core.config import settings
import pytest


'''def test_root(client):
    res = client.get("/")
    #print(res.json().get("message"))
    assert res.json().get("message") == "hellow world outside of ubuntu"'''

def test_create_user(client):
    res = client.post("/user",json={"email":"user123@gmail.com","password":"password1234"})

    new_user = schemas.User_response(**res.json())

    assert new_user.email == "user123@gmail.com"
    assert res.status_code == 201


def test_login_user(client,test_user):
    res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.acces_token, settings.secret_key,algorithms=[settings.algorithm])
    id :str = payload.get("user_id")
    print(login_res.acces_token)
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code,detail,d_content",[
    ("wrongemail@gmail.com","wrongpassword",403,"detail","Invalid credentials"),
    (None,"password1234",422,"assert",None),
    ("user1234@gmail.com",None,422,"assert",None),
    ("user1234@gmail.com","wrongpassword",403,"detail","Invalid credentials")
])
def test_fail_login(client,test_user,email,password,status_code,detail,d_content):
    res  = client.post("/login",data={"username":email,"password":password})

    assert res.status_code == status_code 
    assert res.json().get(detail) == d_content

