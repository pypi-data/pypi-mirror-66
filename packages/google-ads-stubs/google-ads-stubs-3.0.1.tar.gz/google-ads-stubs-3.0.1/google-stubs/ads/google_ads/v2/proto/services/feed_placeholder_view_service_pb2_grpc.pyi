# Stubs for google.ads.google_ads.v2.proto.services.feed_placeholder_view_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class FeedPlaceholderViewServiceStub:
    GetFeedPlaceholderView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class FeedPlaceholderViewServiceServicer:
    def GetFeedPlaceholderView(self, request: Any, context: Any) -> None: ...

def add_FeedPlaceholderViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
