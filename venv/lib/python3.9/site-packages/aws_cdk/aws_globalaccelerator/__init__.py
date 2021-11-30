'''
# AWS::GlobalAccelerator Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Introduction

AWS Global Accelerator (AGA) is a service that improves the availability and performance of your applications with local or global users. It provides static IP addresses that act as a fixed entry point to your application endpoints in a single or multiple AWS Regions, such as your Application Load Balancers, Network Load Balancers or Amazon EC2 instances.

This module supports features under [AWS Global Accelerator](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GlobalAccelerator.html) that allows users set up resources using the `@aws-cdk/aws-globalaccelerator` module.

## Accelerator

The `Accelerator` resource is a Global Accelerator resource type that contains information about how you create an accelerator. An accelerator includes one or more listeners that process inbound connections and direct traffic to one or more endpoint groups, each of which includes endpoints, such as Application Load Balancers, Network Load Balancers, and Amazon EC2 instances.

To create the `Accelerator`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_globalaccelerator as globalaccelerator

globalaccelerator.Accelerator(stack, "Accelerator")
```

## Listener

The `Listener` resource is a Global Accelerator resource type that contains information about how you create a listener to process inbound connections from clients to an accelerator. Connections arrive to assigned static IP addresses on a port, port range, or list of port ranges that you specify.

To create the `Listener` listening on TCP 80:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
globalaccelerator.Listener(stack, "Listener",
    accelerator=accelerator,
    port_ranges=[{
        "from_port": 80,
        "to_port": 80
    }
    ]
)
```

## EndpointGroup

The `EndpointGroup` resource is a Global Accelerator resource type that contains information about how you create an endpoint group for the specified listener. An endpoint group is a collection of endpoints in one AWS Region.

To create the `EndpointGroup`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
globalaccelerator.EndpointGroup(stack, "Group", listener=listener)
```

## Add Endpoint into EndpointGroup

You may use the following methods to add endpoints into the `EndpointGroup`:

* `addEndpoint` to add a generic `endpoint` into the `EndpointGroup`.
* `addLoadBalancer` to add an Application Load Balancer or Network Load Balancer.
* `addEc2Instance` to add an EC2 Instance.
* `addElasticIpAddress` to add an Elastic IP Address.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
endpoint_group = globalaccelerator.EndpointGroup(stack, "Group", listener=listener)
alb = elbv2.ApplicationLoadBalancer(stack, "ALB", vpc=vpc, internet_facing=True)
nlb = elbv2.NetworkLoadBalancer(stack, "NLB", vpc=vpc, internet_facing=True)
eip = ec2.CfnEIP(stack, "ElasticIpAddress")
instances = Array()for ( let i = 0; i < 2; i++) {
  instances.push(new ec2.Instance(stack, `Instance${i}`, {
    vpc,
    machineImage: new ec2.AmazonLinuxImage(),
    instanceType: new ec2.InstanceType('t3.small'),
  }));
}

endpoint_group.add_load_balancer("AlbEndpoint", alb)
endpoint_group.add_load_balancer("NlbEndpoint", nlb)
endpoint_group.add_elastic_ip_address("EipEndpoint", eip)
endpoint_group.add_ec2_instance("InstanceEndpoint", instances[0])
endpoint_group.add_endpoint("InstanceEndpoint2", instances[1].instance_id)
```

## Accelerator Security Groups

When using certain AGA features (client IP address preservation), AGA creates elastic network interfaces (ENI) in your AWS account which are
associated with a Security Group, and which are reused for all AGAs associated with that VPC. Per the
[best practices](https://docs.aws.amazon.com/global-accelerator/latest/dg/best-practices-aga.html) page, AGA creates a specific security group
called `GlobalAccelerator` for each VPC it has an ENI in. You can use the security group created by AGA as a source group in other security
groups, such as those for EC2 instances or Elastic Load Balancers, in order to implement least-privilege security group rules.

CloudFormation doesn't support referencing the security group created by AGA. CDK has a library that enables you to reference the AGA security group
for a VPC using an AwsCustomResource.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = Vpc(stack, "VPC")
alb = elbv2.ApplicationLoadBalancer(stack, "ALB", vpc=vpc, internet_facing=False)
accelerator = ga.Accelerator(stack, "Accelerator")
listener = ga.Listener(stack, "Listener",
    accelerator=accelerator,
    port_ranges=[{
        "from_port": 443,
        "to_port": 443
    }
    ]
)
endpoint_group = ga.EndpointGroup(stack, "Group", listener=listener)
endpoint_group.add_load_balancer("AlbEndpoint", alb)

# Remember that there is only one AGA security group per VPC.
# This code will fail at CloudFormation deployment time if you do not have an AGA
aga_sg = ga.AcceleratorSecurityGroup.from_vpc(stack, "GlobalAcceleratorSG", vpc)

# Allow connections from the AGA to the ALB
alb.connections.allow_from(aga_sg, Port.tcp(443))
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.AcceleratorAttributes",
    jsii_struct_bases=[],
    name_mapping={"accelerator_arn": "acceleratorArn", "dns_name": "dnsName"},
)
class AcceleratorAttributes:
    def __init__(
        self,
        *,
        accelerator_arn: builtins.str,
        dns_name: builtins.str,
    ) -> None:
        '''(experimental) Attributes required to import an existing accelerator to the stack.

        :param accelerator_arn: (experimental) The ARN of the accelerator.
        :param dns_name: (experimental) The DNS name of the accelerator.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_arn": accelerator_arn,
            "dns_name": dns_name,
        }

    @builtins.property
    def accelerator_arn(self) -> builtins.str:
        '''(experimental) The ARN of the accelerator.

        :stability: experimental
        '''
        result = self._values.get("accelerator_arn")
        assert result is not None, "Required property 'accelerator_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_name(self) -> builtins.str:
        '''(experimental) The DNS name of the accelerator.

        :stability: experimental
        '''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceleratorAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.AcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={"accelerator_name": "acceleratorName", "enabled": "enabled"},
)
class AcceleratorProps:
    def __init__(
        self,
        *,
        accelerator_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Construct properties of the Accelerator.

        :param accelerator_name: (experimental) The name of the accelerator. Default: - resource ID
        :param enabled: (experimental) Indicates whether the accelerator is enabled. Default: true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if accelerator_name is not None:
            self._values["accelerator_name"] = accelerator_name
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def accelerator_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the accelerator.

        :default: - resource ID

        :stability: experimental
        '''
        result = self._values.get("accelerator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the accelerator is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AcceleratorSecurityGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.AcceleratorSecurityGroup",
):
    '''(experimental) The security group used by a Global Accelerator to send traffic to resources in a VPC.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromVpc") # type: ignore[misc]
    @builtins.classmethod
    def from_vpc(
        cls,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
        endpoint_group: "EndpointGroup",
    ) -> aws_cdk.aws_ec2.ISecurityGroup:
        '''(experimental) Lookup the Global Accelerator security group at CloudFormation deployment time.

        As of this writing, Global Accelerators (AGA) create a single security group per VPC. AGA security groups are shared
        by all AGAs in an account. Additionally, there is no CloudFormation mechanism to reference the AGA security groups.

        This makes creating security group rules which allow traffic from an AGA complicated in CDK. This lookup will identify
        the AGA security group for a given VPC at CloudFormation deployment time, and lets you create rules for traffic from AGA
        to other resources created by CDK.

        :param scope: -
        :param id: -
        :param vpc: -
        :param endpoint_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.ISecurityGroup, jsii.sinvoke(cls, "fromVpc", [scope, id, vpc, endpoint_group]))


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccelerator(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnAccelerator",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::Accelerator``.

    :cloudformationResource: AWS::GlobalAccelerator::Accelerator
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ip_addresses: typing.Optional[typing.List[builtins.str]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::Accelerator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.
        '''
        props = CfnAcceleratorProps(
            name=name,
            enabled=enabled,
            ip_addresses=ip_addresses,
            ip_address_type=ip_address_type,
            tags=tags,
        )

        jsii.create(CfnAccelerator, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAcceleratorArn")
    def attr_accelerator_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AcceleratorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAcceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Accelerator.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::GlobalAccelerator::Accelerator.Enabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "ipAddresses", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ipAddressType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnAcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "enabled": "enabled",
        "ip_addresses": "ipAddresses",
        "ip_address_type": "ipAddressType",
        "tags": "tags",
    },
)
class CfnAcceleratorProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ip_addresses: typing.Optional[typing.List[builtins.str]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::Accelerator``.

        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Accelerator.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::GlobalAccelerator::Accelerator.Enabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpointGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::EndpointGroup``.

    :cloudformationResource: AWS::GlobalAccelerator::EndpointGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        endpoint_group_region: builtins.str,
        listener_arn: builtins.str,
        endpoint_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        port_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::EndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param port_overrides: ``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.
        '''
        props = CfnEndpointGroupProps(
            endpoint_group_region=endpoint_group_region,
            listener_arn=listener_arn,
            endpoint_configurations=endpoint_configurations,
            health_check_interval_seconds=health_check_interval_seconds,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            port_overrides=port_overrides,
            threshold_count=threshold_count,
            traffic_dial_percentage=traffic_dial_percentage,
        )

        jsii.create(CfnEndpointGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEndpointGroupArn")
    def attr_endpoint_group_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: EndpointGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupRegion")
    def endpoint_group_region(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupRegion"))

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: builtins.str) -> None:
        jsii.set(self, "endpointGroupRegion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @listener_arn.setter
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointConfigurations")
    def endpoint_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]], jsii.get(self, "endpointConfigurations"))

    @endpoint_configurations.setter
    def endpoint_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "endpointConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckIntervalSeconds"))

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPath", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckPort"))

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckPort", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckProtocol"))

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="portOverrides")
    def port_overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-portoverrides
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]], jsii.get(self, "portOverrides"))

    @port_overrides.setter
    def port_overrides(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]],
    ) -> None:
        jsii.set(self, "portOverrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="thresholdCount")
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdCount"))

    @threshold_count.setter
    def threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "thresholdCount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="trafficDialPercentage")
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "trafficDialPercentage"))

    @traffic_dial_percentage.setter
    def traffic_dial_percentage(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "trafficDialPercentage", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_id": "endpointId",
            "client_ip_preservation_enabled": "clientIpPreservationEnabled",
            "weight": "weight",
        },
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint_id: builtins.str,
            client_ip_preservation_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param endpoint_id: ``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.
            :param client_ip_preservation_enabled: ``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.
            :param weight: ``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_id": endpoint_id,
            }
            if client_ip_preservation_enabled is not None:
                self._values["client_ip_preservation_enabled"] = client_ip_preservation_enabled
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def endpoint_id(self) -> builtins.str:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-endpointid
            '''
            result = self._values.get("endpoint_id")
            assert result is not None, "Required property 'endpoint_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_ip_preservation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-clientippreservationenabled
            '''
            result = self._values.get("client_ip_preservation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup.PortOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_port": "endpointPort",
            "listener_port": "listenerPort",
        },
    )
    class PortOverrideProperty:
        def __init__(
            self,
            *,
            endpoint_port: jsii.Number,
            listener_port: jsii.Number,
        ) -> None:
            '''
            :param endpoint_port: ``CfnEndpointGroup.PortOverrideProperty.EndpointPort``.
            :param listener_port: ``CfnEndpointGroup.PortOverrideProperty.ListenerPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_port": endpoint_port,
                "listener_port": listener_port,
            }

        @builtins.property
        def endpoint_port(self) -> jsii.Number:
            '''``CfnEndpointGroup.PortOverrideProperty.EndpointPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-endpointport
            '''
            result = self._values.get("endpoint_port")
            assert result is not None, "Required property 'endpoint_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def listener_port(self) -> jsii.Number:
            '''``CfnEndpointGroup.PortOverrideProperty.ListenerPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-listenerport
            '''
            result = self._values.get("listener_port")
            assert result is not None, "Required property 'listener_port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_group_region": "endpointGroupRegion",
        "listener_arn": "listenerArn",
        "endpoint_configurations": "endpointConfigurations",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "port_overrides": "portOverrides",
        "threshold_count": "thresholdCount",
        "traffic_dial_percentage": "trafficDialPercentage",
    },
)
class CfnEndpointGroupProps:
    def __init__(
        self,
        *,
        endpoint_group_region: builtins.str,
        listener_arn: builtins.str,
        endpoint_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        port_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::EndpointGroup``.

        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param port_overrides: ``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_group_region": endpoint_group_region,
            "listener_arn": listener_arn,
        }
        if endpoint_configurations is not None:
            self._values["endpoint_configurations"] = endpoint_configurations
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if port_overrides is not None:
            self._values["port_overrides"] = port_overrides
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if traffic_dial_percentage is not None:
            self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_region(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        '''
        result = self._values.get("endpoint_group_region")
        assert result is not None, "Required property 'endpoint_group_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        '''
        result = self._values.get("endpoint_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]], result)

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-portoverrides
        '''
        result = self._values.get("port_overrides")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]], result)

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        '''
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        '''
        result = self._values.get("traffic_dial_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListener(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::Listener``.

    :cloudformationResource: AWS::GlobalAccelerator::Listener
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        accelerator_arn: builtins.str,
        port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]],
        protocol: builtins.str,
        client_affinity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.
        '''
        props = CfnListenerProps(
            accelerator_arn=accelerator_arn,
            port_ranges=port_ranges,
            protocol=protocol,
            client_affinity=client_affinity,
        )

        jsii.create(CfnListener, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ListenerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrListenerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @accelerator_arn.setter
    def accelerator_arn(self, value: builtins.str) -> None:
        jsii.set(self, "acceleratorArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="portRanges")
    def port_ranges(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]]:
        '''``AWS::GlobalAccelerator::Listener.PortRanges``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]], jsii.get(self, "portRanges"))

    @port_ranges.setter
    def port_ranges(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]],
    ) -> None:
        jsii.set(self, "portRanges", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientAffinity")
    def client_affinity(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientAffinity"))

    @client_affinity.setter
    def client_affinity(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientAffinity", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            '''
            :param from_port: ``CfnListener.PortRangeProperty.FromPort``.
            :param to_port: ``CfnListener.PortRangeProperty.ToPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "from_port": from_port,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            '''``CfnListener.PortRangeProperty.FromPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-fromport
            '''
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def to_port(self) -> jsii.Number:
            '''``CfnListener.PortRangeProperty.ToPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-toport
            '''
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_arn": "acceleratorArn",
        "port_ranges": "portRanges",
        "protocol": "protocol",
        "client_affinity": "clientAffinity",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        accelerator_arn: builtins.str,
        port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]],
        protocol: builtins.str,
        client_affinity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::Listener``.

        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_arn": accelerator_arn,
            "port_ranges": port_ranges,
            "protocol": protocol,
        }
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity

    @builtins.property
    def accelerator_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        '''
        result = self._values.get("accelerator_arn")
        assert result is not None, "Required property 'accelerator_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port_ranges(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]]:
        '''``AWS::GlobalAccelerator::Listener.PortRanges``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        '''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]], result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-globalaccelerator.ClientAffinity")
class ClientAffinity(enum.Enum):
    '''(experimental) Client affinity lets you direct all requests from a user to the same endpoint, if you have stateful applications, regardless of the port and protocol of the client request.

    Client affinity gives you control over whether to always
    route each client to the same specific endpoint. If you want a given client to always be routed to the same
    endpoint, set client affinity to SOURCE_IP.

    :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners.html#about-listeners-client-affinity
    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) default affinity.

    :stability: experimental
    '''
    SOURCE_IP = "SOURCE_IP"
    '''(experimental) affinity by source IP.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-globalaccelerator.ConnectionProtocol")
