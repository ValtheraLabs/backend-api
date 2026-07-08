from app.models.user import User
from app.services.auth_service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_produces_different_hashes() -> None:
    h1 = hash_password("testpass123")
    h2 = hash_password("testpass123")
    assert h1 != h2
    assert verify_password("testpass123", h1)
    assert verify_password("testpass123", h2)


def test_verify_password_fails_for_wrong_password() -> None:
    hashed = hash_password("correctpw")
    assert not verify_password("wrongpw", hashed)


def test_create_and_decode_token() -> None:
    token = create_access_token(user_id=42)
    assert decode_access_token(token) == 42


def test_decode_invalid_token_returns_none() -> None:
    assert decode_access_token("invalid-token") is None


def test_register_user_creates_user_in_db(db_session) -> None:
    from app.services.auth_service import register_user

    user = register_user(db_session, "test@valthera.io", "Test User", "password123")
    assert user.id is not None
    assert user.email == "test@valthera.io"
    assert user.display_name == "Test User"
    assert user.hashed_password != "password123"  # should be hashed


def test_register_duplicate_email_raises(db_session) -> None:
    from app.services.auth_service import register_user

    register_user(db_session, "dup@valthera.io", "First", "password123")
    import pytest

    with pytest.raises(ValueError, match="Email already registered"):
        register_user(db_session, "dup@valthera.io", "Second", "otherpass456")


def test_authenticate_user_success(db_session) -> None:
    from app.services.auth_service import authenticate_user, register_user

    register_user(db_session, "auth@valthera.io", "Auth User", "securepw")
    user = authenticate_user(db_session, "auth@valthera.io", "securepw")
    assert user is not None
    assert user.email == "auth@valthera.io"


def test_authenticate_user_wrong_password(db_session) -> None:
    from app.services.auth_service import authenticate_user, register_user

    register_user(db_session, "wrongpw@valthera.io", "Wrong PW", "correctpw")
    user = authenticate_user(db_session, "wrongpw@valthera.io", "wrongpw")
    assert user is None
