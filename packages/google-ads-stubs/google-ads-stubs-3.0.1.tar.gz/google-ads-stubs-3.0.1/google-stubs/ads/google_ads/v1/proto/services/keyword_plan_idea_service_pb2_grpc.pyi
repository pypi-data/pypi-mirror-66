# Stubs for google.ads.google_ads.v1.proto.services.keyword_plan_idea_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class KeywordPlanIdeaServiceStub:
    GenerateKeywordIdeas: Any = ...
    def __init__(self, channel: Any) -> None: ...

class KeywordPlanIdeaServiceServicer:
    def GenerateKeywordIdeas(self, request: Any, context: Any) -> None: ...

def add_KeywordPlanIdeaServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
