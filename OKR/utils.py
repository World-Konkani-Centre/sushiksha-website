import slack
from djangoProject.settings import SLACK_TOKEN


def send_okr_message(array):
    name = array[0]
    date_time = array[1]
    key_result = array[2]
    time_spent = array[3]
    objective = array[4]
    update = array[5]
    image = array[6]
    slack_id = array[7]

    message = {
        'channel': '#okrs',
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": name + " added a new entry to OKR table :okr:",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Objective: * " + objective + "\n*Key Result : * " + key_result + "\n*Date : * " +str(date_time) + "\n*Time Spent: * " + str(time_spent) + "\n*Update : * " + update
                },
                "accessory": {
                    "type": "image",
                    "image_url": image,
                    "alt_text": name
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": f":wkc-badge1: <https://sushiksha.konkanischolarship.com/okr/|Sushiksha OKR> | <@{slack_id}>",
                        "type": "mrkdwn"
                    }
                ]
            }
        ]
    }
    client_obj = slack.WebClient(token=SLACK_TOKEN)
    client_obj.chat_postMessage(**message)
    print('Slack message sent')
