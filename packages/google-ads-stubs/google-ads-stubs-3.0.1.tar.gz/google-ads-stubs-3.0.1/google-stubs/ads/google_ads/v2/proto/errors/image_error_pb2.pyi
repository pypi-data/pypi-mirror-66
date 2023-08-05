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

class ImageErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ImageError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "ImageErrorEnum.ImageError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["ImageErrorEnum.ImageError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "ImageErrorEnum.ImageError"]
        ]: ...
        UNSPECIFIED = typing___cast("ImageErrorEnum.ImageError", 0)
        UNKNOWN = typing___cast("ImageErrorEnum.ImageError", 1)
        INVALID_IMAGE = typing___cast("ImageErrorEnum.ImageError", 2)
        STORAGE_ERROR = typing___cast("ImageErrorEnum.ImageError", 3)
        BAD_REQUEST = typing___cast("ImageErrorEnum.ImageError", 4)
        UNEXPECTED_SIZE = typing___cast("ImageErrorEnum.ImageError", 5)
        ANIMATED_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 6)
        ANIMATION_TOO_LONG = typing___cast("ImageErrorEnum.ImageError", 7)
        SERVER_ERROR = typing___cast("ImageErrorEnum.ImageError", 8)
        CMYK_JPEG_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 9)
        FLASH_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 10)
        FLASH_WITHOUT_CLICKTAG = typing___cast("ImageErrorEnum.ImageError", 11)
        FLASH_ERROR_AFTER_FIXING_CLICK_TAG = typing___cast(
            "ImageErrorEnum.ImageError", 12
        )
        ANIMATED_VISUAL_EFFECT = typing___cast("ImageErrorEnum.ImageError", 13)
        FLASH_ERROR = typing___cast("ImageErrorEnum.ImageError", 14)
        LAYOUT_PROBLEM = typing___cast("ImageErrorEnum.ImageError", 15)
        PROBLEM_READING_IMAGE_FILE = typing___cast("ImageErrorEnum.ImageError", 16)
        ERROR_STORING_IMAGE = typing___cast("ImageErrorEnum.ImageError", 17)
        ASPECT_RATIO_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 18)
        FLASH_HAS_NETWORK_OBJECTS = typing___cast("ImageErrorEnum.ImageError", 19)
        FLASH_HAS_NETWORK_METHODS = typing___cast("ImageErrorEnum.ImageError", 20)
        FLASH_HAS_URL = typing___cast("ImageErrorEnum.ImageError", 21)
        FLASH_HAS_MOUSE_TRACKING = typing___cast("ImageErrorEnum.ImageError", 22)
        FLASH_HAS_RANDOM_NUM = typing___cast("ImageErrorEnum.ImageError", 23)
        FLASH_SELF_TARGETS = typing___cast("ImageErrorEnum.ImageError", 24)
        FLASH_BAD_GETURL_TARGET = typing___cast("ImageErrorEnum.ImageError", 25)
        FLASH_VERSION_NOT_SUPPORTED = typing___cast("ImageErrorEnum.ImageError", 26)
        FLASH_WITHOUT_HARD_CODED_CLICK_URL = typing___cast(
            "ImageErrorEnum.ImageError", 27
        )
        INVALID_FLASH_FILE = typing___cast("ImageErrorEnum.ImageError", 28)
        FAILED_TO_FIX_CLICK_TAG_IN_FLASH = typing___cast(
            "ImageErrorEnum.ImageError", 29
        )
        FLASH_ACCESSES_NETWORK_RESOURCES = typing___cast(
            "ImageErrorEnum.ImageError", 30
        )
        FLASH_EXTERNAL_JS_CALL = typing___cast("ImageErrorEnum.ImageError", 31)
        FLASH_EXTERNAL_FS_CALL = typing___cast("ImageErrorEnum.ImageError", 32)
        FILE_TOO_LARGE = typing___cast("ImageErrorEnum.ImageError", 33)
        IMAGE_DATA_TOO_LARGE = typing___cast("ImageErrorEnum.ImageError", 34)
        IMAGE_PROCESSING_ERROR = typing___cast("ImageErrorEnum.ImageError", 35)
        IMAGE_TOO_SMALL = typing___cast("ImageErrorEnum.ImageError", 36)
        INVALID_INPUT = typing___cast("ImageErrorEnum.ImageError", 37)
        PROBLEM_READING_FILE = typing___cast("ImageErrorEnum.ImageError", 38)
    UNSPECIFIED = typing___cast("ImageErrorEnum.ImageError", 0)
    UNKNOWN = typing___cast("ImageErrorEnum.ImageError", 1)
    INVALID_IMAGE = typing___cast("ImageErrorEnum.ImageError", 2)
    STORAGE_ERROR = typing___cast("ImageErrorEnum.ImageError", 3)
    BAD_REQUEST = typing___cast("ImageErrorEnum.ImageError", 4)
    UNEXPECTED_SIZE = typing___cast("ImageErrorEnum.ImageError", 5)
    ANIMATED_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 6)
    ANIMATION_TOO_LONG = typing___cast("ImageErrorEnum.ImageError", 7)
    SERVER_ERROR = typing___cast("ImageErrorEnum.ImageError", 8)
    CMYK_JPEG_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 9)
    FLASH_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 10)
    FLASH_WITHOUT_CLICKTAG = typing___cast("ImageErrorEnum.ImageError", 11)
    FLASH_ERROR_AFTER_FIXING_CLICK_TAG = typing___cast("ImageErrorEnum.ImageError", 12)
    ANIMATED_VISUAL_EFFECT = typing___cast("ImageErrorEnum.ImageError", 13)
    FLASH_ERROR = typing___cast("ImageErrorEnum.ImageError", 14)
    LAYOUT_PROBLEM = typing___cast("ImageErrorEnum.ImageError", 15)
    PROBLEM_READING_IMAGE_FILE = typing___cast("ImageErrorEnum.ImageError", 16)
    ERROR_STORING_IMAGE = typing___cast("ImageErrorEnum.ImageError", 17)
    ASPECT_RATIO_NOT_ALLOWED = typing___cast("ImageErrorEnum.ImageError", 18)
    FLASH_HAS_NETWORK_OBJECTS = typing___cast("ImageErrorEnum.ImageError", 19)
    FLASH_HAS_NETWORK_METHODS = typing___cast("ImageErrorEnum.ImageError", 20)
    FLASH_HAS_URL = typing___cast("ImageErrorEnum.ImageError", 21)
    FLASH_HAS_MOUSE_TRACKING = typing___cast("ImageErrorEnum.ImageError", 22)
    FLASH_HAS_RANDOM_NUM = typing___cast("ImageErrorEnum.ImageError", 23)
    FLASH_SELF_TARGETS = typing___cast("ImageErrorEnum.ImageError", 24)
    FLASH_BAD_GETURL_TARGET = typing___cast("ImageErrorEnum.ImageError", 25)
    FLASH_VERSION_NOT_SUPPORTED = typing___cast("ImageErrorEnum.ImageError", 26)
    FLASH_WITHOUT_HARD_CODED_CLICK_URL = typing___cast("ImageErrorEnum.ImageError", 27)
    INVALID_FLASH_FILE = typing___cast("ImageErrorEnum.ImageError", 28)
    FAILED_TO_FIX_CLICK_TAG_IN_FLASH = typing___cast("ImageErrorEnum.ImageError", 29)
    FLASH_ACCESSES_NETWORK_RESOURCES = typing___cast("ImageErrorEnum.ImageError", 30)
    FLASH_EXTERNAL_JS_CALL = typing___cast("ImageErrorEnum.ImageError", 31)
    FLASH_EXTERNAL_FS_CALL = typing___cast("ImageErrorEnum.ImageError", 32)
    FILE_TOO_LARGE = typing___cast("ImageErrorEnum.ImageError", 33)
    IMAGE_DATA_TOO_LARGE = typing___cast("ImageErrorEnum.ImageError", 34)
    IMAGE_PROCESSING_ERROR = typing___cast("ImageErrorEnum.ImageError", 35)
    IMAGE_TOO_SMALL = typing___cast("ImageErrorEnum.ImageError", 36)
    INVALID_INPUT = typing___cast("ImageErrorEnum.ImageError", 37)
    PROBLEM_READING_FILE = typing___cast("ImageErrorEnum.ImageError", 38)
    global___ImageError = ImageError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ImageErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ImageErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ImageErrorEnum = ImageErrorEnum
