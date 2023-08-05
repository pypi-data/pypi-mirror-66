# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Secret(pulumi.CustomResource):
    content_type: pulumi.Output[str]
    """
    Specifies the content type for the Key Vault Secret.
    """
    expiration_date: pulumi.Output[str]
    """
    Expiration UTC datetime (Y-m-d'T'H:M:S'Z').
    """
    key_vault_id: pulumi.Output[str]
    """
    The ID of the Key Vault where the Secret should be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Key Vault Secret. Changing this forces a new resource to be created.
    """
    not_before_date: pulumi.Output[str]
    """
    Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    value: pulumi.Output[str]
    """
    Specifies the value of the Key Vault Secret.
    """
    version: pulumi.Output[str]
    """
    The current version of the Key Vault Secret.
    """
    def __init__(__self__, resource_name, opts=None, content_type=None, expiration_date=None, key_vault_id=None, name=None, not_before_date=None, tags=None, value=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Key Vault Secret.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content_type: Specifies the content type for the Key Vault Secret.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z').
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault where the Secret should be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] value: Specifies the value of the Key Vault Secret.
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

            __props__['content_type'] = content_type
            __props__['expiration_date'] = expiration_date
            if key_vault_id is None:
                raise TypeError("Missing required property 'key_vault_id'")
            __props__['key_vault_id'] = key_vault_id
            __props__['name'] = name
            __props__['not_before_date'] = not_before_date
            __props__['tags'] = tags
            if value is None:
                raise TypeError("Missing required property 'value'")
            __props__['value'] = value
            __props__['version'] = None
        super(Secret, __self__).__init__(
            'azure:keyvault/secret:Secret',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, content_type=None, expiration_date=None, key_vault_id=None, name=None, not_before_date=None, tags=None, value=None, version=None):
        """
        Get an existing Secret resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content_type: Specifies the content type for the Key Vault Secret.
        :param pulumi.Input[str] expiration_date: Expiration UTC datetime (Y-m-d'T'H:M:S'Z').
        :param pulumi.Input[str] key_vault_id: The ID of the Key Vault where the Secret should be created.
        :param pulumi.Input[str] name: Specifies the name of the Key Vault Secret. Changing this forces a new resource to be created.
        :param pulumi.Input[str] not_before_date: Key not usable before the provided UTC datetime (Y-m-d'T'H:M:S'Z').
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] value: Specifies the value of the Key Vault Secret.
        :param pulumi.Input[str] version: The current version of the Key Vault Secret.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["content_type"] = content_type
        __props__["expiration_date"] = expiration_date
        __props__["key_vault_id"] = key_vault_id
        __props__["name"] = name
        __props__["not_before_date"] = not_before_date
        __props__["tags"] = tags
        __props__["value"] = value
        __props__["version"] = version
        return Secret(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

