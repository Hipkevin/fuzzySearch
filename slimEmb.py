from util.dataTool import slimEmbedding, getEpub, getEnterprise


if __name__ == '__main__':
    # 加载数据，构造corpus
    idx2data = getEpub('data/epub.txt')
    idx2text, text2idx = getEnterprise('data/enterprise.xlsx')

    with open('data/corpus.txt', 'a+', encoding='utf-8') as file:

        # 提取申请人
        for i in range(len(idx2data)):
            file.write(str(idx2data[i][2]) + '\n')

        for i in range(len(idx2text)):
            file.write(str(idx2text[i]['text']) + '\n')

    slimEmbedding('data/corpus.txt', 'data/sgns.wiki.char')