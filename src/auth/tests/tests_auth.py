import httpx
import pytest

# @pytest.mark.asyncio
# async def test():
#     assert 1 == 1


async def test_registration(client: httpx.AsyncClient) -> None:
    response = await client.post("/registration", json={"email": "user@user.com",
                                                        "username": "user",
                                                        "password": "Wallet5231",
                                                        "confirm_password": "Wallet5231"})
    print(response.json())
    assert response.status_code == 201