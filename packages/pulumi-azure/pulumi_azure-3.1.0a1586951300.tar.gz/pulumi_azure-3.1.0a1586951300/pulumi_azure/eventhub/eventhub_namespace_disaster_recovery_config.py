# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class EventhubNamespaceDisasterRecoveryConfig(pulumi.CustomResource):
    alternate_name: pulumi.Output[str]
    """
    An alternate name to use when the Disaster Recovery Config's name is the same as the replicated namespace's name.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Disaster Recovery Config. Changing this forces a new resource to be created.
    """
    namespace_name: pulumi.Output[str]
    """
    Specifies the name of the primary EventHub Namespace to replicate. Changing this forces a new resource to be created.
    """
    partner_namespace_id: pulumi.Output[str]
    """
    The ID of the EventHub Namespace to replicate to.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which the Disaster Recovery Config exists. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, alternate_name=None, name=None, namespace_name=None, partner_namespace_id=None, resource_group_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Disaster Recovery Config for an Event Hub Namespace.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alternate_name: An alternate name to use when the Disaster Recovery Config's name is the same as the replicated namespace's name.
        :param pulumi.Input[str] name: Specifies the name of the Disaster Recovery Config. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the primary EventHub Namespace to replicate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partner_namespace_id: The ID of the EventHub Namespace to replicate to.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Disaster Recovery Config exists. Changing this forces a new resource to be created.
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

            __props__['alternate_name'] = alternate_name
            __props__['name'] = name
            if namespace_name is None:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            if partner_namespace_id is None:
                raise TypeError("Missing required property 'partner_namespace_id'")
            __props__['partner_namespace_id'] = partner_namespace_id
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
        super(EventhubNamespaceDisasterRecoveryConfig, __self__).__init__(
            'azure:eventhub/eventhubNamespaceDisasterRecoveryConfig:EventhubNamespaceDisasterRecoveryConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, alternate_name=None, name=None, namespace_name=None, partner_namespace_id=None, resource_group_name=None):
        """
        Get an existing EventhubNamespaceDisasterRecoveryConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alternate_name: An alternate name to use when the Disaster Recovery Config's name is the same as the replicated namespace's name.
        :param pulumi.Input[str] name: Specifies the name of the Disaster Recovery Config. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the primary EventHub Namespace to replicate. Changing this forces a new resource to be created.
        :param pulumi.Input[str] partner_namespace_id: The ID of the EventHub Namespace to replicate to.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the Disaster Recovery Config exists. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["alternate_name"] = alternate_name
        __props__["name"] = name
        __props__["namespace_name"] = namespace_name
        __props__["partner_namespace_id"] = partner_namespace_id
        __props__["resource_group_name"] = resource_group_name
        return EventhubNamespaceDisasterRecoveryConfig(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

