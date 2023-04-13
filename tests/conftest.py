from fastapi.testclient import TestClient 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app 
from app.config import settings
from app.database import get_db,Base 
from app.oauth2 import create_acces_toke
from app import models
import pytest   

# a hint is just stop the tests when a fail test occurs, when our code grows a lot
# you want to see which test case fail and fix the bug and then continue again, use the -x 
# flag to make that happen 


#this variable is for connect with our database with sqlalchemy
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
#we need to create an engine to connect with the database we want 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#to talk with a database we need to create a session 
TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture()
def session():
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db 
    finally:
        db.close() 


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session 
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def client2(session):
    def override_get_bd():
        try:
            yield session 
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_bd
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user = {"email":"user1234@gmail.com","password":"password1234"}

    res = client.post("/user/",json=user)
    assert res.status_code == 201 
    new_user = res.json() 
    new_user['password'] = user["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_acces_toke(data ={"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}",        
    }
    return client 

@pytest.fixture
def create_posts(test_user,session,test_user2):
    post_data = [
        {"title":"1st title",
         "content":"content1",
         "owner_id":test_user['id']},
        {"title":"2nd title",
         "content":"2nd content",
         "owner_id":test_user['id']},
         {"title":"3rd title",
          "content":"in the end it doesn't even matter",
          "owner_id":test_user['id']},
        {"title":"4st title",
         "content":"content4",
         "owner_id":test_user2['id']},
        {"title":"5nd title",
         "content":"4th content",
         "owner_id":test_user2['id']},
         {"title":"6th title",
          "content":"in the end it doesn't even matter",
          "owner_id":test_user2['id']},
    ]
    
    def create_model_posts(post):
        return models.Post(**post)
    
    post_map= map(create_model_posts,post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()

@pytest.fixture
def test_user2(client):
    user = {"email":"julianpower@gmail.com","password":"password1234"}

    res = client.post("/user/",json=user)
    assert res.status_code == 201 
    new_user = res.json() 
    new_user['password'] = user["password"]
    return new_user


@pytest.fixture 
def like_posts(session,create_posts,test_user,test_user2):

    data = [{"user_id":test_user['id'],"post_id":create_posts[0].id},
            {"user_id":test_user['id'],"post_id":create_posts[1].id},
            {"user_id":test_user['id'],"post_id":create_posts[2].id},]
    
    def create_model_votes(vote):
        post = session.query(models.Post).filter(models.Post.id == vote['post_id']).first()
        post.votes +=1
        session.add(post)
        session.commit()
        return models.Vote(**vote)

    vote_map = map(create_model_votes,data)
    votes = list(vote_map)
    session.add_all(votes)
    session.commit()
    return session.query(models.Vote).all()
