"""
# AWS Cloud Development Kit (CDK) Datadog Integration

This construct makes it easy to integrate your AWS account with Datadog. It
creates nested stacks based on the official
[Datadog Cloudformation templates](https://github.com/DataDog/cloudformation-template/blob/master/aws/main.yaml)
using [Amazon Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/).

## Basic Usage

1. Install the package

```console
npm i --save cdk-datadog-integration
```

1. Import the stack and pass the required parameters.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import aws_cdk.aws_secretsmanager as secrets
from cdk_datadog_integration import DatadogIntegrationStack

app = cdk.App()
DatadogIntegrationStack(app, "DatadogIntegration",
    # Generate an ID here: https://app.datadoghq.com/account/settings#integrations/amazon-web-services
    external_id="",

    # Create or lookup a `Secret` that contains your Datadog API Key
    # Get your API key here: https://app.datadoghq.com/account/settings#api
    api_key=secrets.Secret.from_secret_arn(app, "DatadogApiKey", "arn:aws:secretsmanager:<your region>:<your account>:secret:<your secret name>")
)
```

## Configuration

Use `DatadogIntegrationConfig` to set additional configuration parameters.
Check out [docs](https://github.com/blimmer/cdk-datadog-integration/blob/master/docs/interfaces/datadogintegrationconfig.md)
for more details on what's available.

## Contributing

PRs are welcome!

### Releasing

To release, use `npm version` and push the tag.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_cloudformation
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core

from ._jsii import *


@jsii.data_type(jsii_type="cdk-datadog-integration.DatadogIntegrationConfig", jsii_struct_bases=[], name_mapping={'api_key': 'apiKey', 'external_id': 'externalId', 'additional_forwarder_params': 'additionalForwarderParams', 'additional_integration_role_params': 'additionalIntegrationRoleParams', 'cloud_trails': 'cloudTrails', 'forwarder_name': 'forwarderName', 'forwarder_version': 'forwarderVersion', 'iam_role_name': 'iamRoleName', 'install_datadog_policy_macro': 'installDatadogPolicyMacro', 'log_archives': 'logArchives', 'permissions': 'permissions', 'site': 'site'})
class DatadogIntegrationConfig():
    def __init__(self, *, api_key: aws_cdk.aws_secretsmanager.ISecret, external_id: str, additional_forwarder_params: typing.Optional[typing.Mapping[str, str]]=None, additional_integration_role_params: typing.Optional[typing.Mapping[str, str]]=None, cloud_trails: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, forwarder_name: typing.Optional[str]=None, forwarder_version: typing.Optional[str]=None, iam_role_name: typing.Optional[str]=None, install_datadog_policy_macro: typing.Optional[bool]=None, log_archives: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, permissions: typing.Optional[str]=None, site: typing.Optional[str]=None) -> None:
        """
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        """
        self._values = {
            'api_key': api_key,
            'external_id': external_id,
        }
        if additional_forwarder_params is not None: self._values["additional_forwarder_params"] = additional_forwarder_params
        if additional_integration_role_params is not None: self._values["additional_integration_role_params"] = additional_integration_role_params
        if cloud_trails is not None: self._values["cloud_trails"] = cloud_trails
        if forwarder_name is not None: self._values["forwarder_name"] = forwarder_name
        if forwarder_version is not None: self._values["forwarder_version"] = forwarder_version
        if iam_role_name is not None: self._values["iam_role_name"] = iam_role_name
        if install_datadog_policy_macro is not None: self._values["install_datadog_policy_macro"] = install_datadog_policy_macro
        if log_archives is not None: self._values["log_archives"] = log_archives
        if permissions is not None: self._values["permissions"] = permissions
        if site is not None: self._values["site"] = site

    @builtins.property
    def api_key(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api)."""
        return self._values.get('api_key')

    @builtins.property
    def external_id(self) -> str:
        """External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services)."""
        return self._values.get('external_id')

    @builtins.property
    def additional_forwarder_params(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional parameters to pass through to the underlying Forwarder CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml
        for the latest parameters.
        """
        return self._values.get('additional_forwarder_params')

    @builtins.property
    def additional_integration_role_params(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional parameters to pass through to the underlying Integration Role CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml
        for the latest parameters.
        """
        return self._values.get('additional_integration_role_params')

    @builtins.property
    def cloud_trails(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        """S3 buckets for Datadog CloudTrail integration.

        Permissions will be automatically
        added to the Datadog integration IAM role.
        https://docs.datadoghq.com/integrations/amazon_cloudtrail
        """
        return self._values.get('cloud_trails')

    @builtins.property
    def forwarder_name(self) -> typing.Optional[str]:
        """The Datadog Forwarder Lambda function name.

        DO NOT change when updating an existing
        CloudFormation stack, otherwise the current forwarder function will be replaced and
        all the triggers will be lost.

        default
        :default: DatadogForwarder
        """
        return self._values.get('forwarder_name')

    @builtins.property
    def forwarder_version(self) -> typing.Optional[str]:
        """Specify a version of the forwarder to use.

        See
        https://github.com/DataDog/datadog-serverless-functions/releases. Pass this
        parameter as a version string, e.g., '3.9.0'

        default
        :default: latest
        """
        return self._values.get('forwarder_version')

    @builtins.property
    def iam_role_name(self) -> typing.Optional[str]:
        """Customize the name of IAM role for Datadog AWS integration.

        default
        :default: DatadogIntegrationRole
        """
        return self._values.get('iam_role_name')

    @builtins.property
    def install_datadog_policy_macro(self) -> typing.Optional[bool]:
        """If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again.

        default
        :default: true
        """
        return self._values.get('install_datadog_policy_macro')

    @builtins.property
    def log_archives(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        """S3 paths to store log archives for log rehydration.

        Permissions will be automatically added to the Datadog integration IAM role.
        https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        """
        return self._values.get('log_archives')

    @builtins.property
    def permissions(self) -> typing.Optional[str]:
        """Customize the permission level for the Datadog IAM role.

        Select "Core" to only grant Datadog read-only permissions (not recommended).

        default
        :default: Full
        """
        return self._values.get('permissions')

    @builtins.property
    def site(self) -> typing.Optional[str]:
        """Define your Datadog Site to send data to.

        For the Datadog EU site, set to datadoghq.eu

        default
        :default: datadoghq.com
        """
        return self._values.get('site')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatadogIntegrationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DatadogIntegrationStack(aws_cdk.core.Stack, metaclass=jsii.JSIIMeta, jsii_type="cdk-datadog-integration.DatadogIntegrationStack"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key: aws_cdk.aws_secretsmanager.ISecret, external_id: str, additional_forwarder_params: typing.Optional[typing.Mapping[str, str]]=None, additional_integration_role_params: typing.Optional[typing.Mapping[str, str]]=None, cloud_trails: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, forwarder_name: typing.Optional[str]=None, forwarder_version: typing.Optional[str]=None, iam_role_name: typing.Optional[str]=None, install_datadog_policy_macro: typing.Optional[bool]=None, log_archives: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, permissions: typing.Optional[str]=None, site: typing.Optional[str]=None, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        """
        props = DatadogIntegrationStackConfig(api_key=api_key, external_id=external_id, additional_forwarder_params=additional_forwarder_params, additional_integration_role_params=additional_integration_role_params, cloud_trails=cloud_trails, forwarder_name=forwarder_name, forwarder_version=forwarder_version, iam_role_name=iam_role_name, install_datadog_policy_macro=install_datadog_policy_macro, log_archives=log_archives, permissions=permissions, site=site, description=description, env=env, stack_name=stack_name, tags=tags)

        jsii.create(DatadogIntegrationStack, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-datadog-integration.DatadogIntegrationStackConfig", jsii_struct_bases=[DatadogIntegrationConfig, aws_cdk.core.StackProps], name_mapping={'api_key': 'apiKey', 'external_id': 'externalId', 'additional_forwarder_params': 'additionalForwarderParams', 'additional_integration_role_params': 'additionalIntegrationRoleParams', 'cloud_trails': 'cloudTrails', 'forwarder_name': 'forwarderName', 'forwarder_version': 'forwarderVersion', 'iam_role_name': 'iamRoleName', 'install_datadog_policy_macro': 'installDatadogPolicyMacro', 'log_archives': 'logArchives', 'permissions': 'permissions', 'site': 'site', 'description': 'description', 'env': 'env', 'stack_name': 'stackName', 'tags': 'tags'})
class DatadogIntegrationStackConfig(DatadogIntegrationConfig, aws_cdk.core.StackProps):
    def __init__(self, *, api_key: aws_cdk.aws_secretsmanager.ISecret, external_id: str, additional_forwarder_params: typing.Optional[typing.Mapping[str, str]]=None, additional_integration_role_params: typing.Optional[typing.Mapping[str, str]]=None, cloud_trails: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, forwarder_name: typing.Optional[str]=None, forwarder_version: typing.Optional[str]=None, iam_role_name: typing.Optional[str]=None, install_datadog_policy_macro: typing.Optional[bool]=None, log_archives: typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]=None, permissions: typing.Optional[str]=None, site: typing.Optional[str]=None, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[str, str]]=None) -> None:
        """
        :param api_key: API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api).
        :param external_id: External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services).
        :param additional_forwarder_params: Additional parameters to pass through to the underlying Forwarder CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml for the latest parameters.
        :param additional_integration_role_params: Additional parameters to pass through to the underlying Integration Role CloudFormation template. Use this construct if you need to specify a template variable not yet exposed through this library. See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml for the latest parameters.
        :param cloud_trails: S3 buckets for Datadog CloudTrail integration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/integrations/amazon_cloudtrail
        :param forwarder_name: The Datadog Forwarder Lambda function name. DO NOT change when updating an existing CloudFormation stack, otherwise the current forwarder function will be replaced and all the triggers will be lost. Default: DatadogForwarder
        :param forwarder_version: Specify a version of the forwarder to use. See https://github.com/DataDog/datadog-serverless-functions/releases. Pass this parameter as a version string, e.g., '3.9.0' Default: latest
        :param iam_role_name: Customize the name of IAM role for Datadog AWS integration. Default: DatadogIntegrationRole
        :param install_datadog_policy_macro: If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again. Default: true
        :param log_archives: S3 paths to store log archives for log rehydration. Permissions will be automatically added to the Datadog integration IAM role. https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        :param permissions: Customize the permission level for the Datadog IAM role. Select "Core" to only grant Datadog read-only permissions (not recommended). Default: Full
        :param site: Define your Datadog Site to send data to. For the Datadog EU site, set to datadoghq.eu Default: datadoghq.com
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        """
        if isinstance(env, dict): env = aws_cdk.core.Environment(**env)
        self._values = {
            'api_key': api_key,
            'external_id': external_id,
        }
        if additional_forwarder_params is not None: self._values["additional_forwarder_params"] = additional_forwarder_params
        if additional_integration_role_params is not None: self._values["additional_integration_role_params"] = additional_integration_role_params
        if cloud_trails is not None: self._values["cloud_trails"] = cloud_trails
        if forwarder_name is not None: self._values["forwarder_name"] = forwarder_name
        if forwarder_version is not None: self._values["forwarder_version"] = forwarder_version
        if iam_role_name is not None: self._values["iam_role_name"] = iam_role_name
        if install_datadog_policy_macro is not None: self._values["install_datadog_policy_macro"] = install_datadog_policy_macro
        if log_archives is not None: self._values["log_archives"] = log_archives
        if permissions is not None: self._values["permissions"] = permissions
        if site is not None: self._values["site"] = site
        if description is not None: self._values["description"] = description
        if env is not None: self._values["env"] = env
        if stack_name is not None: self._values["stack_name"] = stack_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def api_key(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """API key for the Datadog account (find at https://app.datadoghq.com/account/settings#api)."""
        return self._values.get('api_key')

    @builtins.property
    def external_id(self) -> str:
        """External ID for the Datadog role (generate at https://app.datadoghq.com/account/settings#integrations/amazon-web-services)."""
        return self._values.get('external_id')

    @builtins.property
    def additional_forwarder_params(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional parameters to pass through to the underlying Forwarder CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/forwarder/latest.yaml
        for the latest parameters.
        """
        return self._values.get('additional_forwarder_params')

    @builtins.property
    def additional_integration_role_params(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Additional parameters to pass through to the underlying Integration Role CloudFormation template.

        Use this construct if you need to specify a template variable not
        yet exposed through this library.

        See https://datadog-cloudformation-template.s3.amazonaws.com/aws/datadog_integration_role.yaml
        for the latest parameters.
        """
        return self._values.get('additional_integration_role_params')

    @builtins.property
    def cloud_trails(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        """S3 buckets for Datadog CloudTrail integration.

        Permissions will be automatically
        added to the Datadog integration IAM role.
        https://docs.datadoghq.com/integrations/amazon_cloudtrail
        """
        return self._values.get('cloud_trails')

    @builtins.property
    def forwarder_name(self) -> typing.Optional[str]:
        """The Datadog Forwarder Lambda function name.

        DO NOT change when updating an existing
        CloudFormation stack, otherwise the current forwarder function will be replaced and
        all the triggers will be lost.

        default
        :default: DatadogForwarder
        """
        return self._values.get('forwarder_name')

    @builtins.property
    def forwarder_version(self) -> typing.Optional[str]:
        """Specify a version of the forwarder to use.

        See
        https://github.com/DataDog/datadog-serverless-functions/releases. Pass this
        parameter as a version string, e.g., '3.9.0'

        default
        :default: latest
        """
        return self._values.get('forwarder_version')

    @builtins.property
    def iam_role_name(self) -> typing.Optional[str]:
        """Customize the name of IAM role for Datadog AWS integration.

        default
        :default: DatadogIntegrationRole
        """
        return self._values.get('iam_role_name')

    @builtins.property
    def install_datadog_policy_macro(self) -> typing.Optional[bool]:
        """If you already deployed a stack using this template, set this parameter to false to skip the installation of the DatadogPolicy Macro again.

        default
        :default: true
        """
        return self._values.get('install_datadog_policy_macro')

    @builtins.property
    def log_archives(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.Bucket]]:
        """S3 paths to store log archives for log rehydration.

        Permissions will be automatically added to the Datadog integration IAM role.
        https://docs.datadoghq.com/logs/archives/rehydrating/?tab=awss
        """
        return self._values.get('log_archives')

    @builtins.property
    def permissions(self) -> typing.Optional[str]:
        """Customize the permission level for the Datadog IAM role.

        Select "Core" to only grant Datadog read-only permissions (not recommended).

        default
        :default: Full
        """
        return self._values.get('permissions')

    @builtins.property
    def site(self) -> typing.Optional[str]:
        """Define your Datadog Site to send data to.

        For the Datadog EU site, set to datadoghq.eu

        default
        :default: datadoghq.com
        """
        return self._values.get('site')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the stack.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.core.Environment]:
        """The AWS environment (account/region) where this stack will be deployed.

        default
        :default:

        - The ``default-account`` and ``default-region`` context parameters will be
          used. If they are undefined, it will not be possible to deploy the stack.
        """
        return self._values.get('env')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """Name to deploy the stack with.

        default
        :default: - Derived from construct path.
        """
        return self._values.get('stack_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Stack tags that will be applied to all the taggable resources and the stack itself.

        default
        :default: {}
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatadogIntegrationStackConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "DatadogIntegrationConfig",
    "DatadogIntegrationStack",
    "DatadogIntegrationStackConfig",
]

publication.publish()
