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

class QueryErrorEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class QueryError(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "QueryErrorEnum.QueryError": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["QueryErrorEnum.QueryError"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "QueryErrorEnum.QueryError"]
        ]: ...
        UNSPECIFIED = typing___cast("QueryErrorEnum.QueryError", 0)
        UNKNOWN = typing___cast("QueryErrorEnum.QueryError", 1)
        QUERY_ERROR = typing___cast("QueryErrorEnum.QueryError", 50)
        BAD_ENUM_CONSTANT = typing___cast("QueryErrorEnum.QueryError", 18)
        BAD_ESCAPE_SEQUENCE = typing___cast("QueryErrorEnum.QueryError", 7)
        BAD_FIELD_NAME = typing___cast("QueryErrorEnum.QueryError", 12)
        BAD_LIMIT_VALUE = typing___cast("QueryErrorEnum.QueryError", 15)
        BAD_NUMBER = typing___cast("QueryErrorEnum.QueryError", 5)
        BAD_OPERATOR = typing___cast("QueryErrorEnum.QueryError", 3)
        BAD_PARAMETER_NAME = typing___cast("QueryErrorEnum.QueryError", 61)
        BAD_PARAMETER_VALUE = typing___cast("QueryErrorEnum.QueryError", 62)
        BAD_RESOURCE_TYPE_IN_FROM_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 45
        )
        BAD_SYMBOL = typing___cast("QueryErrorEnum.QueryError", 2)
        BAD_VALUE = typing___cast("QueryErrorEnum.QueryError", 4)
        DATE_RANGE_TOO_WIDE = typing___cast("QueryErrorEnum.QueryError", 36)
        EXPECTED_AND = typing___cast("QueryErrorEnum.QueryError", 30)
        EXPECTED_BY = typing___cast("QueryErrorEnum.QueryError", 14)
        EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 37
        )
        EXPECTED_FILTERS_ON_DATE_RANGE = typing___cast("QueryErrorEnum.QueryError", 55)
        EXPECTED_FROM = typing___cast("QueryErrorEnum.QueryError", 44)
        EXPECTED_LIST = typing___cast("QueryErrorEnum.QueryError", 41)
        EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 16
        )
        EXPECTED_SELECT = typing___cast("QueryErrorEnum.QueryError", 13)
        EXPECTED_SINGLE_VALUE = typing___cast("QueryErrorEnum.QueryError", 42)
        EXPECTED_VALUE_WITH_BETWEEN_OPERATOR = typing___cast(
            "QueryErrorEnum.QueryError", 29
        )
        INVALID_DATE_FORMAT = typing___cast("QueryErrorEnum.QueryError", 38)
        INVALID_STRING_VALUE = typing___cast("QueryErrorEnum.QueryError", 57)
        INVALID_VALUE_WITH_BETWEEN_OPERATOR = typing___cast(
            "QueryErrorEnum.QueryError", 26
        )
        INVALID_VALUE_WITH_DURING_OPERATOR = typing___cast(
            "QueryErrorEnum.QueryError", 22
        )
        INVALID_VALUE_WITH_LIKE_OPERATOR = typing___cast(
            "QueryErrorEnum.QueryError", 56
        )
        OPERATOR_FIELD_MISMATCH = typing___cast("QueryErrorEnum.QueryError", 35)
        PROHIBITED_EMPTY_LIST_IN_CONDITION = typing___cast(
            "QueryErrorEnum.QueryError", 28
        )
        PROHIBITED_ENUM_CONSTANT = typing___cast("QueryErrorEnum.QueryError", 54)
        PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 31
        )
        PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 40
        )
        PROHIBITED_FIELD_IN_SELECT_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 23
        )
        PROHIBITED_FIELD_IN_WHERE_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 24
        )
        PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 43
        )
        PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 48
        )
        PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 58
        )
        PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 49
        )
        PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 51
        )
        PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
            "QueryErrorEnum.QueryError", 53
        )
        LIMIT_VALUE_TOO_LOW = typing___cast("QueryErrorEnum.QueryError", 25)
        PROHIBITED_NEWLINE_IN_STRING = typing___cast("QueryErrorEnum.QueryError", 8)
        PROHIBITED_VALUE_COMBINATION_IN_LIST = typing___cast(
            "QueryErrorEnum.QueryError", 10
        )
        PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR = typing___cast(
            "QueryErrorEnum.QueryError", 21
        )
        STRING_NOT_TERMINATED = typing___cast("QueryErrorEnum.QueryError", 6)
        TOO_MANY_SEGMENTS = typing___cast("QueryErrorEnum.QueryError", 34)
        UNEXPECTED_END_OF_QUERY = typing___cast("QueryErrorEnum.QueryError", 9)
        UNEXPECTED_FROM_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 47)
        UNRECOGNIZED_FIELD = typing___cast("QueryErrorEnum.QueryError", 32)
        UNEXPECTED_INPUT = typing___cast("QueryErrorEnum.QueryError", 11)
        REQUESTED_METRICS_FOR_MANAGER = typing___cast("QueryErrorEnum.QueryError", 59)
    UNSPECIFIED = typing___cast("QueryErrorEnum.QueryError", 0)
    UNKNOWN = typing___cast("QueryErrorEnum.QueryError", 1)
    QUERY_ERROR = typing___cast("QueryErrorEnum.QueryError", 50)
    BAD_ENUM_CONSTANT = typing___cast("QueryErrorEnum.QueryError", 18)
    BAD_ESCAPE_SEQUENCE = typing___cast("QueryErrorEnum.QueryError", 7)
    BAD_FIELD_NAME = typing___cast("QueryErrorEnum.QueryError", 12)
    BAD_LIMIT_VALUE = typing___cast("QueryErrorEnum.QueryError", 15)
    BAD_NUMBER = typing___cast("QueryErrorEnum.QueryError", 5)
    BAD_OPERATOR = typing___cast("QueryErrorEnum.QueryError", 3)
    BAD_PARAMETER_NAME = typing___cast("QueryErrorEnum.QueryError", 61)
    BAD_PARAMETER_VALUE = typing___cast("QueryErrorEnum.QueryError", 62)
    BAD_RESOURCE_TYPE_IN_FROM_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 45)
    BAD_SYMBOL = typing___cast("QueryErrorEnum.QueryError", 2)
    BAD_VALUE = typing___cast("QueryErrorEnum.QueryError", 4)
    DATE_RANGE_TOO_WIDE = typing___cast("QueryErrorEnum.QueryError", 36)
    EXPECTED_AND = typing___cast("QueryErrorEnum.QueryError", 30)
    EXPECTED_BY = typing___cast("QueryErrorEnum.QueryError", 14)
    EXPECTED_DIMENSION_FIELD_IN_SELECT_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 37
    )
    EXPECTED_FILTERS_ON_DATE_RANGE = typing___cast("QueryErrorEnum.QueryError", 55)
    EXPECTED_FROM = typing___cast("QueryErrorEnum.QueryError", 44)
    EXPECTED_LIST = typing___cast("QueryErrorEnum.QueryError", 41)
    EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 16
    )
    EXPECTED_SELECT = typing___cast("QueryErrorEnum.QueryError", 13)
    EXPECTED_SINGLE_VALUE = typing___cast("QueryErrorEnum.QueryError", 42)
    EXPECTED_VALUE_WITH_BETWEEN_OPERATOR = typing___cast(
        "QueryErrorEnum.QueryError", 29
    )
    INVALID_DATE_FORMAT = typing___cast("QueryErrorEnum.QueryError", 38)
    INVALID_STRING_VALUE = typing___cast("QueryErrorEnum.QueryError", 57)
    INVALID_VALUE_WITH_BETWEEN_OPERATOR = typing___cast("QueryErrorEnum.QueryError", 26)
    INVALID_VALUE_WITH_DURING_OPERATOR = typing___cast("QueryErrorEnum.QueryError", 22)
    INVALID_VALUE_WITH_LIKE_OPERATOR = typing___cast("QueryErrorEnum.QueryError", 56)
    OPERATOR_FIELD_MISMATCH = typing___cast("QueryErrorEnum.QueryError", 35)
    PROHIBITED_EMPTY_LIST_IN_CONDITION = typing___cast("QueryErrorEnum.QueryError", 28)
    PROHIBITED_ENUM_CONSTANT = typing___cast("QueryErrorEnum.QueryError", 54)
    PROHIBITED_FIELD_COMBINATION_IN_SELECT_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 31
    )
    PROHIBITED_FIELD_IN_ORDER_BY_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 40)
    PROHIBITED_FIELD_IN_SELECT_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 23)
    PROHIBITED_FIELD_IN_WHERE_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 24)
    PROHIBITED_RESOURCE_TYPE_IN_FROM_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 43
    )
    PROHIBITED_RESOURCE_TYPE_IN_SELECT_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 48
    )
    PROHIBITED_RESOURCE_TYPE_IN_WHERE_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 58
    )
    PROHIBITED_METRIC_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 49
    )
    PROHIBITED_SEGMENT_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 51
    )
    PROHIBITED_SEGMENT_WITH_METRIC_IN_SELECT_OR_WHERE_CLAUSE = typing___cast(
        "QueryErrorEnum.QueryError", 53
    )
    LIMIT_VALUE_TOO_LOW = typing___cast("QueryErrorEnum.QueryError", 25)
    PROHIBITED_NEWLINE_IN_STRING = typing___cast("QueryErrorEnum.QueryError", 8)
    PROHIBITED_VALUE_COMBINATION_IN_LIST = typing___cast(
        "QueryErrorEnum.QueryError", 10
    )
    PROHIBITED_VALUE_COMBINATION_WITH_BETWEEN_OPERATOR = typing___cast(
        "QueryErrorEnum.QueryError", 21
    )
    STRING_NOT_TERMINATED = typing___cast("QueryErrorEnum.QueryError", 6)
    TOO_MANY_SEGMENTS = typing___cast("QueryErrorEnum.QueryError", 34)
    UNEXPECTED_END_OF_QUERY = typing___cast("QueryErrorEnum.QueryError", 9)
    UNEXPECTED_FROM_CLAUSE = typing___cast("QueryErrorEnum.QueryError", 47)
    UNRECOGNIZED_FIELD = typing___cast("QueryErrorEnum.QueryError", 32)
    UNEXPECTED_INPUT = typing___cast("QueryErrorEnum.QueryError", 11)
    REQUESTED_METRICS_FOR_MANAGER = typing___cast("QueryErrorEnum.QueryError", 59)
    global___QueryError = QueryError
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> QueryErrorEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> QueryErrorEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___QueryErrorEnum = QueryErrorEnum
