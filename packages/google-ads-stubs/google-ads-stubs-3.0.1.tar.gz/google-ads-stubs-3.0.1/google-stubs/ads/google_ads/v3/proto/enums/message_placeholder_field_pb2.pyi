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

class MessagePlaceholderFieldEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class MessagePlaceholderField(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "MessagePlaceholderFieldEnum.MessagePlaceholderField": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["MessagePlaceholderFieldEnum.MessagePlaceholderField"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "MessagePlaceholderFieldEnum.MessagePlaceholderField"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 0
        )
        UNKNOWN = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 1
        )
        BUSINESS_NAME = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 2
        )
        COUNTRY_CODE = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 3
        )
        PHONE_NUMBER = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 4
        )
        MESSAGE_EXTENSION_TEXT = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 5
        )
        MESSAGE_TEXT = typing___cast(
            "MessagePlaceholderFieldEnum.MessagePlaceholderField", 6
        )
    UNSPECIFIED = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 0
    )
    UNKNOWN = typing___cast("MessagePlaceholderFieldEnum.MessagePlaceholderField", 1)
    BUSINESS_NAME = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 2
    )
    COUNTRY_CODE = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 3
    )
    PHONE_NUMBER = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 4
    )
    MESSAGE_EXTENSION_TEXT = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 5
    )
    MESSAGE_TEXT = typing___cast(
        "MessagePlaceholderFieldEnum.MessagePlaceholderField", 6
    )
    global___MessagePlaceholderField = MessagePlaceholderField
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MessagePlaceholderFieldEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MessagePlaceholderFieldEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___MessagePlaceholderFieldEnum = MessagePlaceholderFieldEnum
