# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google-stubs']

package_data = \
{'': ['*'],
 'google-stubs': ['ads/*',
                  'ads/google_ads/*',
                  'ads/google_ads/interceptors/*',
                  'ads/google_ads/v1/*',
                  'ads/google_ads/v1/proto/*',
                  'ads/google_ads/v1/proto/common/*',
                  'ads/google_ads/v1/proto/enums/*',
                  'ads/google_ads/v1/proto/errors/*',
                  'ads/google_ads/v1/proto/resources/*',
                  'ads/google_ads/v1/proto/services/*',
                  'ads/google_ads/v1/services/*',
                  'ads/google_ads/v1/services/transports/*',
                  'ads/google_ads/v2/*',
                  'ads/google_ads/v2/proto/*',
                  'ads/google_ads/v2/proto/common/*',
                  'ads/google_ads/v2/proto/enums/*',
                  'ads/google_ads/v2/proto/errors/*',
                  'ads/google_ads/v2/proto/resources/*',
                  'ads/google_ads/v2/proto/services/*',
                  'ads/google_ads/v2/services/*',
                  'ads/google_ads/v2/services/transports/*',
                  'ads/google_ads/v3/*',
                  'ads/google_ads/v3/proto/*',
                  'ads/google_ads/v3/proto/common/*',
                  'ads/google_ads/v3/proto/enums/*',
                  'ads/google_ads/v3/proto/errors/*',
                  'ads/google_ads/v3/proto/resources/*',
                  'ads/google_ads/v3/proto/services/*',
                  'ads/google_ads/v3/services/*',
                  'ads/google_ads/v3/services/transports/*']}

install_requires = \
['google-ads>=5.0.3,<6.0.0',
 'googleapis-common-protos-stubs>=1.0,<2.0',
 'typing-extensions>=3.7,<4.0',
 'typing>=3.7,<4.0']

setup_kwargs = {
    'name': 'google-ads-stubs',
    'version': '3.0.1',
    'description': 'Type stubs for google-ads',
    'long_description': "# Type stubs for the Google Ads API Client Library for Python\n[![PyPI version](https://badge.fury.io/py/google-ads-stubs.svg)](https://badge.fury.io/py/google-ads-stubs)\n\nThis package provides type stubs for the [Google Ads API Client Library for Python](https://github.com/googleads/google-ads-python). It's currently compatible with v.5.0.3 of this library. It allows you to type check usage of the library with e.g. [mypy](http://mypy-lang.org/) and will also improve autocomplete in many editors.\n\n**This is in no way affiliated with Google.**\n\nThe stubs for protobuf messages were created by [mypy-protobuf](https://github.com/dropbox/mypy-protobuf).\nThe rest were created either by hand or by self-made scripts, with the output of MyPy's `stubgen` as\na starting point.\n\nIf you find incorrect annotations, please create an issue. Contributions for fixes are also welcome.\n\n## Installation\n```\n$ pip install google-ads-stubs\n```\n\n## Caveats\n\nThere are some caveats. The primary one is that type inference does *not* work for the `get_type` and `get_service`\nmethods of `Client`. The workaround is to explicitly state the type. For `get_type` you can also instantiate \nthe object directly.\n\n```python\n# Replace this:\ncampaign_operation = client.get_type('CampaignOperation')\n# With this:\nfrom google.ads.google_ads.v3.types import CampaignOperation\ncampaign_operation: CampaignOperation = client.get_type('CampaignOperation')\n# Or this:\nfrom google.ads.google_ads.v3.types import CampaignOperation\ncampaign_operation = CampaignOperation()\n\n# Replace this:\ngoogle_ads_service = client.get_service('GoogleAdsService')\n# With this:\nfrom google.ads.google_ads.v3.services import GoogleAdsServiceClient\ngoogle_ads_service: GoogleAdsServiceClient = client.get_service('GoogleAdsService')\n```\n\nWhile it is technically possible to type these methods using a combination of overloading and literal types,\nthis is not included in these stubs. The reason is that it requires about 10,000 overloads, which, while simple\nto generate, slows type checking to a crawl.\n\nThis package does not provide complete type annotations, although it should cover what's used by most developers. \nThe bare output from `stubgen` is used by the service stubs and transport classes.\nThe service stubs are unlikely to be typed as long as there is no `mypy-protobuf` equivalent\nfor GRPC stubs. The transport classes may be typed in the future if there is a need for it.\n\nSome service methods allow you to pass in either a protobuf message or a dictionary for certain arguments.\nThere is no check that the dictionary conforms to the message structure, as this would require a `TypedDict` subclass\nfor each message. \n",
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/google-ads-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
