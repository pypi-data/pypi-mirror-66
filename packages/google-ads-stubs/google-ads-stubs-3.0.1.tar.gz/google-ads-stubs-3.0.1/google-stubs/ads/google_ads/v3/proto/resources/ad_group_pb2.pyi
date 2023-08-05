# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v3.proto.common.custom_parameter_pb2 import (
    CustomParameter as google___ads___googleads___v3___common___custom_parameter_pb2___CustomParameter,
)

from google.ads.google_ads.v3.proto.common.explorer_auto_optimizer_setting_pb2 import (
    ExplorerAutoOptimizerSetting as google___ads___googleads___v3___common___explorer_auto_optimizer_setting_pb2___ExplorerAutoOptimizerSetting,
)

from google.ads.google_ads.v3.proto.common.targeting_setting_pb2 import (
    TargetingSetting as google___ads___googleads___v3___common___targeting_setting_pb2___TargetingSetting,
)

from google.ads.google_ads.v3.proto.enums.ad_group_ad_rotation_mode_pb2 import (
    AdGroupAdRotationModeEnum as google___ads___googleads___v3___enums___ad_group_ad_rotation_mode_pb2___AdGroupAdRotationModeEnum,
)

from google.ads.google_ads.v3.proto.enums.ad_group_status_pb2 import (
    AdGroupStatusEnum as google___ads___googleads___v3___enums___ad_group_status_pb2___AdGroupStatusEnum,
)

from google.ads.google_ads.v3.proto.enums.ad_group_type_pb2 import (
    AdGroupTypeEnum as google___ads___googleads___v3___enums___ad_group_type_pb2___AdGroupTypeEnum,
)

from google.ads.google_ads.v3.proto.enums.bidding_source_pb2 import (
    BiddingSourceEnum as google___ads___googleads___v3___enums___bidding_source_pb2___BiddingSourceEnum,
)

