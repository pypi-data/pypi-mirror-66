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

class ProductTypeLevelEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ProductTypeLevel(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "ProductTypeLevelEnum.ProductTypeLevel": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["ProductTypeLevelEnum.ProductTypeLevel"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "ProductTypeLevelEnum.ProductTypeLevel"]
        ]: ...
        UNSPECIFIED = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 0)
        UNKNOWN = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 1)
        LEVEL1 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 7)
        LEVEL2 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 8)
        LEVEL3 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 9)
        LEVEL4 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 10)
        LEVEL5 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 11)
    UNSPECIFIED = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 0)
    UNKNOWN = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 1)
    LEVEL1 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 7)
    LEVEL2 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 8)
    LEVEL3 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 9)
    LEVEL4 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 10)
    LEVEL5 = typing___cast("ProductTypeLevelEnum.ProductTypeLevel", 11)
    global___ProductTypeLevel = ProductTypeLevel
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ProductTypeLevelEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ProductTypeLevelEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ProductTypeLevelEnum = ProductTypeLevelEnum
