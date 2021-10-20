import datetime
import typing

import kubernetes.client

class V1PersistentVolumeSpec:
    access_modes: typing.Optional[list[str]]
    aws_elastic_block_store: typing.Optional[
        kubernetes.client.V1AWSElasticBlockStoreVolumeSource
    ]
    azure_disk: typing.Optional[kubernetes.client.V1AzureDiskVolumeSource]
    azure_file: typing.Optional[kubernetes.client.V1AzureFilePersistentVolumeSource]
    capacity: typing.Optional[dict[str, str]]
    cephfs: typing.Optional[kubernetes.client.V1CephFSPersistentVolumeSource]
    cinder: typing.Optional[kubernetes.client.V1CinderPersistentVolumeSource]
    claim_ref: typing.Optional[kubernetes.client.V1ObjectReference]
    csi: typing.Optional[kubernetes.client.V1CSIPersistentVolumeSource]
    fc: typing.Optional[kubernetes.client.V1FCVolumeSource]
    flex_volume: typing.Optional[kubernetes.client.V1FlexPersistentVolumeSource]
    flocker: typing.Optional[kubernetes.client.V1FlockerVolumeSource]
    gce_persistent_disk: typing.Optional[
        kubernetes.client.V1GCEPersistentDiskVolumeSource
    ]
    glusterfs: typing.Optional[kubernetes.client.V1GlusterfsPersistentVolumeSource]
    host_path: typing.Optional[kubernetes.client.V1HostPathVolumeSource]
    iscsi: typing.Optional[kubernetes.client.V1ISCSIPersistentVolumeSource]
    local: typing.Optional[kubernetes.client.V1LocalVolumeSource]
    mount_options: typing.Optional[list[str]]
    nfs: typing.Optional[kubernetes.client.V1NFSVolumeSource]
    node_affinity: typing.Optional[kubernetes.client.V1VolumeNodeAffinity]
    persistent_volume_reclaim_policy: typing.Optional[str]
    photon_persistent_disk: typing.Optional[
        kubernetes.client.V1PhotonPersistentDiskVolumeSource
    ]
    portworx_volume: typing.Optional[kubernetes.client.V1PortworxVolumeSource]
    quobyte: typing.Optional[kubernetes.client.V1QuobyteVolumeSource]
    rbd: typing.Optional[kubernetes.client.V1RBDPersistentVolumeSource]
    scale_io: typing.Optional[kubernetes.client.V1ScaleIOPersistentVolumeSource]
    storage_class_name: typing.Optional[str]
    storageos: typing.Optional[kubernetes.client.V1StorageOSPersistentVolumeSource]
    volume_mode: typing.Optional[str]
    vsphere_volume: typing.Optional[kubernetes.client.V1VsphereVirtualDiskVolumeSource]
    def __init__(
        self,
        *,
        access_modes: typing.Optional[list[str]] = ...,
        aws_elastic_block_store: typing.Optional[
            kubernetes.client.V1AWSElasticBlockStoreVolumeSource
        ] = ...,
        azure_disk: typing.Optional[kubernetes.client.V1AzureDiskVolumeSource] = ...,
        azure_file: typing.Optional[
            kubernetes.client.V1AzureFilePersistentVolumeSource
        ] = ...,
        capacity: typing.Optional[dict[str, str]] = ...,
        cephfs: typing.Optional[kubernetes.client.V1CephFSPersistentVolumeSource] = ...,
        cinder: typing.Optional[kubernetes.client.V1CinderPersistentVolumeSource] = ...,
        claim_ref: typing.Optional[kubernetes.client.V1ObjectReference] = ...,
        csi: typing.Optional[kubernetes.client.V1CSIPersistentVolumeSource] = ...,
        fc: typing.Optional[kubernetes.client.V1FCVolumeSource] = ...,
        flex_volume: typing.Optional[
            kubernetes.client.V1FlexPersistentVolumeSource
        ] = ...,
        flocker: typing.Optional[kubernetes.client.V1FlockerVolumeSource] = ...,
        gce_persistent_disk: typing.Optional[
            kubernetes.client.V1GCEPersistentDiskVolumeSource
        ] = ...,
        glusterfs: typing.Optional[
            kubernetes.client.V1GlusterfsPersistentVolumeSource
        ] = ...,
        host_path: typing.Optional[kubernetes.client.V1HostPathVolumeSource] = ...,
        iscsi: typing.Optional[kubernetes.client.V1ISCSIPersistentVolumeSource] = ...,
        local: typing.Optional[kubernetes.client.V1LocalVolumeSource] = ...,
        mount_options: typing.Optional[list[str]] = ...,
        nfs: typing.Optional[kubernetes.client.V1NFSVolumeSource] = ...,
        node_affinity: typing.Optional[kubernetes.client.V1VolumeNodeAffinity] = ...,
        persistent_volume_reclaim_policy: typing.Optional[str] = ...,
        photon_persistent_disk: typing.Optional[
            kubernetes.client.V1PhotonPersistentDiskVolumeSource
        ] = ...,
        portworx_volume: typing.Optional[
            kubernetes.client.V1PortworxVolumeSource
        ] = ...,
        quobyte: typing.Optional[kubernetes.client.V1QuobyteVolumeSource] = ...,
        rbd: typing.Optional[kubernetes.client.V1RBDPersistentVolumeSource] = ...,
        scale_io: typing.Optional[
            kubernetes.client.V1ScaleIOPersistentVolumeSource
        ] = ...,
        storage_class_name: typing.Optional[str] = ...,
        storageos: typing.Optional[
            kubernetes.client.V1StorageOSPersistentVolumeSource
        ] = ...,
        volume_mode: typing.Optional[str] = ...,
        vsphere_volume: typing.Optional[
            kubernetes.client.V1VsphereVirtualDiskVolumeSource
        ] = ...
    ) -> None: ...
    def to_dict(self) -> V1PersistentVolumeSpecDict: ...

