# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v3.proto.common.criteria_pb2 import (
    InteractionTypeInfo as google___ads___googleads___v3___common___criteria_pb2___InteractionTypeInfo,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    DoubleValue as google___protobuf___wrappers_pb2___DoubleValue,
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

class CampaignBidModifier(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    @property
    def campaign(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def criterion_id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def bid_modifier(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def interaction_type(
        self,
    ) -> google___ads___googleads___v3___common___criteria_pb2___InteractionTypeInfo: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        campaign: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        criterion_id: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        bid_modifier: typing___Optional[
            google___protobuf___wrappers_pb2___DoubleValue
        ] = None,
        interaction_type: typing___Optional[
            google___ads___googleads___v3___common___criteria_pb2___InteractionTypeInfo
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CampaignBidModifier: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> CampaignBidModifier: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "bid_modifier",
            b"bid_modifier",
            "campaign",
            b"campaign",
            "criterion",
            b"criterion",
            "criterion_id",
            b"criterion_id",
            "interaction_type",
            b"interaction_type",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "bid_modifier",
            b"bid_modifier",
            "campaign",
            b"campaign",
            "criterion",
            b"criterion",
            "criterion_id",
            b"criterion_id",
            "interaction_type",
            b"interaction_type",
            "resource_name",
            b"resource_name",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions___Literal["criterion", b"criterion"]
    ) -> typing_extensions___Literal["interaction_type"]: ...

global___CampaignBidModifier = CampaignBidModifier
