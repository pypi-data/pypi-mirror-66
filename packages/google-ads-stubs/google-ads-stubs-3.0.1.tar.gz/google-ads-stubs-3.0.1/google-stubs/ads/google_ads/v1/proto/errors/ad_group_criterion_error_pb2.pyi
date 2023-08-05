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

class AdGroupCriterionErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class AdGroupCriterionError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "AdGroupCriterionErrorEnum.AdGroupCriterionError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List["AdGroupCriterionErrorEnum.AdGroupCriterionError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str, "AdGroupCriterionErrorEnum.AdGroupCriterionError"
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 0
        )
        UNKNOWN = typing___cast("AdGroupCriterionErrorEnum.AdGroupCriterionError", 1)
        AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 2
        )
        AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 3
        )
        CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 4
        )
        TOO_MANY_OPERATIONS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 5
        )
        CANT_UPDATE_NEGATIVE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 6
        )
        CONCRETE_TYPE_REQUIRED = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 7
        )
        BID_INCOMPATIBLE_WITH_ADGROUP = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 8
        )
        CANNOT_TARGET_AND_EXCLUDE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 9
        )
        ILLEGAL_URL = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 10
        )
        INVALID_KEYWORD_TEXT = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 11
        )
        INVALID_DESTINATION_URL = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 12
        )
        MISSING_DESTINATION_URL_TAG = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 13
        )
        KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 14
        )
        INVALID_USER_STATUS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 15
        )
        CANNOT_ADD_CRITERIA_TYPE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 16
        )
        CANNOT_EXCLUDE_CRITERIA_TYPE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 17
        )
        CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 27
        )
        OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 28
        )
        CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 29
        )
        CANNOT_SET_WITHOUT_FINAL_URLS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 30
        )
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 31
        )
        CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 32
        )
        CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 33
        )
        CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 34
        )
        CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 35
        )
        CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 36
        )
        FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 37
        )
        FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 38
        )
        INVALID_LISTING_GROUP_HIERARCHY = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 39
        )
        LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 40
        )
        LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 41
        )
        LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 42
        )
        LISTING_GROUP_ALREADY_EXISTS = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 43
        )
        LISTING_GROUP_DOES_NOT_EXIST = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 44
        )
        LISTING_GROUP_CANNOT_BE_REMOVED = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 45
        )
        INVALID_LISTING_GROUP_TYPE = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 46
        )
        LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID = typing___cast(
            "AdGroupCriterionErrorEnum.AdGroupCriterionError", 47
        )
    UNSPECIFIED = typing___cast("AdGroupCriterionErrorEnum.AdGroupCriterionError", 0)
    UNKNOWN = typing___cast("AdGroupCriterionErrorEnum.AdGroupCriterionError", 1)
    AD_GROUP_CRITERION_LABEL_DOES_NOT_EXIST = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 2
    )
    AD_GROUP_CRITERION_LABEL_ALREADY_EXISTS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 3
    )
    CANNOT_ADD_LABEL_TO_NEGATIVE_CRITERION = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 4
    )
    TOO_MANY_OPERATIONS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 5
    )
    CANT_UPDATE_NEGATIVE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 6
    )
    CONCRETE_TYPE_REQUIRED = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 7
    )
    BID_INCOMPATIBLE_WITH_ADGROUP = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 8
    )
    CANNOT_TARGET_AND_EXCLUDE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 9
    )
    ILLEGAL_URL = typing___cast("AdGroupCriterionErrorEnum.AdGroupCriterionError", 10)
    INVALID_KEYWORD_TEXT = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 11
    )
    INVALID_DESTINATION_URL = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 12
    )
    MISSING_DESTINATION_URL_TAG = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 13
    )
    KEYWORD_LEVEL_BID_NOT_SUPPORTED_FOR_MANUALCPM = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 14
    )
    INVALID_USER_STATUS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 15
    )
    CANNOT_ADD_CRITERIA_TYPE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 16
    )
    CANNOT_EXCLUDE_CRITERIA_TYPE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 17
    )
    CAMPAIGN_TYPE_NOT_COMPATIBLE_WITH_PARTIAL_FAILURE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 27
    )
    OPERATIONS_FOR_TOO_MANY_SHOPPING_ADGROUPS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 28
    )
    CANNOT_MODIFY_URL_FIELDS_WITH_DUPLICATE_ELEMENTS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 29
    )
    CANNOT_SET_WITHOUT_FINAL_URLS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 30
    )
    CANNOT_CLEAR_FINAL_URLS_IF_FINAL_MOBILE_URLS_EXIST = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 31
    )
    CANNOT_CLEAR_FINAL_URLS_IF_FINAL_APP_URLS_EXIST = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 32
    )
    CANNOT_CLEAR_FINAL_URLS_IF_TRACKING_URL_TEMPLATE_EXISTS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 33
    )
    CANNOT_CLEAR_FINAL_URLS_IF_URL_CUSTOM_PARAMETERS_EXIST = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 34
    )
    CANNOT_SET_BOTH_DESTINATION_URL_AND_FINAL_URLS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 35
    )
    CANNOT_SET_BOTH_DESTINATION_URL_AND_TRACKING_URL_TEMPLATE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 36
    )
    FINAL_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 37
    )
    FINAL_MOBILE_URLS_NOT_SUPPORTED_FOR_CRITERION_TYPE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 38
    )
    INVALID_LISTING_GROUP_HIERARCHY = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 39
    )
    LISTING_GROUP_UNIT_CANNOT_HAVE_CHILDREN = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 40
    )
    LISTING_GROUP_SUBDIVISION_REQUIRES_OTHERS_CASE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 41
    )
    LISTING_GROUP_REQUIRES_SAME_DIMENSION_TYPE_AS_SIBLINGS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 42
    )
    LISTING_GROUP_ALREADY_EXISTS = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 43
    )
    LISTING_GROUP_DOES_NOT_EXIST = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 44
    )
    LISTING_GROUP_CANNOT_BE_REMOVED = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 45
    )
    INVALID_LISTING_GROUP_TYPE = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 46
    )
    LISTING_GROUP_ADD_MAY_ONLY_USE_TEMP_ID = typing___cast(
        "AdGroupCriterionErrorEnum.AdGroupCriterionError", 47
    )
    global___AdGroupCriterionError = AdGroupCriterionError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AdGroupCriterionErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> AdGroupCriterionErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___AdGroupCriterionErrorEnum = AdGroupCriterionErrorEnum
