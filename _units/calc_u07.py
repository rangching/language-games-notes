"""EP07 練習題答案：遵守規則的悖論。
§185 的學生把「+2」延續成 1000, 1004, 1008, 1012；§201：任何做法都能被「解釋」成符合規則。
本程式實際寫出數列、實際代入多項式，不只套公式。執行：python3 calc_u07.py
"""

def plus2_upto(limit):
    """社群的做法：從 0 開始每次加 2，寫到 limit（含）。"""
    out, x = [], 0
    while x <= limit:
        out.append(x)
        x += 2
    return out

def deviant(limit):
    """§185 學生的理解：「到 1000 為止加 2，到 2000 為止加 4，到 3000 為止加 6……」
    步長 = 2 ×（⌊x / 1000⌋ + 1），從 0 寫到 limit（含）。"""
    out, x = [], 0
    while x <= limit:
        out.append(x)
        x += 2 * (x // 1000 + 1)
    return out

# Q1 0、2、4……到 1000 共幾項
q1 = len(plus2_upto(1000))

# Q2 通過 (1,2)(2,4)(3,6)(4,8) 的另一條規則 f(n) = 2n + (n−1)(n−2)(n−3)(n−4)，求 f(5)
f = lambda n: 2 * n + (n - 1) * (n - 2) * (n - 3) * (n - 4)
assert [f(n) for n in range(1, 5)] == [2, 4, 6, 8]      # 和「加 2」在已知點完全重合
q2 = f(5)

# Q3 偏差規則下，1000 之後的第 3 項
d = deviant(5000)
i1000 = d.index(1000)
q3 = d[i1000 + 3]
assert plus2_upto(1000) == d[: i1000 + 1]               # 到 1000 為止兩種做法一模一樣

# Q4 依偏差規則，從 0 寫到 2000（含）共有幾項
q4 = len(deviant(2000))

# 參考：克里普克（Kripke）的 quus：x ⊕ y = x + y（x, y 都小於 57），否則 = 5
quus = lambda x, y: x + y if (x < 57 and y < 57) else 5
agree = sum(1 for x in range(57) for y in range(57) if quus(x, y) == x + y)

print("Q1 0、2、4…到 1000 共幾項                         =", q1)
print("Q2 f(n)=2n+(n−1)(n−2)(n−3)(n−4) 在 n=5 的值       =", q2, "（加 2 規則給 10）")
print("Q3 偏差規則 1000 之後第 3 項                       =", q3, "；前三項", d[i1000 + 1: i1000 + 4])
print("Q4 偏差規則從 0 到 2000（含）共幾項                =", q4)
print("--- 參考：偏差規則 2000 之後的下一項               =", d[d.index(2000) + 1])
print("--- 參考：68 ⊕ 57 =", quus(68, 57), "；68 + 57 =", 68 + 57, "；x,y<57 的", agree, "組加法兩者全同")
