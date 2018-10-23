import datetime
import pytz
import random
import re
import string
from faker import Faker
import buzzword_library as bz

# instantiate faker
fake = Faker('en_US')
ORIGINAL_COMMAND = "inspire me"
ALTERNATE_COMMAND = "inspire us"
VOODO_COMMAND = "share your voodoo wisdom"
MEANING_COMMAND = "what is the meaning of life?"
ANACRONYM_COMMAND = "acronize"
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

def get_time():
    tz = pytz.timezone('America/Denver')
    current_time = datetime.datetime.now(tz).hour
    if current_time <= 7:
        return 'too early'
    elif current_time >= 17:
        return 'too late'
    else:
        return 'perfect'


def create_acronym(command):
    """

    :param command:
    :return: acronym list from last word in command
    """
    buzzwords = bz.get_buzzwords()
    word_to_ancronize = command.split()[-1]
    word_to_ancronize = "".join((char for char in word_to_ancronize if char not in string.punctuation)).upper()
    acronym = []
    for char in word_to_ancronize:
        temp = filter(lambda x: x.startswith(char), buzzwords)
        acronym.append(random.choice(temp))
    return acronym


def handle_command(command, channel, speaker, slack_client):
    """
      Executes bot command if the command is known
    """
    random_choice = random.randint(1, 15)

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*, *{}*, or *{}*.".format(ORIGINAL_COMMAND, VOODO_COMMAND, ANACRONYM_COMMAND)

    # Finds and executes the given command, filling in response
    response = None

    if command.startswith(ORIGINAL_COMMAND) or command.startswith(ALTERNATE_COMMAND):
        response = random.choice(['You gain success when you ', 'Try to ', 'Always remember to ',
                                  'Businesses are successful when employees ', 'An agile team is able to ']) \
                   + fake.bs()
        if random_choice == 4:
            response = 'iNsPiRe mE :mockingspongebob:'
    elif command.startswith(VOODO_COMMAND):
        response = random.choice(['Achieve ', 'Capture ', 'Execute ', 'Over-deliver ', 'Gain ',
                                  'Earn Wings Via ', 'Consummate ']) \
                   + fake.catch_phrase().title() + 's'
        if random_choice == 4:
            response = 'sHaRe YoUr VoOdOo WiSdOm :mockingspongebob:'
    elif command.startswith(MEANING_COMMAND):
        response = "Synergy."
    elif command.startswith(ANACRONYM_COMMAND):
        response = create_acronym(command)
    if random_choice == 1 and not command.startswith(ANACRONYM_COMMAND):
        response = response + '... Betcha you feel way more productive now :wink:'
    # Chris easter egg
    if speaker == "W5J6GARJ4" and random_choice == 2:
        response = "Isn't it your job to inspire us?"
    if random_choice == 4:
        response = 'Naw.. I don\'t really feel like it'

    # Working too late or too early
    current_time = get_time()
    if current_time == 'too early':
        response = random.choice(['It is too early for this, I haven\'t even had coffee yet',
                                  'Sorry champ I\'m getting my swoll on at the gym rn',
                                  'Are you trying to get a promotion? Why are you working so early?'])
    elif current_time == 'too late':
        response = random.choice(['Bro! Don\'t you know that work life balance is essential for success? You should not be working this late.',
                                  'It\'s 5 O\'clock somewhere! Specifically here.. See you at the bar!',
                                  'Error 404: Inspiration not found'])

    # Sends the response back to the channel
    if response:
        slack_client.api_call("chat.postMessage", channel=channel, text=response)
    else:
        slack_client.api_call("chat.postMessage", channel=channel, text=default_response)



