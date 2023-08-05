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

class GeoTargetConstantSuggestionErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class GeoTargetConstantSuggestionError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List[
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError"
        ]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str,
                "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError",
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 0
        )
        UNKNOWN = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 1
        )
        LOCATION_NAME_SIZE_LIMIT = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 2
        )
        LOCATION_NAME_LIMIT = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 3
        )
        INVALID_COUNTRY_CODE = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 4
        )
        REQUEST_PARAMETERS_UNSET = typing___cast(
            "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 5
        )
    UNSPECIFIED = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 0
    )
    UNKNOWN = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 1
    )
    LOCATION_NAME_SIZE_LIMIT = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 2
    )
    LOCATION_NAME_LIMIT = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 3
    )
    INVALID_COUNTRY_CODE = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 4
    )
    REQUEST_PARAMETERS_UNSET = typing___cast(
        "GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError", 5
    )
    global___GeoTargetConstantSuggestionError = GeoTargetConstantSuggestionError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(
            cls, s: builtin___bytes
        ) -> GeoTargetConstantSuggestionErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GeoTargetConstantSuggestionErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___GeoTargetConstantSuggestionErrorEnum = GeoTargetConstantSuggestionErrorEnum
