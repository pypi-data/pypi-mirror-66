# Stubs for google.ads.google_ads.v1.proto.services.customer_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class CustomerServiceStub:
    GetCustomer: Any = ...
    MutateCustomer: Any = ...
    ListAccessibleCustomers: Any = ...
    CreateCustomerClient: Any = ...
    def __init__(self, channel: Any) -> None: ...

class CustomerServiceServicer:
    def GetCustomer(self, request: Any, context: Any) -> None: ...
    def MutateCustomer(self, request: Any, context: Any) -> None: ...
    def ListAccessibleCustomers(self, request: Any, context: Any) -> None: ...
    def CreateCustomerClient(self, request: Any, context: Any) -> None: ...

def add_CustomerServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
