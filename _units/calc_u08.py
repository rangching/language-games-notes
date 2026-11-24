"""EP08 練習題答案：盒子裡的甲蟲（§293）。
n 個盒子、每個盒子有 k 種可能內容（含「空的」）→ 內容配置共 k^n 種，
它們全都對應同一套公共用法。本程式用 itertools 實際列舉。執行：python3 calc_u08.py
"""
from itertools import product

def configs(n, kinds):
    return list(product(kinds, repeat=n))

# Q1 5 個人，每個盒子可能是 {甲蟲, 石頭, 空的} 3 種之一
q1 = len(configs(5, ["甲蟲", "石頭", "空的"]))

# Q2 4 個人，盒子可能是 {甲蟲, 石頭, 羽毛, 空的} 4 種之一
q2 = len(configs(4, ["甲蟲", "石頭", "羽毛", "空的"]))

# Q3 3 個人、3 種內容，「三個盒子內容兩兩不同」的配置有幾種
q3 = sum(1 for c in configs(3, ["甲蟲", "石頭", "空的"]) if len(set(c)) == 3)

# Q4 §265：同一天的同一份早報買 5 份，獨立的消息來源有幾個？
papers = [("某日報", "11/24 早報")] * 5
q4 = len(set(papers))

# 參考：私人感覺日記沒有外部可檢查的標準 → 外部獨立檢查數
diary_external_checks = len([src for src in ["我的記憶", "我對記憶的記憶"] if not src.startswith("我")])

print("Q1 5 人 × 3 種內容的盒內配置數 3^5          =", q1)
print("Q2 4 人 × 4 種內容的盒內配置數 4^4          =", q2)
print("Q3 3 人 × 3 種內容、三盒兩兩不同的配置數    =", q3, "（共", len(configs(3, 'abc')), "種）")
print("Q4 同一份早報買 5 份，獨立消息來源數        =", q4)
print("--- 參考：感覺日記能訴諸的外部獨立檢查數    =", diary_external_checks)
