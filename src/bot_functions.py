import random
import re
from faker import Faker

# instantiate faker
fake = Faker('en_US')
ORIGINAL_COMMAND = "inspire me"
VOODO_COMMAND = "share your voodoo wisdom"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events, starterbot_id):
    """
      Parses a list of events coming from the Slack RTM API to find bot commands.
      If a bot command is found, this function returns a tuple of command and channel.
      If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            speaker = event["user"]
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"], speaker
    return None, None, None


def parse_direct_mention(message_text):
    """
      Finds a direct mention (a mention that is at the beginning) in message text
      and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel, speaker, slack_client):
    """
      Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(ORIGINAL_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(ORIGINAL_COMMAND):
        response = random.choice(['You gain success when you +', 'Try to ', 'Always remember to ', 'Businesses are successful when employees ', 'An agile team is able to ']) \
                   + fake.bs()
    elif command.startswith(VOODO_COMMAND):
        response = random.choice(['Achieve ', 'Capture ', 'Execute ', 'Over-deliver ', 'Gain ', 'Earn Wings Via ', 'Consummate ']) + fake.catch_phrase().title() + 's'
    random_choice = random.randint(1, 5)
    if random_choice == 1:
        response = response + '... Betcha you feel way more productive now ;)'
    # Sends the response back to the channel
    if speaker == "W5J6GARJ4" and random_choice == 2:
        response = "Isn't it your job to inspire us?"
    if response:
        slack_client.api_call("chat.postMessage", channel=channel, text=response)
    else:
        slack_client.api_call("chat.postMessage", channel=channel, text=default_response)



