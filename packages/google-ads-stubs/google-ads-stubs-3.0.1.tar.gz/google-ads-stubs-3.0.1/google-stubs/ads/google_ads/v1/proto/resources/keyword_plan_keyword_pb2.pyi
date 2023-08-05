# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v1.proto.enums.keyword_match_type_pb2 import (
    KeywordMatchTypeEnum as google___ads___googleads___v1___enums___keyword_match_type_pb2___KeywordMatchTypeEnum,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    Int64Value as google___protobuf___wrappers_pb2___Int64Value,
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

from typing import (
    Optional as typing___Optional,
    Text as typing___Text,
    Union as typing___Union,
)

from typing_extensions import Literal as typing_extensions___Literal

builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode

class KeywordPlanKeyword(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    match_type = (
        ...
    )  # type: google___ads___googleads___v1___enums___keyword_match_type_pb2___KeywordMatchTypeEnum.KeywordMatchType
    @property
    def keyword_plan_ad_group(
        self,
    ) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def text(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def cpc_bid_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        keyword_plan_ad_group: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        text: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        match_type: typing___Optional[
            google___ads___googleads___v1___enums___keyword_match_type_pb2___KeywordMatchTypeEnum.KeywordMatchType
        ] = None,
        cpc_bid_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanKeyword: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanKeyword: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "cpc_bid_micros",
            b"cpc_bid_micros",
            "id",
            b"id",
            "keyword_plan_ad_group",
            b"keyword_plan_ad_group",
            "text",
            b"text",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "cpc_bid_micros",
            b"cpc_bid_micros",
            "id",
            b"id",
            "keyword_plan_ad_group",
            b"keyword_plan_ad_group",
            "match_type",
            b"match_type",
            "resource_name",
            b"resource_name",
            "text",
            b"text",
        ],
    ) -> None: ...

global___KeywordPlanKeyword = KeywordPlanKeyword
