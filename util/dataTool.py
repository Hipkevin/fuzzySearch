import pandas as pd
import numpy as np

from tqdm import tqdm

def getEnterprise(path):
    data = pd.read_excel(path)

    idx = data['id']
    code = data['证券代码']
    text = data['关联公司名称']

    text2idx = dict()
    idx2text = dict()

    for i in range(len(idx)):
        idx2text[i] = {'text': text[i], 'code': code[i]}
        text2idx[text[i]] = i

    return idx2text, text2idx

def getEpub(path):
    """
    专利名称 发明人 申请人 申请日 公开日
    """

    with open(path, 'r', encoding='utf-8') as file:
        data = file.read().strip().split('\n')

    idx2data = dict()
    for i in range(len(data)):
        idx2data[i] = eval(data[i])

    return idx2data

def getVector(text, emb):
    vec = np.zeros(300, dtype='float32')
    for word in text:
        vec += emb.get(word, np.zeros(300, dtype='float32'))

    return vec / (len(text) + 1)

def slimEmbedding(corpus_path, emb_path):
    with open(corpus_path, 'r', encoding='utf-8') as file:
        text = file.read().strip().split('\n')

    char_dict = dict()
    for t in text:
        char_dict.update({c: c for c in t})

    res = []
    with open(emb_path, "r", encoding='UTF-8') as file:
        loop = tqdm(file.readlines())
        loop.set_description('Loading embedding model')

        for line in loop:
            lin = line.strip().split(" ")

            if lin[0] in char_dict:
                res.append(line)

    with open('data/slim_embedding.bin', 'w+', encoding='utf-8') as file:
        for r in res:
            file.write(r)


def loadEmbeddingModel(embedding_path):
    embedding_model = dict()
    with open(embedding_path, "r", encoding='UTF-8') as file:
        loop = tqdm(file.readlines())
        loop.set_description('Loading embedding model')

        for line in loop:
            lin = line.strip().split(" ")

            emb = [float(x) for x in lin[1:301]]
            embedding_model[lin[0]] = np.asarray(emb, dtype='float32')

    return embedding_model