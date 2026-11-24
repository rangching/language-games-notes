"""EP10 練習題答案：語境機器，Transformer 讀的是用法。
softmax 把一排分數變成加起來等於 1 的權重；縮放點積注意力先把分數除以 √dₖ 再做 softmax。
只用標準函式庫。執行：python3 calc_u10.py
"""
import math


def softmax(xs):
    m = max(xs)                       # 先減最大值，避免 exp 溢位；結果不變
    es = [math.exp(x - m) for x in xs]
    s = sum(es)
    return [e / s for e in es]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# Q1 「意思」對三個上下文詞的分數為 3、1、0，softmax 後最大的權重是多少？
s1 = [3, 1, 0]
w1 = softmax(s1)
q1 = max(w1)

# Q2 同一組分數，若向量維度 dₖ = 4，先除以 √4 = 2 再做 softmax，最大權重變成多少？
dk = 4
w2 = softmax([x / math.sqrt(dk) for x in s1])
q2 = max(w2)

# Q3 q = (1, 2, 0, 1)、k = (2, 1, 1, 0)，縮放後的分數 q·k / √dₖ 是多少？
q, k = (1, 2, 0, 1), (2, 1, 1, 0)
q3 = dot(q, k) / math.sqrt(len(q))

# Q4 一句話切成 12 個詞元，自注意力的權重矩陣有幾格？（每個詞都對每個詞算一次）
n = 12
q4 = sum(1 for i in range(n) for j in range(n))

print("Q1 softmax([3,1,0]) 最大權重        =", round(q1, 3), "；全部：", [round(x, 3) for x in w1])
print("Q2 除以 √4 後的最大權重             =", round(q2, 3), "；全部：", [round(x, 3) for x in w2])
print("Q3 q·k =", dot(q, k), "；q·k/√4               =", q3)
print("Q4 12 個詞元的注意力矩陣格數        =", q4)
print("--- 參考：分數乘 10 倍（[30,10,0]）最大權重 =", round(max(softmax([30, 10, 0])), 6), "：分數差越大，分佈越尖")
print("--- 參考：全部分數相同（[2,2,2]）的權重     =", [round(x, 3) for x in softmax([2, 2, 2])], "：一樣大就平均分")
