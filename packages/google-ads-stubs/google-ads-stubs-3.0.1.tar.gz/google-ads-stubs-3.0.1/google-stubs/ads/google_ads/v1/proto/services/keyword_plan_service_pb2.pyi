# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v1.proto.common.keyword_plan_common_pb2 import (
    KeywordPlanHistoricalMetrics as google___ads___googleads___v1___common___keyword_plan_common_pb2___KeywordPlanHistoricalMetrics,
)

from google.ads.google_ads.v1.proto.resources.keyword_plan_pb2 import (
    KeywordPlan as google___ads___googleads___v1___resources___keyword_plan_pb2___KeywordPlan,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.field_mask_pb2 import (
    FieldMask as google___protobuf___field_mask_pb2___FieldMask,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    DoubleValue as google___protobuf___wrappers_pb2___DoubleValue,
    Int64Value as google___protobuf___wrappers_pb2___Int64Value,
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

from google.rpc.status_pb2 import Status as google___rpc___status_pb2___Status

from typing import (
    Iterable as typing___Iterable,
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

class GetKeywordPlanRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    def __init__(
        self, *, resource_name: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetKeywordPlanRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GetKeywordPlanRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["resource_name", b"resource_name"]
    ) -> None: ...

global___GetKeywordPlanRequest = GetKeywordPlanRequest

class MutateKeywordPlansRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    customer_id = ...  # type: typing___Text
    partial_failure = ...  # type: builtin___bool
    validate_only = ...  # type: builtin___bool
    @property
    def operations(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___KeywordPlanOperation
    ]: ...
    def __init__(
        self,
        *,
        customer_id: typing___Optional[typing___Text] = None,
        operations: typing___Optional[
            typing___Iterable[global___KeywordPlanOperation]
        ] = None,
        partial_failure: typing___Optional[builtin___bool] = None,
        validate_only: typing___Optional[builtin___bool] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateKeywordPlansRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateKeywordPlansRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "customer_id",
            b"customer_id",
            "operations",
            b"operations",
            "partial_failure",
            b"partial_failure",
            "validate_only",
            b"validate_only",
        ],
    ) -> None: ...

global___MutateKeywordPlansRequest = MutateKeywordPlansRequest

class KeywordPlanOperation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    remove = ...  # type: typing___Text
    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...
    @property
    def create(
        self,
    ) -> google___ads___googleads___v1___resources___keyword_plan_pb2___KeywordPlan: ...
    @property
    def update(
        self,
    ) -> google___ads___googleads___v1___resources___keyword_plan_pb2___KeywordPlan: ...
    def __init__(
        self,
        *,
        update_mask: typing___Optional[
            google___protobuf___field_mask_pb2___FieldMask
        ] = None,
        create: typing___Optional[
            google___ads___googleads___v1___resources___keyword_plan_pb2___KeywordPlan
        ] = None,
        update: typing___Optional[
            google___ads___googleads___v1___resources___keyword_plan_pb2___KeywordPlan
        ] = None,
        remove: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanOperation: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanOperation: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "create",
            b"create",
            "operation",
            b"operation",
            "remove",
            b"remove",
            "update",
            b"update",
            "update_mask",
            b"update_mask",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "create",
            b"create",
            "operation",
            b"operation",
            "remove",
            b"remove",
            "update",
            b"update",
            "update_mask",
            b"update_mask",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions___Literal["operation", b"operation"]
    ) -> typing_extensions___Literal["create", "update", "remove"]: ...

global___KeywordPlanOperation = KeywordPlanOperation

class MutateKeywordPlansResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def partial_failure_error(self) -> google___rpc___status_pb2___Status: ...
    @property
    def results(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___MutateKeywordPlansResult
    ]: ...
    def __init__(
        self,
        *,
        partial_failure_error: typing___Optional[
            google___rpc___status_pb2___Status
        ] = None,
        results: typing___Optional[
            typing___Iterable[global___MutateKeywordPlansResult]
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateKeywordPlansResponse: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateKeywordPlansResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "partial_failure_error", b"partial_failure_error"
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "partial_failure_error", b"partial_failure_error", "results", b"results"
        ],
    ) -> None: ...

global___MutateKeywordPlansResponse = MutateKeywordPlansResponse

class MutateKeywordPlansResult(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    def __init__(
        self, *, resource_name: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateKeywordPlansResult: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateKeywordPlansResult: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["resource_name", b"resource_name"]
    ) -> None: ...

global___MutateKeywordPlansResult = MutateKeywordPlansResult

class GenerateForecastMetricsRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    keyword_plan = ...  # type: typing___Text
    def __init__(
        self, *, keyword_plan: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GenerateForecastMetricsRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GenerateForecastMetricsRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["keyword_plan", b"keyword_plan"]
    ) -> None: ...

global___GenerateForecastMetricsRequest = GenerateForecastMetricsRequest

class GenerateForecastMetricsResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def campaign_forecasts(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___KeywordPlanCampaignForecast
    ]: ...
    @property
    def ad_group_forecasts(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___KeywordPlanAdGroupForecast
    ]: ...
    @property
    def keyword_forecasts(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___KeywordPlanKeywordForecast
    ]: ...
    def __init__(
        self,
        *,
        campaign_forecasts: typing___Optional[
            typing___Iterable[global___KeywordPlanCampaignForecast]
        ] = None,
        ad_group_forecasts: typing___Optional[
            typing___Iterable[global___KeywordPlanAdGroupForecast]
        ] = None,
        keyword_forecasts: typing___Optional[
            typing___Iterable[global___KeywordPlanKeywordForecast]
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GenerateForecastMetricsResponse: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GenerateForecastMetricsResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "ad_group_forecasts",
            b"ad_group_forecasts",
            "campaign_forecasts",
            b"campaign_forecasts",
            "keyword_forecasts",
            b"keyword_forecasts",
        ],
    ) -> None: ...

global___GenerateForecastMetricsResponse = GenerateForecastMetricsResponse

class KeywordPlanCampaignForecast(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def keyword_plan_campaign(
        self,
    ) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def campaign_forecast(self) -> global___ForecastMetrics: ...
    def __init__(
        self,
        *,
        keyword_plan_campaign: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        campaign_forecast: typing___Optional[global___ForecastMetrics] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanCampaignForecast: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanCampaignForecast: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "campaign_forecast",
            b"campaign_forecast",
            "keyword_plan_campaign",
            b"keyword_plan_campaign",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "campaign_forecast",
            b"campaign_forecast",
            "keyword_plan_campaign",
            b"keyword_plan_campaign",
        ],
    ) -> None: ...

global___KeywordPlanCampaignForecast = KeywordPlanCampaignForecast

class KeywordPlanAdGroupForecast(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def keyword_plan_ad_group(
        self,
    ) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def ad_group_forecast(self) -> global___ForecastMetrics: ...
    def __init__(
        self,
        *,
        keyword_plan_ad_group: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        ad_group_forecast: typing___Optional[global___ForecastMetrics] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanAdGroupForecast: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanAdGroupForecast: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "ad_group_forecast",
            b"ad_group_forecast",
            "keyword_plan_ad_group",
            b"keyword_plan_ad_group",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "ad_group_forecast",
            b"ad_group_forecast",
            "keyword_plan_ad_group",
            b"keyword_plan_ad_group",
        ],
    ) -> None: ...

global___KeywordPlanAdGroupForecast = KeywordPlanAdGroupForecast

class KeywordPlanKeywordForecast(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def keyword_plan_ad_group_keyword(
        self,
    ) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def keyword_forecast(self) -> global___ForecastMetrics: ...
    def __init__(
        self,
        *,
        keyword_plan_ad_group_keyword: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        keyword_forecast: typing___Optional[global___ForecastMetrics] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> KeywordPlanKeywordForecast: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanKeywordForecast: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "keyword_forecast",
            b"keyword_forecast",
            "keyword_plan_ad_group_keyword",
            b"keyword_plan_ad_group_keyword",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "keyword_forecast",
            b"keyword_forecast",
            "keyword_plan_ad_group_keyword",
            b"keyword_plan_ad_group_keyword",
        ],
    ) -> None: ...

global___KeywordPlanKeywordForecast = KeywordPlanKeywordForecast

class ForecastMetrics(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def impressions(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def ctr(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def average_cpc(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def clicks(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def cost_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    def __init__(
        self,
        *,
        impressions: typing___Optional[
            google___protobuf___wrappers_pb2___DoubleValue
        ] = None,
        ctr: typing___Optional[google___protobuf___wrappers_pb2___DoubleValue] = None,
        average_cpc: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        clicks: typing___Optional[
            google___protobuf___wrappers_pb2___DoubleValue
        ] = None,
        cost_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ForecastMetrics: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ForecastMetrics: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "average_cpc",
            b"average_cpc",
            "clicks",
            b"clicks",
            "cost_micros",
            b"cost_micros",
            "ctr",
            b"ctr",
            "impressions",
            b"impressions",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "average_cpc",
            b"average_cpc",
            "clicks",
            b"clicks",
            "cost_micros",
            b"cost_micros",
            "ctr",
            b"ctr",
            "impressions",
            b"impressions",
        ],
    ) -> None: ...

global___ForecastMetrics = ForecastMetrics

class GenerateHistoricalMetricsRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    keyword_plan = ...  # type: typing___Text
    def __init__(
        self, *, keyword_plan: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GenerateHistoricalMetricsRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GenerateHistoricalMetricsRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["keyword_plan", b"keyword_plan"]
    ) -> None: ...

global___GenerateHistoricalMetricsRequest = GenerateHistoricalMetricsRequest

class GenerateHistoricalMetricsResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def metrics(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___KeywordPlanKeywordHistoricalMetrics
    ]: ...
    def __init__(
        self,
        *,
        metrics: typing___Optional[
            typing___Iterable[global___KeywordPlanKeywordHistoricalMetrics]
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(
            cls, s: builtin___bytes
        ) -> GenerateHistoricalMetricsResponse: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GenerateHistoricalMetricsResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["metrics", b"metrics"]
    ) -> None: ...

global___GenerateHistoricalMetricsResponse = GenerateHistoricalMetricsResponse

class KeywordPlanKeywordHistoricalMetrics(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def search_query(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def keyword_metrics(
        self,
    ) -> google___ads___googleads___v1___common___keyword_plan_common_pb2___KeywordPlanHistoricalMetrics: ...
    def __init__(
        self,
        *,
        search_query: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        keyword_metrics: typing___Optional[
            google___ads___googleads___v1___common___keyword_plan_common_pb2___KeywordPlanHistoricalMetrics
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(
            cls, s: builtin___bytes
        ) -> KeywordPlanKeywordHistoricalMetrics: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> KeywordPlanKeywordHistoricalMetrics: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "keyword_metrics", b"keyword_metrics", "search_query", b"search_query"
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "keyword_metrics", b"keyword_metrics", "search_query", b"search_query"
        ],
    ) -> None: ...

global___KeywordPlanKeywordHistoricalMetrics = KeywordPlanKeywordHistoricalMetrics
