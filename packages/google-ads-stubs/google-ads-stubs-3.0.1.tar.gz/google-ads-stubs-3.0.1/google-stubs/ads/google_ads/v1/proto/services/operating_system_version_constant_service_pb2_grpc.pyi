# Stubs for google.ads.google_ads.v1.proto.services.operating_system_version_constant_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class OperatingSystemVersionConstantServiceStub:
    GetOperatingSystemVersionConstant: Any = ...
    def __init__(self, channel: Any) -> None: ...

class OperatingSystemVersionConstantServiceServicer:
    def GetOperatingSystemVersionConstant(self, request: Any, context: Any) -> None: ...

def add_OperatingSystemVersionConstantServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
