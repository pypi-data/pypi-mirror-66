from typing import Any

class ExpandedLandingPageViewServiceStub:
    GetExpandedLandingPageView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class ExpandedLandingPageViewServiceServicer:
    def GetExpandedLandingPageView(self, request: Any, context: Any) -> None: ...

def add_ExpandedLandingPageViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
