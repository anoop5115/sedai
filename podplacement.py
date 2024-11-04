
import requests
import client
import config


def get_pod_placement():
    config.load_kube_config()  # Adjust for in-cluster setup with load_incluster_config()
    v1 = client.CoreV1Api()
    pod_placement = []

    pods = v1.list_pod_for_all_namespaces(watch=False)
    for pod in pods.items:
        pod_info = {
            "pod_name": pod.metadata.name,
            "node_name": pod.spec.node_name
        }
        pod_placement.append(pod_info)

    return pod_placement


# Example usage
if name == "main":
    pod_placement = get_pod_placement()
    for pod in pod_placement:
        print(pod)


PROMETHEUS = "http://<your-prometheus-server>:9090"


def query_prometheus(query):
    response = requests.get(
        f"{PROMETHEUS}/api/v1/query", params={"query": query})
    return response.json()["data"]["result"]


def get_node_stats():
    cpu_usage_query = 'avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)'
    memory_usage_query = 'node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes'

    cpu_usage = query_prometheus(cpu_usage_query)
    memory_usage = query_prometheus(memory_usage_query)

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage
    }


# Example usage
if name == "main":
    node_stats = get_node_stats()
    print(node_stats)
# Code for api-pod-stats
# This fetches CPU and memory stats for individual pods.


def get_pod_stats():
    cpu_usage_query = 'sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)'
    memory_usage_query = 'sum(container_memory_usage_bytes) by (pod)'

    cpu_usage = query_prometheus(cpu_usage_query)
    memory_usage = query_prometheus(memory_usage_query)

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage
    }
