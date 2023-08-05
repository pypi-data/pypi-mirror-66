# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v3.proto.common.tag_snippet_pb2 import (
    TagSnippet as google___ads___googleads___v3___common___tag_snippet_pb2___TagSnippet,
)

from google.ads.google_ads.v3.proto.enums.attribution_model_pb2 import (
    AttributionModelEnum as google___ads___googleads___v3___enums___attribution_model_pb2___AttributionModelEnum,
)

from google.ads.google_ads.v3.proto.enums.conversion_action_category_pb2 import (
    ConversionActionCategoryEnum as google___ads___googleads___v3___enums___conversion_action_category_pb2___ConversionActionCategoryEnum,
)

from google.ads.google_ads.v3.proto.enums.conversion_action_counting_type_pb2 import (
    ConversionActionCountingTypeEnum as google___ads___googleads___v3___enums___conversion_action_counting_type_pb2___ConversionActionCountingTypeEnum,
)

from google.ads.google_ads.v3.proto.enums.conversion_action_status_pb2 import (
    ConversionActionStatusEnum as google___ads___googleads___v3___enums___conversion_action_status_pb2___ConversionActionStatusEnum,
)

from google.ads.google_ads.v3.proto.enums.conversion_action_type_pb2 import (
    ConversionActionTypeEnum as google___ads___googleads___v3___enums___conversion_action_type_pb2___ConversionActionTypeEnum,
)

