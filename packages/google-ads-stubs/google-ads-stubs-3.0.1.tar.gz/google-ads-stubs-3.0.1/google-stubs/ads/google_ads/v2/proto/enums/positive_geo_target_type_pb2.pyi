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

class PositiveGeoTargetTypeEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class PositiveGeoTargetType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "PositiveGeoTargetTypeEnum.PositiveGeoTargetType": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["PositiveGeoTargetTypeEnum.PositiveGeoTargetType"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "PositiveGeoTargetTypeEnum.PositiveGeoTargetType"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 0
        )
        UNKNOWN = typing___cast("PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 1)
        PRESENCE_OR_INTEREST = typing___cast(
            "PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 5
        )
        SEARCH_INTEREST = typing___cast(
            "PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 6
        )
        PRESENCE = typing___cast("PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 7)
    UNSPECIFIED = typing___cast("PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 0)
    UNKNOWN = typing___cast("PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 1)
    PRESENCE_OR_INTEREST = typing___cast(
        "PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 5
    )
    SEARCH_INTEREST = typing___cast(
        "PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 6
    )
    PRESENCE = typing___cast("PositiveGeoTargetTypeEnum.PositiveGeoTargetType", 7)
    global___PositiveGeoTargetType = PositiveGeoTargetType
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> PositiveGeoTargetTypeEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> PositiveGeoTargetTypeEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___PositiveGeoTargetTypeEnum = PositiveGeoTargetTypeEnum
