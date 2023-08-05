# Stubs for google.ads.google_ads.v2.services.transports.custom_interest_service_grpc_transport (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class CustomInterestServiceGrpcTransport:
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
    def get_custom_interest(self): ...
    @property
    def mutate_custom_interests(self): ...
