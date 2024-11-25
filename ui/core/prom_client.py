from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

QUERY_CPU_USAGE = 'sum(rate(container_cpu_usage_seconds_total[1m]))%20by%20(pod)'
QUERY_CPU_LIMIT = 'sum(kube_pod_container_resource_limits%7Bresource%3D"cpu"%7D)%20by%20(pod)'
QUERY_MEMORY_USAGE = 'sum(container_memory_usage_bytes)%20by%20(pod)'
QUERY_MEMORY_LIMIT = 'sum(kube_pod_container_resource_limits%7Bresource%3D"memory"%7D)%20by%20(pod)'
QUERY_STATUS = 'kube_pod_status_phase{pod=~".*"}'

class PromClient:
    def __init__(self):
        self.api_url = os.getenv('PROM_API_URL')
    
    def execute_query(self, query):
        response = requests.get(self.api_url + query)
        if response.status_code == 200:
            query_result = json.loads(response.text)
            return query_result
        else:
            print(f'Prom query {query} failed with status code {response.status_code}.')
            return None

    
    def get_pod_cpu_metrics(self):
        cpu_usage_metrics = self.execute_query(QUERY_CPU_USAGE)
        cpu_limit_metrics = self.execute_query(QUERY_CPU_LIMIT)
        print(cpu_usage_metrics, '\n')
        print(cpu_limit_metrics)
    
    def get_pod_memory_metrics():
        pass
    
    
    def process_hardware_metrics():
        pass
    
    
    def get_pod_status_metrics():
        pass
    
    
    def process_state_metrics():
        pass
    

if __name__ == '__main__':
    prom_client = PromClient()
    prom_client.get_pod_cpu_metrics()