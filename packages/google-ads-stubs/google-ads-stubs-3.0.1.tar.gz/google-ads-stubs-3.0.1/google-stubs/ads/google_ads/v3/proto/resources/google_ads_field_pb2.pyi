# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v3.proto.enums.google_ads_field_category_pb2 import (
    GoogleAdsFieldCategoryEnum as google___ads___googleads___v3___enums___google_ads_field_category_pb2___GoogleAdsFieldCategoryEnum,
)

from google.ads.google_ads.v3.proto.enums.google_ads_field_data_type_pb2 import (
    GoogleAdsFieldDataTypeEnum as google___ads___googleads___v3___enums___google_ads_field_data_type_pb2___GoogleAdsFieldDataTypeEnum,
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

class GoogleAdsField(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    category = (
        ...
    )  # type: google___ads___googleads___v3___enums___google_ads_field_category_pb2___GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory
    data_type = (
        ...
    )  # type: google___ads___googleads___v3___enums___google_ads_field_data_type_pb2___GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def selectable(self) -> google___protobuf___wrappers_pb2___BoolValue: ...
    @property
    def filterable(self) -> google___protobuf___wrappers_pb2___BoolValue: ...
    @property
    def sortable(self) -> google___protobuf___wrappers_pb2___BoolValue: ...
    @property
    def selectable_with(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    @property
    def attribute_resources(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    @property
    def metrics(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    @property
    def segments(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    @property
    def enum_values(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        google___protobuf___wrappers_pb2___StringValue
    ]: ...
    @property
    def type_url(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def is_repeated(self) -> google___protobuf___wrappers_pb2___BoolValue: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        category: typing___Optional[
            google___ads___googleads___v3___enums___google_ads_field_category_pb2___GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory
        ] = None,
        selectable: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
        filterable: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
        sortable: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
        selectable_with: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        attribute_resources: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        metrics: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        segments: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        enum_values: typing___Optional[
            typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
        ] = None,
        data_type: typing___Optional[
            google___ads___googleads___v3___enums___google_ads_field_data_type_pb2___GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType
        ] = None,
        type_url: typing___Optional[
            google___protobuf___wrappers_pb2___StringValue
        ] = None,
        is_repeated: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GoogleAdsField: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GoogleAdsField: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "filterable",
            b"filterable",
            "is_repeated",
            b"is_repeated",
            "name",
            b"name",
            "selectable",
            b"selectable",
            "sortable",
            b"sortable",
            "type_url",
            b"type_url",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "attribute_resources",
            b"attribute_resources",
            "category",
            b"category",
            "data_type",
            b"data_type",
            "enum_values",
            b"enum_values",
            "filterable",
            b"filterable",
            "is_repeated",
            b"is_repeated",
            "metrics",
            b"metrics",
            "name",
            b"name",
            "resource_name",
            b"resource_name",
            "segments",
            b"segments",
            "selectable",
            b"selectable",
            "selectable_with",
            b"selectable_with",
            "sortable",
            b"sortable",
            "type_url",
            b"type_url",
        ],
    ) -> None: ...

global___GoogleAdsField = GoogleAdsField
