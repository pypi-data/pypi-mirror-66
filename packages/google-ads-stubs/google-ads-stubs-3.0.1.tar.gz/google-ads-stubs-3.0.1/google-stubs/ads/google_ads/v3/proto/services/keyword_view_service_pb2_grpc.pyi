from typing import Any

class KeywordViewServiceStub:
    GetKeywordView: Any = ...
    def __init__(self, channel: Any) -> None: ...

class KeywordViewServiceServicer:
    def GetKeywordView(self, request: Any, context: Any) -> None: ...

def add_KeywordViewServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
