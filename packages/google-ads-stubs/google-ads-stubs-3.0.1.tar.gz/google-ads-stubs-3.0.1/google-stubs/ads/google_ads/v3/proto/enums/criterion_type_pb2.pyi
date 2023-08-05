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

class CriterionTypeEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class CriterionType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "CriterionTypeEnum.CriterionType": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["CriterionTypeEnum.CriterionType"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "CriterionTypeEnum.CriterionType"]
        ]: ...
        UNSPECIFIED = typing___cast("CriterionTypeEnum.CriterionType", 0)
        UNKNOWN = typing___cast("CriterionTypeEnum.CriterionType", 1)
        KEYWORD = typing___cast("CriterionTypeEnum.CriterionType", 2)
        PLACEMENT = typing___cast("CriterionTypeEnum.CriterionType", 3)
        MOBILE_APP_CATEGORY = typing___cast("CriterionTypeEnum.CriterionType", 4)
        MOBILE_APPLICATION = typing___cast("CriterionTypeEnum.CriterionType", 5)
        DEVICE = typing___cast("CriterionTypeEnum.CriterionType", 6)
        LOCATION = typing___cast("CriterionTypeEnum.CriterionType", 7)
        LISTING_GROUP = typing___cast("CriterionTypeEnum.CriterionType", 8)
        AD_SCHEDULE = typing___cast("CriterionTypeEnum.CriterionType", 9)
        AGE_RANGE = typing___cast("CriterionTypeEnum.CriterionType", 10)
        GENDER = typing___cast("CriterionTypeEnum.CriterionType", 11)
        INCOME_RANGE = typing___cast("CriterionTypeEnum.CriterionType", 12)
        PARENTAL_STATUS = typing___cast("CriterionTypeEnum.CriterionType", 13)
        YOUTUBE_VIDEO = typing___cast("CriterionTypeEnum.CriterionType", 14)
        YOUTUBE_CHANNEL = typing___cast("CriterionTypeEnum.CriterionType", 15)
        USER_LIST = typing___cast("CriterionTypeEnum.CriterionType", 16)
        PROXIMITY = typing___cast("CriterionTypeEnum.CriterionType", 17)
        TOPIC = typing___cast("CriterionTypeEnum.CriterionType", 18)
        LISTING_SCOPE = typing___cast("CriterionTypeEnum.CriterionType", 19)
        LANGUAGE = typing___cast("CriterionTypeEnum.CriterionType", 20)
        IP_BLOCK = typing___cast("CriterionTypeEnum.CriterionType", 21)
        CONTENT_LABEL = typing___cast("CriterionTypeEnum.CriterionType", 22)
        CARRIER = typing___cast("CriterionTypeEnum.CriterionType", 23)
        USER_INTEREST = typing___cast("CriterionTypeEnum.CriterionType", 24)
        WEBPAGE = typing___cast("CriterionTypeEnum.CriterionType", 25)
        OPERATING_SYSTEM_VERSION = typing___cast("CriterionTypeEnum.CriterionType", 26)
        APP_PAYMENT_MODEL = typing___cast("CriterionTypeEnum.CriterionType", 27)
        MOBILE_DEVICE = typing___cast("CriterionTypeEnum.CriterionType", 28)
        CUSTOM_AFFINITY = typing___cast("CriterionTypeEnum.CriterionType", 29)
        CUSTOM_INTENT = typing___cast("CriterionTypeEnum.CriterionType", 30)
        LOCATION_GROUP = typing___cast("CriterionTypeEnum.CriterionType", 31)
    UNSPECIFIED = typing___cast("CriterionTypeEnum.CriterionType", 0)
    UNKNOWN = typing___cast("CriterionTypeEnum.CriterionType", 1)
    KEYWORD = typing___cast("CriterionTypeEnum.CriterionType", 2)
    PLACEMENT = typing___cast("CriterionTypeEnum.CriterionType", 3)
    MOBILE_APP_CATEGORY = typing___cast("CriterionTypeEnum.CriterionType", 4)
    MOBILE_APPLICATION = typing___cast("CriterionTypeEnum.CriterionType", 5)
    DEVICE = typing___cast("CriterionTypeEnum.CriterionType", 6)
    LOCATION = typing___cast("CriterionTypeEnum.CriterionType", 7)
    LISTING_GROUP = typing___cast("CriterionTypeEnum.CriterionType", 8)
    AD_SCHEDULE = typing___cast("CriterionTypeEnum.CriterionType", 9)
    AGE_RANGE = typing___cast("CriterionTypeEnum.CriterionType", 10)
    GENDER = typing___cast("CriterionTypeEnum.CriterionType", 11)
    INCOME_RANGE = typing___cast("CriterionTypeEnum.CriterionType", 12)
    PARENTAL_STATUS = typing___cast("CriterionTypeEnum.CriterionType", 13)
    YOUTUBE_VIDEO = typing___cast("CriterionTypeEnum.CriterionType", 14)
    YOUTUBE_CHANNEL = typing___cast("CriterionTypeEnum.CriterionType", 15)
    USER_LIST = typing___cast("CriterionTypeEnum.CriterionType", 16)
    PROXIMITY = typing___cast("CriterionTypeEnum.CriterionType", 17)
    TOPIC = typing___cast("CriterionTypeEnum.CriterionType", 18)
    LISTING_SCOPE = typing___cast("CriterionTypeEnum.CriterionType", 19)
    LANGUAGE = typing___cast("CriterionTypeEnum.CriterionType", 20)
    IP_BLOCK = typing___cast("CriterionTypeEnum.CriterionType", 21)
    CONTENT_LABEL = typing___cast("CriterionTypeEnum.CriterionType", 22)
    CARRIER = typing___cast("CriterionTypeEnum.CriterionType", 23)
    USER_INTEREST = typing___cast("CriterionTypeEnum.CriterionType", 24)
    WEBPAGE = typing___cast("CriterionTypeEnum.CriterionType", 25)
    OPERATING_SYSTEM_VERSION = typing___cast("CriterionTypeEnum.CriterionType", 26)
    APP_PAYMENT_MODEL = typing___cast("CriterionTypeEnum.CriterionType", 27)
    MOBILE_DEVICE = typing___cast("CriterionTypeEnum.CriterionType", 28)
    CUSTOM_AFFINITY = typing___cast("CriterionTypeEnum.CriterionType", 29)
    CUSTOM_INTENT = typing___cast("CriterionTypeEnum.CriterionType", 30)
    LOCATION_GROUP = typing___cast("CriterionTypeEnum.CriterionType", 31)
    global___CriterionType = CriterionType
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CriterionTypeEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> CriterionTypeEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___CriterionTypeEnum = CriterionTypeEnum
