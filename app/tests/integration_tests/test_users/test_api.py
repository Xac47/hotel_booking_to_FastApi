import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kot3@gmail.com", "qwert12345", 200),
        ("kot3@gmail.com", "qwert", 409),
        ("hamster@gmail.com", "qwert12345", 200),
    ],
)
async def test_sign_up(ac: AsyncClient, email, password, status_code):

    response = await ac.post(
        "/auth/sign_up",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.request.url.path == "/auth/sign_up"
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@example.com", "test", 200),
    ],
)
async def test_sign_in(ac: AsyncClient, email, password, status_code):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.request.url.path == "/auth/login"
    assert response.status_code == status_code
