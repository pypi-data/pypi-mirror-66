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

class ExtensionTypeEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ExtensionType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "ExtensionTypeEnum.ExtensionType": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["ExtensionTypeEnum.ExtensionType"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "ExtensionTypeEnum.ExtensionType"]
        ]: ...
        UNSPECIFIED = typing___cast("ExtensionTypeEnum.ExtensionType", 0)
        UNKNOWN = typing___cast("ExtensionTypeEnum.ExtensionType", 1)
        NONE = typing___cast("ExtensionTypeEnum.ExtensionType", 2)
        APP = typing___cast("ExtensionTypeEnum.ExtensionType", 3)
        CALL = typing___cast("ExtensionTypeEnum.ExtensionType", 4)
        CALLOUT = typing___cast("ExtensionTypeEnum.ExtensionType", 5)
        MESSAGE = typing___cast("ExtensionTypeEnum.ExtensionType", 6)
        PRICE = typing___cast("ExtensionTypeEnum.ExtensionType", 7)
        PROMOTION = typing___cast("ExtensionTypeEnum.ExtensionType", 8)
        REVIEW = typing___cast("ExtensionTypeEnum.ExtensionType", 9)
        SITELINK = typing___cast("ExtensionTypeEnum.ExtensionType", 10)
        STRUCTURED_SNIPPET = typing___cast("ExtensionTypeEnum.ExtensionType", 11)
        LOCATION = typing___cast("ExtensionTypeEnum.ExtensionType", 12)
        AFFILIATE_LOCATION = typing___cast("ExtensionTypeEnum.ExtensionType", 13)
    UNSPECIFIED = typing___cast("ExtensionTypeEnum.ExtensionType", 0)
    UNKNOWN = typing___cast("ExtensionTypeEnum.ExtensionType", 1)
    NONE = typing___cast("ExtensionTypeEnum.ExtensionType", 2)
    APP = typing___cast("ExtensionTypeEnum.ExtensionType", 3)
    CALL = typing___cast("ExtensionTypeEnum.ExtensionType", 4)
    CALLOUT = typing___cast("ExtensionTypeEnum.ExtensionType", 5)
    MESSAGE = typing___cast("ExtensionTypeEnum.ExtensionType", 6)
    PRICE = typing___cast("ExtensionTypeEnum.ExtensionType", 7)
    PROMOTION = typing___cast("ExtensionTypeEnum.ExtensionType", 8)
    REVIEW = typing___cast("ExtensionTypeEnum.ExtensionType", 9)
    SITELINK = typing___cast("ExtensionTypeEnum.ExtensionType", 10)
    STRUCTURED_SNIPPET = typing___cast("ExtensionTypeEnum.ExtensionType", 11)
    LOCATION = typing___cast("ExtensionTypeEnum.ExtensionType", 12)
    AFFILIATE_LOCATION = typing___cast("ExtensionTypeEnum.ExtensionType", 13)
    global___ExtensionType = ExtensionType
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ExtensionTypeEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ExtensionTypeEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ExtensionTypeEnum = ExtensionTypeEnum
