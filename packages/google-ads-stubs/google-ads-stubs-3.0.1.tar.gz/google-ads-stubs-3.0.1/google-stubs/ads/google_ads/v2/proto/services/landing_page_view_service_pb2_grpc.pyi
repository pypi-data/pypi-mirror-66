# Stubs for google.ads.google_ads.v2.proto.services.landing_page_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class LandingPageViewServiceStub:
    GetLandingPageView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class LandingPageViewServiceServicer:
    def GetLandingPageView(self, request: Any, context: Any) -> None: ...

def add_LandingPageViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
