# Stubs for google.ads.google_ads.v1.proto.services.detail_placement_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class DetailPlacementViewServiceStub:
    GetDetailPlacementView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class DetailPlacementViewServiceServicer:
    def GetDetailPlacementView(self, request: Any, context: Any) -> None: ...

def add_DetailPlacementViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
