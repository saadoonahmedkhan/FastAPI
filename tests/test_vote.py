def test_votes(auth_client, posts):
    vote_data = {
        "post_id": posts[0].id,
        "dir": 1
    }
    res = auth_client.post("/votes/", json=vote_data)
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully added vote"
    print(f"Vote Response: {res.json()}")

def test_duplicate_vote(auth_client, posts, votes):
    vote_data = {
        "post_id": posts[0].id,
        "dir": 1
    }
    res = auth_client.post("/votes/", json=vote_data)
    assert res.status_code == 409
    print(f"Duplicate Vote Response: {res.json()}")

def test_remove_vote(auth_client, posts, votes):
    vote_data = {
        "post_id": posts[0].id,
        "dir": 0
    }
    res = auth_client.post("/votes/", json=vote_data)
    assert res.status_code == 201
    assert res.json()["message"] == "Successfully deleted vote"
    print(f"Remove Vote Response: {res.json()}")

def test_invalid_vote_direction(auth_client, posts):
    vote_data = {
        "post_id": posts[0].id,
        "dir": 3
    }
    res = auth_client.post("/votes/", json=vote_data)
    assert res.status_code == 422
    print(f"Invalid Vote Direction Response: {res.json()}")

def test_vote_on_nonexistent_post(auth_client):
    vote_data = {
        "post_id": 9999,
        "dir": 1
    }
    res = auth_client.post("/votes/", json=vote_data)
    assert res.status_code == 404
    print(f"Vote on Nonexistent Post Response: {res.json()}")