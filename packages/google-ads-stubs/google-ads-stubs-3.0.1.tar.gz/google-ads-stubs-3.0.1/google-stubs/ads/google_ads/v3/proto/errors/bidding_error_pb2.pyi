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

class BiddingErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class BiddingError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "BiddingErrorEnum.BiddingError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["BiddingErrorEnum.BiddingError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "BiddingErrorEnum.BiddingError"]
        ]: ...
        UNSPECIFIED = typing___cast("BiddingErrorEnum.BiddingError", 0)
        UNKNOWN = typing___cast("BiddingErrorEnum.BiddingError", 1)
        BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED = typing___cast(
            "BiddingErrorEnum.BiddingError", 2
        )
        CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN = typing___cast(
            "BiddingErrorEnum.BiddingError", 7
        )
        INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE = typing___cast(
            "BiddingErrorEnum.BiddingError", 10
        )
        INVALID_BIDDING_STRATEGY_TYPE = typing___cast(
            "BiddingErrorEnum.BiddingError", 14
        )
        INVALID_BID = typing___cast("BiddingErrorEnum.BiddingError", 17)
        BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = typing___cast(
            "BiddingErrorEnum.BiddingError", 18
        )
        CONVERSION_TRACKING_NOT_ENABLED = typing___cast(
            "BiddingErrorEnum.BiddingError", 19
        )
        NOT_ENOUGH_CONVERSIONS = typing___cast("BiddingErrorEnum.BiddingError", 20)
        CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY = typing___cast(
            "BiddingErrorEnum.BiddingError", 21
        )
        CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY = typing___cast(
            "BiddingErrorEnum.BiddingError", 23
        )
        BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE = typing___cast(
            "BiddingErrorEnum.BiddingError", 24
        )
        PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER = typing___cast(
            "BiddingErrorEnum.BiddingError", 25
        )
        PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA = typing___cast(
            "BiddingErrorEnum.BiddingError", 26
        )
        BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS = typing___cast(
            "BiddingErrorEnum.BiddingError", 27
        )
        BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS = typing___cast(
            "BiddingErrorEnum.BiddingError", 28
        )
        BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION = typing___cast(
            "BiddingErrorEnum.BiddingError", 29
        )
        BID_TOO_SMALL = typing___cast("BiddingErrorEnum.BiddingError", 30)
        BID_TOO_BIG = typing___cast("BiddingErrorEnum.BiddingError", 31)
        BID_TOO_MANY_FRACTIONAL_DIGITS = typing___cast(
            "BiddingErrorEnum.BiddingError", 32
        )
        INVALID_DOMAIN_NAME = typing___cast("BiddingErrorEnum.BiddingError", 33)
        NOT_COMPATIBLE_WITH_PAYMENT_MODE = typing___cast(
            "BiddingErrorEnum.BiddingError", 34
        )
        NOT_COMPATIBLE_WITH_BUDGET_TYPE = typing___cast(
            "BiddingErrorEnum.BiddingError", 35
        )
        NOT_COMPATIBLE_WITH_BIDDING_STRATEGY_TYPE = typing___cast(
            "BiddingErrorEnum.BiddingError", 36
        )
        BIDDING_STRATEGY_TYPE_INCOMPATIBLE_WITH_SHARED_BUDGET = typing___cast(
            "BiddingErrorEnum.BiddingError", 37
        )
    UNSPECIFIED = typing___cast("BiddingErrorEnum.BiddingError", 0)
    UNKNOWN = typing___cast("BiddingErrorEnum.BiddingError", 1)
    BIDDING_STRATEGY_TRANSITION_NOT_ALLOWED = typing___cast(
        "BiddingErrorEnum.BiddingError", 2
    )
    CANNOT_ATTACH_BIDDING_STRATEGY_TO_CAMPAIGN = typing___cast(
        "BiddingErrorEnum.BiddingError", 7
    )
    INVALID_ANONYMOUS_BIDDING_STRATEGY_TYPE = typing___cast(
        "BiddingErrorEnum.BiddingError", 10
    )
    INVALID_BIDDING_STRATEGY_TYPE = typing___cast("BiddingErrorEnum.BiddingError", 14)
    INVALID_BID = typing___cast("BiddingErrorEnum.BiddingError", 17)
    BIDDING_STRATEGY_NOT_AVAILABLE_FOR_ACCOUNT_TYPE = typing___cast(
        "BiddingErrorEnum.BiddingError", 18
    )
    CONVERSION_TRACKING_NOT_ENABLED = typing___cast("BiddingErrorEnum.BiddingError", 19)
    NOT_ENOUGH_CONVERSIONS = typing___cast("BiddingErrorEnum.BiddingError", 20)
    CANNOT_CREATE_CAMPAIGN_WITH_BIDDING_STRATEGY = typing___cast(
        "BiddingErrorEnum.BiddingError", 21
    )
    CANNOT_TARGET_CONTENT_NETWORK_ONLY_WITH_CAMPAIGN_LEVEL_POP_BIDDING_STRATEGY = typing___cast(
        "BiddingErrorEnum.BiddingError", 23
    )
    BIDDING_STRATEGY_NOT_SUPPORTED_WITH_AD_SCHEDULE = typing___cast(
        "BiddingErrorEnum.BiddingError", 24
    )
    PAY_PER_CONVERSION_NOT_AVAILABLE_FOR_CUSTOMER = typing___cast(
        "BiddingErrorEnum.BiddingError", 25
    )
    PAY_PER_CONVERSION_NOT_ALLOWED_WITH_TARGET_CPA = typing___cast(
        "BiddingErrorEnum.BiddingError", 26
    )
    BIDDING_STRATEGY_NOT_ALLOWED_FOR_SEARCH_ONLY_CAMPAIGNS = typing___cast(
        "BiddingErrorEnum.BiddingError", 27
    )
    BIDDING_STRATEGY_NOT_SUPPORTED_IN_DRAFTS_OR_EXPERIMENTS = typing___cast(
        "BiddingErrorEnum.BiddingError", 28
    )
    BIDDING_STRATEGY_TYPE_DOES_NOT_SUPPORT_PRODUCT_TYPE_ADGROUP_CRITERION = typing___cast(
        "BiddingErrorEnum.BiddingError", 29
    )
    BID_TOO_SMALL = typing___cast("BiddingErrorEnum.BiddingError", 30)
    BID_TOO_BIG = typing___cast("BiddingErrorEnum.BiddingError", 31)
    BID_TOO_MANY_FRACTIONAL_DIGITS = typing___cast("BiddingErrorEnum.BiddingError", 32)
    INVALID_DOMAIN_NAME = typing___cast("BiddingErrorEnum.BiddingError", 33)
    NOT_COMPATIBLE_WITH_PAYMENT_MODE = typing___cast(
        "BiddingErrorEnum.BiddingError", 34
    )
    NOT_COMPATIBLE_WITH_BUDGET_TYPE = typing___cast("BiddingErrorEnum.BiddingError", 35)
    NOT_COMPATIBLE_WITH_BIDDING_STRATEGY_TYPE = typing___cast(
        "BiddingErrorEnum.BiddingError", 36
    )
    BIDDING_STRATEGY_TYPE_INCOMPATIBLE_WITH_SHARED_BUDGET = typing___cast(
        "BiddingErrorEnum.BiddingError", 37
    )
    global___BiddingError = BiddingError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BiddingErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> BiddingErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___BiddingErrorEnum = BiddingErrorEnum
