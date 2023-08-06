
import os
import requests
import pandas as pd
import snowflake.connector

from pyrasgo.feature_list import FeatureList

class RasgoConnection(object):

    def __init__(self, api_key):
        self._api_key = api_key
        self._hostname = os.environ.get("RAGSO_DOMAIN", "rasgo-api-prod.herokuapp.com")

    def get_lists(self):
        response = self._request("/features/lists/")
        response.raise_for_status()
        lists = response.json()['data']
        return [FeatureList(entry) for entry in lists]

    def get_feature_list(self, list_id):
        response = self._request("/features/lists/{}".format(list_id))
        response.raise_for_status()
        entry = response.json()['data']
        return FeatureList(entry)

    def get_feature_data(self, feature_list_id):
        feature_list = self.get_feature_list(feature_list_id)
        
        conn = self._snowflake_connection(feature_list.author())
        
        table_metadata = feature_list.snowflake_table_metadata()
        query = self._make_select_statement(table_metadata)
        result_set = self._run_query(conn, query)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    def _run_query(self, conn, query):
        cursor = conn.cursor().execute(query)
        return cursor

    def _make_select_statement(self, table_metadata):
        return "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
    
    def _snowflake_connection(self, member):
        creds = member.snowflake_creds()
        conn = snowflake.connector.connect(**creds)
        return conn

    def _request(self, resource):
        return requests.get(self._url(resource), headers=self._headers())

    def _headers(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % self._api_key,
            }
        return headers
    
    def _url(self, resource):
        return f'https://{self._hostname}/api/v1{resource}'
