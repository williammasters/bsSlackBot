#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 9 22:18:12 2018
​
@author: wmaste756
"""
import os
import time
import bot_functions as bf
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, speaker = bf.parse_bot_commands(slack_client.rtm_read(), starterbot_id)
            if command:
                bf.handle_command(command, channel, speaker, slack_client)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")