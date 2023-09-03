import httpx


async def log_in_user(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                              "password": "Wallet5231",
                                              "remember": False})


async def test_get_orders(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get("/api/v1/get_orders")
    print(response.json())
    assert response.status_code == 200


async def test_get_order(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/get_order?product={1}")
    print(response.json())
    assert response.status_code == 401