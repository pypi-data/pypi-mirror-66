from typing import Any

class MobileAppCategoryConstantServiceStub:
    GetMobileAppCategoryConstant: Any = ...
    def __init__(self, channel: Any) -> None: ...

class MobileAppCategoryConstantServiceServicer:
    def GetMobileAppCategoryConstant(self, request: Any, context: Any) -> None: ...

def add_MobileAppCategoryConstantServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
