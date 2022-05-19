verbose = 0

def get_ids(service, user_id='me', labels=[], quantity=25):
    """
    Retrieves all IDs of emails by parsing through each
    page of email IDs given an API connection.

    Parameters:
    service -- gmail API connection
    user_id -- user ID of messages to retrieve
    labels -- labels for which to retrieve messages

    Returns:
    list of email message IDs based on specified criteria
    """
    count = quantity
    try:
        next_page_token = ''
        msgs_list = []
        while count > 0:
            num_messages = min(500, count)
            msgs = service.users().messages().list(userId=user_id, labelIds=labels,
                                                   maxResults=num_messages,
                                                   pageToken=next_page_token).execute()
            msgs_list += msgs['messages']
            count -= num_messages
            if 'nextPageToken' not in msgs.keys():
                break
            next_page_token = msgs['nextPageToken']
        return [msg['id'] for msg in msgs_list]
    except Exception as error:
        print('An error occurred here: %s' % error)

# TODO fix &#39; &quot; and other characters
# TODO fix author field to exclude <email@address.com> for initial display, but pass in separately
def get_metadata_from_id(service, message_id, user_id='me'):
    msg = service.users().messages().get(userId=user_id, id=message_id, format='metadata').execute()
    metadata = {}

    payload = msg['payload']
    headers = payload.get("headers")


    metadata['id'] = msg['id']
    metadata['preview'] = msg.get('snippet')

    if 'labelIds' in msg: metadata['labels'] = msg['labelIds']
    else: metadata['labels'] = []

    if 'IMPORTANT' in msg['labelIds']: metadata['type'] = 'important'
    else: metadata['type'] = 'unimportant'

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from': metadata['author'] = value
            if name.lower() == "to": metadata['to'] = value
            if name.lower() == "subject": metadata['subject'] = value
    metadata['date'] = msg['internalDate']
    if verbose >= 1: print("=" * 50)
    return metadata


def get_metadata_from_ids(service, ids, user_id='me'):
    metadata = []
    for id in ids:
        metadata.append(get_metadata_from_id(service, id, user_id=user_id))
    return metadata