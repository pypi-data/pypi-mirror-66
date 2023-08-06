# Slack notifitacions
Slack callback function to send alerts to any channel. It can be use for various errors on critical pieces of data pipelines. 

## Install 
To install it is neccessary python 3.6 or greater, so review it 
`python3 --version`
Then just need to type this
`pip3 install slack-notifications-datateam`

## Test it
To test it you can use the following code `test_slack.py`, just need to replace **webhook_url** and **text** values
```python
from slack_notifications import slack_messages

webhook_url = 'https://hooks.slack.com/services/T00XXXXXX/B000XXXXXXX/XXXxxXXXXxXX0'
text = "Testing slack package. No need to investigate"

slack_messages.send_message(webhook_url=webhook_url,text=text)
```

And the just execute it 