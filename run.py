import pandas as pd
import numpy as np
import Levenshtein

from tqdm import tqdm
from config import Config
from util.search import QueryEngine
from util.dataTool import getEpub, getEnterprise, loadEmbeddingModel, getVector

if __name__ == '__main__':
    config = Config()

    # 提取数据
    print('Data loading...')
    idx2data = getEpub('data/epub.txt')
    idx2text, text2idx = getEnterprise('data/enterprise.xlsx')

    embedding = loadEmbeddingModel('data/slim_embedding.bin')

    # 查询向量集合
    query_list = list()
    for i in range(len(idx2data)):
        text = str(idx2data[i][2])

        query_list.append(getVector(text, embedding))

    # 向量检索库
    print('Engine loading...')
    database = list()
    for i in range(len(idx2text)):
        text = str(idx2text[i]['text'])

        database.append(getVector(text, embedding))

    database = np.asarray(database).astype('float32')
    engine = QueryEngine(database, config)

    print('Matching...')
    result = list()
    for i in tqdm(range(len(query_list))):
        query = query_list[i][np.newaxis, :]
        query_text = idx2data[i][2]

        D, I = engine.query(query, 3)

        if len(D[D < 0.5]) == 0:
            continue

        recall = engine.indexResult(idx2text, I[0])

        match_id = np.argmin([Levenshtein.distance(r['text'], query_text) for r in recall])

        enterprise_id = text2idx[recall[match_id]['text']]
        result.append([idx2text[enterprise_id]['code'], idx2text[enterprise_id]['text']] +
                      idx2data[i])

    result = pd.DataFrame(result, columns=['股票代码', '公司名称', '专利名称', '发明人', '申请人', '申请日', '公开日'])
    result.to_excel('data/result.xlsx', index=False)