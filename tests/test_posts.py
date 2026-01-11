from App import schema

def test_get_all_posts(auth_client, posts):
    res = auth_client.get("/posts/")

    def validate(row):
        return schema.Post(**row["post"])  # 👈 dict access

    posts_list = list(map(validate, res.json()))
    assert res.status_code == 200
    assert len(posts_list) == len(posts)
    print(f"Get All Posts Response: {res.json()}")

def test_get_single_post(auth_client, posts):
    post_id = posts[0].id
    res = auth_client.get(f"/posts/{post_id}")
    single_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert single_post.id == post_id
    print(f"Get Single Post Response: {res.json()}")

def test_create_post(auth_client):
    res = auth_client.post(
        "/posts/",
        json={
            "title": "New Test Post",
            "content": "Content for the new test post",
            "published": True
        },
        )
    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "New Test Post"
    assert created_post.content == "Content for the new test post"
    assert created_post.published is True
    print(f"Create Post Response: {res.json()}")

def test_unauthorized_user_delete_post(client, posts):
    post_id = posts[0].id
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 401
    print(f"Unauthorized Delete Post Response: {res.json()}")

def test_authorized_user_delete_post(auth_client, posts):
    post_id = posts[0].id
    res = auth_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204 
    print(f"Authorized Delete Post Response: {res.status_code}")

def test_delete_nonexistent_post(auth_client):
    res = auth_client.delete("/posts/9999")  
    assert res.status_code == 404
    print(f"Delete Nonexistent Post Response: {res.json()}")

def test_delete_other_user_post(auth_client,posts,users):
    post_id = posts[2].id
    res = auth_client.delete(f"/posts/{post_id}")
    assert res.status_code == 403

def test_update_post(auth_client, posts, users):
    post_id = posts[0].id
    res = auth_client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Test Post",
            "content": "Updated content for the test post",
            "published": False
        },
    )
    updated_post = schema.Post(**res.json())
    assert res.status_code == 202
    assert updated_post.title == "Updated Test Post"
    assert updated_post.content == "Updated content for the test post"
    assert updated_post.published is False
def test_other_user_update_post(auth_client, posts):
    post_id = posts[1].id
    res = auth_client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated Test Post",
            "content": "Updated content for the test post",
            "published": False
        },
    )
    print(f"Other User Update Post Response: {res.json()}")
    assert res.status_code == 403