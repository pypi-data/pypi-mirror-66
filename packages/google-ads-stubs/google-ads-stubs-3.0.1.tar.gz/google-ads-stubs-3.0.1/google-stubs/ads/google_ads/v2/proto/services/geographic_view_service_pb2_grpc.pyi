# Stubs for google.ads.google_ads.v2.proto.services.geographic_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class GeographicViewServiceStub:
    GetGeographicView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class GeographicViewServiceServicer:
    def GetGeographicView(self, request: Any, context: Any) -> None: ...

def add_GeographicViewServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
