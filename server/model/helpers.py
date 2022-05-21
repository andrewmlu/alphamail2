import pickle

def save_data(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def load_data(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data