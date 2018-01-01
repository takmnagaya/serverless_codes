import json
import requests
import os


class DeployEvent:
    def __init__(self, eventTriggerName, applicationName, deploymentId, deploymentGroupName, status, errorInformation):
        self.eventTriggerName = eventTriggerName
        self.applicationName = applicationName
        self.deploymentId = deploymentId
        self.deploymentGroupName = deploymentGroupName
        self.status = status
        self.errorInformation = errorInformation

    def is_failed(self):
        return self.status == 'Failed'

    def event_message(self):
        if self.is_failed():
            message = """
            @channel {0} {1}のデプロイに失敗しました
            deploymentId: {2}
            ErrorCode: {3}
            ErrorMessage: {4}
            """.format(self.applicationName, self.deploymentGroupName, self.deploymentId,
                       self.errorInformation['ErrorCode'], self.errorInformation['ErrorMessage'])
        else:
            message = """
            @channel {0} {1}のデプロイに成功しました
            deploymentId: {2}
            """.format(self.applicationName, self.deploymentGroupName, self.deploymentId)
        return message


def sns_message(event):
    return json.loads(event['Records'][0]['Sns']['Message'])


def webhook_icon(event):
    if event.is_failed():
        return ':rotating_light:'
    else:
        return ':white_check_mark:'


def notify_to_slack(event, context):
    message = sns_message(event)
    deploy_event = DeployEvent(message['eventTriggerName'], message['applicationName'], message['deploymentId'],
                               message['deploymentGroupName'], message['status'], message['errorInformation'])
    requests.post(os.environ['SLACK_WEBHOOK_URL'], data=json.dumps({
        'text': deploy_event.event_message(),
        'link_names': 1,  # メンションを有効にする
        'icon_emoji': webhook_icon(deploy_event),
    }))
