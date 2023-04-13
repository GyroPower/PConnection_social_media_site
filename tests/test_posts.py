from app import schemas
from jose import jwt 
from app.config import settings
import pytest

def test_get_all_posts(create_posts,authorized_client):
    res = authorized_client.get("/posts/")
    
    def validate(post):
        
        return schemas.Post_response(**post)

    if len(res.json()) >1:


        posts_map = map(validate,res.json())
        posts = list(posts_map) 
        assert res.status_code == 200
        assert len(posts) == len(create_posts)
        assert posts[0].id == create_posts[0].id

def test_anaunthorized_user_get_all_posts(client,create_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_get_one_post(authorized_client,create_posts,id):

    res = authorized_client.get(f"/posts/{id}")

    assert res.status_code == 200 
    assert res.json().get("id") == id

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_anauthorized_client_try_get_one_post(client,create_posts,id):
    res = client.get(f"posts/{id}")

    assert res.status_code == 401
    assert res.json().get("assert") == None

@pytest.mark.parametrize("post",[
    ({"title":"title1","content":"content1","published":True}),
    ({"title":"title2","content":"content2","published":True}),
    ({"title":"title3","content":"content3","published":True})
])
def test_create_posts(authorized_client,post):
    

    res = authorized_client.post("/posts/",json=post)

    assert res.status_code == 201

@pytest.mark.parametrize("post",[
    ({"title":"title1","content":"content1","published":True}),
    ({"title":"title2","content":"content2","published":True}),
    ({"title":"title3","content":"content3","published":True})
])
def test_create_post_with_anauthorized_client(client,post):
    res = client.post("/posts/",json=post)

    assert res.status_code == 401 
    assert res.json().get("assert") == None

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_delete_a_post(authorized_client,create_posts,id):
    res = authorized_client.delete(f"/posts/{id}")
    
    assert res.status_code == 204 


@pytest.mark.parametrize("id",[
    (4),
    (5),
    (6)
])
def test_delete_a_post_which_dont_exists(authorized_client,id):
    res = authorized_client.delete(f"/posts/{id}")
    
    assert res.status_code == 404 

@pytest.mark.parametrize("id",[
    (4),
    (5),
    (6)
])
def test_delete_a_post_dont_belong_to_user(authorized_client,create_posts,id):
    res = authorized_client.delete(f"/posts/{id}")
    assert res.status_code == 401

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_delete_a_post_anuathorized_user(client,create_posts,id):
    res = client.delete(f"/posts/{id}")

    assert res.status_code == 401

@pytest.mark.parametrize("id,title,content",[
    (1,"Another1","asdff"),
    (2,"another2","1245"),
    (3,"another3","mnbvc")
])
def test_update_post(authorized_client,create_posts,id,title,content):
    data = {"title":title,"content":content}
    res = authorized_client.put(f"/posts/{id}",json=data)

    assert res.status_code == 201

@pytest.mark.parametrize("id,title,content",[
    (4,"Another1","asdff"),
    (5,"another2","1245"),
    (6,"another3","mnbvc")
])
def test_update_post_dont_belong_to_user(authorized_client,create_posts,id,title,content):
    data = {"title":title,"content":content}
    res = authorized_client.put(f"/posts/{id}",json=data)

    assert res.status_code == 401
    