# coding=utf-8
# Copyright (c) 2015 EMC Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import unicode_literals

from storops.unity.resource import UnityResource, UnityResourceList
from storops.unity.resource.storage_resource import UnityStorageResource

__author__ = 'Cedric Zhuang'


class UnityDataStore(UnityResource):
    @classmethod
    def create(cls, cli, name, vvol_datastore_type, description=None,
               hosts=None,
               capability_profiles=None):
        vvol_ds_cp_parameters = {"addCapabilityProfile": [
            {"capProfile": {"id": x.id}, "sizeTotal": x.pool.size_total} for x
            in capability_profiles]}

        req_body = cli.make_body(
            name=name,
            vvolDatastoreType=vvol_datastore_type,
            description=description,
            hosts=hosts,
            vvolDatastoreCapabilityProfilesParameters=vvol_ds_cp_parameters)

        resp = cli.type_action(UnityStorageResource().resource_class,
                               'createVVolDatastore', **req_body)
        resp.raise_if_err()
        return UnityStorageResource(_id=resp.resource_id, cli=cli)


class UnityDataStoreList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityDataStore


class UnityVmDisk(UnityResource):
    pass


class UnityVmDiskList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVmDisk


class UnityVm(UnityResource):
    pass


class UnityVmList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVm


class UnityVirtualVolume(UnityResource):
    pass


class UnityVirtualVolumeList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVirtualVolume


class UnityHostVvolDatastore(UnityResource):
    pass


class UnityHostVvolDatastoreList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityHostVvolDatastore


class UnityCapabilityProfile(UnityResource):
    @classmethod
    def create(cls, cli, name, pool, description=None,
               usage_tags=None, constraints=None):
        req_body = cli.make_body(name=name,
                                 pool=pool,
                                 description=description,
                                 usageTags=usage_tags,
                                 constraints=constraints)
        resp = cli.post(cls().resource_class, **req_body)
        resp.raise_if_err()
        return cls.get(cli, resp.resource_id)


class UnityCapabilityProfileList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityCapabilityProfile


class UnityVirtualVolumeBinding(UnityResource):
    pass


class UnityVirtualVolumeBindingList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVirtualVolume


class UnityVmwarePE(UnityResource):
    pass


class UnityVmwarePEList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVmwarePE


class UnityVmwareNasPEServer(UnityResource):
    pass


class UnityVmwareNasPEServerList(UnityResourceList):
    @classmethod
    def get_resource_class(cls):
        return UnityVmwareNasPEServer
