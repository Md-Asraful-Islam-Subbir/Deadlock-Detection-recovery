class Process:
    def __init__(self, pid, allocated_resources, max_resources):
        self.pid = pid
        self.allocated_resources = allocated_resources
        self.max_resources = max_resources

class Resource:
    def __init__(self, rid, total, available):
        self.rid = rid
        self.total = total
        self.available = available
