# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anymotion_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'anymotion-sdk',
    'version': '1.0.0',
    'description': 'AnyMotion SDK for Python',
    'long_description': '# AnyMotion Python SDK\n\n[![CircleCI][ci-status]][ci] [![codecov][codecov-status]][codecov]\n\nAnyMotion SDK for Python.\n\n## Installation\n\nInstall using [pip](https://pip.pypa.io/en/stable/quickstart/):\n\n```sh\n$ pip install anymotion-sdk\n```\n\n## Usage\n\nSet the client id and client secret issued by the [AnyMotion Portal](https://portal.anymotion.jp/).\n\n```py\nfrom anymotion_sdk import Client\n\n# Setup client\nclient = Client(client_id="your_client_id", client_secret="your_client_secret")\n\n# Upload image file\nupload_result = client.upload("image.jpg")\n\n# Extract keypoint\nkeypoint_id = client.extract_keypoint(image_id=upload_result.image_id)\nextraction_result = client.wait_for_extraction(keypoint_id)\n\n# Get keypoint data from result\nkeypoint = extraction_result.json\n\n# Get keypoint data from keypoint_id\nkeypoint = client.get_keypoint(keypoint_id)\n```\n\n## Change Log\n\nSee [CHANGELOG.md](CHANGELOG.md).\n\n[ci]: https://circleci.com/gh/nttpc/anymotion-python-sdk\n[ci-status]: https://circleci.com/gh/nttpc/anymotion-python-sdk/tree/master.svg?style=shield&circle-token=b9824650553efb30dabe07e3ab2b140ae2efa60c\n[codecov]: https://codecov.io/gh/nttpc/anymotion-python-sdk\n[codecov-status]: https://codecov.io/gh/nttpc/anymotion-python-sdk/branch/master/graph/badge.svg?token=5QG7KUBZ7K\n',
    'author': 'Yusuke Kumihashi',
    'author_email': 'y_kumiha@nttpc.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nttpc/anymotion-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
