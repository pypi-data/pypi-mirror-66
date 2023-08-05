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

class HotelPlaceholderFieldEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class HotelPlaceholderField(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "HotelPlaceholderFieldEnum.HotelPlaceholderField": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["HotelPlaceholderFieldEnum.HotelPlaceholderField"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "HotelPlaceholderFieldEnum.HotelPlaceholderField"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 0
        )
        UNKNOWN = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 1)
        PROPERTY_ID = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 2
        )
        PROPERTY_NAME = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 3
        )
        DESTINATION_NAME = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 4
        )
        DESCRIPTION = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 5
        )
        ADDRESS = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 6)
        PRICE = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 7)
        FORMATTED_PRICE = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 8
        )
        SALE_PRICE = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 9)
        FORMATTED_SALE_PRICE = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 10
        )
        IMAGE_URL = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 11)
        CATEGORY = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 12)
        STAR_RATING = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 13
        )
        CONTEXTUAL_KEYWORDS = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 14
        )
        FINAL_URLS = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 15
        )
        FINAL_MOBILE_URLS = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 16
        )
        TRACKING_URL = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 17
        )
        ANDROID_APP_LINK = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 18
        )
        SIMILAR_PROPERTY_IDS = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 19
        )
        IOS_APP_LINK = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 20
        )
        IOS_APP_STORE_ID = typing___cast(
            "HotelPlaceholderFieldEnum.HotelPlaceholderField", 21
        )
    UNSPECIFIED = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 0)
    UNKNOWN = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 1)
    PROPERTY_ID = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 2)
    PROPERTY_NAME = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 3)
    DESTINATION_NAME = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 4
    )
    DESCRIPTION = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 5)
    ADDRESS = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 6)
    PRICE = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 7)
    FORMATTED_PRICE = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 8
    )
    SALE_PRICE = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 9)
    FORMATTED_SALE_PRICE = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 10
    )
    IMAGE_URL = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 11)
    CATEGORY = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 12)
    STAR_RATING = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 13)
    CONTEXTUAL_KEYWORDS = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 14
    )
    FINAL_URLS = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 15)
    FINAL_MOBILE_URLS = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 16
    )
    TRACKING_URL = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 17)
    ANDROID_APP_LINK = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 18
    )
    SIMILAR_PROPERTY_IDS = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 19
    )
    IOS_APP_LINK = typing___cast("HotelPlaceholderFieldEnum.HotelPlaceholderField", 20)
    IOS_APP_STORE_ID = typing___cast(
        "HotelPlaceholderFieldEnum.HotelPlaceholderField", 21
    )
    global___HotelPlaceholderField = HotelPlaceholderField
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> HotelPlaceholderFieldEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> HotelPlaceholderFieldEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___HotelPlaceholderFieldEnum = HotelPlaceholderFieldEnum
