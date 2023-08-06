# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_responses']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.1']

setup_kwargs = {
    'name': 'async-responses',
    'version': '1.0.0',
    'description': 'aiohttp testing library',
    'long_description': "# Async Responses\n\n[![Documentation Status](https://readthedocs.org/projects/async-responses/badge/?version=latest)](http://async-responses.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/ulamlabs/async-responses/branch/master/graph/badge.svg)](https://codecov.io/gh/ulamlabs/async-responses) ![Python package](https://github.com/ulamlabs/async-responses/workflows/Python%20package/badge.svg) ![Upload Python Package](https://github.com/ulamlabs/async-responses/workflows/Upload%20Python%20Package/badge.svg)\n\nAsync Responses is a library providing an easy way to mock aiohttp responses inspired by [aioresponses](https://github.com/pnuckowski/aioresponses).\n\n## Installation\n\nLibrary is available on PyPi, you can simply install it using `pip`.\n\n```shell\n$ pip install async-responses\n```\n\n## Usage\n### As an instance\n```python\nar = AsyncResponses()\nar.get(...)\n```\n\n### As a context manager\n```python\nwith AsyncResponses() as ar:\n    ar.get(...)\n```\n\n### With dict as handler\nPassing dict as `handler` argument to async-responses would result in it being\nreturned as a JSON payload.\n\n```python\nimport aiohttp\nfrom async_responses import AsyncResponses\n\n\nasync def test_response():\n    ar = AsyncResponses()\n    payload = {'status': 'ok'}\n    ar.get('http://mock.url', '/v1/status', handler=payload)\n    async with aiohttp.ClientSession() as session:\n        response = await session.get('http://mock.url/v1/status')\n        assert await response.json() == payload\n```\n\n### With exception as handler\nCalling Async Responses with an exception as `handler` argument would result in\nit being raised.\n\n```python\nimport aiohttp\nfrom async_responses import AsyncResponses\nimport pytest\n\n\nasync def test_response():\n    ar = AsyncResponses()\n    ar.get('http://mock.url', '/v1/status', handler=ZeroDivisionError)\n    with pytest.raises(ZeroDivisionError):\n        async with aiohttp.ClientSession() as session:\n            await session.get('http://mock.url/v1/status')\n```\n\n### With string as handler\n```python\nimport aiohttp\nfrom async_responses import AsyncResponses\n\nasync def test_response():\n    ar = AsyncResponses()\n    payload = 'ok'\n    ar.get('http://mock.url', '/v1/status', handler=payload)\n    async with aiohttp.ClientSession() as session:\n        response = await session.get('http://mock.url/v1/status')\n        assert await response.text() == payload\n```\n\n### With callable as handler\n```python\nimport aiohttp\nfrom async_responses import AsyncResponses\n\n\nasync def test_response():\n    def handler(data, **kwargs):\n        return {'status': 'ok'}\n\n    ar = AsyncResponses()\n    ar.get('http://mock.url', '/v1/status', handler=payload)\n    async with aiohttp.ClientSession() as session:\n        response = await session.get('http://mock.url/v1/status')\n        assert await response.json() == {'status': 'ok'}\n```\n\n### With a custom status code\n```python\nimport aiohttp\nfrom async_responses import AsyncResponses\n\n\nasync def test_response():\n    payload = {'status': 'not good'}\n    ar = AsyncResponses()\n    ar.get('http://mock.url', '/v1/status', handler=payload, status=500)\n    async with aiohttp.ClientSession() as session:\n        response = await session.get('http://mock.url/v1/status')\n        assert response.status == 500\n        assert await response.json() == payload\n```\n\n### With a custom response class\nasync-responses will make use of a response class passed as an argument to \nClientSession, so you can use things like custom JSON serializer.\n\n```python\nimport aiohttp\n\nasync def test_response():\n    class CustomResponse(aiohttp.ClientResponse):\n        async def json(self, *args, **kwargs):\n            return {'hello': 'world'}\n\n    ar = AsyncResponses()\n    ar.get('http://mock.url', '/v1/status', handler='')\n    async with aiohttp.ClientSession(response_class=CustomResponse) as session:\n        response = await session.get('http://mock.url/v1/status')\n        assert await response.json() == {'hello': 'world'}\n        assert isinstance(response, CustomResponse)\n```\n",
    'author': 'Sławomir Górawski',
    'author_email': 'slawomir@ulam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ulam.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
