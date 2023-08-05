# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v1.proto.common.dates_pb2 import (
    DateRange as google___ads___googleads___v1___common___dates_pb2___DateRange,
)

from google.ads.google_ads.v1.proto.enums.keyword_plan_forecast_interval_pb2 import (
    KeywordPlanForecastIntervalEnum as google___ads___googleads___v1___enums___keyword_plan_forecast_interval_pb2___KeywordPlanForecastIntervalEnum,
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

class KeywordPlan(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def forecast_period(self) -> global___KeywordPlanForecastPeriod: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        forecast_period: typing___Optional[global___KeywordPlanForecastPeriod] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlan: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlan: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "forecast_period", b"forecast_period", "id", b"id", "name", b"name"
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "forecast_period",
            b"forecast_period",
            "id",
            b"id",
            "name",
            b"name",
            "resource_name",
            b"resource_name",
        ],
    ) -> None: ...

global___KeywordPlan = KeywordPlan

class KeywordPlanForecastPeriod(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    date_interval = (
        ...
    )  # type: google___ads___googleads___v1___enums___keyword_plan_forecast_interval_pb2___KeywordPlanForecastIntervalEnum.KeywordPlanForecastInterval
    @property
    def date_range(
        self,
    ) -> google___ads___googleads___v1___common___dates_pb2___DateRange: ...
    def __init__(
        self,
        *,
        date_interval: typing___Optional[
            google___ads___googleads___v1___enums___keyword_plan_forecast_interval_pb2___KeywordPlanForecastIntervalEnum.KeywordPlanForecastInterval
        ] = None,
        date_range: typing___Optional[
            google___ads___googleads___v1___common___dates_pb2___DateRange
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanForecastPeriod: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanForecastPeriod: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "date_interval",
            b"date_interval",
            "date_range",
            b"date_range",
            "interval",
            b"interval",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "date_interval",
            b"date_interval",
            "date_range",
            b"date_range",
            "interval",
            b"interval",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions___Literal["interval", b"interval"]
    ) -> typing_extensions___Literal["date_interval", "date_range"]: ...

global___KeywordPlanForecastPeriod = KeywordPlanForecastPeriod
