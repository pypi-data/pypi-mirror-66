# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetConfigurationStoreResult:
    """
    A collection of values returned by getConfigurationStore.
    """
    def __init__(__self__, endpoint=None, id=None, location=None, name=None, primary_read_keys=None, primary_write_keys=None, resource_group_name=None, secondary_read_keys=None, secondary_write_keys=None, sku=None, tags=None):
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        __self__.endpoint = endpoint
        """
        The Endpoint used to access this App Configuration.
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
        The Azure Region where the App Configuration exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if primary_read_keys and not isinstance(primary_read_keys, list):
            raise TypeError("Expected argument 'primary_read_keys' to be a list")
        __self__.primary_read_keys = primary_read_keys
        """
        A `primary_read_key` block as defined below containing the primary read access key.
        """
        if primary_write_keys and not isinstance(primary_write_keys, list):
            raise TypeError("Expected argument 'primary_write_keys' to be a list")
        __self__.primary_write_keys = primary_write_keys
        """
        A `primary_write_key` block as defined below containing the primary write access key.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if secondary_read_keys and not isinstance(secondary_read_keys, list):
            raise TypeError("Expected argument 'secondary_read_keys' to be a list")
        __self__.secondary_read_keys = secondary_read_keys
        """
        A `secondary_read_key` block as defined below containing the secondary read access key.
        """
        if secondary_write_keys and not isinstance(secondary_write_keys, list):
            raise TypeError("Expected argument 'secondary_write_keys' to be a list")
        __self__.secondary_write_keys = secondary_write_keys
        """
        A `secondary_write_key` block as defined below containing the secondary write access key.
        """
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        The name of the SKU used for this App Configuration.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the App Configuration.
        """
class AwaitableGetConfigurationStoreResult(GetConfigurationStoreResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationStoreResult(
            endpoint=self.endpoint,
            id=self.id,
            location=self.location,
            name=self.name,
            primary_read_keys=self.primary_read_keys,
            primary_write_keys=self.primary_write_keys,
            resource_group_name=self.resource_group_name,
            secondary_read_keys=self.secondary_read_keys,
            secondary_write_keys=self.secondary_write_keys,
            sku=self.sku,
            tags=self.tags)

def get_configuration_store(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing App Configuration.




    :param str name: The Name of this App Configuration.
    :param str resource_group_name: The name of the Resource Group where the App Configuration exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:appconfiguration/getConfigurationStore:getConfigurationStore', __args__, opts=opts).value

    return AwaitableGetConfigurationStoreResult(
        endpoint=__ret__.get('endpoint'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        primary_read_keys=__ret__.get('primaryReadKeys'),
        primary_write_keys=__ret__.get('primaryWriteKeys'),
        resource_group_name=__ret__.get('resourceGroupName'),
        secondary_read_keys=__ret__.get('secondaryReadKeys'),
        secondary_write_keys=__ret__.get('secondaryWriteKeys'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'))
