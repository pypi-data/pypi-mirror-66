# Stubs for google.ads.google_ads.v1.proto.services.location_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class LocationViewServiceStub:
    GetLocationView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class LocationViewServiceServicer:
    def GetLocationView(self, request: Any, context: Any) -> None: ...

def add_LocationViewServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
