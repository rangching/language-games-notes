"""EP04 練習題答案：意義就是使用（指物猜謎的假設空間）。
設定與 sims/u04.html 相同：每組物件有 4 個屬性維度，各 3 種值：
  顏色（紅、藍、綠）、形狀（圓、方、三角）、數量（1、2、3）、材質（木、石、玻璃）
一個「假設」＝新詞的意思是哪一種條件：每個維度要嘛「不限」，要嘛限定某一個值。
（全部不限＝「東西」；四個維度都限定＝「就是長這樣的一組」，接近專名。）
用例：「這是／這也是 X」（肯定）或「這不是 X」（否定）。與用例不相容的假設就刪掉。
本程式實際列舉全部假設與物件，不只套公式。執行：python3 calc_u04.py
"""
from itertools import product, combinations

DIMS = [("顏色", ["紅", "藍", "綠"]), ("形狀", ["圓", "方", "三角"]),
        ("數量", [1, 2, 3]), ("材質", ["木", "石", "玻璃"])]
ANY = None
HYPS = list(product(*[[ANY] + vals for _, vals in DIMS]))     # 4^4 = 256
OBJS = list(product(*[vals for _, vals in DIMS]))              # 3^4 = 81

def fits(h, o):
    return all(hv is ANY or hv == ov for hv, ov in zip(h, o))

def prune(hyps, obj, positive):
    return [h for h in hyps if fits(h, obj) == positive]

# 第一次指認：指著「兩顆木頭色的圓形核桃」—— 這裡用（紅, 圓, 2, 木）代表
first = ("紅", "圓", 2, "木")
h0 = len(HYPS)
h1 = prune(HYPS, first, True)
# 第二個用例：「這也是 X」——（藍, 方, 2, 玻璃），只有數量和第一組相同
h2 = prune(h1, ("藍", "方", 2, "玻璃"), True)
# 第三個用例：「這不是 X」——（紅, 圓, 3, 木），只有數量和第一組不同
h3 = prune(h2, ("紅", "圓", 3, "木"), False)

# 最少要幾個用例（含第一次指認）才能把「數量＝2」唯一確定？暴力搜尋全部用例組合
target = (ANY, ANY, 2, ANY)
def unique_after(examples):
    hs = HYPS
    for o in examples:
        hs = prune(hs, o, fits(target, o))
    return hs == [target]
min_n = None
for n in range(1, 5):
    if any(unique_after(c) for c in combinations(OBJS, n)):
        min_n = n
        break

# 西洋棋：開局 32 枚棋子，有幾「種」？（§31：先懂下棋，「這是國王」才有意思）
start = ["車", "馬", "象", "后", "王", "象", "馬", "車"] + ["兵"] * 8
pieces = [(c, p) for c in "白黑" for p in start]
kinds = len({p for _, p in pieces})

print("--- 參考：假設空間總數（4 維 × 每維 3 值＋不限）=", h0, "；物件組合數 =", len(OBJS))
print("Q1 第一次指認後，仍相容的假設數                =", len(h1))
print("Q2 再看一個「只有數量相同」的肯定用例後剩下    =", len(h2), [tuple('不限' if v is None else v for v in h) for h in h2])
print("Q3 再看一個「只有數量不同」的否定用例後剩下    =", len(h3))
print("Q4 唯一確定「數量＝2」最少需要的用例數（暴力搜尋）=", min_n)
print("Q5 西洋棋開局棋子總數 =", len(pieces), "；棋子種類數 =", kinds)
print("--- 參考：若先說「這個『數量』叫 X」（§29），只剩只限定數量的假設，指認後剩",
      len([h for h in h1 if h[0] is ANY and h[1] is ANY and h[3] is ANY and h[2] is not ANY]))
