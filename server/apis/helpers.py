import html
import re
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
import sys
import ast

verbose = 0

def get_email_address(service, user_id='me'):
    """
    Retrieves the email address of the user.
    Parameters:
    service -- gmail API connection
    user_id -- user ID of user to retrieve email address
    """
    try:
        # Get the profile information of the currently authenticated user
        profile = service.users().getProfile(userId=user_id).execute()
        email_address = profile['emailAddress']
        email_prefix = email_address.split('@')[0]
        return email_prefix
    except Exception as error:
        print('An error occurred: %s' % error)

def get_ids(service, user_id='me', labels=[], quantity=sys.maxsize):
    """
    Retrieves all IDs of threads by parsing through each
    page of thread IDs given an API connection.
    Parameters:
    service -- gmail API connection
    user_id -- user ID of threads to retrieve
    labels -- labels for which to retrieve threads
    quantity -- number of thread ids to retrieve (default to all)
    Returns:
    list of email thread IDs based on specified criteria
    """
    count = quantity
    start_time = time.time()
    try:
        next_page_token = ''
        threads_list = []
        while count > 0:
            num_threads = min(500, count)
            threads = service.users().threads().list(userId=user_id, labelIds=labels,
                                                   maxResults=num_threads,
                                                   pageToken=next_page_token).execute()
            threads_list += threads['threads']
            count -= num_threads
            if 'nextPageToken' not in threads.keys():
                break
            next_page_token = threads['nextPageToken']
        print(f'get_ids execution time: {(time.time() - start_time):.3f} seconds')
        return [thread['id'] for thread in threads_list]
    except Exception as error:
        print('An error occurred here: %s' % error)


def get_thread_from_id(service, thread_id, user_id='me'):
    return service.users().threads().get(userId=user_id, id=thread_id, format='full').execute()

def get_emails_from_thread(thread):
    data = get_metadata_from_thread(thread)
    for msg, msg_data in zip(thread['messages'], data['messages']):
        email = get_email_from_message(msg)
        msg_data['body-html'] = email['body-html']
        msg_data['body-text'] = email['body-text']
    return data


# DONE 2022.05.19-12.23 fix &#39; &quot; and other characters in preview (and maybe subject?)
# DONE 2022.05.19-12.43 fix author field to exclude <email@address.com> for initial display, but pass in separately
# DONE 2022.06.09-17.15 add thread id
def get_metadata_from_message(msg):
    metadata = {}

    payload = msg['payload']
    headers = payload.get("headers")

    metadata['message-id'] = msg['id']
    metadata['preview'] = html.unescape(msg.get('snippet'))

    if 'labelIds' in msg:
        metadata['labels'] = msg['labelIds']
    else:
        metadata['labels'] = []

    if 'IMPORTANT' in metadata['labels']:
        metadata['type'] = 'important'
    else:
        metadata['type'] = 'unimportant'

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                metadata['author'] = re.sub(r'(.*)\s<(.*)>', r'\1',
                                            value)  # based on alphamail-v0.2 helpers.py and https://docs.python.org/3/library/re.html
                metadata['author-address'] = re.sub(r'(.*)\s<(.*)>', r'\2',
                                                    value)  # for context on r operator, see https://stackoverflow.com/questions/26163798/using-r-with-string-literals-in-python
            if name.lower() == "to": metadata['to'] = value
            if name.lower() == "subject": metadata['subject'] = html.unescape(value)
            if name.lower() == "date": metadata['date'] = value
    if verbose >= 1: print("=" * 50)
    return metadata


def get_metadata_from_thread(thread):
    metadata = {'thread-id': thread['id'], 'labels': [], 'type': 'unimportant', 'preview': '', 'subject': '', 'msg-count': 0, 'authors': [], 'date-rec': '', 'date-sent': ''}
    message_metadata = []

    for msg in thread['messages']:
        msg_metadata = get_metadata_from_message(msg)
        message_metadata.append(msg_metadata)
        for label in msg_metadata['labels']:
            if label not in metadata['labels']:
                metadata['labels'].append(label)
        if 'SENT' not in msg_metadata['labels']:
            metadata['date-rec'] = msg_metadata['date']
        else:
            metadata['date-sent'] = msg_metadata['date']
        if msg_metadata['author'] not in metadata['authors']:
            metadata['authors'].append(msg_metadata['author'])

    if 'preview' in message_metadata[-1]:
        metadata['preview'] = ['preview']
    else:
        print('no preview', thread['id'])
        metadata['preview'] = 'no preview'
    if 'subject' in message_metadata[0]:
        metadata['subject'] = message_metadata[0]['subject']
    else:
        print('no preview', thread['id'])
        metadata['subject'] = 'no subject'
    metadata['msg-count'] = len(message_metadata)

    metadata['messages'] = message_metadata
    return metadata


