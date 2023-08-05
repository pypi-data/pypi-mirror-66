# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class ComputeClusterVmGroup(pulumi.CustomResource):
    compute_cluster_id: pulumi.Output[str]
    """
    The [managed object reference
    ID][docs-about-morefs] of the cluster to put the group in.  Forces a new
    resource if changed.
    """
    name: pulumi.Output[str]
    """
    The name of the VM group. This must be unique in the
    cluster. Forces a new resource if changed.
    """
    virtual_machine_ids: pulumi.Output[list]
    """
    The UUIDs of the virtual machines in this
    group.
    """
    def __init__(__self__, resource_name, opts=None, compute_cluster_id=None, name=None, virtual_machine_ids=None, __props__=None, __name__=None, __opts__=None):
        """
        The `.ComputeClusterVmGroup` resource can be used to manage groups of
        virtual machines in a cluster, either created by the
        [`.ComputeCluster`][tf-vsphere-cluster-resource] resource or looked up
        by the [`.ComputeCluster`][tf-vsphere-cluster-data-source] data source.

        [tf-vsphere-cluster-resource]: /docs/providers/vsphere/r/compute_cluster.html
        [tf-vsphere-cluster-data-source]: /docs/providers/vsphere/d/compute_cluster.html

        This resource mainly serves as an input to the
        [`.ComputeClusterVmDependencyRule`][tf-vsphere-cluster-vm-dependency-rule-resource]
        and
        [`.ComputeClusterVmHostRule`][tf-vsphere-cluster-vm-host-rule-resource]
        resources. See the individual resource documentation pages for more information.

        [tf-vsphere-cluster-vm-dependency-rule-resource]: /docs/providers/vsphere/r/compute_cluster_vm_dependency_rule.html
        [tf-vsphere-cluster-vm-host-rule-resource]: /docs/providers/vsphere/r/compute_cluster_vm_host_rule.html

        > **NOTE:** This resource requires vCenter and is not available on direct ESXi
        connections.

        > **NOTE:** vSphere DRS requires a vSphere Enterprise Plus license.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compute_cluster_id: The [managed object reference
               ID][docs-about-morefs] of the cluster to put the group in.  Forces a new
               resource if changed.
        :param pulumi.Input[str] name: The name of the VM group. This must be unique in the
               cluster. Forces a new resource if changed.
        :param pulumi.Input[list] virtual_machine_ids: The UUIDs of the virtual machines in this
               group.
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

            if compute_cluster_id is None:
                raise TypeError("Missing required property 'compute_cluster_id'")
            __props__['compute_cluster_id'] = compute_cluster_id
            __props__['name'] = name
            __props__['virtual_machine_ids'] = virtual_machine_ids
        super(ComputeClusterVmGroup, __self__).__init__(
            'vsphere:index/computeClusterVmGroup:ComputeClusterVmGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, compute_cluster_id=None, name=None, virtual_machine_ids=None):
        """
        Get an existing ComputeClusterVmGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compute_cluster_id: The [managed object reference
               ID][docs-about-morefs] of the cluster to put the group in.  Forces a new
               resource if changed.
        :param pulumi.Input[str] name: The name of the VM group. This must be unique in the
               cluster. Forces a new resource if changed.
        :param pulumi.Input[list] virtual_machine_ids: The UUIDs of the virtual machines in this
               group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["compute_cluster_id"] = compute_cluster_id
        __props__["name"] = name
        __props__["virtual_machine_ids"] = virtual_machine_ids
        return ComputeClusterVmGroup(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

