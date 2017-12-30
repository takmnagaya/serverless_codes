import json
import boto3
import re


class AutoScalingLifeCycleEvent:
    def __init__(self, AutoScalingGroupName, EC2InstanceId, Event):
        self.AutoScalingGroupName = AutoScalingGroupName
        self.EC2InstanceId = EC2InstanceId
        self.Event = Event

    def cpu_threshold(self):
        return 80

    def disk_space_threshold(self):
        return 80

    def memory_threshold(self):
        return 80

    def cloudwatch(self):
        return boto3.resource('cloudwatch')

    def cloudwatch_alarms_sns(self):
        return 'arn:aws:sns:ap-northeast-1:000000000000:cloudwatch-alarms'

    def cpu_utilization_alarm_name(self):
        return 'AWS/EC2-CPUUtilization({0})@{1}-{2}'.format(self.cpu_threshold(), self.EC2InstanceId,
                                                            self.AutoScalingGroupName)

    def disk_space_utilization_alarm_name(self):
        return 'System/Linux-DiskSpaceUtilization({0})@{1}-{2}'.format(self.cpu_threshold(), self.EC2InstanceId,
                                                                       self.AutoScalingGroupName)

    def memory_utilization_alarm_name(self):
        return 'System/Linux-MemoryUtilization({0})@{1}-{2}'.format(self.cpu_threshold(), self.EC2InstanceId,
                                                                    self.AutoScalingGroupName)

    def is_terminated(self):
        return re.match("autoscaling:EC2_INSTANCE_TERMINATE", self.Event)

    def is_launched(self):
        return re.match("autoscaling:EC2_INSTANCE_LAUNCH", self.Event)

    def put_alarm_cpu_utilization(self):
        metric = self.cloudwatch().Metric('AWS/EC2', 'CPUUtilization')
        metric.put_alarm(
            AlarmName=self.cpu_utilization_alarm_name(),
            AlarmDescription='CPUUtilization {0} > actual@{1}'.format(self.cpu_threshold(), self.EC2InstanceId),
            OKActions=[
                self.cloudwatch_alarms_sns()
            ],
            AlarmActions=[
                self.cloudwatch_alarms_sns()
            ],
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': '{0}'.format(self.EC2InstanceId)
                }
            ],
            Period=300,
            Unit='Percent',
            EvaluationPeriods=2,
            Threshold=self.cpu_threshold(),
            ComparisonOperator='GreaterThanThreshold',
            TreatMissingData='ignore'
        )

    def put_alarm_disk_space_utilization(self):
        metric = self.cloudwatch().Metric('System/Linux', 'DiskSpaceUtilization')
        metric.put_alarm(
            AlarmName=self.disk_space_utilization_alarm_name(),
            AlarmDescription='DiskSpaceUtilization {0} > actual@{1}'.format(self.disk_space_threshold(),
                                                                            self.EC2InstanceId),
            OKActions=[
                self.cloudwatch_alarms_sns()
            ],
            AlarmActions=[
                self.cloudwatch_alarms_sns()
            ],
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': '{0}'.format(self.EC2InstanceId)
                },
                {
                    'Name': 'MountPath',
                    'Value': '/'
                },
                {
                    'Name': 'Filesystem',
                    'Value': '/dev/xvda1'
                }
            ],
            Period=300,
            Unit='Percent',
            EvaluationPeriods=2,
            Threshold=self.disk_space_threshold(),
            ComparisonOperator='GreaterThanThreshold',
            TreatMissingData='ignore'
        )

    def put_alarm_memory_utilization(self):
        metric = self.cloudwatch().Metric('System/Linux', 'MemoryUtilization')
        metric.put_alarm(
            AlarmName=self.memory_utilization_alarm_name(),
            AlarmDescription='MemoryUtilization {0} > actual@{1}'.format(self.memory_threshold(), self.EC2InstanceId),
            OKActions=[
                self.cloudwatch_alarms_sns()
            ],
            AlarmActions=[
                self.cloudwatch_alarms_sns()
            ],
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': '{0}'.format(self.EC2InstanceId)
                }
            ],
            Period=300,
            Unit='Percent',
            EvaluationPeriods=2,
            Threshold=self.memory_threshold(),
            ComparisonOperator='GreaterThanThreshold',
            TreatMissingData='ignore'
        )

    def put_alarms(self):
        self.put_alarm_cpu_utilization()
        self.put_alarm_disk_space_utilization()
        self.put_alarm_memory_utilization()
        print('Put CloudWatch alarms@{0}'.format(self.EC2InstanceId))

    def delete_alarm_cpu_utilization(self):
        alarm = self.cloudwatch().Alarm(self.cpu_utilization_alarm_name())
        alarm.delete()

    def delete_alarm_disk_space_utilization(self):
        alarm = self.cloudwatch().Alarm(self.disk_space_utilization_alarm_name())
        alarm.delete()

    def delete_alarm_memory_utilization(self):
        alarm = self.cloudwatch().Alarm(self.memory_utilization_alarm_name())
        alarm.delete()

    def delete_alarms(self):
        self.delete_alarm_cpu_utilization()
        self.delete_alarm_disk_space_utilization()
        self.delete_alarm_memory_utilization()
        print('Delete CloudWatch alarms@{0}'.format(self.EC2InstanceId))


def sns_message(event):
    return json.loads(event['Records'][0]['Sns']['Message'])


def create_or_delete_alarms(event, context):
    message = sns_message(event)
    print(message)
    hook_event = AutoScalingLifeCycleEvent(message['AutoScalingGroupName'], message['EC2InstanceId'], message['Event'])
    if hook_event.is_terminated():
        hook_event.delete_alarms()
    elif hook_event.is_launched():
        hook_event.put_alarms()
