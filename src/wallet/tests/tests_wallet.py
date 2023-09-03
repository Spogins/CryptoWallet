import httpx


async def log_in_user(client: httpx.AsyncClient) -> None:
    await client.post("/api/v1/log_in", json={"email": "user@user.com",
                                              "password": "Wallet5231",
                                              "remember": False})




async def test_create_eth_wallet(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    await client.post("/api/v1/create_eth_asset")
    response = await client.post(f"/api/v1/create_eth_wallet")
    print(response.json())
    assert response.status_code == 201


async def test_create_eth_wallet(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.post(f"api/v1/import_eth_wallet?private_key=0x17f270e0a153579b024b38a35ed11397e4b1a56c36f55b144d477ca1869f432e")
    print(response.json())
    assert response.status_code == 201


async def test_db_user_wallets(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/user_wallets?user={1}")
    print(response.json())
    assert response.status_code == 200


async def test_get_wallet(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/get_wallet/{1}")
    print(response.json())
    assert response.status_code == 200


async def test_wallet_balance(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/wallet_balance?wallet_address=0x44fe49b6c180B660933548A8632bE93079010F28")
    print(response.json())
    assert response.status_code == 200


# async def test_update_wallet_balance(client: httpx.AsyncClient) -> None:
#     await log_in_user(client)
#     response = await client.put(f"/api/v1/update_wallet_balance?wallet_address=0x44fe49b6c180B660933548A8632bE93079010F28")
#     print(response.json())
#     assert response.status_code == 200
#
#
# async def test_update_all_wallets_balance(client: httpx.AsyncClient) -> None:
#     await log_in_user(client)
#     response = await client.put(f"/api/v1/update_all_wallets_balance")
#     print(response.json())
#     assert response.status_code == 200



async def test_wallet_db_transactions(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get(f"/api/v1/wallet_db_transactions?address=0x44fe49b6c180B660933548A8632bE93079010F28&limit=10")
    print(response.json())
    assert response.status_code == 200


async def test_db_transactions(client: httpx.AsyncClient) -> None:
    await log_in_user(client)
    response = await client.get("/api/v1/db_transactions?limit=10")
    print(response.json())
    assert response.status_code == 200