# Stubs for google.ads.google_ads.v1.proto.services.topic_constant_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class TopicConstantServiceStub:
    GetTopicConstant: Any = ...
    def __init__(self, channel: Any) -> None: ...

class TopicConstantServiceServicer:
    def GetTopicConstant(self, request: Any, context: Any) -> None: ...

def add_TopicConstantServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
