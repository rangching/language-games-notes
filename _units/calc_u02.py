"""EP02 練習題答案：每個詞都是名字嗎？
§1 五個紅蘋果、§2 建築工人的四個詞。用 itertools 實際列舉，不只套公式。
執行：python3 calc_u02.py（只用標準函式庫）"""
from fractions import Fraction
from itertools import product

WORDS = ["方石", "柱石", "石板", "石樑"]            # §2：Würfel, Säule, Platte, Balken

# Q1 四個詞、連喊 3 次，有幾種不同的指令序列
q1 = len(list(product(WORDS, repeat=3)))

# Q2 §1 五個紅蘋果：店員對三個詞各做了什麼（每個動作算一步）
steps = {
    "蘋果": ["打開標著「蘋果」的抽屜"],
    "紅":   ["在色卡表上查到「紅」旁邊的色樣"],
    "五":   [f"數「{n}」並拿一顆和色樣同色的蘋果" for n in "一二三四五"],
}
q2_five = len(steps["五"])
q2_total = sum(len(v) for v in steps.values())

# Q3 照「小塔」藍圖（方石、方石、石板、柱石、石樑）蓋好，最少要喊幾次？
tower = ["方石", "方石", "石板", "柱石", "石樑"]
seqs = list(product(WORDS, repeat=len(tower)))        # 所有長度 5 的喊法
q3 = len(tower)                                       # 一塊石頭一聲，而且順序對的只有 1 種
right = sum(1 for s in seqs if list(s) == tower)

# Q4 沒受過訓練的 B 每次都亂猜（四種石頭各 1/4）。A 照藍圖喊，拿錯就退回重喊。
#     蓋好「門」（柱石、柱石、石樑）平均要喊幾次？每塊是成功率 p 的幾何分配，期望 1/p 次。
p = Fraction(1, 4)
q4 = 3 * (1 / p)

print("Q1 四個詞連喊 3 次的指令序列數                  =", q1)
print("Q2 為了「五」，店員數數拿蘋果幾次               =", q2_five, "；三個詞一共幾步 =", q2_total)
print("Q3 照「小塔」藍圖最少要喊幾次                   =", q3, f"（長度 5 的喊法共 {len(seqs)} 種，完全照藍圖的只有 {right} 種）")
print("Q4 沒受訓的 B 蓋好「門」平均要喊幾次            =", int(q4))
