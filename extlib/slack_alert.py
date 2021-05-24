import slack
import os


def send_slack_msg(msg, title, channel):
    """Slack helper function

    Arguments:
        msg {str} -- message to be sent
        title {str} -- title of message
        channel {str} -- channel to send to
    """
    client = slack.WebClient(os.environ['SLACK_KEY'])
    client.chat_postMessage(
        channel=channel,
        icon_url='https://cdn.inprnt.com/thumbs/a2/0b/a20b43443f99849fcf5031393aedcea4@2x.jpg',
        parse='full',
        text=msg,
        username=title,
    )