# for any low-level data tasks
def get_message_from_id(service, id, user_id='me', format=format):
    return service.users().messages().get(userId=user_id, id=id, format=format).execute()

# perhaps from https://stackoverflow.com/questions/67658283/how-do-i-send-a-batch-request-to-the-gmail-api-in-python?
# DONE 2023.04.16-21.00 limit request rate for gmail api query limit
def batch_request_threads_from_ids(service, ids, format, user_id='me'):
    print("batch_request_threads_from_ids start")
    start_time = time.time()
    data = []
    while len(ids) > 0:
        batch = service.new_batch_http_request()
        if len(ids) > 100:
            batch_ids = ids[:100]
            ids = ids[100:]
            time.sleep(4)  # slow rate limit to 15000 queries per minute (250 per sec) for gmail api
            print('Remaining: ' + str(len(ids)))
        else:
            batch_ids = ids
            ids = []
        for id in batch_ids:
            batch.add(service.users().threads().get(userId=user_id, id=id, format=format))
        batch.execute()
        for res in list(batch._responses.values()):  # extract data from batch response
            data.append(ast.literal_eval(res[1].decode('UTF-8')))
            # TODO understand different string formats like UTF-8
    print(
        f'batch_request_from_ids execution time: {(time.time() - start_time):.3f} seconds')  # see https://stackoverflow.com/questions/1995615/how-can-i-format-a-decimal-to-always-show-2-decimal-places
    return data


# DONE 2022.05.19-12.59 track execution runtime
# TODO optimize through multithreading https://stackoverflow.com/questions/16982569/making-multiple-api-calls-in-parallel-using-python-ipython & https://medium.com/swlh/parallel-asynchronous-api-call-in-python-f6aa663206c6
# DONE 2022.05.26-19.10 consider using batch operations https://stackoverflow.com/questions/65730876/gmail-api-how-can-i-get-the-message-body
def get_metadata_from_threads(threads):
    start_time = time.time()
    metadata = []
    for thread in threads:
        metadata.append(get_metadata_from_thread(thread))
    print(f'get_metadata_from_thread execution time: {(time.time() - start_time):.3f} seconds')
    return metadata


# DONE 2022.05.19-23.04 embed HTML in message display
# based on https://www.thepythoncode.com/article/use-gmail-api-in-python
def get_email_from_message(msg):
    message = {}
    # return msg  # debug mode
    payload = msg['payload']
    if 'labelIds' in msg:
        labels = msg['labelIds']
    else:
        labels = []
    headers = payload.get("headers")
    message['preview'] = msg.get('snippet')
    parts = payload.get("parts")
    has_subject = False
    if headers:
        # print(headers)
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                message['author'] = re.sub(r'(.*)\s<(.*)>', r'\1', value)
                message['author-address'] = re.sub(r'(.*)\s<(.*)>', r'\2', value)
            if name.lower() == "to": message['to'] = value
            if name.lower() == "subject": message['subject'] = html.unescape(value)
    #         TODO reduce metadata processing redundancy with get_metadata_from_message function
    message['body-html'], message['body-text'] = parse_parts(parts)
    return message


# TODO improve html and text recursive pattern
# see https://www.ehfeng.com/gmail-api-mime-types/ for detail on mime types
def parse_parts(parts):
    """
    Utility function that parses the content of an email partition
    """
    full_text = None  # None becomes null in json objects
    full_html = None
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                body_html, body_text = parse_parts(part.get("parts"))
                full_text = full_text + body_text if full_text else body_text
                full_html = full_html + body_html if full_html else body_html
            if mimeType == "text/plain" and data:
                # if the email part is text plain
                body_text = urlsafe_b64decode(data).decode()
            elif mimeType == "text/html":
                # if the email part is an HTML content
                full_html = urlsafe_b64decode(data).decode('utf-8')
                # print(full_html)
    return full_html, full_text

# TODO write documentation and analysis on gmail api message
