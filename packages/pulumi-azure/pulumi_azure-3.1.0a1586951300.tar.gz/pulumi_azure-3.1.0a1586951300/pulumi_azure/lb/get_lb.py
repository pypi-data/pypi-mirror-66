# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetLBResult:
    """
    A collection of values returned by getLB.
    """
    def __init__(__self__, frontend_ip_configurations=None, id=None, location=None, name=None, private_ip_address=None, private_ip_addresses=None, resource_group_name=None, sku=None, tags=None):
        if frontend_ip_configurations and not isinstance(frontend_ip_configurations, list):
            raise TypeError("Expected argument 'frontend_ip_configurations' to be a list")
        __self__.frontend_ip_configurations = frontend_ip_configurations
        """
        (Optional) A `frontend_ip_configuration` block as documented below.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure location where the Load Balancer exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The name of the Frontend IP Configuration.
        """
        if private_ip_address and not isinstance(private_ip_address, str):
            raise TypeError("Expected argument 'private_ip_address' to be a str")
        __self__.private_ip_address = private_ip_address
        """
        Private IP Address to assign to the Load Balancer.
        """
        if private_ip_addresses and not isinstance(private_ip_addresses, list):
            raise TypeError("Expected argument 'private_ip_addresses' to be a list")
        __self__.private_ip_addresses = private_ip_addresses
        """
        The list of private IP address assigned to the load balancer in `frontend_ip_configuration` blocks, if any.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        The SKU of the Load Balancer.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
class AwaitableGetLBResult(GetLBResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLBResult(
            frontend_ip_configurations=self.frontend_ip_configurations,
            id=self.id,
            location=self.location,
            name=self.name,
            private_ip_address=self.private_ip_address,
            private_ip_addresses=self.private_ip_addresses,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags)

def get_lb(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Load Balancer




    :param str name: Specifies the name of the Load Balancer.
    :param str resource_group_name: The name of the Resource Group in which the Load Balancer exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:lb/getLB:getLB', __args__, opts=opts).value

    return AwaitableGetLBResult(
        frontend_ip_configurations=__ret__.get('frontendIpConfigurations'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        private_ip_address=__ret__.get('privateIpAddress'),
        private_ip_addresses=__ret__.get('privateIpAddresses'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'))
