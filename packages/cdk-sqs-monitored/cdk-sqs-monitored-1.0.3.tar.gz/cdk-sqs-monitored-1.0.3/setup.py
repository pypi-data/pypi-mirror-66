import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-sqs-monitored",
    "version": "1.0.3",
    "description": "AWS CDK SQS Construct with alarms and dead letter queue",
    "license": "MIT",
    "url": "https://github.com/kamilbiela/cdk-sqs-monitored.git",
    "long_description_content_type": "text/markdown",
    "author": "Kamil Biela<kamil.biela@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/kamilbiela/cdk-sqs-monitored.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_sqs_monitored",
        "cdk_sqs_monitored._jsii"
    ],
    "package_data": {
        "cdk_sqs_monitored._jsii": [
            "cdk-sqs-monitored@1.0.3.jsii.tgz"
        ],
        "cdk_sqs_monitored": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=1.2.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudwatch-actions==1.32.2",
        "aws-cdk.aws-sns==1.32.2",
        "aws-cdk.aws-sns-subscriptions==1.32.2",
        "aws-cdk.aws-sqs==1.32.2",
        "aws-cdk.core==1.32.2",
        "constructs==2.0.1"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
