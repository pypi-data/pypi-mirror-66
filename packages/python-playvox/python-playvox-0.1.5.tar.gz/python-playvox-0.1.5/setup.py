# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_playvox']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'python-playvox',
    'version': '0.1.5',
    'description': 'A Python wrapper for the Playvox REST API.',
    'long_description': "# python-playvox\n\npython-playvox is a simple API wrapper for the Playvox REST API.\n\nDocumentation for the Playvox API can be found [here.](https://developers.playvox.com/restapis/#/introduction/api-reference)\n\nPlease note, this wrapper is in beta. There has been no testing and documentation is a work in progress.\n\n## Usage\n\n### Playvox Instantiation\nTo instantiate the API wrapper you will need the subdomain for your your API uid and your API key.\n\n```python\nfrom python-playvox import Playvox\n\nsubdomain = 'mysubdomain'\nuid = 'my-playvox-uid'\nkey = 'my-playvox-key'\n\npv = Playvox(subdomain, uid, key)\n```\n\nThis will create an instance of the wrapper that makes calls to 'https://mysubdomain.playvox.com/api/v1/' and authenticates with your playvox uid and key.\n\n### Methods\n\n#### Playvox.get_coachings(**kwargs)\n\nGets all coachings that meet the specified parameters.\n\nAcceptable Keyword Arguments\n\n|argument|type|description|\n|---|---|---|\n|include|string|use `include='all'` to include all coaching related objects information|\n|page|int|number of page for data pagination|\n|per_page|int|number of resources per page for data pagination, max: 100, default: 12|\n|query|string|JSON specifying resource filters|\n|fields|string|comma separated list of fields to be returned|\n|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|\n\n---\n\n#### Playvox.get_learning_sessions(**kwargs)\n\nGets all learning sessions that meet the specified parameters.\n\nAcceptable Keyword Arguments\n\n|argument|type|description|\n|---|---|---|\n|include|string|use `include='all'` to include all coaching related objects information|\n|page|int|number of page for data pagination|\n|per_page|int|number of resources per page for data pagination, max: 100, default: 12|\n|query|string|JSON specifying resource filters|\n|fields|string|comma separated list of fields to be returned|\n|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|\n\n---\n\n#### Playvox.get_campaigns(**kwargs)\n\nGets all learning sessions that meet the specified parameters.\n\nAcceptable Keyword Arguments\n\n|argument|type|description|\n|---|---|---|\n|include|string|use `include='all'` to include all coaching related objects information|\n|page|int|number of page for data pagination|\n|per_page|int|number of resources per page for data pagination, max: 100, default: 12|\n|query|string|JSON specifying resource filters|\n|fields|string|comma separated list of fields to be returned|\n|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|\n\n---\n\n#### Playvox.get_campaign(campaign_id)\n\nGets the specified campaign.\n\ncampaign_id should be of type string\n\n---\n\n#### Playvox.get_campaign_vars(campaign_id)\n\nGets the variables for the specified campaign.\n\ncampaign_id should be of type string.\n\n#### Playvox.get_campaign_users(campaign_id)\n\nGets the users for the specified campaign.\n\ncampaign_id should be of type string.\n\n---\n\n#### Playvox.send_campaign_data(campaign_id, campaign_data)\n\nAdds the specified data to the specified campaign.\n\ncampaign_id should be of type string.\ncampaign_data should be of type dict.\n\n---\n\n#### Playvox.get_calibrations(**kwargs)\n\nGets all calibrations that meet the specified parameters.",
    'author': 'Moses Wynn',
    'author_email': 'mail@moseswynn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.moseswynn.com/moseswynn/python-playvox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
