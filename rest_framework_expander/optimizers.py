class ExpanderOptimizer():
    """
    Optimizes querysets for inline expansion.
    """

    def __init__(self, adapter):
        self.adapter = adapter

    def optimize(self):
        return self.adapter.instance
