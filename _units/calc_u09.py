"""EP09 練習題答案：鴨兔圖、內克方塊與面相（PPF §111–§261）。
每個雙穩態圖形有 2 種讀法；彼此獨立的 n 個圖形整體有 2^n 種讀法（實際列舉）。
Q4 用精確二項分布算「語境其實沒有作用」時出現極端結果的機率。執行：python3 calc_u09.py
"""
from itertools import product
from math import comb

def readings(figs):
    """figs：每個圖形的讀法清單；回傳所有整體讀法。"""
    return list(product(*figs))

DR = ["鴨", "兔"]
NECKER = ["左下面在前", "右上面在前"]

# Q1 3 張彼此獨立的鴨兔圖，整體讀法數
q1 = len(readings([DR] * 3))
# Q2 一個內克方塊有幾種深度讀法
q2 = len(readings([NECKER]))
# Q3 2 張鴨兔圖 + 2 個內克方塊，整體讀法數
q3 = len(readings([DR, DR, NECKER, NECKER]))
# Q4 假設語境完全沒有作用（每個人看成鴨的機率都是 1/2），10 個人在「鴨群」語境下
#    至少 8 人第一眼看成鴨的機率（四捨五入到小數第 3 位）
n = 10
p = sum(comb(n, k) for k in range(8, n + 1)) / 2 ** n
# 也用列舉驗證：所有 2^10 種結果中，鴨 ≥ 8 的比例
p_enum = sum(1 for r in product([0, 1], repeat=n) if sum(r) >= 8) / 2 ** n
assert abs(p - p_enum) < 1e-12
q4 = round(p, 3)

print("Q1 3 張獨立鴨兔圖的整體讀法數                 =", q1)
print("Q2 一個內克方塊的讀法數                       =", q2)
print("Q3 2 張鴨兔圖 + 2 個內克方塊的整體讀法數      =", q3)
print("Q4 語境無作用時 10 人中 ≥ 8 人看成鴨的機率    =", q4, f"（精確值 {p:.6f} = {int(p * 1024)}/1024）")
