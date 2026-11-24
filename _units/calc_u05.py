"""EP05 練習題答案：家族相似。
資料：../../source/games_features.json（16 種活動 × 10 項特徵；1＝通常具備）。
與 sims/u05.html 同一套算法：
  Jaccard(A, B) ＝ 兩者都具備的特徵數 ÷ 至少一方具備的特徵數
  相似之網：Jaccard ≥ 門檻 就連一條邊；連通分量用 BFS 計算。
只用標準函式庫。執行：python3 calc_u05.py
"""
import json
from itertools import combinations
from pathlib import Path

data = json.loads((Path(__file__).resolve().parents[2] / "source" / "games_features.json").read_text(encoding="utf-8"))
F, G = data["features"], data["items"]
n, m = len(G), len(F)

# Q1 全部 16 種活動都具備的特徵有幾項
common = [F[j]["zh"] for j in range(m) if all(g["f"][j] for g in G)]
per_feature = {F[j]["zh"]: sum(g["f"][j] for g in G) for j in range(m)}

def jac(a, b):
    both = sum(x and y for x, y in zip(a["f"], b["f"]))
    either = sum(x or y for x, y in zip(a["f"], b["f"]))
    return both / either if either else 0.0

pairs = [(jac(a, b), a["zh"], b["zh"]) for a, b in combinations(G, 2)]
best = max(p[0] for p in pairs)
top = [p for p in pairs if abs(p[0] - best) < 1e-12]
second = max(p[0] for p in pairs if p[0] < best - 1e-12)
top2 = [p for p in pairs if abs(p[0] - second) < 1e-12]

def graph(th):
    adj = {i: [] for i in range(n)}
    E = 0
    for i, j in combinations(range(n), 2):
        if jac(G[i], G[j]) >= th - 1e-12:
            adj[i].append(j); adj[j].append(i); E += 1
    seen, comps = set(), []
    for s in range(n):
        if s in seen: continue
        q, comp = [s], []
        seen.add(s)
        while q:
            u = q.pop(0); comp.append(u)
            for v in adj[u]:
                if v not in seen: seen.add(v); q.append(v)
        comps.append(comp)
    return E, comps

E, comps = graph(0.5)

# 「定義」實驗：把一組特徵當定義（必須全部具備），列舉全部 2^10−1 組非空特徵
cover_all = 0
best_cov, best_sets = 0, []
for r in range(1, m + 1):
    for S in combinations(range(m), r):
        cov = sum(all(g["f"][j] for j in S) for g in G)
        if cov == n: cover_all += 1
        if cov > best_cov: best_cov, best_sets = cov, [S]
        elif cov == best_cov: best_sets.append(S)

print("Q1 16 種活動全部共有的特徵數                  =", len(common), common)
print("    各特徵有幾種活動具備：", per_feature)
print("Q2 Jaccard 最高值 =", best, "；並列的對數 =", len(top), [(a, b) for _, a, b in top])
print("    次高值 = %.4f" % second, [(a, b) for _, a, b in top2])
print("Q3 門檻 0.5（≥0.5 才連線）時的邊數            =", E)
print("Q4 門檻 0.5 時的連通分量數                    =", len(comps))
print("    各分量：", [[G[i]["zh"] for i in c] for c in comps])
print("--- 參考：以「全部具備」當定義，1023 組非空特徵中能涵蓋全部 16 種的組數 =", cover_all)
print("--- 參考：單一定義最多涵蓋", best_cov, "種：", [[F[j]["zh"] for j in S] for S in best_sets])
for th in (0.3, 0.4, 0.6, 0.7, 0.8):
    e, c = graph(th)
    print(f"--- 參考：門檻 {th} 邊數 {e}、分量數 {len(c)}")