class ConnectionProtocol(enum.Enum):
    '''(experimental) The protocol for the connections from clients to the accelerator.

    :stability: experimental
    '''

    TCP = "TCP"
    '''(experimental) TCP.

    :stability: experimental
    '''
    UDP = "UDP"
    '''(experimental) UDP.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.Ec2Instance",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId"},
)
class Ec2Instance:
    def __init__(self, *, instance_id: builtins.str) -> None:
        '''(experimental) EC2 Instance interface.

        :param instance_id: (experimental) The id of the instance resource.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "instance_id": instance_id,
        }

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''(experimental) The id of the instance resource.

        :stability: experimental
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2Instance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.ElasticIpAddress",
    jsii_struct_bases=[],
    name_mapping={"attr_allocation_id": "attrAllocationId"},
)
class ElasticIpAddress:
    def __init__(self, *, attr_allocation_id: builtins.str) -> None:
        '''(experimental) EIP Interface.

        :param attr_allocation_id: (experimental) allocation ID of the EIP resoruce.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "attr_allocation_id": attr_allocation_id,
        }

    @builtins.property
    def attr_allocation_id(self) -> builtins.str:
        '''(experimental) allocation ID of the EIP resoruce.

        :stability: experimental
        '''
        result = self._values.get("attr_allocation_id")
        assert result is not None, "Required property 'attr_allocation_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EndpointConfiguration(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointConfiguration",
):
    '''(experimental) The class for endpoint configuration.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        endpoint_group: "EndpointGroup",
        endpoint_id: builtins.str,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param endpoint_group: (experimental) The endopoint group reesource. [disable-awslint:ref-via-interface]
        :param endpoint_id: (experimental) An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.
        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        props = EndpointConfigurationProps(
            endpoint_group=endpoint_group,
            endpoint_id=endpoint_id,
            client_ip_reservation=client_ip_reservation,
            weight=weight,
        )

        jsii.create(EndpointConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(
        self,
    ) -> CfnEndpointGroup.EndpointConfigurationProperty:
        '''(experimental) render the endpoint configuration for the endpoint group.

        :stability: experimental
        '''
        return typing.cast(CfnEndpointGroup.EndpointConfigurationProperty, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def props(self) -> "EndpointConfigurationProps":
        '''(experimental) The property containing all the configuration to be rendered.

        :stability: experimental
        '''
        return typing.cast("EndpointConfigurationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={"client_ip_reservation": "clientIpReservation", "weight": "weight"},
)
class EndpointConfigurationOptions:
    def __init__(
        self,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Options for ``addLoadBalancer``, ``addElasticIpAddress`` and ``addEc2Instance`` to add endpoints into the endpoint group.

        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if client_ip_reservation is not None:
            self._values["client_ip_reservation"] = client_ip_reservation
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def client_ip_reservation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("client_ip_reservation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The weight associated with the endpoint.

        When you add weights to endpoints, you configure AWS Global Accelerator
        to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5,
        5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is
        routed both to the second and third endpoints, and 6/20 is routed to the last endpoint.

        :default: - not specified

        :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html
        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointConfigurationProps",
    jsii_struct_bases=[EndpointConfigurationOptions],
    name_mapping={
        "client_ip_reservation": "clientIpReservation",
        "weight": "weight",
        "endpoint_group": "endpointGroup",
        "endpoint_id": "endpointId",
    },
)
class EndpointConfigurationProps(EndpointConfigurationOptions):
    def __init__(
        self,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
        endpoint_group: "EndpointGroup",
        endpoint_id: builtins.str,
    ) -> None:
        '''(experimental) Properties to create EndpointConfiguration.

        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified
        :param endpoint_group: (experimental) The endopoint group reesource. [disable-awslint:ref-via-interface]
        :param endpoint_id: (experimental) An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_group": endpoint_group,
            "endpoint_id": endpoint_id,
        }
        if client_ip_reservation is not None:
            self._values["client_ip_reservation"] = client_ip_reservation
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def client_ip_reservation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("client_ip_reservation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The weight associated with the endpoint.

        When you add weights to endpoints, you configure AWS Global Accelerator
        to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5,
        5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is
        routed both to the second and third endpoints, and 6/20 is routed to the last endpoint.

        :default: - not specified

        :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html
        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def endpoint_group(self) -> "EndpointGroup":
        '''(experimental) The endopoint group reesource.

        [disable-awslint:ref-via-interface]

        :stability: experimental
        '''
        result = self._values.get("endpoint_group")
        assert result is not None, "Required property 'endpoint_group' is missing"
        return typing.cast("EndpointGroup", result)

    @builtins.property
    def endpoint_id(self) -> builtins.str:
        '''(experimental) An ID for the endpoint.

        If the endpoint is a Network Load Balancer or Application Load Balancer,
        this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address,
        this is the Elastic IP address allocation ID. For EC2 instances, this is the EC2 instance ID.

        :stability: experimental
        '''
        result = self._values.get("endpoint_id")
        assert result is not None, "Required property 'endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "listener": "listener",
        "endpoint_group_name": "endpointGroupName",
        "region": "region",
    },
)
class EndpointGroupProps:
    def __init__(
        self,
        *,
        listener: "IListener",
        endpoint_group_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Property of the EndpointGroup.

        :param listener: (experimental) The Amazon Resource Name (ARN) of the listener.
        :param endpoint_group_name: (experimental) Name of the endpoint group. Default: - logical ID of the resource
        :param region: (experimental) The AWS Region where the endpoint group is located. Default: - the region of the current stack

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if endpoint_group_name is not None:
            self._values["endpoint_group_name"] = endpoint_group_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def listener(self) -> "IListener":
        '''(experimental) The Amazon Resource Name (ARN) of the listener.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast("IListener", result)

    @builtins.property
    def endpoint_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the endpoint group.

        :default: - logical ID of the resource

        :stability: experimental
        '''
        result = self._values.get("endpoint_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS Region where the endpoint group is located.

        :default: - the region of the current stack

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IAccelerator")
class IAccelerator(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) The interface of the Accelerator.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IAcceleratorProxy"]:
        return _IAcceleratorProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''(experimental) The ARN of the accelerator.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''(experimental) The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAcceleratorProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) The interface of the Accelerator.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IAccelerator"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''(experimental) The ARN of the accelerator.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''(experimental) The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IEndpointGroup")
class IEndpointGroup(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) The interface of the EndpointGroup.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEndpointGroupProxy"]:
        return _IEndpointGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''(experimental) EndpointGroup ARN.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IEndpointGroupProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) The interface of the EndpointGroup.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IEndpointGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''(experimental) EndpointGroup ARN.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupArn"))


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IListener")
class IListener(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''(experimental) Interface of the Listener.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IListenerProxy"]:
        return _IListenerProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) The ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IListenerProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''(experimental) Interface of the Listener.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IListener"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) The ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))


@jsii.implements(IListener)
class Listener(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.Listener",
):
    '''(experimental) The construct for the Listener.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator: IAccelerator,
        port_ranges: typing.List["PortRange"],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accelerator: (experimental) The accelerator for this listener.
        :param port_ranges: (experimental) The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: (experimental) Client affinity to direct all requests from a user to the same endpoint. Default: NONE
        :param listener_name: (experimental) Name of the listener. Default: - logical ID of the resource
        :param protocol: (experimental) The protocol for the connections from clients to the accelerator. Default: TCP

        :stability: experimental
        '''
        props = ListenerProps(
            accelerator=accelerator,
            port_ranges=port_ranges,
            client_affinity=client_affinity,
            listener_name=listener_name,
            protocol=protocol,
        )

        jsii.create(Listener, self, [scope, id, props])

    @jsii.member(jsii_name="fromListenerArn") # type: ignore[misc]
    @builtins.classmethod
    def from_listener_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        listener_arn: builtins.str,
    ) -> IListener:
        '''(experimental) import from ARN.

        :param scope: -
        :param id: -
        :param listener_arn: -

        :stability: experimental
        '''
        return typing.cast(IListener, jsii.sinvoke(cls, "fromListenerArn", [scope, id, listener_arn]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) The ARN of the listener.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerName")
    def listener_name(self) -> builtins.str:
        '''(experimental) The name of the listener.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.ListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator": "accelerator",
        "port_ranges": "portRanges",
        "client_affinity": "clientAffinity",
        "listener_name": "listenerName",
        "protocol": "protocol",
    },
)
class ListenerProps:
    def __init__(
        self,
        *,
        accelerator: IAccelerator,
        port_ranges: typing.List["PortRange"],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
    ) -> None:
        '''(experimental) construct properties for Listener.

        :param accelerator: (experimental) The accelerator for this listener.
        :param port_ranges: (experimental) The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: (experimental) Client affinity to direct all requests from a user to the same endpoint. Default: NONE
        :param listener_name: (experimental) Name of the listener. Default: - logical ID of the resource
        :param protocol: (experimental) The protocol for the connections from clients to the accelerator. Default: TCP

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator": accelerator,
            "port_ranges": port_ranges,
        }
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if listener_name is not None:
            self._values["listener_name"] = listener_name
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def accelerator(self) -> IAccelerator:
        '''(experimental) The accelerator for this listener.

        :stability: experimental
        '''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(IAccelerator, result)

    @builtins.property
    def port_ranges(self) -> typing.List["PortRange"]:
        '''(experimental) The list of port ranges for the connections from clients to the accelerator.

        :stability: experimental
        '''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.List["PortRange"], result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[ClientAffinity]:
        '''(experimental) Client affinity to direct all requests from a user to the same endpoint.

        :default: NONE

        :stability: experimental
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[ClientAffinity], result)

    @builtins.property
    def listener_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the listener.

        :default: - logical ID of the resource

        :stability: experimental
        '''
        result = self._values.get("listener_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ConnectionProtocol]:
        '''(experimental) The protocol for the connections from clients to the accelerator.

        :default: TCP

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ConnectionProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.LoadBalancer",
    jsii_struct_bases=[],
    name_mapping={"load_balancer_arn": "loadBalancerArn"},
)
class LoadBalancer:
    def __init__(self, *, load_balancer_arn: builtins.str) -> None:
        '''(experimental) LoadBalancer Interface.

        :param load_balancer_arn: (experimental) The ARN of this load balancer.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_arn": load_balancer_arn,
        }

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) The ARN of this load balancer.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.PortRange",
    jsii_struct_bases=[],
    name_mapping={"from_port": "fromPort", "to_port": "toPort"},
)
class PortRange:
    def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
        '''(experimental) The list of port ranges for the connections from clients to the accelerator.

        :param from_port: (experimental) The first port in the range of ports, inclusive.
        :param to_port: (experimental) The last port in the range of ports, inclusive.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "from_port": from_port,
            "to_port": to_port,
        }

    @builtins.property
    def from_port(self) -> jsii.Number:
        '''(experimental) The first port in the range of ports, inclusive.

        :stability: experimental
        '''
        result = self._values.get("from_port")
        assert result is not None, "Required property 'from_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def to_port(self) -> jsii.Number:
        '''(experimental) The last port in the range of ports, inclusive.

        :stability: experimental
        '''
        result = self._values.get("to_port")
        assert result is not None, "Required property 'to_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PortRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAccelerator)
