from app.config import Settings
from app.infrastructure.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_round_trip() -> None:
    hashed = hash_password("senha-segura-123")

    assert hashed != "senha-segura-123"
    assert verify_password("senha-segura-123", hashed)
    assert not verify_password("senha-errada", hashed)


def test_access_token_contains_subject_and_role() -> None:
    settings = Settings(jwt_secret_key="a" * 32)
    token = create_access_token("user-1", "porteiro", settings)

    payload = decode_access_token(token, settings)
    assert payload["sub"] == "user-1"
    assert payload["role"] == "porteiro"
