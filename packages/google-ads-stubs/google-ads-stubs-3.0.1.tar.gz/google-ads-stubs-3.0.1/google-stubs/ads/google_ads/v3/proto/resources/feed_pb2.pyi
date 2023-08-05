# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v3.proto.enums.affiliate_location_feed_relationship_type_pb2 import (
    AffiliateLocationFeedRelationshipTypeEnum as google___ads___googleads___v3___enums___affiliate_location_feed_relationship_type_pb2___AffiliateLocationFeedRelationshipTypeEnum,
)

from google.ads.google_ads.v3.proto.enums.feed_attribute_type_pb2 import (
    FeedAttributeTypeEnum as google___ads___googleads___v3___enums___feed_attribute_type_pb2___FeedAttributeTypeEnum,
)

from google.ads.google_ads.v3.proto.enums.feed_origin_pb2 import (
    FeedOriginEnum as google___ads___googleads___v3___enums___feed_origin_pb2___FeedOriginEnum,
)

from google.ads.google_ads.v3.proto.enums.feed_status_pb2 import (
    FeedStatusEnum as google___ads___googleads___v3___enums___feed_status_pb2___FeedStatusEnum,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from google.protobuf.wrappers_pb2 import (
    BoolValue as google___protobuf___wrappers_pb2___BoolValue,
    Int64Value as google___protobuf___wrappers_pb2___Int64Value,
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

from typing_extensions import Literal as typing_extensions___Literal

builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode

class Feed(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class PlacesLocationFeedData(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        class OAuthInfo(google___protobuf___message___Message):
            DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
            @property
            def http_method(self) -> google___protobuf___wrappers_pb2___StringValue: ...
            @property
            def http_request_url(
                self,
            ) -> google___protobuf___wrappers_pb2___StringValue: ...
            @property
            def http_authorization_header(
                self,
            ) -> google___protobuf___wrappers_pb2___StringValue: ...
            def __init__(
                self,
                *,
                http_method: typing___Optional[
                    google___protobuf___wrappers_pb2___StringValue
                ] = None,
                http_request_url: typing___Optional[
                    google___protobuf___wrappers_pb2___StringValue
                ] = None,
                http_authorization_header: typing___Optional[
                    google___protobuf___wrappers_pb2___StringValue
                ] = None,
            ) -> None: ...
            if sys.version_info >= (3,):
                @classmethod
                def FromString(
                    cls, s: builtin___bytes
                ) -> Feed.PlacesLocationFeedData.OAuthInfo: ...
            else:
                @classmethod
                def FromString(
                    cls,
                    s: typing___Union[
                        builtin___bytes, builtin___buffer, builtin___unicode
                    ],
                ) -> Feed.PlacesLocationFeedData.OAuthInfo: ...
            def MergeFrom(
                self, other_msg: google___protobuf___message___Message
            ) -> None: ...
            def CopyFrom(
                self, other_msg: google___protobuf___message___Message
            ) -> None: ...
            def HasField(
                self,
                field_name: typing_extensions___Literal[
                    "http_authorization_header",
                    b"http_authorization_header",
                    "http_method",
                    b"http_method",
                    "http_request_url",
                    b"http_request_url",
                ],
            ) -> builtin___bool: ...
            def ClearField(
                self,
                field_name: typing_extensions___Literal[
                    "http_authorization_header",
                    b"http_authorization_header",
                    "http_method",
                    b"http_method",
                    "http_request_url",
                    b"http_request_url",
                ],
            ) -> None: ...
        global___OAuthInfo = OAuthInfo
        @property
        def oauth_info(self) -> global___Feed.PlacesLocationFeedData.OAuthInfo: ...
        @property
        def email_address(self) -> google___protobuf___wrappers_pb2___StringValue: ...
        @property
        def business_account_id(
            self,
        ) -> google___protobuf___wrappers_pb2___StringValue: ...
        @property
        def business_name_filter(
            self,
        ) -> google___protobuf___wrappers_pb2___StringValue: ...
        @property
        def category_filters(
            self,
        ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
            google___protobuf___wrappers_pb2___StringValue
        ]: ...
        @property
        def label_filters(
            self,
        ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
            google___protobuf___wrappers_pb2___StringValue
        ]: ...
        def __init__(
            self,
            *,
            oauth_info: typing___Optional[
                global___Feed.PlacesLocationFeedData.OAuthInfo
            ] = None,
            email_address: typing___Optional[
                google___protobuf___wrappers_pb2___StringValue
            ] = None,
            business_account_id: typing___Optional[
                google___protobuf___wrappers_pb2___StringValue
            ] = None,
            business_name_filter: typing___Optional[
                google___protobuf___wrappers_pb2___StringValue
            ] = None,
            category_filters: typing___Optional[
                typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
            ] = None,
            label_filters: typing___Optional[
                typing___Iterable[google___protobuf___wrappers_pb2___StringValue]
            ] = None,
        ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(cls, s: builtin___bytes) -> Feed.PlacesLocationFeedData: ...
        else:
            @classmethod
            def FromString(
                cls,
                s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode],
            ) -> Feed.PlacesLocationFeedData: ...
        def MergeFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def CopyFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def HasField(
            self,
            field_name: typing_extensions___Literal[
                "business_account_id",
                b"business_account_id",
                "business_name_filter",
                b"business_name_filter",
                "email_address",
                b"email_address",
                "oauth_info",
                b"oauth_info",
            ],
        ) -> builtin___bool: ...
        def ClearField(
            self,
            field_name: typing_extensions___Literal[
                "business_account_id",
                b"business_account_id",
                "business_name_filter",
                b"business_name_filter",
                "category_filters",
                b"category_filters",
                "email_address",
                b"email_address",
                "label_filters",
                b"label_filters",
                "oauth_info",
                b"oauth_info",
            ],
        ) -> None: ...
    global___PlacesLocationFeedData = PlacesLocationFeedData
    class AffiliateLocationFeedData(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        relationship_type = (
            ...
        )  # type: google___ads___googleads___v3___enums___affiliate_location_feed_relationship_type_pb2___AffiliateLocationFeedRelationshipTypeEnum.AffiliateLocationFeedRelationshipType
        @property
        def chain_ids(
            self,
        ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
            google___protobuf___wrappers_pb2___Int64Value
        ]: ...
        def __init__(
            self,
            *,
            chain_ids: typing___Optional[
                typing___Iterable[google___protobuf___wrappers_pb2___Int64Value]
            ] = None,
            relationship_type: typing___Optional[
                google___ads___googleads___v3___enums___affiliate_location_feed_relationship_type_pb2___AffiliateLocationFeedRelationshipTypeEnum.AffiliateLocationFeedRelationshipType
            ] = None,
        ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(
                cls, s: builtin___bytes
            ) -> Feed.AffiliateLocationFeedData: ...
        else:
            @classmethod
            def FromString(
                cls,
                s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode],
            ) -> Feed.AffiliateLocationFeedData: ...
        def MergeFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def CopyFrom(
            self, other_msg: google___protobuf___message___Message
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions___Literal[
                "chain_ids", b"chain_ids", "relationship_type", b"relationship_type"
            ],
        ) -> None: ...
    global___AffiliateLocationFeedData = AffiliateLocationFeedData

    resource_name = ...  # type: typing___Text
    origin = (
        ...
    )  # type: google___ads___googleads___v3___enums___feed_origin_pb2___FeedOriginEnum.FeedOrigin
    status = (
        ...
    )  # type: google___ads___googleads___v3___enums___feed_status_pb2___FeedStatusEnum.FeedStatus
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def attributes(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___FeedAttribute
    ]: ...
    @property
    def attribute_operations(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___FeedAttributeOperation
    ]: ...
    @property
    def places_location_feed_data(self) -> global___Feed.PlacesLocationFeedData: ...
    @property
    def affiliate_location_feed_data(
        self,
    ) -> global___Feed.AffiliateLocationFeedData: ...
    def __init__(
        self,
        *,
        resource_name: typing___Optional[typing___Text] = None,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        attributes: typing___Optional[typing___Iterable[global___FeedAttribute]] = None,
        attribute_operations: typing___Optional[
            typing___Iterable[global___FeedAttributeOperation]
        ] = None,
        origin: typing___Optional[
            google___ads___googleads___v3___enums___feed_origin_pb2___FeedOriginEnum.FeedOrigin
        ] = None,
        status: typing___Optional[
            google___ads___googleads___v3___enums___feed_status_pb2___FeedStatusEnum.FeedStatus
        ] = None,
        places_location_feed_data: typing___Optional[
            global___Feed.PlacesLocationFeedData
        ] = None,
        affiliate_location_feed_data: typing___Optional[
            global___Feed.AffiliateLocationFeedData
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Feed: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> Feed: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "affiliate_location_feed_data",
            b"affiliate_location_feed_data",
            "id",
            b"id",
            "name",
            b"name",
            "places_location_feed_data",
            b"places_location_feed_data",
            "system_feed_generation_data",
            b"system_feed_generation_data",
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "affiliate_location_feed_data",
            b"affiliate_location_feed_data",
            "attribute_operations",
            b"attribute_operations",
            "attributes",
            b"attributes",
            "id",
            b"id",
            "name",
            b"name",
            "origin",
            b"origin",
            "places_location_feed_data",
            b"places_location_feed_data",
            "resource_name",
            b"resource_name",
            "status",
            b"status",
            "system_feed_generation_data",
            b"system_feed_generation_data",
        ],
    ) -> None: ...
    def WhichOneof(
        self,
        oneof_group: typing_extensions___Literal[
            "system_feed_generation_data", b"system_feed_generation_data"
        ],
    ) -> typing_extensions___Literal[
        "places_location_feed_data", "affiliate_location_feed_data"
    ]: ...

global___Feed = Feed

class FeedAttribute(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    type = (
        ...
    )  # type: google___ads___googleads___v3___enums___feed_attribute_type_pb2___FeedAttributeTypeEnum.FeedAttributeType
    @property
    def id(self) -> google___protobuf___wrappers_pb2___Int64Value: ...
    @property
    def name(self) -> google___protobuf___wrappers_pb2___StringValue: ...
    @property
    def is_part_of_key(self) -> google___protobuf___wrappers_pb2___BoolValue: ...
    def __init__(
        self,
        *,
        id: typing___Optional[google___protobuf___wrappers_pb2___Int64Value] = None,
        name: typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        type: typing___Optional[
            google___ads___googleads___v3___enums___feed_attribute_type_pb2___FeedAttributeTypeEnum.FeedAttributeType
        ] = None,
        is_part_of_key: typing___Optional[
            google___protobuf___wrappers_pb2___BoolValue
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> FeedAttribute: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> FeedAttribute: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions___Literal[
            "id", b"id", "is_part_of_key", b"is_part_of_key", "name", b"name"
        ],
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "id",
            b"id",
            "is_part_of_key",
            b"is_part_of_key",
            "name",
            b"name",
            "type",
            b"type",
        ],
    ) -> None: ...

global___FeedAttribute = FeedAttribute

class FeedAttributeOperation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class Operator(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> "FeedAttributeOperation.Operator": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List["FeedAttributeOperation.Operator"]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[builtin___str, "FeedAttributeOperation.Operator"]
        ]: ...
        UNSPECIFIED = typing___cast("FeedAttributeOperation.Operator", 0)
        UNKNOWN = typing___cast("FeedAttributeOperation.Operator", 1)
        ADD = typing___cast("FeedAttributeOperation.Operator", 2)
    UNSPECIFIED = typing___cast("FeedAttributeOperation.Operator", 0)
    UNKNOWN = typing___cast("FeedAttributeOperation.Operator", 1)
    ADD = typing___cast("FeedAttributeOperation.Operator", 2)
    global___Operator = Operator

    operator = ...  # type: global___FeedAttributeOperation.Operator
    @property
    def value(self) -> global___FeedAttribute: ...
    def __init__(
        self,
        *,
        operator: typing___Optional[global___FeedAttributeOperation.Operator] = None,
        value: typing___Optional[global___FeedAttribute] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> FeedAttributeOperation: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> FeedAttributeOperation: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(
        self, field_name: typing_extensions___Literal["value", b"value"]
    ) -> builtin___bool: ...
    def ClearField(
        self,
        field_name: typing_extensions___Literal[
            "operator", b"operator", "value", b"value"
        ],
    ) -> None: ...

global___FeedAttributeOperation = FeedAttributeOperation
