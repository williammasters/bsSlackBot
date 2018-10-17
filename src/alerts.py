# Posts message to slack channel alerting of a bot restart
from slackclient import SlackClient
import os
import datetime



def slackAlert():
    channel = 'CBMQMKXHB'
    # instantiate Slack client
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    if slack_client.rtm_connect(with_team_state=False):
        alert_response = 'BS generator was restarted at {}'.format(datetime.datetime.now())
        slack_client.api_call("chat.postMessage", channel=channel, text=alert_response)
    else:
        print("Connection failed. Exception traceback printed above.")
