# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetCustomAttributeResult:
    """
    A collection of values returned by getCustomAttribute.
    """
    def __init__(__self__, id=None, managed_object_type=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
        if managed_object_type and not isinstance(managed_object_type, str):
            raise TypeError("Expected argument 'managed_object_type' to be a str")
        __self__.managed_object_type = managed_object_type
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
class AwaitableGetCustomAttributeResult(GetCustomAttributeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomAttributeResult(
            id=self.id,
            managed_object_type=self.managed_object_type,
            name=self.name)

def get_custom_attribute(name=None,opts=None):
    """
    Use this data source to access information about an existing resource.

    :param str name: The name of the custom attribute.
    """
    __args__ = dict()


    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('vsphere:index/getCustomAttribute:getCustomAttribute', __args__, opts=opts).value

    return AwaitableGetCustomAttributeResult(
        id=__ret__.get('id'),
        managed_object_type=__ret__.get('managedObjectType'),
        name=__ret__.get('name'))
