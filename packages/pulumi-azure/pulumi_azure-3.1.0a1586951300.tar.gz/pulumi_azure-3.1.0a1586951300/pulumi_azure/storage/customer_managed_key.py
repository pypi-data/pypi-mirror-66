# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class CustomerManagedKey(pulumi.CustomResource):
    key_name: pulumi.Output[str]
    """
    The name of Key Vault Key.
    """
    key_vault_id: pulumi.Output[str]
    """
    The ID of the Key Vault. Changing this forces a new resource to be created.
    """
    key_version: pulumi.Output[str]
    """
    The version of Key Vault Key.
    """
    storage_account_id: pulumi.Output[str]
    """
    The ID of the Storage Account. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, key_name=None, key_vault_id=None, key_version=None, storage_account_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Customer Managed Key for a Storage Account.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account. Changing this forces a new resource to be created.
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

            if key_name is None:
                raise TypeError("Missing required property 'key_name'")
            __props__['key_name'] = key_name
            if key_vault_id is None:
                raise TypeError("Missing required property 'key_vault_id'")
            __props__['key_vault_id'] = key_vault_id
            if key_version is None:
                raise TypeError("Missing required property 'key_version'")
            __props__['key_version'] = key_version
            if storage_account_id is None:
                raise TypeError("Missing required property 'storage_account_id'")
            __props__['storage_account_id'] = storage_account_id
        super(CustomerManagedKey, __self__).__init__(
            'azure:storage/customerManagedKey:CustomerManagedKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, key_name=None, key_vault_id=None, key_version=None, storage_account_id=None):
        """
        Get an existing CustomerManagedKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_name: The name of Key Vault Key.
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault. Changing this forces a new resource to be created.
        :param pulumi.Input[str] key_version: The version of Key Vault Key.
        :param pulumi.Input[str] storage_account_id: The ID of the Storage Account. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["key_name"] = key_name
        __props__["key_vault_id"] = key_vault_id
        __props__["key_version"] = key_version
        __props__["storage_account_id"] = storage_account_id
        return CustomerManagedKey(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

