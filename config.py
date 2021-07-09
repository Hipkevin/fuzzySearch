import faiss

class Config:
    def __init__(self):
        super(Config, self).__init__()

        self.embedding_size = 300
        self.cluster_num = 32
        self.query_num = 3
        self.distance_pattern = faiss.METRIC_L2