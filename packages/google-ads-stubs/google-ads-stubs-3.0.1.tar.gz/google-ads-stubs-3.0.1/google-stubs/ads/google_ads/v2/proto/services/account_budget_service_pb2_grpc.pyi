# Stubs for google.ads.google_ads.v2.proto.services.account_budget_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class AccountBudgetServiceStub:
    GetAccountBudget: Any = ...
    def __init__(self, channel: Any) -> None: ...

class AccountBudgetServiceServicer:
    def GetAccountBudget(self, request: Any, context: Any) -> None: ...

def add_AccountBudgetServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
