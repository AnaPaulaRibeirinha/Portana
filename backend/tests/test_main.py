from app.main import redirect_to_docs


def test_root_redirects_to_swagger() -> None:
    response = redirect_to_docs()

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
