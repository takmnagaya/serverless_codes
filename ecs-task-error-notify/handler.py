import json
import requests
import os


class Container:
    def __init__(self, exitCode, lastStatus, name, taskArn):
        self.exitCode = exitCode
        self.lastStatus = lastStatus
        self.name = name
        self.taskArn = taskArn

    def info_message(self):
        message = """
exitCode: {0}
lastStatus: {1}
name: {2}
taskArn: {3}
        """.format(self.exitCode, self.lastStatus, self.name, self.taskArn)
        return message


class TaskEvent:
    def __init__(self, time, container_info):
        self.time = time
        self.container = Container(container_info.get('exitCode'), container_info.get('lastStatus'),
                                   container_info.get('name'), container_info.get('taskArn'))

    def info_message(self):
        message = """
@channel ECSタスクが失敗しました
{0}
        """.format(self.container.info_message())
        return message


def sns_message(event):
    return json.loads(event['Records'][0]['Sns']['Message'])


def webhook_icon():
    return ':rotating_light:'


def slack_webhook_url():
    return os.environ['SLACK_WEBHOOK_URL']


def notify_to_slack(event, context):
    message = sns_message(event)
    print(message)
    event = TaskEvent(message.get('time'), message['detail']['containers'][0])
    requests.post(slack_webhook_url(), data=json.dumps({
        'text': event.info_message(),
        'link_names': 1,  # メンションを有効にする
        'icon_emoji': webhook_icon(),
    }))
