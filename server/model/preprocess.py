from server.apis.helpers import get_email_address, get_ids, get_metadata_from_threads, batch_request_threads_from_ids
from server.model.helpers import save_data, load_data
import os
from dotenv import load_dotenv
import datetime
import numpy as np
import random
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY') # seems like need to rerun python in terminal in order to refresh code, .env is based on location of terminal run not file location

# DONE 2023.04.16-19.09 create env file and var for openai api key

# DONE 2022.05.20-12.26 save files like metadata
# DONE 2022.05.20-12.26 load files
# DONE 2022.05.20-11.00 process metadata into headlines
# DONE 2022.05.20-17.10 randomize data

random.seed(1)

# DONE 2023.04.18-18.01 add ability to limit dataset size
# DONE 2023.04.18-18.01 add ability to save threads and load directly from threads dataset
# DONE 2023.04.18-18.25 add better file naming
def generate_dataset(service, limit=None, enable_loading=True, file_name='metadata', file_path='server/data', override=False):
    email_address = get_email_address(service)
    date = datetime.datetime.now().strftime('%y%m%d')
    file_loc = f'{file_path}/{file_name}-{email_address}-{date}-{limit if limit else "all"}'
    if override:
        file_loc = f'{file_path}/{file_name}'
    if os.path.isfile(file_loc) and enable_loading:
        metadata = load_data(file_loc)
    else:
        if os.path.isfile(f'{file_loc}-threads') and enable_loading:
            threads = load_data(f'{file_loc}-threads')
        else:
            # DONE 2023.04.16-22.46 fix get_metadata_from_ids for threads
            ids = get_ids(service, quantity=limit) if limit else get_ids(service)
            threads = batch_request_threads_from_ids(service, ids, format='metadata')
        save_data(threads, f'{file_loc}-threads')
        metadata = get_metadata_from_threads(threads)
        # metadata = get_metadata_from_ids(service, ids)
        # DONE 2023.04.18-15.05 do not save metadata if specified not to
        if file_name is not None:
            save_data(metadata, file_loc)
    dataset = []
    count = 0
    for msg_metadata in metadata:
        msg_headline = f'{msg_metadata["authors"]}: {msg_metadata["subject"]}'
        importance = 0.55 if 'IMPORTANT' in msg_metadata['labels'] else 0
        # DONE 2023.04.18-18.21 include starring and reading into importance/priority
        importance += 0.3 if 'STARRED' in msg_metadata['labels'] else 0
        importance += 0.15 if 'UNREAD' not in msg_metadata['labels'] else 0
        dataset.append([msg_headline, importance])
        count += 1
        # if count % 50 == 0:
        #     print(count, end=' ')
        #     print(msg_headline, importance)
    dataset = np.array(dataset, dtype=object)  # keeps the Y values as numbers
    return dataset


def split_dataset(dataset, train_pct, val_pct, test_pct):
    total_pct = train_pct + val_pct + test_pct
    val_idx = int(train_pct / total_pct * len(dataset))
    test_idx = int((val_pct + train_pct) / total_pct * len(dataset))
    indices = np.arange(len(dataset))
    random.shuffle(indices)
    train_x = np.array(dataset[indices[0:val_idx], :-1], dtype='U')
    train_y = np.array(dataset[indices[0:val_idx], -1:], dtype='f')
    val_x = np.array(dataset[indices[val_idx:test_idx], :-1], dtype='U')
    val_y = np.array(dataset[indices[val_idx:test_idx], -1:], dtype='f')
    test_x = np.array(dataset[indices[test_idx:], :-1], dtype='U')
    test_y = np.array(dataset[indices[test_idx:], -1:], dtype='f')
    return train_x, train_y, val_x, val_y, test_x, test_y

# DONE 2023.04.18-18.12 changed y values from ints to floats

def get_embedding(text, model='text-embedding-ada-002'):
    """
    Returns OpenAI text model embedding or batch of embeddings
    """
    return openai.Embedding.create(input=text, model=model)['data']

# DONE 2023.02.04-05.47 batch embedding API calls
def get_embeddings(dataset):
    embeddings = []
    batch = []
    for i, text in enumerate(dataset):
        batch.append(text[0])
        if (i % 100 == 99 or i == len(dataset)-1) and len(batch) != 0:
            print("embedding progress:", i+1, "of", len(dataset))
            # print(batch)
            for embedding in get_embedding(batch):
                embeddings.append(embedding['embedding'])
            batch = []

    return np.array(embeddings)
