"""
AWS CDK SQS Construct with alarms and dead letter queue

## What it does

Creates:

* two queues, one main and one dead letter. Dead letter has added suffix "--dead-letter" to name passed in `queueSettings.queueName`
* SNS topic with target configured to email from `alarmEmail` parameter
* alarms for both queues

  * for main queue: message age, passed as `alarmWhenMessageOlderThanSeconds` parameter
  * for dead letter: alarm triggered if there is any message

Alarms are configured to be sent as fast as possible. Note that SQS report values to CloudWatch every 5 mins.

## Installation

```bash
npm install --save cdk-sqs-monitored
```

## Usage

Minimal config:

```js
import * as cdk from '@aws-cdk/core';
import * as lib from 'cdk-sqs-monitored';

const app = new cdk.App();

export class SampleAppStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
      super(scope, id, props);

      new lib.MonitoredQueue(this, 'q1', {
          alarmEmail: 'your-email@test.com',
          alarmWhenMessageOlderThanSeconds: 300,
          maxReceiveCount: 3,
          queueSettings: {
              queueName: 'test-queue',
          }
      })
  }
}

new SampleAppStack(app, 'SampleappStack');
```

queueSettings parameter expects standard @aws-cdk/aws-sqs [QueueProps](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html) object

## Modyfying and PR

You're always welcome to create PR, but it might be best solution for you to just fork the repository and apply
the changes in your repo.

## License

MIT
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudwatch_actions
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.aws_sqs
import aws_cdk.core
import constructs

__jsii_assembly__ = jsii.JSIIAssembly.load("cdk-sqs-monitored", "1.0.2", "cdk_sqs_monitored", "cdk-sqs-monitored@1.0.2.jsii.tgz")


class MonitoredQueue(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-sqs-monitored.MonitoredQueue"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, alarm_email: str, alarm_when_message_older_than_seconds: jsii.Number, queue_settings: aws_cdk.aws_sqs.QueueProps, max_receive_count: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param alarm_email: Alarm to which send CloudWatch alarms/ok state changes.
        :param alarm_when_message_older_than_seconds: Issue alarm when message is older than X seconds in queue.
        :param queue_settings: Queue settings as in sqs.QueueProps, deadLetterQueue property is ignored.
        :param max_receive_count: Max receive count of message after which it's moved to dead letter queue. Default: 3
        """
        props = MonitoredQueueProps(alarm_email=alarm_email, alarm_when_message_older_than_seconds=alarm_when_message_older_than_seconds, queue_settings=queue_settings, max_receive_count=max_receive_count)

        jsii.create(MonitoredQueue, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueueArn")
    def dead_letter_queue_arn(self) -> str:
        """
        return
        :return: the Arn of the dead letter queue
        """
        return jsii.get(self, "deadLetterQueueArn")

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueueName")
    def dead_letter_queue_name(self) -> str:
        """
        return
        :return: the name of the dead letter queue
        """
        return jsii.get(self, "deadLetterQueueName")

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueueUrl")
    def dead_letter_queue_url(self) -> str:
        """
        return
        :return: the URL of the dead letter queue
        """
        return jsii.get(self, "deadLetterQueueUrl")

    @builtins.property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """
        return
        :return: the Arn of the main queue
        """
        return jsii.get(self, "queueArn")

    @builtins.property
    @jsii.member(jsii_name="queueName")
    def queue_name(self) -> str:
        """
        return
        :return: the name of the main queue
        """
        return jsii.get(self, "queueName")

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> str:
        """
        return
        :return: the URL of the main queue
        """
        return jsii.get(self, "queueUrl")


@jsii.data_type(jsii_type="cdk-sqs-monitored.MonitoredQueueProps", jsii_struct_bases=[], name_mapping={'alarm_email': 'alarmEmail', 'alarm_when_message_older_than_seconds': 'alarmWhenMessageOlderThanSeconds', 'queue_settings': 'queueSettings', 'max_receive_count': 'maxReceiveCount'})
class MonitoredQueueProps():
    def __init__(self, *, alarm_email: str, alarm_when_message_older_than_seconds: jsii.Number, queue_settings: aws_cdk.aws_sqs.QueueProps, max_receive_count: typing.Optional[jsii.Number]=None):
        """
        :param alarm_email: Alarm to which send CloudWatch alarms/ok state changes.
        :param alarm_when_message_older_than_seconds: Issue alarm when message is older than X seconds in queue.
        :param queue_settings: Queue settings as in sqs.QueueProps, deadLetterQueue property is ignored.
        :param max_receive_count: Max receive count of message after which it's moved to dead letter queue. Default: 3
        """
        if isinstance(queue_settings, dict): queue_settings = aws_cdk.aws_sqs.QueueProps(**queue_settings)
        self._values = {
            'alarm_email': alarm_email,
            'alarm_when_message_older_than_seconds': alarm_when_message_older_than_seconds,
            'queue_settings': queue_settings,
        }
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count

    @builtins.property
    def alarm_email(self) -> str:
        """Alarm to which send CloudWatch alarms/ok state changes."""
        return self._values.get('alarm_email')

    @builtins.property
    def alarm_when_message_older_than_seconds(self) -> jsii.Number:
        """Issue alarm when message is older than X seconds in queue."""
        return self._values.get('alarm_when_message_older_than_seconds')

    @builtins.property
    def queue_settings(self) -> aws_cdk.aws_sqs.QueueProps:
        """Queue settings as in sqs.QueueProps, deadLetterQueue property is ignored."""
        return self._values.get('queue_settings')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """Max receive count of message after which it's moved to dead letter queue.

        default
        :default: 3
        """
        return self._values.get('max_receive_count')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MonitoredQueueProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["MonitoredQueue", "MonitoredQueueProps", "__jsii_assembly__"]

publication.publish()
