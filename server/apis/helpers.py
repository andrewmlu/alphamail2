import html
import re
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
import sys

verbose = 0

def get_ids(service, user_id='me', labels=[], quantity=sys.maxsize):
    """
    Retrieves all IDs of emails by parsing through each
    page of email IDs given an API connection.

    Parameters:
    service -- gmail API connection
    user_id -- user ID of messages to retrieve
    labels -- labels for which to retrieve messages
    quantity -- number of email ids to retrieve (default to all)

    Returns:
    list of email message IDs based on specified criteria
    """
    count = quantity
    start_time = time.time()
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
        print(f'get_ids execution time: {(time.time() - start_time):.3f} seconds')
        return [msg['id'] for msg in msgs_list]
    except Exception as error:
        print('An error occurred here: %s' % error)

# DONE 2022.05.19-12.23 fix &#39; &quot; and other characters in preview (and maybe subject?)
# DONE 2022.05.19-12.43 fix author field to exclude <email@address.com> for initial display, but pass in separately
def get_metadata_from_id(service, message_id, user_id='me'):
    msg = service.users().messages().get(userId=user_id, id=message_id, format='metadata').execute()
    metadata = {}

    payload = msg['payload']
    headers = payload.get("headers")

    metadata['id'] = msg['id']
    metadata['preview'] = html.unescape(msg.get('snippet'))

    if 'labelIds' in msg: metadata['labels'] = msg['labelIds']
    else: metadata['labels'] = []

    if 'IMPORTANT' in metadata['labels']: metadata['type'] = 'important'
    else: metadata['type'] = 'unimportant'

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                metadata['author'] = re.sub(r'(.*)\s<(.*)>', r'\1', value)  # based on alphamail-v0.2 helpers.py and https://docs.python.org/3/library/re.html
                metadata['author-address'] = re.sub(r'(.*)\s<(.*)>', r'\2', value)  # for context on r operator, see https://stackoverflow.com/questions/26163798/using-r-with-string-literals-in-python
            if name.lower() == "to": metadata['to'] = value
            if name.lower() == "subject": metadata['subject'] = html.unescape(value)
    metadata['date'] = msg['internalDate']
    if verbose >= 1: print("=" * 50)
    return metadata

# for any low-level data tasks
def get_raw_data_from_id(service, id, user_id='me', format=format):
    return service.users().messages().get(userId=user_id, id=id, format=format).execute()


# DONE 2022.05.19-12.59 track execution runtime
# TODO optimize through multithreading https://stackoverflow.com/questions/16982569/making-multiple-api-calls-in-parallel-using-python-ipython & https://medium.com/swlh/parallel-asynchronous-api-call-in-python-f6aa663206c6
# TODO consider using batch operations https://stackoverflow.com/questions/65730876/gmail-api-how-can-i-get-the-message-body
def get_metadata_from_ids(service, ids, user_id='me'):
    start_time = time.time()
    metadata = []
    count = 0
    for id in ids:
        metadata.append(get_metadata_from_id(service, id, user_id=user_id))
        count += 1
        if count % 50 == 0:
            print(f'{count}/{len(ids)}: {(time.time()-start_time):.3f} seconds')
    print(f'get_metadata_from_ids execution time: {(time.time()-start_time):.3f} seconds')  # see https://stackoverflow.com/questions/1995615/how-can-i-format-a-decimal-to-always-show-2-decimal-places
    return metadata

# DONE 2022.05.19-23.04 embed HTML in message display
# based on https://www.thepythoncode.com/article/use-gmail-api-in-python
def get_email_from_id(service, id, user_id='me'):
    message = {}
    msg = service.users().messages().get(userId=user_id, id=id, format='full').execute()
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
    message['body-html'], message['body-text'] = parse_parts(service, parts)
    return message

# TODO improve html and text recursive pattern
# see https://www.ehfeng.com/gmail-api-mime-types/ for detail on mime types
def parse_parts(service, parts):
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
                body_html, body_text = parse_parts(service, part.get("parts"))
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