import networkx as nx
from process import Process, Resource

class DeadlockDetector:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process(self, process):
        self.graph.add_node(process.pid, type='process')

    def add_resource(self, resource):
        self.graph.add_node(resource.rid, type='resource')

    def add_allocation(self, process_id, resource_id):
        """Add allocation edge from resource to process."""
        self.graph.add_edge(resource_id, process_id, type='allocation')

    def add_request(self, process_id, resource_id):
        """Add request edge from process to resource."""
        self.graph.add_edge(process_id, resource_id, type='request')

    def detect_deadlock(self):
        # Debugging: Print graph nodes and edges
        print("Graph Nodes:", self.graph.nodes(data=True))
        print("Graph Edges:", self.graph.edges(data=True))
        
        try:
            # Check for cycles which represent deadlocks
            cycle = nx.find_cycle(self.graph, orientation='original')
            print("Deadlock detected in the following cycle:", cycle)
            return cycle
        except nx.NetworkXNoCycle:
            print("No deadlock detected.")
            return None
