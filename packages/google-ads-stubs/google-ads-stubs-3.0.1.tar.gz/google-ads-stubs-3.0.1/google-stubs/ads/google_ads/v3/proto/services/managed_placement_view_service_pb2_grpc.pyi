from typing import Any

class ManagedPlacementViewServiceStub:
    GetManagedPlacementView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class ManagedPlacementViewServiceServicer:
    def GetManagedPlacementView(self, request: Any, context: Any) -> None: ...

def add_ManagedPlacementViewServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
