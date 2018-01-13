import json
import requests
import os


def webhook_icon():
    return ':rotating_light:'

def notification_message(message):
    return """
@channel CloudWatch Logsでエラーが検出されました。担当者はご確認ください。
AlarmName: {0},
AlarmDescription: {1},
StateChangeTime: {2}
    """.format(message.get('AlarmName'), message.get('AlarmDescription'), message.get('StateChangeTime'))

# {
#     "AlarmName": "sample-error",
#     "AlarmDescription": "sampleでエラーが発生しました。",
#     "AWSAccountId": "xxxxxxxxxxxx",
#     "NewStateValue": "ALARM",
#     "NewStateReason": "Threshold Crossed: 1 datapoint [2.0 (29/11/17 01:09:00)] was greater than or equal to the threshold (1.0).",
#     "StateChangeTime": "2017-11-29T01:10:32.907+0000",
#     "Region": "Asia Pacific (Tokyo)",
#     "OldStateValue": "OK",
#     "Trigger": {
#         "MetricName": "sample-metric",
#         "Namespace": "LogMetrics",
#         "StatisticType": "Statistic",
#         "Statistic": "SUM",
#         "Unit": null,
#         "Dimensions": [],
#         "Period": 60,
#         "EvaluationPeriods": 1,
#         "ComparisonOperator": "GreaterThanOrEqualToThreshold",
#         "Threshold": 1,
#         "TreatMissingData": "- TreatMissingData:                    NonBreaching",
#         "EvaluateLowSampleCountPercentile": ""
#     }
# }
def sns_message(event):
    return json.loads(event['Records'][0]['Sns']['Message'])


def server_error(event, context):
    message = sns_message(event)
    print(message)
    requests.post(os.environ['SLACK_WEBHOOK_URL'], data=json.dumps({
        'text': notification_message(message),
        'link_names': 1,  # メンションを有効にする
        'icon_emoji': webhook_icon(),
    }))
