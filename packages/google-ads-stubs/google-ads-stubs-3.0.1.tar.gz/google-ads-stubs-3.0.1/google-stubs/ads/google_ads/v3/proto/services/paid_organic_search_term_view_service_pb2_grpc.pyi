from typing import Any

class PaidOrganicSearchTermViewServiceStub:
    GetPaidOrganicSearchTermView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class PaidOrganicSearchTermViewServiceServicer:
    def GetPaidOrganicSearchTermView(self, request: Any, context: Any) -> None: ...

def add_PaidOrganicSearchTermViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
