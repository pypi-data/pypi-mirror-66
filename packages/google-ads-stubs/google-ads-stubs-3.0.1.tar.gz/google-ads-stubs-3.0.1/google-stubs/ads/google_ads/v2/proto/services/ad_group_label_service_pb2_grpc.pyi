# Stubs for google.ads.google_ads.v2.proto.services.ad_group_label_service_pb2_grpc (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

class AdGroupLabelServiceStub:
    GetAdGroupLabel: Any = ...
    MutateAdGroupLabels: Any = ...
    def __init__(self, channel: Any) -> None: ...

class AdGroupLabelServiceServicer:
    def GetAdGroupLabel(self, request: Any, context: Any) -> None: ...
    def MutateAdGroupLabels(self, request: Any, context: Any) -> None: ...

def add_AdGroupLabelServiceServicer_to_server(servicer: Any, server: Any) -> None: ...
