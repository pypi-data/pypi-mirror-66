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

class AuthorizationErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class AuthorizationError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "AuthorizationErrorEnum.AuthorizationError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["AuthorizationErrorEnum.AuthorizationError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "AuthorizationErrorEnum.AuthorizationError"]
        ]: ...
        UNSPECIFIED = typing___cast("AuthorizationErrorEnum.AuthorizationError", 0)
        UNKNOWN = typing___cast("AuthorizationErrorEnum.AuthorizationError", 1)
        USER_PERMISSION_DENIED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 2
        )
        DEVELOPER_TOKEN_NOT_WHITELISTED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 3
        )
        DEVELOPER_TOKEN_PROHIBITED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 4
        )
        PROJECT_DISABLED = typing___cast("AuthorizationErrorEnum.AuthorizationError", 5)
        AUTHORIZATION_ERROR = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 6
        )
        ACTION_NOT_PERMITTED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 7
        )
        INCOMPLETE_SIGNUP = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 8
        )
        CUSTOMER_NOT_ENABLED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 24
        )
        MISSING_TOS = typing___cast("AuthorizationErrorEnum.AuthorizationError", 9)
        DEVELOPER_TOKEN_NOT_APPROVED = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 10
        )
        INVALID_LOGIN_CUSTOMER_ID_SERVING_CUSTOMER_ID_COMBINATION = typing___cast(
            "AuthorizationErrorEnum.AuthorizationError", 11
        )
    UNSPECIFIED = typing___cast("AuthorizationErrorEnum.AuthorizationError", 0)
    UNKNOWN = typing___cast("AuthorizationErrorEnum.AuthorizationError", 1)
    USER_PERMISSION_DENIED = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 2
    )
    DEVELOPER_TOKEN_NOT_WHITELISTED = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 3
    )
    DEVELOPER_TOKEN_PROHIBITED = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 4
    )
    PROJECT_DISABLED = typing___cast("AuthorizationErrorEnum.AuthorizationError", 5)
    AUTHORIZATION_ERROR = typing___cast("AuthorizationErrorEnum.AuthorizationError", 6)
    ACTION_NOT_PERMITTED = typing___cast("AuthorizationErrorEnum.AuthorizationError", 7)
    INCOMPLETE_SIGNUP = typing___cast("AuthorizationErrorEnum.AuthorizationError", 8)
    CUSTOMER_NOT_ENABLED = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 24
    )
    MISSING_TOS = typing___cast("AuthorizationErrorEnum.AuthorizationError", 9)
    DEVELOPER_TOKEN_NOT_APPROVED = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 10
    )
    INVALID_LOGIN_CUSTOMER_ID_SERVING_CUSTOMER_ID_COMBINATION = typing___cast(
        "AuthorizationErrorEnum.AuthorizationError", 11
    )
    global___AuthorizationError = AuthorizationError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AuthorizationErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> AuthorizationErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___AuthorizationErrorEnum = AuthorizationErrorEnum
