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

class CriterionErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class CriterionError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "CriterionErrorEnum.CriterionError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["CriterionErrorEnum.CriterionError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "CriterionErrorEnum.CriterionError"]
        ]: ...
        UNSPECIFIED = typing___cast("CriterionErrorEnum.CriterionError", 0)
        UNKNOWN = typing___cast("CriterionErrorEnum.CriterionError", 1)
        CONCRETE_TYPE_REQUIRED = typing___cast("CriterionErrorEnum.CriterionError", 2)
        INVALID_EXCLUDED_CATEGORY = typing___cast(
            "CriterionErrorEnum.CriterionError", 3
        )
        INVALID_KEYWORD_TEXT = typing___cast("CriterionErrorEnum.CriterionError", 4)
        KEYWORD_TEXT_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 5)
        KEYWORD_HAS_TOO_MANY_WORDS = typing___cast(
            "CriterionErrorEnum.CriterionError", 6
        )
        KEYWORD_HAS_INVALID_CHARS = typing___cast(
            "CriterionErrorEnum.CriterionError", 7
        )
        INVALID_PLACEMENT_URL = typing___cast("CriterionErrorEnum.CriterionError", 8)
        INVALID_USER_LIST = typing___cast("CriterionErrorEnum.CriterionError", 9)
        INVALID_USER_INTEREST = typing___cast("CriterionErrorEnum.CriterionError", 10)
        INVALID_FORMAT_FOR_PLACEMENT_URL = typing___cast(
            "CriterionErrorEnum.CriterionError", 11
        )
        PLACEMENT_URL_IS_TOO_LONG = typing___cast(
            "CriterionErrorEnum.CriterionError", 12
        )
        PLACEMENT_URL_HAS_ILLEGAL_CHAR = typing___cast(
            "CriterionErrorEnum.CriterionError", 13
        )
        PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE = typing___cast(
            "CriterionErrorEnum.CriterionError", 14
        )
        PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION = typing___cast(
            "CriterionErrorEnum.CriterionError", 15
        )
        INVALID_TOPIC_PATH = typing___cast("CriterionErrorEnum.CriterionError", 16)
        INVALID_YOUTUBE_CHANNEL_ID = typing___cast(
            "CriterionErrorEnum.CriterionError", 17
        )
        INVALID_YOUTUBE_VIDEO_ID = typing___cast(
            "CriterionErrorEnum.CriterionError", 18
        )
        YOUTUBE_VERTICAL_CHANNEL_DEPRECATED = typing___cast(
            "CriterionErrorEnum.CriterionError", 19
        )
        YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED = typing___cast(
            "CriterionErrorEnum.CriterionError", 20
        )
        YOUTUBE_URL_UNSUPPORTED = typing___cast("CriterionErrorEnum.CriterionError", 21)
        CANNOT_EXCLUDE_CRITERIA_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 22
        )
        CANNOT_ADD_CRITERIA_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 23
        )
        INVALID_PRODUCT_FILTER = typing___cast("CriterionErrorEnum.CriterionError", 24)
        PRODUCT_FILTER_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 25)
        CANNOT_EXCLUDE_SIMILAR_USER_LIST = typing___cast(
            "CriterionErrorEnum.CriterionError", 26
        )
        CANNOT_ADD_CLOSED_USER_LIST = typing___cast(
            "CriterionErrorEnum.CriterionError", 27
        )
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS = typing___cast(
            "CriterionErrorEnum.CriterionError", 28
        )
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS = typing___cast(
            "CriterionErrorEnum.CriterionError", 29
        )
        CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS = typing___cast(
            "CriterionErrorEnum.CriterionError", 30
        )
        CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS = typing___cast(
            "CriterionErrorEnum.CriterionError", 31
        )
        CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS = typing___cast(
            "CriterionErrorEnum.CriterionError", 32
        )
        CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 33
        )
        INVALID_CUSTOM_AFFINITY = typing___cast("CriterionErrorEnum.CriterionError", 96)
        INVALID_CUSTOM_INTENT = typing___cast("CriterionErrorEnum.CriterionError", 97)
        INVALID_IP_ADDRESS = typing___cast("CriterionErrorEnum.CriterionError", 34)
        INVALID_IP_FORMAT = typing___cast("CriterionErrorEnum.CriterionError", 35)
        INVALID_MOBILE_APP = typing___cast("CriterionErrorEnum.CriterionError", 36)
        INVALID_MOBILE_APP_CATEGORY = typing___cast(
            "CriterionErrorEnum.CriterionError", 37
        )
        INVALID_CRITERION_ID = typing___cast("CriterionErrorEnum.CriterionError", 38)
        CANNOT_TARGET_CRITERION = typing___cast("CriterionErrorEnum.CriterionError", 39)
        CANNOT_TARGET_OBSOLETE_CRITERION = typing___cast(
            "CriterionErrorEnum.CriterionError", 40
        )
        CRITERION_ID_AND_TYPE_MISMATCH = typing___cast(
            "CriterionErrorEnum.CriterionError", 41
        )
        INVALID_PROXIMITY_RADIUS = typing___cast(
            "CriterionErrorEnum.CriterionError", 42
        )
        INVALID_PROXIMITY_RADIUS_UNITS = typing___cast(
            "CriterionErrorEnum.CriterionError", 43
        )
        INVALID_STREETADDRESS_LENGTH = typing___cast(
            "CriterionErrorEnum.CriterionError", 44
        )
        INVALID_CITYNAME_LENGTH = typing___cast("CriterionErrorEnum.CriterionError", 45)
        INVALID_REGIONCODE_LENGTH = typing___cast(
            "CriterionErrorEnum.CriterionError", 46
        )
        INVALID_REGIONNAME_LENGTH = typing___cast(
            "CriterionErrorEnum.CriterionError", 47
        )
        INVALID_POSTALCODE_LENGTH = typing___cast(
            "CriterionErrorEnum.CriterionError", 48
        )
        INVALID_COUNTRY_CODE = typing___cast("CriterionErrorEnum.CriterionError", 49)
        INVALID_LATITUDE = typing___cast("CriterionErrorEnum.CriterionError", 50)
        INVALID_LONGITUDE = typing___cast("CriterionErrorEnum.CriterionError", 51)
        PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL = typing___cast(
            "CriterionErrorEnum.CriterionError", 52
        )
        INVALID_PROXIMITY_ADDRESS = typing___cast(
            "CriterionErrorEnum.CriterionError", 53
        )
        INVALID_USER_DOMAIN_NAME = typing___cast(
            "CriterionErrorEnum.CriterionError", 54
        )
        CRITERION_PARAMETER_TOO_LONG = typing___cast(
            "CriterionErrorEnum.CriterionError", 55
        )
        AD_SCHEDULE_TIME_INTERVALS_OVERLAP = typing___cast(
            "CriterionErrorEnum.CriterionError", 56
        )
        AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS = typing___cast(
            "CriterionErrorEnum.CriterionError", 57
        )
        AD_SCHEDULE_INVALID_TIME_INTERVAL = typing___cast(
            "CriterionErrorEnum.CriterionError", 58
        )
        AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT = typing___cast(
            "CriterionErrorEnum.CriterionError", 59
        )
        AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS = typing___cast(
            "CriterionErrorEnum.CriterionError", 60
        )
        CANNOT_BID_MODIFY_CRITERION_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 61
        )
        CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT = typing___cast(
            "CriterionErrorEnum.CriterionError", 62
        )
        CANNOT_BID_MODIFY_NEGATIVE_CRITERION = typing___cast(
            "CriterionErrorEnum.CriterionError", 63
        )
        BID_MODIFIER_ALREADY_EXISTS = typing___cast(
            "CriterionErrorEnum.CriterionError", 64
        )
        FEED_ID_NOT_ALLOWED = typing___cast("CriterionErrorEnum.CriterionError", 65)
        ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 66
        )
        CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY = typing___cast(
            "CriterionErrorEnum.CriterionError", 67
        )
        CANNOT_EXCLUDE_CRITERION = typing___cast(
            "CriterionErrorEnum.CriterionError", 68
        )
        CANNOT_REMOVE_CRITERION = typing___cast("CriterionErrorEnum.CriterionError", 69)
        PRODUCT_SCOPE_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 70)
        PRODUCT_SCOPE_TOO_MANY_DIMENSIONS = typing___cast(
            "CriterionErrorEnum.CriterionError", 71
        )
        PRODUCT_PARTITION_TOO_LONG = typing___cast(
            "CriterionErrorEnum.CriterionError", 72
        )
        PRODUCT_PARTITION_TOO_MANY_DIMENSIONS = typing___cast(
            "CriterionErrorEnum.CriterionError", 73
        )
        INVALID_PRODUCT_DIMENSION = typing___cast(
            "CriterionErrorEnum.CriterionError", 74
        )
        INVALID_PRODUCT_DIMENSION_TYPE = typing___cast(
            "CriterionErrorEnum.CriterionError", 75
        )
        INVALID_PRODUCT_BIDDING_CATEGORY = typing___cast(
            "CriterionErrorEnum.CriterionError", 76
        )
        MISSING_SHOPPING_SETTING = typing___cast(
            "CriterionErrorEnum.CriterionError", 77
        )
        INVALID_MATCHING_FUNCTION = typing___cast(
            "CriterionErrorEnum.CriterionError", 78
        )
        LOCATION_FILTER_NOT_ALLOWED = typing___cast(
            "CriterionErrorEnum.CriterionError", 79
        )
        INVALID_FEED_FOR_LOCATION_FILTER = typing___cast(
            "CriterionErrorEnum.CriterionError", 98
        )
        LOCATION_FILTER_INVALID = typing___cast("CriterionErrorEnum.CriterionError", 80)
        CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP = typing___cast(
            "CriterionErrorEnum.CriterionError", 81
        )
        HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION = typing___cast(
            "CriterionErrorEnum.CriterionError", 82
        )
        HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION = typing___cast(
            "CriterionErrorEnum.CriterionError", 83
        )
        FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING = typing___cast(
            "CriterionErrorEnum.CriterionError", 84
        )
        INVALID_WEBPAGE_CONDITION = typing___cast(
            "CriterionErrorEnum.CriterionError", 85
        )
        INVALID_WEBPAGE_CONDITION_URL = typing___cast(
            "CriterionErrorEnum.CriterionError", 86
        )
        WEBPAGE_CONDITION_URL_CANNOT_BE_EMPTY = typing___cast(
            "CriterionErrorEnum.CriterionError", 87
        )
        WEBPAGE_CONDITION_URL_UNSUPPORTED_PROTOCOL = typing___cast(
            "CriterionErrorEnum.CriterionError", 88
        )
        WEBPAGE_CONDITION_URL_CANNOT_BE_IP_ADDRESS = typing___cast(
            "CriterionErrorEnum.CriterionError", 89
        )
        WEBPAGE_CONDITION_URL_DOMAIN_NOT_CONSISTENT_WITH_CAMPAIGN_SETTING = typing___cast(
            "CriterionErrorEnum.CriterionError", 90
        )
        WEBPAGE_CONDITION_URL_CANNOT_BE_PUBLIC_SUFFIX = typing___cast(
            "CriterionErrorEnum.CriterionError", 91
        )
        WEBPAGE_CONDITION_URL_INVALID_PUBLIC_SUFFIX = typing___cast(
            "CriterionErrorEnum.CriterionError", 92
        )
        WEBPAGE_CONDITION_URL_VALUE_TRACK_VALUE_NOT_SUPPORTED = typing___cast(
            "CriterionErrorEnum.CriterionError", 93
        )
        WEBPAGE_CRITERION_URL_EQUALS_CAN_HAVE_ONLY_ONE_CONDITION = typing___cast(
            "CriterionErrorEnum.CriterionError", 94
        )
        WEBPAGE_CRITERION_NOT_SUPPORTED_ON_NON_DSA_AD_GROUP = typing___cast(
            "CriterionErrorEnum.CriterionError", 95
        )
    UNSPECIFIED = typing___cast("CriterionErrorEnum.CriterionError", 0)
    UNKNOWN = typing___cast("CriterionErrorEnum.CriterionError", 1)
    CONCRETE_TYPE_REQUIRED = typing___cast("CriterionErrorEnum.CriterionError", 2)
    INVALID_EXCLUDED_CATEGORY = typing___cast("CriterionErrorEnum.CriterionError", 3)
    INVALID_KEYWORD_TEXT = typing___cast("CriterionErrorEnum.CriterionError", 4)
    KEYWORD_TEXT_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 5)
    KEYWORD_HAS_TOO_MANY_WORDS = typing___cast("CriterionErrorEnum.CriterionError", 6)
    KEYWORD_HAS_INVALID_CHARS = typing___cast("CriterionErrorEnum.CriterionError", 7)
    INVALID_PLACEMENT_URL = typing___cast("CriterionErrorEnum.CriterionError", 8)
    INVALID_USER_LIST = typing___cast("CriterionErrorEnum.CriterionError", 9)
    INVALID_USER_INTEREST = typing___cast("CriterionErrorEnum.CriterionError", 10)
    INVALID_FORMAT_FOR_PLACEMENT_URL = typing___cast(
        "CriterionErrorEnum.CriterionError", 11
    )
    PLACEMENT_URL_IS_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 12)
    PLACEMENT_URL_HAS_ILLEGAL_CHAR = typing___cast(
        "CriterionErrorEnum.CriterionError", 13
    )
    PLACEMENT_URL_HAS_MULTIPLE_SITES_IN_LINE = typing___cast(
        "CriterionErrorEnum.CriterionError", 14
    )
    PLACEMENT_IS_NOT_AVAILABLE_FOR_TARGETING_OR_EXCLUSION = typing___cast(
        "CriterionErrorEnum.CriterionError", 15
    )
    INVALID_TOPIC_PATH = typing___cast("CriterionErrorEnum.CriterionError", 16)
    INVALID_YOUTUBE_CHANNEL_ID = typing___cast("CriterionErrorEnum.CriterionError", 17)
    INVALID_YOUTUBE_VIDEO_ID = typing___cast("CriterionErrorEnum.CriterionError", 18)
    YOUTUBE_VERTICAL_CHANNEL_DEPRECATED = typing___cast(
        "CriterionErrorEnum.CriterionError", 19
    )
    YOUTUBE_DEMOGRAPHIC_CHANNEL_DEPRECATED = typing___cast(
        "CriterionErrorEnum.CriterionError", 20
    )
    YOUTUBE_URL_UNSUPPORTED = typing___cast("CriterionErrorEnum.CriterionError", 21)
    CANNOT_EXCLUDE_CRITERIA_TYPE = typing___cast(
        "CriterionErrorEnum.CriterionError", 22
    )
    CANNOT_ADD_CRITERIA_TYPE = typing___cast("CriterionErrorEnum.CriterionError", 23)
    INVALID_PRODUCT_FILTER = typing___cast("CriterionErrorEnum.CriterionError", 24)
    PRODUCT_FILTER_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 25)
    CANNOT_EXCLUDE_SIMILAR_USER_LIST = typing___cast(
        "CriterionErrorEnum.CriterionError", 26
    )
    CANNOT_ADD_CLOSED_USER_LIST = typing___cast("CriterionErrorEnum.CriterionError", 27)
    CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_ONLY_CAMPAIGNS = typing___cast(
        "CriterionErrorEnum.CriterionError", 28
    )
    CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SEARCH_CAMPAIGNS = typing___cast(
        "CriterionErrorEnum.CriterionError", 29
    )
    CANNOT_ADD_DISPLAY_ONLY_LISTS_TO_SHOPPING_CAMPAIGNS = typing___cast(
        "CriterionErrorEnum.CriterionError", 30
    )
    CANNOT_ADD_USER_INTERESTS_TO_SEARCH_CAMPAIGNS = typing___cast(
        "CriterionErrorEnum.CriterionError", 31
    )
    CANNOT_SET_BIDS_ON_CRITERION_TYPE_IN_SEARCH_CAMPAIGNS = typing___cast(
        "CriterionErrorEnum.CriterionError", 32
    )
    CANNOT_ADD_URLS_TO_CRITERION_TYPE_FOR_CAMPAIGN_TYPE = typing___cast(
        "CriterionErrorEnum.CriterionError", 33
    )
    INVALID_CUSTOM_AFFINITY = typing___cast("CriterionErrorEnum.CriterionError", 96)
    INVALID_CUSTOM_INTENT = typing___cast("CriterionErrorEnum.CriterionError", 97)
    INVALID_IP_ADDRESS = typing___cast("CriterionErrorEnum.CriterionError", 34)
    INVALID_IP_FORMAT = typing___cast("CriterionErrorEnum.CriterionError", 35)
    INVALID_MOBILE_APP = typing___cast("CriterionErrorEnum.CriterionError", 36)
    INVALID_MOBILE_APP_CATEGORY = typing___cast("CriterionErrorEnum.CriterionError", 37)
    INVALID_CRITERION_ID = typing___cast("CriterionErrorEnum.CriterionError", 38)
    CANNOT_TARGET_CRITERION = typing___cast("CriterionErrorEnum.CriterionError", 39)
    CANNOT_TARGET_OBSOLETE_CRITERION = typing___cast(
        "CriterionErrorEnum.CriterionError", 40
    )
    CRITERION_ID_AND_TYPE_MISMATCH = typing___cast(
        "CriterionErrorEnum.CriterionError", 41
    )
    INVALID_PROXIMITY_RADIUS = typing___cast("CriterionErrorEnum.CriterionError", 42)
    INVALID_PROXIMITY_RADIUS_UNITS = typing___cast(
        "CriterionErrorEnum.CriterionError", 43
    )
    INVALID_STREETADDRESS_LENGTH = typing___cast(
        "CriterionErrorEnum.CriterionError", 44
    )
    INVALID_CITYNAME_LENGTH = typing___cast("CriterionErrorEnum.CriterionError", 45)
    INVALID_REGIONCODE_LENGTH = typing___cast("CriterionErrorEnum.CriterionError", 46)
    INVALID_REGIONNAME_LENGTH = typing___cast("CriterionErrorEnum.CriterionError", 47)
    INVALID_POSTALCODE_LENGTH = typing___cast("CriterionErrorEnum.CriterionError", 48)
    INVALID_COUNTRY_CODE = typing___cast("CriterionErrorEnum.CriterionError", 49)
    INVALID_LATITUDE = typing___cast("CriterionErrorEnum.CriterionError", 50)
    INVALID_LONGITUDE = typing___cast("CriterionErrorEnum.CriterionError", 51)
    PROXIMITY_GEOPOINT_AND_ADDRESS_BOTH_CANNOT_BE_NULL = typing___cast(
        "CriterionErrorEnum.CriterionError", 52
    )
    INVALID_PROXIMITY_ADDRESS = typing___cast("CriterionErrorEnum.CriterionError", 53)
    INVALID_USER_DOMAIN_NAME = typing___cast("CriterionErrorEnum.CriterionError", 54)
    CRITERION_PARAMETER_TOO_LONG = typing___cast(
        "CriterionErrorEnum.CriterionError", 55
    )
    AD_SCHEDULE_TIME_INTERVALS_OVERLAP = typing___cast(
        "CriterionErrorEnum.CriterionError", 56
    )
    AD_SCHEDULE_INTERVAL_CANNOT_SPAN_MULTIPLE_DAYS = typing___cast(
        "CriterionErrorEnum.CriterionError", 57
    )
    AD_SCHEDULE_INVALID_TIME_INTERVAL = typing___cast(
        "CriterionErrorEnum.CriterionError", 58
    )
    AD_SCHEDULE_EXCEEDED_INTERVALS_PER_DAY_LIMIT = typing___cast(
        "CriterionErrorEnum.CriterionError", 59
    )
    AD_SCHEDULE_CRITERION_ID_MISMATCHING_FIELDS = typing___cast(
        "CriterionErrorEnum.CriterionError", 60
    )
    CANNOT_BID_MODIFY_CRITERION_TYPE = typing___cast(
        "CriterionErrorEnum.CriterionError", 61
    )
    CANNOT_BID_MODIFY_CRITERION_CAMPAIGN_OPTED_OUT = typing___cast(
        "CriterionErrorEnum.CriterionError", 62
    )
    CANNOT_BID_MODIFY_NEGATIVE_CRITERION = typing___cast(
        "CriterionErrorEnum.CriterionError", 63
    )
    BID_MODIFIER_ALREADY_EXISTS = typing___cast("CriterionErrorEnum.CriterionError", 64)
    FEED_ID_NOT_ALLOWED = typing___cast("CriterionErrorEnum.CriterionError", 65)
    ACCOUNT_INELIGIBLE_FOR_CRITERIA_TYPE = typing___cast(
        "CriterionErrorEnum.CriterionError", 66
    )
    CRITERIA_TYPE_INVALID_FOR_BIDDING_STRATEGY = typing___cast(
        "CriterionErrorEnum.CriterionError", 67
    )
    CANNOT_EXCLUDE_CRITERION = typing___cast("CriterionErrorEnum.CriterionError", 68)
    CANNOT_REMOVE_CRITERION = typing___cast("CriterionErrorEnum.CriterionError", 69)
    PRODUCT_SCOPE_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 70)
    PRODUCT_SCOPE_TOO_MANY_DIMENSIONS = typing___cast(
        "CriterionErrorEnum.CriterionError", 71
    )
    PRODUCT_PARTITION_TOO_LONG = typing___cast("CriterionErrorEnum.CriterionError", 72)
    PRODUCT_PARTITION_TOO_MANY_DIMENSIONS = typing___cast(
        "CriterionErrorEnum.CriterionError", 73
    )
    INVALID_PRODUCT_DIMENSION = typing___cast("CriterionErrorEnum.CriterionError", 74)
    INVALID_PRODUCT_DIMENSION_TYPE = typing___cast(
        "CriterionErrorEnum.CriterionError", 75
    )
    INVALID_PRODUCT_BIDDING_CATEGORY = typing___cast(
        "CriterionErrorEnum.CriterionError", 76
    )
    MISSING_SHOPPING_SETTING = typing___cast("CriterionErrorEnum.CriterionError", 77)
    INVALID_MATCHING_FUNCTION = typing___cast("CriterionErrorEnum.CriterionError", 78)
    LOCATION_FILTER_NOT_ALLOWED = typing___cast("CriterionErrorEnum.CriterionError", 79)
    INVALID_FEED_FOR_LOCATION_FILTER = typing___cast(
        "CriterionErrorEnum.CriterionError", 98
    )
    LOCATION_FILTER_INVALID = typing___cast("CriterionErrorEnum.CriterionError", 80)
    CANNOT_ATTACH_CRITERIA_AT_CAMPAIGN_AND_ADGROUP = typing___cast(
        "CriterionErrorEnum.CriterionError", 81
    )
    HOTEL_LENGTH_OF_STAY_OVERLAPS_WITH_EXISTING_CRITERION = typing___cast(
        "CriterionErrorEnum.CriterionError", 82
    )
    HOTEL_ADVANCE_BOOKING_WINDOW_OVERLAPS_WITH_EXISTING_CRITERION = typing___cast(
        "CriterionErrorEnum.CriterionError", 83
    )
    FIELD_INCOMPATIBLE_WITH_NEGATIVE_TARGETING = typing___cast(
        "CriterionErrorEnum.CriterionError", 84
    )
    INVALID_WEBPAGE_CONDITION = typing___cast("CriterionErrorEnum.CriterionError", 85)
    INVALID_WEBPAGE_CONDITION_URL = typing___cast(
        "CriterionErrorEnum.CriterionError", 86
    )
    WEBPAGE_CONDITION_URL_CANNOT_BE_EMPTY = typing___cast(
        "CriterionErrorEnum.CriterionError", 87
    )
    WEBPAGE_CONDITION_URL_UNSUPPORTED_PROTOCOL = typing___cast(
        "CriterionErrorEnum.CriterionError", 88
    )
    WEBPAGE_CONDITION_URL_CANNOT_BE_IP_ADDRESS = typing___cast(
        "CriterionErrorEnum.CriterionError", 89
    )
    WEBPAGE_CONDITION_URL_DOMAIN_NOT_CONSISTENT_WITH_CAMPAIGN_SETTING = typing___cast(
        "CriterionErrorEnum.CriterionError", 90
    )
    WEBPAGE_CONDITION_URL_CANNOT_BE_PUBLIC_SUFFIX = typing___cast(
        "CriterionErrorEnum.CriterionError", 91
    )
    WEBPAGE_CONDITION_URL_INVALID_PUBLIC_SUFFIX = typing___cast(
        "CriterionErrorEnum.CriterionError", 92
    )
    WEBPAGE_CONDITION_URL_VALUE_TRACK_VALUE_NOT_SUPPORTED = typing___cast(
        "CriterionErrorEnum.CriterionError", 93
    )
    WEBPAGE_CRITERION_URL_EQUALS_CAN_HAVE_ONLY_ONE_CONDITION = typing___cast(
        "CriterionErrorEnum.CriterionError", 94
    )
    WEBPAGE_CRITERION_NOT_SUPPORTED_ON_NON_DSA_AD_GROUP = typing___cast(
        "CriterionErrorEnum.CriterionError", 95
    )
    global___CriterionError = CriterionError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CriterionErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> CriterionErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___CriterionErrorEnum = CriterionErrorEnum
