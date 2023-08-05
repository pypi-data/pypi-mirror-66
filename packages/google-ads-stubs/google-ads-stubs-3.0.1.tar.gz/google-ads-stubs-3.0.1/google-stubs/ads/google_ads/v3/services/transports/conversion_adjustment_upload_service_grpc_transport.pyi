from google.ads.google_ads.v3.proto.services import (
    conversion_adjustment_upload_service_pb2_grpc as conversion_adjustment_upload_service_pb2_grpc,
)
from typing import Any, Optional

class ConversionAdjustmentUploadServiceGrpcTransport:
    def __init__(
        self,
        channel: Optional[Any] = ...,
        credentials: Optional[Any] = ...,
        address: str = ...,
    ) -> None: ...
    @classmethod
    def create_channel(
        cls, address: str = ..., credentials: Optional[Any] = ..., **kwargs: Any
    ): ...
    @property
    def channel(self): ...
    @property
    def upload_conversion_adjustments(self): ...
