from orkg.utils import NamespacedClient, dict_to_url_params
from orkg.out import OrkgResponse
from typing import List
import pandas as pd


class ContributionsClient(NamespacedClient):

    def simcomp_available(func):
        def check_if_simcomp_available(self, *args, **kwargs):
            if not self.client.simcomp_available:
                raise ValueError("simcomp_host must be provided in the ORKG wrapper class!")
            return func(self, *args, **kwargs)

        return check_if_simcomp_available

    @simcomp_available
    def similar(self, cont_id: str) -> OrkgResponse:
        self.client.simcomp._append_slash = True
        response = self.client.simcomp.similar(cont_id).GET()
        return OrkgResponse(response=response)

    @simcomp_available
    def compare(self, contributions: List[str]) -> OrkgResponse:
        self.client.simcomp._append_slash = False
        params = f'?contributions={",".join(contributions)}'
        response = self.client.simcomp.compare.GET(params)
        return OrkgResponse(response=response)

    def compare_dataframe(self, contributions: List[str]) -> pd.DataFrame:
        response = self.compare(contributions)
        if not response.succeeded:
            return pd.DataFrame()
        content = response.content
        contributions_list = content['contributions']
        columns = [f"{contribution['title']}/{contribution['contributionLabel']}" for contribution in contributions_list]
        properties_list = content['properties']
        property_lookup = {prop['id']: prop['label'] for prop in properties_list}
        # create table view of the data
        data = content['data']
        indices = []
        rows = []
        for prop_id, values in data.items():
            indices.append(property_lookup[prop_id])
            row = []
            for index, value in enumerate(values):
                if not value[0]:
                    row.append('')
                else:
                    row.append('/'.join([v['label'] for v in value]))
            rows.append(row)
        # create dataframe from peaces
        df = pd.DataFrame(rows, columns=columns, index=indices)
        return df
