from dotenv import load_dotenv
import os
import json
import requests
from pprint import pprint

load_dotenv()

QUERY_CPU_USAGE = 'sum(rate(container_cpu_usage_seconds_total[1m]))%20by%20(pod)'
QUERY_CPU_LIMIT = 'sum(kube_pod_container_resource_requests{resource="cpu"})%20by%20(pod)'
QUERY_MEMORY_USAGE = 'sum(container_memory_usage_bytes)%20by%20(pod)'
QUERY_MEMORY_LIMIT = 'sum(kube_pod_container_resource_requests{resource="memory"})%20by%20(pod)'
QUERY_STATUS = 'kube_pod_status_phase{pod=~".*"}'

class PromClient:
    def __init__(self):
        self.api_url = os.getenv('PROM_API_URL')
        self.processed_data = {}
    
    
    def execute_query(self, query):
        response = requests.get(self.api_url + query)
        if response.status_code == 200:
            query_result = json.loads(response.text)
            return query_result
        else:
            print(f'Prom query {query} failed with status code {response.status_code}.')
            return None
        
        
    def process_query(self, query, metric_name):
        metrics = self.execute_query(query)
        for metric in metrics['data']['result']:
            pod = metric['metric']['pod']
            value = metric['value'][1]
            if self.processed_data.get(pod, None) == None:
                self.processed_data[pod] = {'cpu_usage': None, 
                                            'cpu_limit': None, 
                                            'memory_usage': None, 
                                            'memory_limit': None, 
                                            'status': None,
                                            'cpu_usage_percentage': None,
                                            'memory_usage_percentage': None}
            
            self.processed_data[pod][metric_name] = value
        
        pprint(self.processed_data)
    
    
    def process_all_queries(self):
        self.process_query(QUERY_CPU_USAGE, 'cpu_usage')
        self.process_query(QUERY_CPU_LIMIT, 'cpu_limit')
        self.process_query(QUERY_MEMORY_USAGE, 'memory_usage')
        self.process_query(QUERY_MEMORY_LIMIT, 'memory_limit')
        self.process_query(QUERY_STATUS, 'status')
    
    
    def get_utilization_percentages(self):
        self.calculate_utilization('cpu_usage', 'cpu_limit', 'cpu_usage_percentage')
        self.calculate_utilization('memory_usage', 'memory_limit', 'memory_usage_percentage')
    
        
    def calculate_utilization(self, metric_usage, metric_limit, metric_usage_percentage_name):
        for pod in self.processed_data:
            if self.processed_data[pod][metric_usage] and self.processed_data[pod][metric_limit]:
                self.processed_data[pod][metric_usage_percentage_name] = round(float(self.processed_data[pod][metric_usage]) / float(self.processed_data[pod][metric_limit]), 2) * 100



if __name__ == '__main__':
    prom_client = PromClient()
    prom_client.process_all_queries()
    prom_client.get_utilization_percentages()
    pprint(prom_client.processed_data)