# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_rabbitmqmon', 'jetblack_rabbitmqmon.clients']

package_data = \
{'': ['*']}

extras_require = \
{'aiohttp': ['aiohttp>=3.6.2,<4.0.0'],
 'bareclient': ['bareclient>=4.0.1,<5.0.0']}

setup_kwargs = {
    'name': 'jetblack-rabbitmqmon',
    'version': '2.0.0',
    'description': 'RabbitMQ Monitor',
    'long_description': "# jetblack-rabbitmqmon\n\nThis is an asyncio RabbitMQ monitor API.\n\nIt wraps the RabbitMQ management plugin REST api. This allows retrieving\nmetrics and peeking into the queues.\n\n## Status\n\nThis is work in progress, but is functional.\n\n## Installation\n\nThis can be installed with pip.\n\nMultiple clients a supported and one *must* be selected. Choose one of:\n\n* [aiohttp](https://github.com/aio-libs/aiohttp)\n* [bareclient](https://github.com/rob-blackbourn/bareClient)\n\n```bash\npip install jetblack-rabbitmqmon[bareclient]\n```\n\nOr alternatively:\n\n```bash\npip install jetblack-rabbitmqmon[aiohttp]\n```\n\n\n## Usage\n\nThe following gets an overview using the bareclient.\n\n```python\nimport asyncio\nfrom jetblack_rabbitmqmon.monitor import Monitor\nfrom jetblack_rabbitmqmon.clients.bareclient_requester import BareRequester\n\nasync def main_async():\n    mon = Monitor(\n        BareRequester(\n            'http://mq.example.com:15672',\n            'admin',\n            'admins password'\n        )\n    )\n\n    overview = await mon.overview()\n    print(overview)\n\nif __name__ == '__main__':\n    asyncio.run(main_async())\n```\n\nThe follow explores a vhost.\n\n```python\nimport asyncio\nfrom jetblack_rabbitmqmon.monitor import Monitor\nfrom jetblack_rabbitmqmon.clients.aiohttp_requester import AioHttpRequester\n\nasync def main_async():\n    mon = Monitor(\n        AioHttpRequester(\n            'http://mq.example.com:15672',\n            'admin',\n            'admins password'\n        )\n    )\n\n    vhosts = await mon.vhosts()\n    for vhost in vhosts.values(): # vhost is a dict\n      exchanges = await vhost.exchanges()\n      for exchange in exchanges.values(): # exchanges is a dict\n          print(exchange)\n          # Objects can be refreshed to gather new metrics.\n          await exchange.refresh()\n          print(exchange)\n          bindings = await exchange.bindings()\n          for binding in bindings:\n              print(binding)\n\nif __name__ == '__main__':\n    asyncio.run(main_async())\n```\n\nThe following gets some messages from an exchange:\n\n```python\nimport asyncio\nfrom jetblack_rabbitmqmon.monitor import Monitor\nfrom jetblack_rabbitmqmon.clients.bareclient_requester import BareRequester\n\nasync def main_async():\n    mon = Monitor(\n        BareRequester(\n            'http://mq.example.com:15672',\n            'admin',\n            'admins password'\n        )\n    )\n\n    vhosts = await mon.vhosts()\n    vhost = vhosts['/some-vhost']\n    queues = await vhost.queues()\n    queue = queues['some.queue']\n    messages = await queue.get_messages()\n    print(messages)\n\nif __name__ == '__main__':\n    asyncio.run(main_async())\n```\n\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-rabbitmqmon',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
