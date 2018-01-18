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
        return self.status == 'FAILED'

    def error_code(self):
        return json.loads(self.errorInformation)['ErrorCode']

    def error_message(self):
        return json.loads(self.errorInformation)['ErrorMessage']

    def event_message(self):
        if self.is_failed():
            message = """
@channel デプロイに失敗しました
applicationName: {0}
deploymentGroupName: {1}
deploymentId: {2}
ErrorCode: {3}
ErrorMessage: {4}
            """.format(self.applicationName, self.deploymentGroupName, self.deploymentId,
                       self.error_code(), self.error_message())
        else:
            message = """
@channel デプロイに成功しました
applicationName: {0}
deploymentGroupName: {1}
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
    print(message)
    deploy_event = DeployEvent(message.get('eventTriggerName'), message.get('applicationName'),
                               message.get('deploymentId'),
                               message.get('deploymentGroupName'), message.get('status'),
                               message.get('errorInformation'))
    requests.post(os.environ['SLACK_WEBHOOK_URL'], data=json.dumps({
        'text': deploy_event.event_message(),
        'link_names': 1,  # メンションを有効にする
        'icon_emoji': webhook_icon(deploy_event),
    }))
