# Stubs for google.ads.google_ads.v2.proto.services.change_status_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class ChangeStatusServiceStub:
    GetChangeStatus: Any = ...
    def __init__(self, channel: Any) -> None: ...

class ChangeStatusServiceServicer:
    def GetChangeStatus(self, request: Any, context: Any) -> None: ...

def add_ChangeStatusServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
