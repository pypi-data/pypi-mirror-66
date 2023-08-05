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

class AdvertisingChannelSubTypeEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class AdvertisingChannelSubType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List[
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType"
        ]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 0
        )
        UNKNOWN = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 1
        )
        SEARCH_MOBILE_APP = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 2
        )
        DISPLAY_MOBILE_APP = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 3
        )
        SEARCH_EXPRESS = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 4
        )
        DISPLAY_EXPRESS = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 5
        )
        SHOPPING_SMART_ADS = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 6
        )
        DISPLAY_GMAIL_AD = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 7
        )
        DISPLAY_SMART_CAMPAIGN = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 8
        )
        VIDEO_OUTSTREAM = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 9
        )
        VIDEO_ACTION = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 10
        )
        VIDEO_NON_SKIPPABLE = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 11
        )
        APP_CAMPAIGN = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 12
        )
        APP_CAMPAIGN_FOR_ENGAGEMENT = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 13
        )
        SHOPPING_COMPARISON_LISTING_ADS = typing___cast(
            "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 15
        )
    UNSPECIFIED = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 0
    )
    UNKNOWN = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 1
    )
    SEARCH_MOBILE_APP = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 2
    )
    DISPLAY_MOBILE_APP = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 3
    )
    SEARCH_EXPRESS = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 4
    )
    DISPLAY_EXPRESS = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 5
    )
    SHOPPING_SMART_ADS = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 6
    )
    DISPLAY_GMAIL_AD = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 7
    )
    DISPLAY_SMART_CAMPAIGN = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 8
    )
    VIDEO_OUTSTREAM = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 9
    )
    VIDEO_ACTION = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 10
    )
    VIDEO_NON_SKIPPABLE = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 11
    )
    APP_CAMPAIGN = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 12
    )
    APP_CAMPAIGN_FOR_ENGAGEMENT = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 13
    )
    SHOPPING_COMPARISON_LISTING_ADS = typing___cast(
        "AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType", 15
    )
    global___AdvertisingChannelSubType = AdvertisingChannelSubType
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AdvertisingChannelSubTypeEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> AdvertisingChannelSubTypeEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___AdvertisingChannelSubTypeEnum = AdvertisingChannelSubTypeEnum
