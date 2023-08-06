# python-playvox

python-playvox is a simple API wrapper for the Playvox REST API.

Documentation for the Playvox API can be found [here.](https://developers.playvox.com/restapis/#/introduction/api-reference)

Please note, this wrapper is in beta. There has been no testing and documentation is a work in progress.

## Usage

### Playvox Instantiation
To instantiate the API wrapper you will need the subdomain for your your API uid and your API key.

```python
from python-playvox import Playvox

subdomain = 'mysubdomain'
uid = 'my-playvox-uid'
key = 'my-playvox-key'

pv = Playvox(subdomain, uid, key)
```

This will create an instance of the wrapper that makes calls to 'https://mysubdomain.playvox.com/api/v1/' and authenticates with your playvox uid and key.

### Methods

#### Playvox.get_coachings(**kwargs)

Gets all coachings that meet the specified parameters.

Acceptable Keyword Arguments

|argument|type|description|
|---|---|---|
|include|string|use `include='all'` to include all coaching related objects information|
|page|int|number of page for data pagination|
|per_page|int|number of resources per page for data pagination, max: 100, default: 12|
|query|string|JSON specifying resource filters|
|fields|string|comma separated list of fields to be returned|
|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|

---

#### Playvox.get_learning_sessions(**kwargs)

Gets all learning sessions that meet the specified parameters.

Acceptable Keyword Arguments

|argument|type|description|
|---|---|---|
|include|string|use `include='all'` to include all coaching related objects information|
|page|int|number of page for data pagination|
|per_page|int|number of resources per page for data pagination, max: 100, default: 12|
|query|string|JSON specifying resource filters|
|fields|string|comma separated list of fields to be returned|
|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|

---

#### Playvox.get_campaigns(**kwargs)

Gets all learning sessions that meet the specified parameters.

Acceptable Keyword Arguments

|argument|type|description|
|---|---|---|
|include|string|use `include='all'` to include all coaching related objects information|
|page|int|number of page for data pagination|
|per_page|int|number of resources per page for data pagination, max: 100, default: 12|
|query|string|JSON specifying resource filters|
|fields|string|comma separated list of fields to be returned|
|sort|string|sort attributes separated by commas, use '+' as a prefix for ASC sorting and '-' for DESC sorting|

---

#### Playvox.get_campaign(campaign_id)

Gets the specified campaign.

campaign_id should be of type string

---

#### Playvox.get_campaign_vars(campaign_id)

Gets the variables for the specified campaign.

campaign_id should be of type string.

#### Playvox.get_campaign_users(campaign_id)

Gets the users for the specified campaign.

campaign_id should be of type string.

---

#### Playvox.send_campaign_data(campaign_id, campaign_data)

Adds the specified data to the specified campaign.

campaign_id should be of type string.
campaign_data should be of type dict.

---

#### Playvox.get_calibrations(**kwargs)

Gets all calibrations that meet the specified parameters.