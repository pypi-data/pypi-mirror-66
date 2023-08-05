# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.ads.google_ads.v2.proto.resources.customer_feed_pb2 import (
    CustomerFeed as google___ads___googleads___v2___resources___customer_feed_pb2___CustomerFeed,
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

class GetCustomerFeedRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    def __init__(
        self, *, resource_name: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetCustomerFeedRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> GetCustomerFeedRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["resource_name", b"resource_name"]
    ) -> None: ...

global___GetCustomerFeedRequest = GetCustomerFeedRequest

class MutateCustomerFeedsRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    customer_id = ...  # type: typing___Text
    partial_failure = ...  # type: builtin___bool
    validate_only = ...  # type: builtin___bool
    @property
    def operations(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___CustomerFeedOperation
    ]: ...
    def __init__(
        self,
        *,
        customer_id: typing___Optional[typing___Text] = None,
        operations: typing___Optional[
            typing___Iterable[global___CustomerFeedOperation]
        ] = None,
        partial_failure: typing___Optional[builtin___bool] = None,
        validate_only: typing___Optional[builtin___bool] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateCustomerFeedsRequest: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateCustomerFeedsRequest: ...
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

global___MutateCustomerFeedsRequest = MutateCustomerFeedsRequest

class CustomerFeedOperation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    remove = ...  # type: typing___Text
    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...
    @property
    def create(
        self,
    ) -> google___ads___googleads___v2___resources___customer_feed_pb2___CustomerFeed: ...
    @property
    def update(
        self,
    ) -> google___ads___googleads___v2___resources___customer_feed_pb2___CustomerFeed: ...
    def __init__(
        self,
        *,
        update_mask: typing___Optional[
            google___protobuf___field_mask_pb2___FieldMask
        ] = None,
        create: typing___Optional[
            google___ads___googleads___v2___resources___customer_feed_pb2___CustomerFeed
        ] = None,
        update: typing___Optional[
            google___ads___googleads___v2___resources___customer_feed_pb2___CustomerFeed
        ] = None,
        remove: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CustomerFeedOperation: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> CustomerFeedOperation: ...
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

global___CustomerFeedOperation = CustomerFeedOperation

class MutateCustomerFeedsResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    @property
    def partial_failure_error(self) -> google___rpc___status_pb2___Status: ...
    @property
    def results(
        self,
    ) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[
        global___MutateCustomerFeedResult
    ]: ...
    def __init__(
        self,
        *,
        partial_failure_error: typing___Optional[
            google___rpc___status_pb2___Status
        ] = None,
        results: typing___Optional[
            typing___Iterable[global___MutateCustomerFeedResult]
        ] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateCustomerFeedsResponse: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateCustomerFeedsResponse: ...
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

global___MutateCustomerFeedsResponse = MutateCustomerFeedsResponse

class MutateCustomerFeedResult(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    resource_name = ...  # type: typing___Text
    def __init__(
        self, *, resource_name: typing___Optional[typing___Text] = None,
    ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MutateCustomerFeedResult: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> MutateCustomerFeedResult: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(
        self, field_name: typing_extensions___Literal["resource_name", b"resource_name"]
    ) -> None: ...

global___MutateCustomerFeedResult = MutateCustomerFeedResult
