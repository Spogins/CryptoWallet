from datetime import datetime


async def parse_trans_data(trans, block_time, status, _hash):
    # current_time = datetime.utcnow()
    # past_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    # time_difference = current_time - past_time
    # # Получение количества дней, часов, минут и секунд
    # days = time_difference.days
    # hours, remainder = divmod(time_difference.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    gas_price_gwei = int(trans.get('gasPrice'))  # Пример: 100 Gwei
    gas_limit = int(trans.get('gas'))  # Пример: стандартный лимит для отправки эфира
    txn_fee_wei = gas_price_gwei * gas_limit * 10 ** 9  # 1 Gwei = 10^9 Wei
    txn_fee_eth = txn_fee_wei / 10 ** 18

    transaction = {
        "hash": _hash,
        "from_address": trans.get('from'),
        "to_address": trans.get('to'),
        "value": int(trans.get('value')) / 10 ** 18,
        "age": str(block_time),
        "txn_fee": txn_fee_eth / 10 ** 9,
        'status': status
    }
    return transaction
