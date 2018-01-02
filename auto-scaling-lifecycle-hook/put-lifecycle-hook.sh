#!/bin/sh

# https://dev.classmethod.jp/cloud/aws/autoscaling-lifecyclehook/ 参考
# auto_scaling_group_name, sns_arn, notification_target_arnは適切な値に設定してください
auto_scaling_group_name=auto-scaling-group-name
sns_arn=arn:aws:sns:ap-northeast-1:0000000000000:auto-scaling-lifecycle
# https://docs.aws.amazon.com/ja_jp/autoscaling/latest/userguide/lifecycle-hooks.html#sns-notifications 参考にIAMロール作成
notification_target_arn=arn:aws:iam::0000000000000:role/NotificationAccessRole

aws autoscaling put-lifecycle-hook \
--lifecycle-hook-name create-cloudwatch-alarms \
--lifecycle-transition autoscaling:EC2_INSTANCE_LAUNCHING \
--heartbeat-timeout 600 \
--default-result CONTINUE \
--auto-scaling-group-name $auto_scaling_group_name \
--notification-target-arn $sns_arn \
--role-arn $notification_target_arn

aws autoscaling put-lifecycle-hook \
--lifecycle-hook-name delete-cloudwatch-alarms \
--lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING \
--heartbeat-timeout 600 \
--default-result CONTINUE \
--auto-scaling-group-name $auto_scaling_group_name \
--notification-target-arn $sns_arn \
--role-arn $notification_target_arn
