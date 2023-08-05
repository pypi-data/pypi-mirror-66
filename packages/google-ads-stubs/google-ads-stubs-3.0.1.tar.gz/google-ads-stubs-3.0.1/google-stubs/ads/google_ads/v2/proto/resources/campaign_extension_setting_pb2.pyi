# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v2.proto.enums.extension_setting_device_pb2 import (
    ExtensionSettingDeviceEnum as google___ads___googleads___v2___enums___extension_setting_device_pb2___ExtensionSettingDeviceEnum,
)

from google.ads.google_ads.v2.proto.enums.extension_type_pb2 import (
    ExtensionTypeEnum as google___ads___googleads___v2___enums___extension_type_pb2___ExtensionTypeEnum,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
    Union as typing___Union,
)

from typing_extensions import Literal as typing_extensions___Literal

builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode

class CampaignExtensionSetting(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    extension_type = (
        ...
    )  # type: google___ads___googleads___v2___enums___extension_type_pb2___ExtensionTypeEnum.ExtensionType
    device = (
        ...
    )  # type: google___ads___googleads___v2___enums___extension_setting_device_pb2___ExtensionSettingDeviceEnum.ExtensionSettingDevice
    @property
    def campaign(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def extension_feed_items(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        extension_type: typing___Optional[
            google___ads___googleads___v2___enums___extension_type_pb2___ExtensionTypeEnum.ExtensionType
        ] = None,
        campaign: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        extension_feed_items: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        device: typing___Optional[
            google___ads___googleads___v2___enums___extension_setting_device_pb2___ExtensionSettingDeviceEnum.ExtensionSettingDevice
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CampaignExtensionSetting: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> CampaignExtensionSetting: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self, field_name: typing_extensions___Literal["campaign", b"campaign"]
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "campaign",
            b"campaign",
            "device",
            b"device",
            "extension_feed_items",
            b"extension_feed_items",
            "extension_type",
            b"extension_type",
            "resource_name",
            b"resource_name",
        ],
    ) -> None: ...

global___CampaignExtensionSetting = CampaignExtensionSetting
