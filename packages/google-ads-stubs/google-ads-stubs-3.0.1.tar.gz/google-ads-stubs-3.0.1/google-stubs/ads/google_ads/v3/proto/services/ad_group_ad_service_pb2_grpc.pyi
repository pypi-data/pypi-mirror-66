from typing import Any

class AdGroupAdServiceStub:
    GetAdGroupAd: Any = ...
    MutateAdGroupAds: Any = ...
    def __init__(self, channel: Any) -> None: ...

class AdGroupAdServiceServicer:
    def GetAdGroupAd(self, request: Any, context: Any) -> None: ...
    def MutateAdGroupAds(self, request: Any, context: Any) -> None: ...

def add_AdGroupAdServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
