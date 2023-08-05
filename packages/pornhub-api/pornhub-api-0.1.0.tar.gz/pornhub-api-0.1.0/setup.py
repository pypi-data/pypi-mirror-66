# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pornhub_api',
 'pornhub_api.backends',
 'pornhub_api.modules',
 'pornhub_api.schemas']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['pydantic>=1.4,<2.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pornhub-api',
    'version': '0.1.0',
    'description': '',
    'long_description': '===============================\nUnofficial api for pornhub.com\n===============================\n\nKey Features\n============\n- response are fully-annotated with pydantic_\n- rest without parsing\n\n.. _pydantic: https://pydantic-docs.helpmanual.io/\n\nGetting started\n===============\nInitiate Api client\n___________________\n.. code-block:: python\n\n    from pornhub_api import PornhubApi\n\n    api = PornhubApi()\n\n\nSearch Videos\n_____________\n.. code-block:: python\n\n    data = api.search(\n        "chechick",\n        ordering="mostviewed",\n        period="weekly",\n        tags=["black"],\n    )\n    for vid in data.videos:\n        print(vid.title, vid.video_id)\n\nGet Stars\n___________\n.. code-block:: python\n\n    api.stars.all()\n    or\n    api.stats.all_detailed()\n\n\n\nGet single Video details\n________________________\n.. code-block:: python\n\n   video = api.video.get_by_id("ph560b93077ddae")\n   print(video.title)\n\n\nGet all videos tags or categories\n_________________________________\n.. code-block:: python\n\n   categories = api.video.categories()\n   tags = api.video.tags("a")\n\n\nCheck Video availability\n_________________________\n.. code-block:: python\n\n   active = api.video.is_active("ph560b93077ddae")\n\n\nSearch video by random tag and category\n_______________________________________\n.. code-block:: python\n\n\n    import random\n    api = PornhubApi()\n\n    tags = random.sample(api.video.tags("f").tags, 5)\n    category = random.choice(api.video.categories().categories)\n    result = api.search.search(ordering="mostviewed", tags=tags, category=category)\n\n    print(result.size())\n    for vid in result.videos:\n        print(vid.title, vid.url)\n',
    'author': 'Andrew Grinevich',
    'author_email': 'beule@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Derfirm/pornhub_api',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
