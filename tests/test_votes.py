import pytest 

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_like_post(authorized_client,create_posts,id):
    res = authorized_client.post(f"/votes/{id}")
    
    assert res.json().get("msg") == "Liked"
    assert res.status_code == 200


@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3),
])
def test_unlike_post(authorized_client,create_posts,id,like_posts):
    res = authorized_client.post(f"/votes/{id}")

    assert res.json().get("msg") == "Unliked"
    assert res.status_code == 200

@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_like_post_anauthorized(client,create_posts,id):
    res = client.post(f"/votes/{id}")

    assert res.status_code == 401


@pytest.mark.parametrize("id",[
    (1),
    (2),
    (3)
])
def test_unlike_post_anauthorized(client2,create_posts,id,like_posts):
    res = client2.post(f"/votes/{id}")
    assert res.json().get("assert") == None
    assert res.status_code == 401



