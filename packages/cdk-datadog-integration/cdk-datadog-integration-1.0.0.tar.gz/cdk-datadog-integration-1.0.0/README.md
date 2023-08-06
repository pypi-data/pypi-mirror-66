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
