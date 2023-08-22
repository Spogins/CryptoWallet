import pickle


async def decode_data(data):
    data = pickle.loads(data)
    return data