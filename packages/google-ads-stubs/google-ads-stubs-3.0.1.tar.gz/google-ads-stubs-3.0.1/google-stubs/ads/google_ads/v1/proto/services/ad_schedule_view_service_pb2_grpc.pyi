# Stubs for google.ads.google_ads.v1.proto.services.ad_schedule_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class AdScheduleViewServiceStub:
    GetAdScheduleView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class AdScheduleViewServiceServicer:
    def GetAdScheduleView(self, request: Any, context: Any) -> None: ...

def add_AdScheduleViewServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
