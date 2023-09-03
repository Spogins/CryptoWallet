import httpx


async def test_registration(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/v1/registration", json={"email": "user@user.com",
                                                        "username": "user",
                                                        "password": "Wallet5231",
                                                        "confirm_password": "Wallet5231"})
    print(response.json())
    assert response.status_code == 201


async def test_log_in(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                                        "password": "Wallet5231",
                                                        "remember": False})
    print(response.json())
    assert response.status_code == 200


async def test_log_out(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                                         "password": "Wallet5231",
                                                         "remember": False})
    response = await client.post("/api/v1/log_out")
    print(response.json())
    assert response.status_code == 200