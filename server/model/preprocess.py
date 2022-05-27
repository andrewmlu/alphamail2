from server.apis.helpers import get_ids, get_metadata_from_ids
from server.model.helpers import save_data, load_data
import os.path
import numpy as np
import random

# DONE 2022.05.20-12.26 save files like metadata
# DONE 2022.05.20-12.26 load files
# DONE 2022.05.20-11.00 process metadata into headlines
# DONE 2022.05.20-17.10 randomize data

random.seed(1)

def generate_dataset(service=None, file_name='metadata', file_path='server/data'):
    file_loc = f'{file_path}/{file_name}'
    if os.path.isfile(file_loc):
        metadata = load_data(file_loc)
    else:
        ids = get_ids(service)
        metadata = get_metadata_from_ids(service, ids)
        save_data(metadata, file_loc)
    dataset = []
    count = 0
    for msg_metadata in metadata:
        msg_headline = f'{msg_metadata["author"]} <{msg_metadata["author-address"]}>: {msg_metadata["subject"]}'
        importance = 1 if 'IMPORTANT' in msg_metadata['labels'] else 0
        dataset.append([msg_headline, importance])
        count += 1
        # if count % 50 == 0:
        #     print(count, end=' ')
        #     print(msg_headline, importance)
    dataset = np.array(dataset, dtype=object)  # keeps the Y values as integers
    return dataset


def split_dataset(dataset, train_pct, val_pct, test_pct):
    total_pct = train_pct + val_pct + test_pct
    val_idx = int(train_pct / total_pct * len(dataset))
    test_idx = int((val_pct + train_pct) / total_pct * len(dataset))
    indices = np.arange(len(dataset))
    random.shuffle(indices)
    train_x = np.array(dataset[indices[0:val_idx], :-1], dtype='U')
    train_y = np.array(dataset[indices[0:val_idx], -1:], dtype='i')
    val_x = np.array(dataset[indices[val_idx:test_idx], :-1], dtype='U')
    val_y = np.array(dataset[indices[val_idx:test_idx], -1:], dtype='i')
    test_x = np.array(dataset[indices[test_idx:], :-1], dtype='U')
    test_y = np.array(dataset[indices[test_idx:], -1:], dtype='i')
    return train_x, train_y, val_x, val_y, test_x, test_y
