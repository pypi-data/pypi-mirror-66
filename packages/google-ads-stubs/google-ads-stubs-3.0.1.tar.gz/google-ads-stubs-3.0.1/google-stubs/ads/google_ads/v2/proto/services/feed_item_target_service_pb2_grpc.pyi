# Stubs for google.ads.google_ads.v2.proto.services.feed_item_target_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class FeedItemTargetServiceStub:
    GetFeedItemTarget: Any = ...
    MutateFeedItemTargets: Any = ...
    def __init__(self, channel: Any) -> None: ...

class FeedItemTargetServiceServicer:
    def GetFeedItemTarget(self, request: Any, context: Any) -> None: ...
    def MutateFeedItemTargets(self, request: Any, context: Any) -> None: ...

def add_FeedItemTargetServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
