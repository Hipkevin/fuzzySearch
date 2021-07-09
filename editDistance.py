
def distance(string1, string2):
    """
    动态规划计算两字符串编辑距离

    在计算文本的相似性时，经常会用到编辑距离。
    编辑距离，又称Levenshtein距离，是指两个字串之间，由一个转成另一个所需的最少编辑操作次数。
    通常来说，编辑距离越小，两个文本的相似性越大。

    编辑操作主要包括三种：
    插入：将一个字符插入某个字符串；
    删除：将字符串中的某个字符删除；
    替换：将字符串中的某个字符替换为另外一个字符。

    当两个字符串都为空串，那么编辑距离为0；
    当其中一个字符串为空串时，那么编辑距离为另一个非空字符串的长度；
    当两个字符串均为非空时(长度分别为 i 和 j )，取以下三种情况最小值即可：
    1、长度分别为 i-1 和 j 的字符串的编辑距离已知，那么加1即可；
    2、长度分别为 i 和 j-1 的字符串的编辑距离已知，那么加1即可；
    3、长度分别为 i-1 和 j-1 的字符串的编辑距离已知，此时考虑两种情况，若第i个字符和第j个字符不同，那么加1即可；如果相同，则不需要加1。

    :param string1: 字符串1
    :param string2: 字符串2
    :return: 编辑距离
    """
    edit = [[i+j for j in range(len(string2)+1)] for i in range(len(string1)+1)]

    for i in range(1, len(string1)+1):
        for j in range(1, len(string2)+1):

            if string1[i-1] == string2[j-1]:
                d = 0
            else:
                d = 1

            edit[i][j] = min(edit[i-1][j] + 1, edit[i][j-1] + 1, edit[i-1][j-1] + d)

    return edit[len(string1)][len(string2)]


def distance_compress(string1, string2):
    """
    压缩形式的动态规划：
    只保留两个dp向量，每轮更新之后向下移动

    空间复杂度降为 O(s) s = min(m, n)

    :param string1: 字符串1
    :param string2: 字符串2
    :return: 编辑距离
    """
    if len(string1) > len(string2):
        string1, string2 = string2, string1

    n = len(string1)
    m = len(string2)

    dp0 = list(range(n + 1))
    dp1 = list(range(n + 1))
    for i in range(1, m+1):
        for j in range(1, n+1):

            if string1[j-1] == string2[i-1]:
                d = 0
            else:
                d = 1

            if j == 1:
                dp1[0] = i

            dp1[j] = min(dp1[j-1]+1, dp0[j]+1, dp0[j-1]+d)

        # 更新dp0时只传值
        dp0 = dp1.copy()

    return dp1[-1]


print(distance('batyu', 'beauty'))
print(distance_compress('batyu', 'beauty'))