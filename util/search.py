import faiss


class QueryEngine:
    """
    基于faiss的向量检索引擎

    负责引擎索引训练及维护

    """
    def __init__(self, database, config):
        super(QueryEngine, self).__init__()
        self.__config = config

        self.vector_size = config.embedding_size
        self.cluster_num = config.cluster_num
        self.query_num = config.query_num
        self.distance_pattern = config.distance_pattern

        # 量化器
        self.__quantizer = faiss.IndexFlatL2(config.embedding_size)

        # METRIC_L2计算L2距离, 或faiss.METRIC_INNER_PRODUCT计算内积
        self.__index = faiss.IndexIVFFlat(self.__quantizer, self.vector_size, self.cluster_num, self.distance_pattern)

        # 训练数据集应该与数据库数据集同分布
        self.__index.train(database)

        # 查找类簇的数量
        self.__index.nprobe = config.query_num
        self.__index.add(database)

    @staticmethod
    def indexResult(corpus_dict, I):
        """
        查询接口翻译
        :param corpus_dict: 检索语料库
        :param I: 查询结果索引列表
        :return: 字典检索结果
        """
        result = list()
        for index in I:
            result.append(corpus_dict[index])

        return result

    def query(self, q, k):
        """
        搜索接口
        :param q: 查询向量 q.shape --> (sample_num, embedding_size)
        :param k: topK值
        :return:  返回距离和索引 D, I --> (Distance, Index)

        ::Example
            >>> from config import Config
            >>> config = Config()  # 加载配置

            >>> corpus_handle = CorpusHandle(config)  # 语料库句柄
            >>> embedding_handle = EmbeddingHandle(config)  # 词嵌入句柄
            >>> database = embedding_handle.corpusEmbedding(corpus_handle.corpus)  # 构建检索向量DB
            >>> query_engine = QueryEngine(database, config)  # 构建搜索引擎

            >>> query_string = 'xxx'
            >>> query = embedding_handle.getEmbedding(query_string)  # 查询语句词嵌入
            >>> D, I = query_engine.query(q=query, k=k)
            >>> query_engine.indexResult(corpus_handle.corpus, I)  # 检索结果映射

        """
        return self.__index.search(q, k)