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

class ExternalConversionSourceEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ExternalConversionSource(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "ExternalConversionSourceEnum.ExternalConversionSource": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["ExternalConversionSourceEnum.ExternalConversionSource"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "ExternalConversionSourceEnum.ExternalConversionSource"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 0
        )
        UNKNOWN = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 1
        )
        WEBPAGE = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 2
        )
        ANALYTICS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 3
        )
        UPLOAD = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 4
        )
        AD_CALL_METRICS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 5
        )
        WEBSITE_CALL_METRICS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 6
        )
        STORE_VISITS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 7
        )
        ANDROID_IN_APP = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 8
        )
        IOS_IN_APP = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 9
        )
        IOS_FIRST_OPEN = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 10
        )
        APP_UNSPECIFIED = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 11
        )
        ANDROID_FIRST_OPEN = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 12
        )
        UPLOAD_CALLS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 13
        )
        FIREBASE = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 14
        )
        CLICK_TO_CALL = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 15
        )
        SALESFORCE = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 16
        )
        STORE_SALES_CRM = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 17
        )
        STORE_SALES_PAYMENT_NETWORK = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 18
        )
        GOOGLE_PLAY = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 19
        )
        THIRD_PARTY_APP_ANALYTICS = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 20
        )
        GOOGLE_ATTRIBUTION = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 21
        )
        STORE_SALES_DIRECT = typing___cast(
            "ExternalConversionSourceEnum.ExternalConversionSource", 22
        )
    UNSPECIFIED = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 0
    )
    UNKNOWN = typing___cast("ExternalConversionSourceEnum.ExternalConversionSource", 1)
    WEBPAGE = typing___cast("ExternalConversionSourceEnum.ExternalConversionSource", 2)
    ANALYTICS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 3
    )
    UPLOAD = typing___cast("ExternalConversionSourceEnum.ExternalConversionSource", 4)
    AD_CALL_METRICS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 5
    )
    WEBSITE_CALL_METRICS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 6
    )
    STORE_VISITS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 7
    )
    ANDROID_IN_APP = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 8
    )
    IOS_IN_APP = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 9
    )
    IOS_FIRST_OPEN = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 10
    )
    APP_UNSPECIFIED = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 11
    )
    ANDROID_FIRST_OPEN = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 12
    )
    UPLOAD_CALLS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 13
    )
    FIREBASE = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 14
    )
    CLICK_TO_CALL = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 15
    )
    SALESFORCE = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 16
    )
    STORE_SALES_CRM = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 17
    )
    STORE_SALES_PAYMENT_NETWORK = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 18
    )
    GOOGLE_PLAY = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 19
    )
    THIRD_PARTY_APP_ANALYTICS = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 20
    )
    GOOGLE_ATTRIBUTION = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 21
    )
    STORE_SALES_DIRECT = typing___cast(
        "ExternalConversionSourceEnum.ExternalConversionSource", 22
    )
    global___ExternalConversionSource = ExternalConversionSource
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ExternalConversionSourceEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ExternalConversionSourceEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ExternalConversionSourceEnum = ExternalConversionSourceEnum
