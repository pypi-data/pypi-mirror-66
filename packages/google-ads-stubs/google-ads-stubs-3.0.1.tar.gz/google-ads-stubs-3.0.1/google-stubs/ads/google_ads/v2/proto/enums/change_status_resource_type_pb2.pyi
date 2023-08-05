# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from typing import (
    List as typing___List,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

builtin___bytes = bytes
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode

class ChangeStatusResourceTypeEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ChangeStatusResourceType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "ChangeStatusResourceTypeEnum.ChangeStatusResourceType": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["ChangeStatusResourceTypeEnum.ChangeStatusResourceType"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "ChangeStatusResourceTypeEnum.ChangeStatusResourceType"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 0
        )
        UNKNOWN = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 1
        )
        AD_GROUP = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 3
        )
        AD_GROUP_AD = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 4
        )
        AD_GROUP_CRITERION = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 5
        )
        CAMPAIGN = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 6
        )
        CAMPAIGN_CRITERION = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 7
        )
        FEED = typing___cast("ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 9)
        FEED_ITEM = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 10
        )
        AD_GROUP_FEED = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 11
        )
        CAMPAIGN_FEED = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 12
        )
        AD_GROUP_BID_MODIFIER = typing___cast(
            "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 13
        )
    UNSPECIFIED = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 0
    )
    UNKNOWN = typing___cast("ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 1)
    AD_GROUP = typing___cast("ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 3)
    AD_GROUP_AD = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 4
    )
    AD_GROUP_CRITERION = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 5
    )
    CAMPAIGN = typing___cast("ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 6)
    CAMPAIGN_CRITERION = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 7
    )
    FEED = typing___cast("ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 9)
    FEED_ITEM = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 10
    )
    AD_GROUP_FEED = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 11
    )
    CAMPAIGN_FEED = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 12
    )
    AD_GROUP_BID_MODIFIER = typing___cast(
        "ChangeStatusResourceTypeEnum.ChangeStatusResourceType", 13
    )
    global___ChangeStatusResourceType = ChangeStatusResourceType
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ChangeStatusResourceTypeEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ChangeStatusResourceTypeEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ChangeStatusResourceTypeEnum = ChangeStatusResourceTypeEnum
