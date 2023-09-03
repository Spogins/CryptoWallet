import httpx


async def log_in_user(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                              "password": "Wallet5231",
                                              "remember": False})


async def test_add_product(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.post("/api/v1/add_product", json={
        "title": "string",
        "wallet": 1,
        "price": 0.01,
        "image": ""
    })
    print(response.json())
    assert response.status_code == 201


async def test_get_products(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get("/api/v1/get_products")
    print(response.json())
    assert response.status_code == 200


async def test_get_product(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/get_product?product={1}")
    print(response.json())
    assert response.status_code == 200


async def test_buy_product(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.post("/api/v1/buy_product", json={
        "id": 1,
        "wallet": "0x44fe49b6c180B660933548A8632bE93079010F28"
    })
    print(response.json())
    assert response.status_code == 200