from google.ads.google_ads.v3.proto.enums.targeting_dimension_pb2 import (
    TargetingDimensionEnum as google___ads___googleads___v3___enums___targeting_dimension_pb2___TargetingDimensionEnum,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
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

class AdGroup(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    status = (
        ...
    )  # type: google___ads___googleads___v3___enums___ad_group_status_pb2___AdGroupStatusEnum.AdGroupStatus
    type = (
        ...
    )  # type: google___ads___googleads___v3___enums___ad_group_type_pb2___AdGroupTypeEnum.AdGroupType
    ad_rotation_mode = (
        ...
    )  # type: google___ads___googleads___v3___enums___ad_group_ad_rotation_mode_pb2___AdGroupAdRotationModeEnum.AdGroupAdRotationMode
    display_custom_bid_dimension = (
        ...
    )  # type: google___ads___googleads___v3___enums___targeting_dimension_pb2___TargetingDimensionEnum.TargetingDimension
    effective_target_cpa_source = (
        ...
    )  # type: google___ads___googleads___v3___enums___bidding_source_pb2___BiddingSourceEnum.BiddingSource
    effective_target_roas_source = (
        ...
    )  # type: google___ads___googleads___v3___enums___bidding_source_pb2___BiddingSourceEnum.BiddingSource
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def base_ad_group(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def tracking_url_template(
        self,
    ) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def url_custom_parameters(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___ads___googleads___v3___common___custom_parameter_pb2___CustomParameter
    ]: ...
    @property
    def campaign(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def cpc_bid_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def cpm_bid_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def target_cpa_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def cpv_bid_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def target_cpm_micros(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def target_roas(self) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def percent_cpc_bid_micros(
        self,
    ) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def explorer_auto_optimizer_setting(
        self,
    ) -> google___ads___googleads___v3___common___explorer_auto_optimizer_setting_pb2___ExplorerAutoOptimizerSetting: ...
    @property
    def final_url_suffix(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def targeting_setting(
        self,
    ) -> google___ads___googleads___v3___common___targeting_setting_pb2___TargetingSetting: ...
    @property
    def effective_target_cpa_micros(
        self,
    ) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def effective_target_roas(
        self,
    ) -> google___protobuf___wrappers_pb2___DoubleValue: ...
    @property
    def labels(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        status: typing___Optional[
            google___ads___googleads___v3___enums___ad_group_status_pb2___AdGroupStatusEnum.AdGroupStatus
        ] = None,
        type: typing___Optional[
            google___ads___googleads___v3___enums___ad_group_type_pb2___AdGroupTypeEnum.AdGroupType
        ] = None,
        ad_rotation_mode: typing___Optional[
            google___ads___googleads___v3___enums___ad_group_ad_rotation_mode_pb2___AdGroupAdRotationModeEnum.AdGroupAdRotationMode
        ] = None,
        base_ad_group: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        tracking_url_template: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        url_custom_parameters: typing___Optional[
            typing___Iterable[
                google___ads___googleads___v3___common___custom_parameter_pb2___CustomParameter
            ]
        ] = None,
        campaign: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        cpc_bid_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        cpm_bid_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        target_cpa_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        cpv_bid_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        target_cpm_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        target_roas: typing___Optional[
            google___protobuf___wrappers_pb2___DoubleValue
        ] = None,
        percent_cpc_bid_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        explorer_auto_optimizer_setting: typing___Optional[
            google___ads___googleads___v3___common___explorer_auto_optimizer_setting_pb2___ExplorerAutoOptimizerSetting
        ] = None,
        display_custom_bid_dimension: typing___Optional[
            google___ads___googleads___v3___enums___targeting_dimension_pb2___TargetingDimensionEnum.TargetingDimension
        ] = None,
        final_url_suffix: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        targeting_setting: typing___Optional[
            google___ads___googleads___v3___common___targeting_setting_pb2___TargetingSetting
        ] = None,
        effective_target_cpa_micros: typing___Optional[
            google___protobuf___wrappers_pb2___Int64Value
        ] = None,
        effective_target_cpa_source: typing___Optional[
            google___ads___googleads___v3___enums___bidding_source_pb2___BiddingSourceEnum.BiddingSource
        ] = None,
        effective_target_roas: typing___Optional[
            google___protobuf___wrappers_pb2___DoubleValue
        ] = None,
        effective_target_roas_source: typing___Optional[
            google___ads___googleads___v3___enums___bidding_source_pb2___BiddingSourceEnum.BiddingSource
        ] = None,
        labels: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AdGroup: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> AdGroup: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "base_ad_group",
            b"base_ad_group",
            "campaign",
            b"campaign",
            "cpc_bid_micros",
            b"cpc_bid_micros",
            "cpm_bid_micros",
            b"cpm_bid_micros",
            "cpv_bid_micros",
            b"cpv_bid_micros",
            "effective_target_cpa_micros",
            b"effective_target_cpa_micros",
            "effective_target_roas",
            b"effective_target_roas",
            "explorer_auto_optimizer_setting",
            b"explorer_auto_optimizer_setting",
            "final_url_suffix",
            b"final_url_suffix",
            "id",
            b"id",
            "name",
            b"name",
            "percent_cpc_bid_micros",
            b"percent_cpc_bid_micros",
            "target_cpa_micros",
            b"target_cpa_micros",
            "target_cpm_micros",
            b"target_cpm_micros",
            "target_roas",
            b"target_roas",
            "targeting_setting",
            b"targeting_setting",
            "tracking_url_template",
            b"tracking_url_template",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "ad_rotation_mode",
            b"ad_rotation_mode",
            "base_ad_group",
            b"base_ad_group",
            "campaign",
            b"campaign",
            "cpc_bid_micros",
            b"cpc_bid_micros",
            "cpm_bid_micros",
            b"cpm_bid_micros",
            "cpv_bid_micros",
            b"cpv_bid_micros",
            "display_custom_bid_dimension",
            b"display_custom_bid_dimension",
            "effective_target_cpa_micros",
            b"effective_target_cpa_micros",
            "effective_target_cpa_source",
            b"effective_target_cpa_source",
            "effective_target_roas",
            b"effective_target_roas",
            "effective_target_roas_source",
            b"effective_target_roas_source",
            "explorer_auto_optimizer_setting",
            b"explorer_auto_optimizer_setting",
            "final_url_suffix",
            b"final_url_suffix",
            "id",
            b"id",
            "labels",
            b"labels",
            "name",
            b"name",
            "percent_cpc_bid_micros",
            b"percent_cpc_bid_micros",
            "resource_name",
            b"resource_name",
            "status",
            b"status",
            "target_cpa_micros",
            b"target_cpa_micros",
            "target_cpm_micros",
            b"target_cpm_micros",
            "target_roas",
            b"target_roas",
            "targeting_setting",
            b"targeting_setting",
            "tracking_url_template",
            b"tracking_url_template",
            "type",
            b"type",
            "url_custom_parameters",
            b"url_custom_parameters",
        ],
    ) -> None: ...

global___AdGroup = AdGroup
