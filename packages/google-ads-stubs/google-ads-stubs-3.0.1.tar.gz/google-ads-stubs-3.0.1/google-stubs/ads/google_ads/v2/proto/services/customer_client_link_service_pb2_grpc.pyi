# Stubs for google.ads.google_ads.v2.proto.services.customer_client_link_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class CustomerClientLinkServiceStub:
    GetCustomerClientLink: Any = ...
    MutateCustomerClientLink: Any = ...
    def __init__(self, channel: Any) -> None: ...

class CustomerClientLinkServiceServicer:
    def GetCustomerClientLink(self, request: Any, context: Any) -> None: ...
    def MutateCustomerClientLink(self, request: Any, context: Any) -> None: ...

def add_CustomerClientLinkServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
