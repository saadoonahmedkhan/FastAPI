from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from fastapi.testclient import TestClient
import pytest

from App.config import settings
from App.main import app
from App import schema, database, models, oauth2, utils

# URL encode password (handles special chars)
encoded_password = quote(settings.database_password, safe="")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{settings.database_username}:"
    f"{encoded_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------- DB SESSION --------------------

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- CLIENT --------------------

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)

# -------------------- SINGLE USER (API) --------------------

@pytest.fixture
def user(client):
    res = client.post(
        "/users/",
        json={
            "email": "B10TtR@example.com",
            "password": "password123",
            "username": "testuser",
        },
    )
    return res.json()  # 👈 dict

# -------------------- MULTIPLE USERS (ORM) --------------------

@pytest.fixture
def users(session):
    users_data = [
        {"email": "B3TtR@example.com", "password": "password123", "username": "testuser1"},
        {"email": "c3TtR@example.com", "password": "password123", "username": "testuser2"},
        {"email": "b3TtR@example.com", "password": "password123", "username": "testuser3"},
    ]

    db_users = []
    for u in users_data:
        db_user = models.User(
            email=u["email"],
            username=u["username"],
            password=utils.hash(u["password"]),
        )
        db_users.append(db_user)

    session.add_all(db_users)
    session.commit()

    return session.query(models.User).all()  # 👈 ORM objects

# -------------------- TOKEN --------------------

@pytest.fixture
def token(user):
    return schema.Token(
        access_token=oauth2.create_access_token(
            data={"sub": str(user["id"])}  # 👈 user is dict
        ),
        token_type="bearer",
    )

# -------------------- AUTH CLIENT --------------------

@pytest.fixture
def auth_client(client, token):
    client.headers.update(
        {"Authorization": f"Bearer {token.access_token}"}
    )
    return client

# -------------------- POSTS --------------------

@pytest.fixture
def posts(users, session):
    session.add_all([
        models.Post(
            title="First Post",
            content="Content of first post",
            owner_id=users[0].id,   # ✅ FIXED
        ),
        models.Post(
            title="Second Post",
            content="Content of second post",
            owner_id=users[1].id,
        ),
        models.Post(
            title="Third Post",
            content="Content of third post",
            owner_id=users[2].id,
        ),
    ])

    session.commit()
    return session.query(models.Post).all()

@pytest.fixture
def votes(users, posts, session):
    vote1 = models.Vote(user_id=users[0].id, post_id=posts[1].id)
    vote2 = models.Vote(user_id=users[0].id, post_id=posts[0].id)
    vote3 = models.Vote(user_id=users[1].id, post_id=posts[2].id)

    session.add_all([vote1, vote2, vote3])
    session.commit()