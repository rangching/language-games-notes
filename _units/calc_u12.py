"""EP12 練習題答案：體驗時代：從經驗中學習。
用純 Python 在「與 sims/u12.html 預設完全相同」的格子世界上跑價值迭代（同步更新）。
預設設定讀自 ROOT/source/ep12_gridworld.json（sim 內嵌同一份）；只用標準函式庫。
執行：python3 calc_u12.py
"""
import json
from pathlib import Path

CFG = json.loads((Path(__file__).resolve().parents[2] / "source" / "ep12_gridworld.json").read_text(encoding="utf-8"))
MOVES = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
LEFT = {"N": "W", "E": "N", "S": "E", "W": "S"}
RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}


def value_iteration(grid, gamma, step_cost, slip_on, fwd=0.8, side=0.1, tol=1e-4, max_iter=10000):
    R, C = len(grid), len(grid[0])
    term = CFG["terminal_values"]
    V = [[0.0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if grid[r][c] in term:
                V[r][c] = float(term[grid[r][c]])

    def step(r, c, a):
        dr, dc = MOVES[a]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] == "#":
            return r, c                      # 撞牆或出界：留在原地
        return nr, nc

    def q(V, r, c, a):
        outs = [(fwd, a), (side, LEFT[a]), (side, RIGHT[a])] if slip_on else [(1.0, a)]
        return sum(p * (step_cost + gamma * V[nr][nc]) for p, d in outs for nr, nc in [step(r, c, d)])

    it, delta = 0, None
    while it < max_iter:
        newV = [row[:] for row in V]
        delta = 0.0
        for r in range(R):
            for c in range(C):
                if grid[r][c] in term or grid[r][c] == "#":
                    continue
                newV[r][c] = max(q(V, r, c, a) for a in "NESW")
                delta = max(delta, abs(newV[r][c] - V[r][c]))
        V = newV
        it += 1
        if delta < tol:
            break
    policy = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] in ".S":
                qs = [q(V, r, c, a) for a in "NESW"]
                policy[(r, c)] = "NESW"[qs.index(max(qs))]
    return V, it, delta, policy


grid = CFG["grid"]
start = next((r, row.index("S")) for r, row in enumerate(grid) if "S" in row)
g, sc, tol = CFG["gamma"], CFG["step_cost"], CFG["tol"]
fwd, side = CFG["slip"]["forward"], CFG["slip"]["left"]

# Q1 折扣回報：γ=0.9，連續 3 步各得 1 分 → G = 1 + 0.9 + 0.9²
q1 = sum(1 * 0.9 ** k for k in range(3))
# Q2、Q3 預設格子世界（滑動開啟）
V, it, d, pol = value_iteration(grid, g, sc, True, fwd, side, tol)
# Q4 同一個格子，把滑動關掉（行動百分之百照指令）
Vd, itd, dd, pold = value_iteration(grid, g, sc, False, tol=tol)
# 參考：γ=0.5（很短視）時起點的價值
Vh, ith, _, _ = value_iteration(grid, 0.5, sc, True, fwd, side, tol)

ARW = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
print(f"設定：{len(grid)}×{len(grid[0])} 格，γ={g}，每步代價={sc}，滑動 {fwd}/{side}/{side}，收斂門檻 max|ΔV| < {tol}")
print("Q1 γ=0.9 連續 3 步各得 1 分的折扣回報             =", round(q1, 4))
print("Q2 預設格子收斂後，起點的價值（取 3 位小數）       =", round(V[start[0]][start[1]], 3), f"（完整 {V[start[0]][start[1]]:.6f}）")
print("Q3 預設格子收斂所需的迭代次數                     =", it, f"（最後一步最大變動量 {d:.2e}）")
print("Q4 同一格子關掉滑動後，起點的價值                 =", round(Vd[start[0]][start[1]], 3), f"（迭代 {itd} 次）")
print("--- 參考：γ=0.5 時起點的價值 =", round(Vh[start[0]][start[1]], 3), f"（迭代 {ith} 次）")
print("--- 預設格子收斂後的數值與最佳行動：")
for r, row in enumerate(grid):
    cells = []
    for c, ch in enumerate(row):
        if ch == "#":
            cells.append("  ####  ")
        elif ch in "GT":
            cells.append(f" {V[r][c]:+.2f}{ch} ")
        else:
            cells.append(f"{V[r][c]:+.3f}{ARW[pol[(r, c)]]}")
    print("   ", " ".join(cells))