from google.ads.google_ads.v3.proto.enums.data_driven_model_status_pb2 import (
    DataDrivenModelStatusEnum as google___ads___googleads___v3___enums___data_driven_model_status_pb2___DataDrivenModelStatusEnum,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    BoolValue as google___protobuf___wrappers_pb2___BoolValue,
    DoubleValue as google___protobuf___wrappers_pb2___DoubleValue,
    Int64Value as google___protobuf___wrappers_pb2___Int64Value,
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

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

class ConversionAction(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class AttributionModelSettings(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        attribution_model = (
            ...
        )  # type: google___ads___googleads___v3___enums___attribution_model_pb2___AttributionModelEnum.AttributionModel
        data_driven_model_status = (
            ...
        )  # type: google___ads___googleads___v3___enums___data_driven_model_status_pb2___DataDrivenModelStatusEnum.DataDrivenModelStatus
        def __init__(
            self,
            *,
            attribution_model: typing___Optional[
                google___ads___googleads___v3___enums___attribution_model_pb2___AttributionModelEnum.AttributionModel
            ] = None,
            data_driven_model_status: typing___Optional[
                google___ads___googleads___v3___enums___data_driven_model_status_pb2___DataDrivenModelStatusEnum.DataDrivenModelStatus
            ] = None,
        ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(
                cls, s: builtin___bytes
            ) -> ConversionAction.AttributionModelSettings: ...
        else:
            @classmethod
            def FromString(
                cls,
                s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode],
            ) -> ConversionAction.AttributionModelSettings: ...
        def MergeFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def CopyFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions___Literal[
                "attribution_model",
                b"attribution_model",
                "data_driven_model_status",
                b"data_driven_model_status",
            ],
        ) -> None: ...
    global___AttributionModelSettings = AttributionModelSettings
    class ValueSettings(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        @property
        def default_value(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
        @property
        def default_currency_code(
            self,
        ) -> google___protobuf___wrappers_pb2___StringValue: ...
        @property
        def always_use_default_value(
            self,
        ) -> google___protobuf___wrappers_pb2___BoolValue: ...
        def __init__(
            self,
            *,
            default_value: typing___Optional[
                google___protobuf___wrappers_pb2___DoubleValue
            ] = None,
            default_currency_code: typing___Optional[
                google___protobuf___wrappers_pb2___StringValue
            ] = None,
            always_use_default_value: typing___Optional[
                google___protobuf___wrappers_pb2___BoolValue
            ] = None,
        ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(
                cls, s: builtin___bytes
            ) -> ConversionAction.ValueSettings: ...
        else:
            @classmethod
            def FromString(
                cls,
                s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode],
            ) -> ConversionAction.ValueSettings: ...
        def MergeFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def CopyFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def HasField(
            self,
            field_name: typing_extensions___Literal[
                "always_use_default_value",
                b"always_use_default_value",
                "default_currency_code",
                b"default_currency_code",
                "default_value",
                b"default_value",
            ],
        ) -> builtin___bool: ...
        def ClearField(
            self,
            field_name: typing_extensions___Literal[
                "always_use_default_value",
                b"always_use_default_value",
                "default_currency_code",
                b"default_currency_code",
                "default_value",
                b"default_value",
            ],
        ) -> None: ...
    global___ValueSettings = ValueSettings

    resource_name = ...  # type: typing___Text
    status = (
        ...
    )  # type: google___ads___googleads___v3___enums___conversion_action_status_pb2___ConversionActionStatusEnum.ConversionActionStatus
    type = (
        ...
    )  # type: google___ads___googleads___v3___enums___conversion_action_type_pb2___ConversionActionTypeEnum.ConversionActionType
    category = (
        ...
    )  # type: google___ads___googleads___v3___enums___conversion_action_category_pb2___ConversionActionCategoryEnum.ConversionActionCategory
    counting_type = (
        ...
    )  # type: google___ads___googleads___v3___enums___conversion_action_counting_type_pb2___ConversionActionCountingTypeEnum.ConversionActionCountingType
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def owner_customer(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def include_in_conversions_metric(
        self,
    ) -> google___protobuf___wrappers_pb2___BoolValue: ...
    @property
    def click_through_lookback_window_days(
        self,
    ) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def view_through_lookback_window_days(
        self,
    ) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def value_settings(self) -> global___ConversionAction.ValueSettings: ...
    @property
    def attribution_model_settings(
        self,
    ) -> global___ConversionAction.AttributionModelSettings: ...
    @property
    def tag_snippets(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___ads___googleads___v3___common___tag_snippet_pb2___TagSnippet
    ]: ...
    @property
    def phone_call_duration_seconds(
        self,
    ) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def app_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        status: typing___Optional[
            google___ads___googleads___v3___enums___conversion_action_status_pb2___ConversionActionStatusEnum.ConversionActionStatus
        ] = None,
        type: typing___Optional[
            google___ads___googleads___v3___enums___conversion_action_type_pb2___ConversionActionTypeEnum.ConversionActionType
        ] = None,
        category: typing___Optional[
            google___ads___googleads___v3___enums___conversion_action_category_pb2___ConversionActionCategoryEnum.ConversionActionCategory
        ] = None,
        owner_customer: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        include_in_conversions_metric: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
        click_through_lookback_window_days: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        view_through_lookback_window_days: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        value_settings: typing___Optional[
            global___ConversionAction.ValueSettings
        ] = None,
        counting_type: typing___Optional[
            google___ads___googleads___v3___enums___conversion_action_counting_type_pb2___ConversionActionCountingTypeEnum.ConversionActionCountingType
        ] = None,
        attribution_model_settings: typing___Optional[
            global___ConversionAction.AttributionModelSettings
        ] = None,
        tag_snippets: typing___Optional[
            typing___Iterable[
                google___ads___googleads___v3___common___tag_snippet_pb2___TagSnippet
            ]
        ] = None,
        phone_call_duration_seconds: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        app_id: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ConversionAction: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ConversionAction: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "app_id",
            b"app_id",
            "attribution_model_settings",
            b"attribution_model_settings",
            "click_through_lookback_window_days",
            b"click_through_lookback_window_days",
            "id",
            b"id",
            "include_in_conversions_metric",
            b"include_in_conversions_metric",
            "name",
            b"name",
            "owner_customer",
            b"owner_customer",
            "phone_call_duration_seconds",
            b"phone_call_duration_seconds",
            "value_settings",
            b"value_settings",
            "view_through_lookback_window_days",
            b"view_through_lookback_window_days",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "app_id",
            b"app_id",
            "attribution_model_settings",
            b"attribution_model_settings",
            "category",
            b"category",
            "click_through_lookback_window_days",
            b"click_through_lookback_window_days",
            "counting_type",
            b"counting_type",
            "id",
            b"id",
            "include_in_conversions_metric",
            b"include_in_conversions_metric",
            "name",
            b"name",
            "owner_customer",
            b"owner_customer",
            "phone_call_duration_seconds",
            b"phone_call_duration_seconds",
            "resource_name",
            b"resource_name",
            "status",
            b"status",
            "tag_snippets",
            b"tag_snippets",
            "type",
            b"type",
            "value_settings",
            b"value_settings",
            "view_through_lookback_window_days",
            b"view_through_lookback_window_days",
        ],
    ) -> None: ...

global___ConversionAction = ConversionAction
