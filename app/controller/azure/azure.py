from .api import GET, POST
import base64
from datetime import datetime, timedelta
import concurrent.futures
from urllib.parse import quote

class AzureDevops:
    def __init__(self, pat, org):
        self._pat = pat
        self._org = org
    
    def _get_headers(self, content_type='application/json'):
        return {
                "Accept": content_type,
                "Authorization": "Basic " + base64.b64encode(
                    bytes(":" + self._pat, "ascii")
                ).decode("ascii")
            }
    
    def _get(self, url, content_type='application/json'):
        headers = self._get_headers(content_type)
        return GET(url, headers)

    def projetos(self):
        url = f"https://dev.azure.com/{self._org}/_apis/projects?api-version=7.2-preview.4"
        return self._get(url)['value']
    
    def list_work_items(self, project):
        org = self._org
        project_name = project['name']
        url = f"https://dev.azure.com/{org}/{quote(project_name)}/_apis/wit/wiql?api-version=7.1-preview.2"

        date = datetime.now() - timedelta(days=30)
        formatted_date = date.strftime("%Y-%m-%d")
        
        query = {
            "query": f"""
            Select [System.Id], [System.Title], [System.State], [System.WorkItemType], [Microsoft.VSTS.Common.StateChangeDate], [System.TeamProject], [System.BoardColumn]
            from WorkItems
            WHERE [System.TeamProject] = '{project_name}' AND [Microsoft.VSTS.Common.StateChangeDate] >= '{formatted_date}'
            """}

        response = POST(url, query, self._get_headers())
        return response['workItems']
    
class AzureWorkitems:
    def __init__(self, pat, org):
        self.azure_api = AzureDevops(pat, org)
        
    def _from_azure(self, obj):
        project, wi = obj
        response = self.azure_api._get(wi['url'])

        board = response['fields']['System.BoardColumn'] if 'System.BoardColumn' in response['fields'] else 'SEM'

        data = {
            'Id': wi['id'],
            'Projeto': project['name'],
            'Titulo': response['fields']['System.Title'],
            'Tipo': response['fields']['System.WorkItemType'],
            'Board': board,
            'State': response['fields']['System.State'],
            'Data': response['fields']['System.CreatedDate'],
            'Link': response['_links']['html']['href'],
        }

        return data

    def get_all(self):
        response = []
        projects = self.azure_api.projetos()

        for p in projects:
            list_wi = self.azure_api.list_work_items(p)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                response.extend(executor.map(self._from_azure, zip([p for _ in range(len(list_wi))], list_wi)))

        return response