class V1PersistentVolumeSpecDict(typing.TypedDict, total=False):
    accessModes: typing.Optional[list[str]]
    awsElasticBlockStore: typing.Optional[
        kubernetes.client.V1AWSElasticBlockStoreVolumeSourceDict
    ]
    azureDisk: typing.Optional[kubernetes.client.V1AzureDiskVolumeSourceDict]
    azureFile: typing.Optional[kubernetes.client.V1AzureFilePersistentVolumeSourceDict]
    capacity: typing.Optional[dict[str, str]]
    cephfs: typing.Optional[kubernetes.client.V1CephFSPersistentVolumeSourceDict]
    cinder: typing.Optional[kubernetes.client.V1CinderPersistentVolumeSourceDict]
    claimRef: typing.Optional[kubernetes.client.V1ObjectReferenceDict]
    csi: typing.Optional[kubernetes.client.V1CSIPersistentVolumeSourceDict]
    fc: typing.Optional[kubernetes.client.V1FCVolumeSourceDict]
    flexVolume: typing.Optional[kubernetes.client.V1FlexPersistentVolumeSourceDict]
    flocker: typing.Optional[kubernetes.client.V1FlockerVolumeSourceDict]
    gcePersistentDisk: typing.Optional[
        kubernetes.client.V1GCEPersistentDiskVolumeSourceDict
    ]
    glusterfs: typing.Optional[kubernetes.client.V1GlusterfsPersistentVolumeSourceDict]
    hostPath: typing.Optional[kubernetes.client.V1HostPathVolumeSourceDict]
    iscsi: typing.Optional[kubernetes.client.V1ISCSIPersistentVolumeSourceDict]
    local: typing.Optional[kubernetes.client.V1LocalVolumeSourceDict]
    mountOptions: typing.Optional[list[str]]
    nfs: typing.Optional[kubernetes.client.V1NFSVolumeSourceDict]
    nodeAffinity: typing.Optional[kubernetes.client.V1VolumeNodeAffinityDict]
    persistentVolumeReclaimPolicy: typing.Optional[str]
    photonPersistentDisk: typing.Optional[
        kubernetes.client.V1PhotonPersistentDiskVolumeSourceDict
    ]
    portworxVolume: typing.Optional[kubernetes.client.V1PortworxVolumeSourceDict]
    quobyte: typing.Optional[kubernetes.client.V1QuobyteVolumeSourceDict]
    rbd: typing.Optional[kubernetes.client.V1RBDPersistentVolumeSourceDict]
    scaleIO: typing.Optional[kubernetes.client.V1ScaleIOPersistentVolumeSourceDict]
    storageClassName: typing.Optional[str]
    storageos: typing.Optional[kubernetes.client.V1StorageOSPersistentVolumeSourceDict]
    volumeMode: typing.Optional[str]
    vsphereVolume: typing.Optional[
        kubernetes.client.V1VsphereVirtualDiskVolumeSourceDict
    ]
