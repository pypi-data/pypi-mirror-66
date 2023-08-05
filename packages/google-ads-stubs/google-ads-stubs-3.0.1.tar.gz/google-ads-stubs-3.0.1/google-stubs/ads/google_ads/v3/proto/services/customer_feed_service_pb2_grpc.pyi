from typing import Any

class CustomerFeedServiceStub:
    GetCustomerFeed: Any = ...
    MutateCustomerFeeds: Any = ...
    def __init__(self, channel: Any) -> None: ...

class CustomerFeedServiceServicer:
    def GetCustomerFeed(self, request: Any, context: Any) -> None: ...
    def MutateCustomerFeeds(self, request: Any, context: Any) -> None: ...

def add_CustomerFeedServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
