import httpx


async def log_in_user(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                              "password": "Wallet5231",
                                              "remember": False})


# async def test_send_message(client: httpx.AsyncClient) -> None:
#     await log_in_user(client)
#     response = await client.post("/api/v1/send_message", json={
#         "text": "Hi test!",
#         "image": ""
#     })
#     print(response.json())
#     assert response.status_code == 201

async def test_get_chat(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get("/api/v1/get_chat")
    print(response.json())
    assert response.status_code == 200