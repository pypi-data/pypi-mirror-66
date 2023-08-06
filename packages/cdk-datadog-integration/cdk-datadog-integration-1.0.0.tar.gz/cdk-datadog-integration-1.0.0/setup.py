import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-datadog-integration",
    "version": "1.0.0",
    "description": "cdk-datadog-integration",
    "license": "Apache-2.0",
    "url": "https://github.com/blimmer/cdk-datadog-integration.git",
    "long_description_content_type": "text/markdown",
    "author": "Ben Limmer",
    "project_urls": {
        "Source": "https://github.com/blimmer/cdk-datadog-integration.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_datadog_integration",
        "cdk_datadog_integration._jsii"
    ],
    "package_data": {
        "cdk_datadog_integration._jsii": [
            "cdk-datadog-integration@1.0.0.jsii.tgz"
        ],
        "cdk_datadog_integration": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.4.1, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation>=1.35.0, <2.0.0",
        "aws-cdk.aws-s3>=1.35.0, <2.0.0",
        "aws-cdk.aws-secretsmanager>=1.35.0, <2.0.0",
        "aws-cdk.core==1.35.0"
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
