import json
from typing import Optional

import requests

def send_message(webhook_url: Optiona[str] = None, text: Optional[str] = None, fail = False, **kwargs) -> None: 

    if webhook_url is None:
            raise ValueError('No valid Slack token.')
    if text is None:
        raise ValueError('A text is needed.')
    
    slack_data = {
        "text": text,
        **kwargs
    }

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )
    if fail and response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )