"""EP11 練習題答案：走出語義孤島，從 RAG 到知識圖譜。
資料：../../source/ep11_corpus.json（全部虛構的小語料＋由它整理出的三元組；sims/u11.html 內嵌同一份）。
只用標準函式庫。執行：python3 calc_u11.py
"""
import json
import math
import re
from collections import Counter, deque
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parents[2] / "source" / "ep11_corpus.json").read_text(encoding="utf-8"))
nodes = [n["id"] for n in DATA["nodes"]]
triples = DATA["triples"]
paras = DATA["paragraphs"]

# ---------- 圖：不分方向的鄰接表（找路徑時兩個方向都能走） ----------
adj = {n: set() for n in nodes}
for t in triples:
    adj[t["s"]].add(t["o"])
    adj[t["o"]].add(t["s"])


def bfs(src):
    """回傳 {節點: 距離}，只走得到的節點。"""
    dist, q = {src: 0}, deque([src])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def shortest_path(a, b):
    prev, q = {a: None}, deque([a])
    while q:
        u = q.popleft()
        if u == b:
            break
        for v in sorted(adj[u]):
            if v not in prev:
                prev[v] = u
                q.append(v)
    path, u = [], b
    while u is not None:
        path.append(u)
        u = prev[u]
    return path[::-1]


# ---------- 相似度檢索：字元二元組詞袋的餘弦相似度（與 sim 相同） ----------
def bigrams(s):
    s = "".join(re.findall(r"[0-9A-Za-z一-鿿]", s)).lower()
    return Counter(s[i:i + 2] for i in range(len(s) - 1))


def cos(a, b):
    dot = sum(a[k] * b.get(k, 0) for k in a)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def rank(question):
    qv = bigrams(question)
    sc = [(cos(qv, bigrams(p["text"])), p["id"]) for p in paras]
    sc.sort(key=lambda x: (-x[0], int(x[1][1:])))
    return sc


# Q1 三元組數
q1 = len(triples)

# Q2 「許若嵐」到「新竹」的最短路徑長度（跳數）
p2 = shortest_path("許若嵐", "新竹")
q2 = len(p2) - 1

# Q3 從「石楠精工」出發，兩跳以內可到達幾個節點（不含自己）
d3 = bfs("石楠精工")
q3 = sum(1 for n, d in d3.items() if 1 <= d <= 2)

# Q4 兩跳問題用相似度排序時，記載「雲杉塑膠在台中」的那一段（p4）排第幾名
qs = {q["id"]: q for q in DATA["questions"]}
r4 = rank(qs["q2"]["text"])
q4 = [pid for _, pid in r4].index("p4") + 1

# 參考：全域問題的正確答案（數每一條「簽約方」關聯）
cnt = Counter(t["o"] for t in triples if t["p"] == "簽約方")

print("Q1 三元組數                                   =", q1)
print("Q2 許若嵐 → 新竹 最短路徑長度                 =", q2, "；路徑：", " — ".join(p2))
print("Q3 石楠精工 兩跳以內可到達的節點數            =", q3,
      "；一跳", sum(1 for d in d3.values() if d == 1), "、兩跳", sum(1 for d in d3.values() if d == 2))
print("Q4 兩跳問題中 p4（雲杉塑膠在台中）的相似度名次 =", q4, "／", len(paras))
print("--- 參考：節點數 =", len(nodes), "；段落數 =", len(paras))
for q in DATA["questions"]:
    print(f"--- 參考：〈{q['text']}〉相似度前 5：",
          "、".join(f"{pid}({s:.3f})" for s, pid in rank(q["text"])[:5]))
print("--- 參考：各供應商出現的合約數 =", dict(cnt.most_common()))
print("--- 參考：晨光電鍋 C5 → 台中 最短路徑：", " — ".join(shortest_path("晨光電鍋 C5", "台中")))


# 參考：社群（與 sim 相同的確定性貪婪合併：每次合併讓模組度 Q 上升最多的一對相鄰社群）
def modularity(parts):
    m = len(triples)
    deg = {n: sum(1 for t in triples if n in (t["s"], t["o"])) for n in nodes}
    q = 0.0
    for part in parts:
        lc = sum(1 for t in triples if t["s"] in part and t["o"] in part)
        dc = sum(deg[n] for n in part)
        q += lc / m - (dc / (2 * m)) ** 2
    return q


parts = [{n} for n in nodes]
while True:
    best, bq = None, modularity(parts)
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            if not any(o in parts[j] for n in parts[i] for o in adj[n]):
                continue
            trial = [p for x, p in enumerate(parts) if x not in (i, j)] + [parts[i] | parts[j]]
            q = modularity(trial)
            if q > bq + 1e-12:
                best, bq = (i, j), q
    if not best:
        break
    i, j = best
    parts = [p for x, p in enumerate(parts) if x not in (i, j)] + [parts[i] | parts[j]]
print(f"--- 參考：社群數 = {len(parts)}，模組度 Q = {modularity(parts):.3f}")
for p in sorted(parts, key=lambda p: min(nodes.index(n) for n in p)):
    print("    ", "、".join(sorted(p, key=nodes.index)))