class Accelerator(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.Accelerator",
):
    '''(experimental) The Accelerator construct.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accelerator_name: (experimental) The name of the accelerator. Default: - resource ID
        :param enabled: (experimental) Indicates whether the accelerator is enabled. Default: true

        :stability: experimental
        '''
        props = AcceleratorProps(accelerator_name=accelerator_name, enabled=enabled)

        jsii.create(Accelerator, self, [scope, id, props])

    @jsii.member(jsii_name="fromAcceleratorAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_accelerator_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator_arn: builtins.str,
        dns_name: builtins.str,
    ) -> IAccelerator:
        '''(experimental) import from attributes.

        :param scope: -
        :param id: -
        :param accelerator_arn: (experimental) The ARN of the accelerator.
        :param dns_name: (experimental) The DNS name of the accelerator.

        :stability: experimental
        '''
        attrs = AcceleratorAttributes(
            accelerator_arn=accelerator_arn, dns_name=dns_name
        )

        return typing.cast(IAccelerator, jsii.sinvoke(cls, "fromAcceleratorAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''(experimental) The ARN of the accelerator.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''(experimental) The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))


@jsii.implements(IEndpointGroup)
class EndpointGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointGroup",
):
    '''(experimental) EndpointGroup construct.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: IListener,
        endpoint_group_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param listener: (experimental) The Amazon Resource Name (ARN) of the listener.
        :param endpoint_group_name: (experimental) Name of the endpoint group. Default: - logical ID of the resource
        :param region: (experimental) The AWS Region where the endpoint group is located. Default: - the region of the current stack

        :stability: experimental
        '''
        props = EndpointGroupProps(
            listener=listener, endpoint_group_name=endpoint_group_name, region=region
        )

        jsii.create(EndpointGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromEndpointGroupArn") # type: ignore[misc]
    @builtins.classmethod
    def from_endpoint_group_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        endpoint_group_arn: builtins.str,
    ) -> IEndpointGroup:
        '''(experimental) import from ARN.

        :param scope: -
        :param id: -
        :param endpoint_group_arn: -

        :stability: experimental
        '''
        return typing.cast(IEndpointGroup, jsii.sinvoke(cls, "fromEndpointGroupArn", [scope, id, endpoint_group_arn]))

    @jsii.member(jsii_name="addEc2Instance")
    def add_ec2_instance(
        self,
        id: builtins.str,
        instance: Ec2Instance,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> EndpointConfiguration:
        '''(experimental) Add an EC2 Instance as an endpoint in this endpoint group.

        :param id: -
        :param instance: -
        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        props = EndpointConfigurationOptions(
            client_ip_reservation=client_ip_reservation, weight=weight
        )

        return typing.cast(EndpointConfiguration, jsii.invoke(self, "addEc2Instance", [id, instance, props]))

    @jsii.member(jsii_name="addElasticIpAddress")
    def add_elastic_ip_address(
        self,
        id: builtins.str,
        eip: ElasticIpAddress,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> EndpointConfiguration:
        '''(experimental) Add an EIP as an endpoint in this endpoint group.

        :param id: -
        :param eip: -
        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        props = EndpointConfigurationOptions(
            client_ip_reservation=client_ip_reservation, weight=weight
        )

        return typing.cast(EndpointConfiguration, jsii.invoke(self, "addElasticIpAddress", [id, eip, props]))

    @jsii.member(jsii_name="addEndpoint")
    def add_endpoint(
        self,
        id: builtins.str,
        endpoint_id: builtins.str,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> EndpointConfiguration:
        '''(experimental) Add an endpoint.

        :param id: -
        :param endpoint_id: -
        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        props = EndpointConfigurationOptions(
            client_ip_reservation=client_ip_reservation, weight=weight
        )

        return typing.cast(EndpointConfiguration, jsii.invoke(self, "addEndpoint", [id, endpoint_id, props]))

    @jsii.member(jsii_name="addLoadBalancer")
    def add_load_balancer(
        self,
        id: builtins.str,
        lb: LoadBalancer,
        *,
        client_ip_reservation: typing.Optional[builtins.bool] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> EndpointConfiguration:
        '''(experimental) Add an Elastic Load Balancer as an endpoint in this endpoint group.

        :param id: -
        :param lb: -
        :param client_ip_reservation: (experimental) Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. Default: true
        :param weight: (experimental) The weight associated with the endpoint. When you add weights to endpoints, you configure AWS Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. Default: - not specified

        :stability: experimental
        '''
        props = EndpointConfigurationOptions(
            client_ip_reservation=client_ip_reservation, weight=weight
        )

        return typing.cast(EndpointConfiguration, jsii.invoke(self, "addLoadBalancer", [id, lb, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''(experimental) EndpointGroup ARN.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupName")
    def endpoint_group_name(self) -> builtins.str:
        '''(experimental) The name of the endpoint group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpoints")
    def _endpoints(self) -> typing.List[EndpointConfiguration]:
        '''(experimental) The array of the endpoints in this endpoint group.

        :stability: experimental
        '''
        return typing.cast(typing.List[EndpointConfiguration], jsii.get(self, "endpoints"))


__all__ = [
    "Accelerator",
    "AcceleratorAttributes",
    "AcceleratorProps",
    "AcceleratorSecurityGroup",
    "CfnAccelerator",
    "CfnAcceleratorProps",
    "CfnEndpointGroup",
    "CfnEndpointGroupProps",
    "CfnListener",
    "CfnListenerProps",
    "ClientAffinity",
    "ConnectionProtocol",
    "Ec2Instance",
    "ElasticIpAddress",
    "EndpointConfiguration",
    "EndpointConfigurationOptions",
    "EndpointConfigurationProps",
    "EndpointGroup",
    "EndpointGroupProps",
    "IAccelerator",
    "IEndpointGroup",
    "IListener",
    "Listener",
    "ListenerProps",
    "LoadBalancer",
    "PortRange",
]

publication.publish()
