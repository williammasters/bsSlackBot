# Posts message to slack channel alerting of a bot restart
from slackclient import SlackClient
import os
import datetime


def slackAlert():
    channel = 'CBMQMKXHB'
    # instantiate Slack client
    slack_client_alert = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    try:
        alert_response = 'BS generator was restarted at {}'.format(datetime.datetime.now())
        slack_client_alert.api_call("chat.postMessage", channel=channel, text=alert_response)
    except:
        print("Connection failed. Exception traceback printed above.")
