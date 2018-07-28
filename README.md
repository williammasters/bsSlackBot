# BS SlackBot

This slackbot's purpose is to post motivational and synergistic phrases o a workspace leveraging the faker package in python. Currently it responds to "@BSgenerator inspire me" posting a 3 word randomly generated phrase. Support for more features and functionality will come over time.

## Installation insructions
Currently working on a way to make the app one click deployment to workspaces, but right now installation is still fairly easy to install on your workspace's servers.

1. Install required packages into the server you wish to run the bot from requirements.txt
2. Using the slack app to generate OAuth tokens run the command `export SLACK_BOT_TOKEN='your bot user access token here'`
3. Run the bot with `nohup python bsPot.py &` 
