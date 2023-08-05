# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetVmfsDisksResult:
    """
    A collection of values returned by getVmfsDisks.
    """
    def __init__(__self__, disks=None, filter=None, host_system_id=None, id=None, rescan=None):
        if disks and not isinstance(disks, list):
            raise TypeError("Expected argument 'disks' to be a list")
        __self__.disks = disks
        """
        A lexicographically sorted list of devices discovered by the
        operation, matching the supplied `filter`, if provided.
        """
        if filter and not isinstance(filter, str):
            raise TypeError("Expected argument 'filter' to be a str")
        __self__.filter = filter
        if host_system_id and not isinstance(host_system_id, str):
            raise TypeError("Expected argument 'host_system_id' to be a str")
        __self__.host_system_id = host_system_id
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
        if rescan and not isinstance(rescan, bool):
            raise TypeError("Expected argument 'rescan' to be a bool")
        __self__.rescan = rescan
class AwaitableGetVmfsDisksResult(GetVmfsDisksResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVmfsDisksResult(
            disks=self.disks,
            filter=self.filter,
            host_system_id=self.host_system_id,
            id=self.id,
            rescan=self.rescan)

def get_vmfs_disks(filter=None,host_system_id=None,rescan=None,opts=None):
    """
    The `.getVmfsDisks` data source can be used to discover the storage
    devices available on an ESXi host. This data source can be combined with the
    [`.VmfsDatastore`][data-source-vmfs-datastore] resource to create VMFS
    datastores based off a set of discovered disks.

    [data-source-vmfs-datastore]: /docs/providers/vsphere/r/vmfs_datastore.html




    :param str filter: A regular expression to filter the disks against. Only
           disks with canonical names that match will be included.
    :param str host_system_id: The [managed object ID][docs-about-morefs] of
           the host to look for disks on.
    :param bool rescan: Whether or not to rescan storage adapters before
           searching for disks. This may lengthen the time it takes to perform the
           search. Default: `false`.
    """
    __args__ = dict()


    __args__['filter'] = filter
    __args__['hostSystemId'] = host_system_id
    __args__['rescan'] = rescan
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('vsphere:index/getVmfsDisks:getVmfsDisks', __args__, opts=opts).value

    return AwaitableGetVmfsDisksResult(
        disks=__ret__.get('disks'),
        filter=__ret__.get('filter'),
        host_system_id=__ret__.get('hostSystemId'),
        id=__ret__.get('id'),
        rescan=__ret__.get('rescan'))
