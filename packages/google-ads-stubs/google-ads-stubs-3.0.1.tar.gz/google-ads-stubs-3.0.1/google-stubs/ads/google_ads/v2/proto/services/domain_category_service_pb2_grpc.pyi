# Stubs for google.ads.google_ads.v2.proto.services.domain_category_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class DomainCategoryServiceStub:
    GetDomainCategory: Any = ...
    def __init__(self, channel: Any) -> None: ...

class DomainCategoryServiceServicer:
    def GetDomainCategory(self, request: Any, context: Any) -> None: ...

def add_DomainCategoryServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
