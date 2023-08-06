import requests


class Playvox:
    def __init__(self, pv_subdomain, uid, key):
        self.auth = (uid, key)
        self.url = 'https://{}.playvox.com/api/v1/'.format(pv_subdomain)
        self.ui_api_url = 'https://{}.playvox.com/v1/'.format(pv_subdomain)

    def make_request(self, method='GET', endpoint=None, data=None):
        if method == 'GET':
            return requests.get(self.url+endpoint, auth=self.auth).json()
        elif method == 'POST':
            return requests.post(self.url+endpoint, data=data, auth=self.auth).json()
        elif method == 'PUT':
            return requests.put(self.url+endpoint, data=data, auth=self.auth).json()
        elif method == 'DELETE':
            return requests.delete(self.url+endpoint).json()
        else:
            error_message = "{} is not a valid request method.".format(method)
            raise ValueError(error_message)
    
    def make_ui_api_request(self, method='GET', endpoint=None, data=None):
        if method == 'GET':
            return requests.get(self.ui_api_url+endpoint, auth=self.auth, data=None).json()
        elif method == 'POST':
            return requests.post(self.ui_api_url+endpoint, data=data, auth=self.auth).json()
        elif method == 'PUT':
            return requests.put(self.ui_api_url+endpoint, data=data, auth=self.auth).json()
        elif method == 'DELETE':
            return requests.delete(self.ui_api_url+endpoint).json()
        else:
            error_message = "{} is not a valid request method.".format(method)
            raise ValueError(error_message)

    def make_querystring(self, parameters):
        querystring = '?'
        for k, v in parameters.items():
            querystring += k+'='+str(v)+'&'
        return querystring

    def get_coachings(self, **kwargs):
        endpoint = 'coachings'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_learning_sessions(self, **kwargs):
        endpoint = 'learning-results'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_campaigns(self, **kwargs):
        endpoint = 'campaigns'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        print(endpoint)
        return self.make_request(endpoint=endpoint)

    def get_campaign(self, campaign_id):
        endpoint = 'campaigns/{}'.format(campaign_id)
        return self.make_request(endpoint=endpoint)

    def get_campaign_vars(self, campaign_id):
        endpoint = 'campaigns/{}/actions?o=vars-by-type'.format(campaign_id)
        return self.make_request(endpoint=endpoint)

    def get_campaign_users(self, campaign_id):
        endpoint = 'campaigns/{}/actions?o=users'.format(campaign_id)
        return self.make_request(endpoint=endpoint)

    def send_campaign_data(self, campaign_id, campaign_data):
        endpoint = 'campaigns/{}/metrics'.format(campaign_id)
        return self.make_request(method='POST', endpoint=endpoint, data=campaign_data)

    def get_calibrations(self, **kwargs):
        endpoint = 'calibrations'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_evaluations(self, **kwargs):
        endpoint = 'evaluations'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_scorecards(self, **kwargs):
        endpoint = 'scorecards'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_teams(self, **kwargs):
        endpoint = 'teams'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def create_new_team(self, team_dict):
        endpoint = 'teams'
        return self.make_request(method='POST', endpoint=endpoint, data=team_dict)

    def update_team(self, team_id, team_dict):
        endpoint = 'teams/{}'.format(team_id)
        return self.make_request(method='POST', endpoint=endpoint, data=team_dict)

    def add_team_user(self, team_id, user_id):
        endpoint = 'teams/{}/users'
        data = {
            "id": user_id
        }
        return self.make_request(method='POST', endpoint=endpoint, data=data)

    def remove_team_user(self, team_id, user_id):
        endpoint = 'teams/{}/users/{}'.format(team_id, user_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def delete_team(self, team_id):
        endpoint = 'teams/{}'.format(team_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def get_users(self, **kwargs):
        endpoint = 'users'
        if len(kwargs) > 0:
            endpoint+=(self.make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def create_user(self, user_dict):
        endpoint = 'users'
        return self.make_request(method='POST', endpoint=endpoint, data=user_dict)

    def update_user(self, user_id, user_dict):
        endpoint = 'users/{}'.format(user_id)
        return self.make_request(method='POST', endpoint=endpoint, data=user_dict)

    def deactivate_user(self, user_id, user_dict):
        endpoint = 'users/{}'.format(user_id)
        return self.make_request(method='POST', endpoint=endpoint, data=user_dict)

    def activate_user(self, user_id):
        endpoint = 'users/{}'.format(user_id)
        data = {
            "status": "active",
            "deactivation_type": "",
            "deactivation_reason": ""
        }
        return self.make_request(method='POST', endpoint=endpoint, data=data)

    def get_roles(self, **kwargs):
        endpoint = 'roles'
        if len(kwargs) > 0:
            endpoint+=(make_querystring(kwargs))
        return self.make_request(endpoint=endpoint)

    def get_integrations(self):
        endpoint = 'integrations'
        return self.make_request(endpoint=endpoint)

    def create_integration(self, integration_dict):
        endpoint = 'integrations'
        return self.make_request(method='POST', endpoint=endpoint, data=integration_dict)

    def update_integration(self, integration_id, integration_dict):
        endpoint = 'integrations/{}'.format(integration_id)
        return self.make_request(method='PUT', endpoint=endpoint, data=integration_dict)

    def delete_integration(self, integration_id):
        endpoint = 'integrations/{}'.format(integration_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def add_integration_metadata(self, integration_id, metadata_dict):
        endpoint = 'integrations/{}/metadata'.format(integration_id)
        return self.make_request(method='POST', endpoint=endpoint, data=metadata_dict)

    def update_integration_metadata(self, integration_id, metadata_id, metadata_dict):
        endpoint = 'integrations/{}/metadata/{}'.format(
            integration_id, metadata_id)
        return self.make_request(method='PUT', endpoint=endpoint, data=metadata_dict)

    def delete_integration_metadata(self, integration_id, metadata_id):
        endpoint = 'integrations/{}/metadata/{}'.format(
            integration_id, metadata_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def get_integration_interactions(self, integration_id):
        endpoint = 'integrations/{}/interactions'.format(integration_id)
        return self.make_request(endpoint=endpoint)

    def add_integration_interaction(self, integration_id, interaction_dict):
        endpoint = 'integrations/{}/interactions'.format(integration_id)
        return self.make_request(method='POST', endpoint=endpoint, data=interaction_dict)

    def update_integration_interaction(self, integration_id, interaction_id, interaction_dict):
        endpoint = 'integrations/{}/interactions/{}'.format(
            integration_id, interaction_id)
        return self.make_request(method='PUT', endpoint=endpoint, data=interaction_dict)

    def delete_integration_interaction(self, integration_id, interaction_id):
        endpoint = 'integrations/{}/interactions/{}'.format(
            integration_id, interaction_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def get_interaction_comments(self, interaction_id):
        endpoint = 'interactions/{}/comments'.format(interaction_id)
        return self.make_request(endpoint=endpoint)

    def add_interaction_comment(self, interaction_id, comment_dict):
        endpoint = 'interactions/{}/comments'.format(interaction_id)
        return self.make_request(method='POST', endpoint=endpoint, data=comment_dict)

    def update_interaction_comment(self, interaction_id, comment_id, comment_dict):
        endpoint = 'interactions/{}/comments/{}'.format(
            interaction_id, comment_id)
        return self.make_request(method='PUT', endpoint=endpoint, data=comment_dict)

    def delete_interaction_comment(self, interaction_id, comment_id):
        endpoint = 'interactions/{}/comments/{}'.format(
            interaction_id, comment_id)
        return self.make_request(method='DELETE', endpoint=endpoint)

    def create_bulk_interactions(self, integration_id, bulk_interactions_dict):
        endpoint = 'integrations/{}/bulk/interactions'.format(integration_id)
        return self.make_request(method='POST', endpoint=endpoint, data=bulk_interactions_dict)

    def get_bulk_job(self, job_id):
        endpoint = 'jobs/{}'.format(job_id)
        return self.make_request(endpoint=endpoint)
