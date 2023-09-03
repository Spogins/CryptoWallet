import httpx


async def log_in_user(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                              "password": "Wallet5231",
                                              "remember": False})


async def test_users(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get("/api/v1/users")
    print(response.json())
    assert response.status_code == 200


async def test_user(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/user/{1}")
    print(response.json())
    assert response.status_code == 200


async def test_edit_profile(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.put(f"/api/v1/edit_profile", json={
        "username": "ttest",
        "new_password": "",
        "repeat_password": "",
        "avatar": ""
    })
    print(response.json())
    assert response.status_code == 200


# async def test_remove_user(client: httpx.AsyncClient) -> None:
#     await log_in_user(client)
#     response = await client.delete(f"/api/v1/user/{1}")
#     assert response.status_code == 204
