# Stubs for google.ads.google_ads.v2.proto.services.keyword_plan_campaign_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class KeywordPlanCampaignServiceStub:
    GetKeywordPlanCampaign: Any = ...
    MutateKeywordPlanCampaigns: Any = ...
    def __init__(self, channel: Any) -> None: ...

class KeywordPlanCampaignServiceServicer:
    def GetKeywordPlanCampaign(self, request: Any, context: Any) -> None: ...
    def MutateKeywordPlanCampaigns(self, request: Any, context: Any) -> None: ...

def add_KeywordPlanCampaignServiceServicer_to_server(
    servicer: Any, server: Any
) -> None: ...
