# Stubs for google.ads.google_ads.v2.proto.services.ad_parameter_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class AdParameterServiceStub:
    GetAdParameter: Any = ...
    MutateAdParameters: Any = ...
    def __init__(self, channel: Any) -> None: ...

class AdParameterServiceServicer:
    def GetAdParameter(self, request: Any, context: Any) -> None: ...
    def MutateAdParameters(self, request: Any, context: Any) -> None: ...

def add_AdParameterServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
