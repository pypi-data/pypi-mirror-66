# Stubs for google.ads.google_ads.v1.proto.services.custom_interest_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class CustomInterestServiceStub:
    GetCustomInterest: Any = ...
    MutateCustomInterests: Any = ...
    def __init__(self, channel: Any) -> None: ...

class CustomInterestServiceServicer:
    def GetCustomInterest(self, request: Any, context: Any) -> None: ...
    def MutateCustomInterests(self, request: Any, context: Any) -> None: ...

def add_CustomInterestServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
