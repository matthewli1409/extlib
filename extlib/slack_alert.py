import slack

from settings import SLACK_KEY


def send_slack_msg(msg, title, channel, icon_emoji=None):
    """Slack helper function

    Arguments:
        msg {str} -- message to be sent
        title {str} -- title of message
        channel {str} -- channel to send to

    Keyword Arguments:
        icon_emoji {str} -- icon emoji to show on slack avatar (default: {None})
    """
    default_url = 'https://cdn.inprnt.com/thumbs/a2/0b/a20b43443f99849fcf5031393aedcea4@2x.jpg'
    client = slack.WebClient(SLACK_KEY)
    client.chat_postMessage(
        channel=channel,
        icon_emoji=icon_emoji,
        icon_url=default_url,
        parse='full',
        text=msg,
        username=title,
    )
