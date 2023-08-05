# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Instance(pulumi.CustomResource):
    apikey: pulumi.Output[str]
    """
    API key for the CloudAMQP instance
    """
    host: pulumi.Output[str]
    """
    Host name for the CloudAMQP instance
    """
    name: pulumi.Output[str]
    """
    Name of the instance
    """
    nodes: pulumi.Output[float]
    """
    Number of nodes in cluster (plan must support it)
    """
    plan: pulumi.Output[str]
    """
    Name of the plan, valid options are: lemur, tiger, bunny, rabbit, panda, ape, hippo, lion
    """
    region: pulumi.Output[str]
    """
    Name of the region you want to create your instance in
    """
    rmq_version: pulumi.Output[str]
    """
    RabbitMQ version
    """
    tags: pulumi.Output[list]
    """
    Tag the instances with optional tags
    """
    url: pulumi.Output[str]
    """
    URL of the CloudAMQP instance
    """
    vhost: pulumi.Output[str]
    """
    The virtual host
    """
    vpc_subnet: pulumi.Output[str]
    """
    Dedicated VPC subnet, shouldn't overlap with your current VPC's subnet
    """
    def __init__(__self__, resource_name, opts=None, name=None, nodes=None, plan=None, region=None, rmq_version=None, tags=None, vpc_subnet=None, __props__=None, __name__=None, __opts__=None):
        """
        Create a Instance resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the instance
        :param pulumi.Input[float] nodes: Number of nodes in cluster (plan must support it)
        :param pulumi.Input[str] plan: Name of the plan, valid options are: lemur, tiger, bunny, rabbit, panda, ape, hippo, lion
        :param pulumi.Input[str] region: Name of the region you want to create your instance in
        :param pulumi.Input[str] rmq_version: RabbitMQ version
        :param pulumi.Input[list] tags: Tag the instances with optional tags
        :param pulumi.Input[str] vpc_subnet: Dedicated VPC subnet, shouldn't overlap with your current VPC's subnet
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['name'] = name
            __props__['nodes'] = nodes
            if plan is None:
                raise TypeError("Missing required property 'plan'")
            __props__['plan'] = plan
            if region is None:
                raise TypeError("Missing required property 'region'")
            __props__['region'] = region
            __props__['rmq_version'] = rmq_version
            __props__['tags'] = tags
            __props__['vpc_subnet'] = vpc_subnet
            __props__['apikey'] = None
            __props__['host'] = None
            __props__['url'] = None
            __props__['vhost'] = None
        super(Instance, __self__).__init__(
            'cloudamqp:index/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, apikey=None, host=None, name=None, nodes=None, plan=None, region=None, rmq_version=None, tags=None, url=None, vhost=None, vpc_subnet=None):
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] apikey: API key for the CloudAMQP instance
        :param pulumi.Input[str] host: Host name for the CloudAMQP instance
        :param pulumi.Input[str] name: Name of the instance
        :param pulumi.Input[float] nodes: Number of nodes in cluster (plan must support it)
        :param pulumi.Input[str] plan: Name of the plan, valid options are: lemur, tiger, bunny, rabbit, panda, ape, hippo, lion
        :param pulumi.Input[str] region: Name of the region you want to create your instance in
        :param pulumi.Input[str] rmq_version: RabbitMQ version
        :param pulumi.Input[list] tags: Tag the instances with optional tags
        :param pulumi.Input[str] url: URL of the CloudAMQP instance
        :param pulumi.Input[str] vhost: The virtual host
        :param pulumi.Input[str] vpc_subnet: Dedicated VPC subnet, shouldn't overlap with your current VPC's subnet
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["apikey"] = apikey
        __props__["host"] = host
        __props__["name"] = name
        __props__["nodes"] = nodes
        __props__["plan"] = plan
        __props__["region"] = region
        __props__["rmq_version"] = rmq_version
        __props__["tags"] = tags
        __props__["url"] = url
        __props__["vhost"] = vhost
        __props__["vpc_subnet"] = vpc_subnet
        return Instance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

