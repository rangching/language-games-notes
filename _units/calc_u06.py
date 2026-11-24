"""EP06 練習題答案：哲學病與捕蠅瓶。
§107：光滑的冰面「條件理想」，卻沒有摩擦力，所以走不動。
摩擦力模型與 sims/u06.html 相同：
  正向力 N ＝ m·g（平地），腳能向後蹬、地面回推的最大水平力 F_max ＝ μ·N
  想以加速度 a 起步，需要水平力 m·a；F_max ≥ m·a 才走得動。
只用標準函式庫。執行：python3 calc_u06.py
"""
m, g = 60.0, 9.8          # 體重 60 kg、重力加速度 9.8 m/s²

def f_max(mu, mass=m):
    return mu * mass * g

# Q1 §89 到 §133（含頭尾）共幾節：逐節數
q1 = sum(1 for s in range(89, 134))
# Q2 μ = 0.4（乾燥柏油路上的鞋底量級）時，60 kg 的人最大推進力
q2 = f_max(0.4)
# Q3 μ = 0（§107 的理想冰面）時的最大推進力
q3 = f_max(0.0)
# Q4 想以 1.5 m/s² 起步，μ 至少要多少？逐步掃描 μ（步長 0.0001），找第一個 F_max ≥ m·a 的值
a_need = 1.5
mu, step = 0.0, 0.0001
while f_max(mu) < m * a_need - 1e-9:
    mu += step
q4 = round(mu, 4)

print("Q1 §89–§133 共幾節                          =", q1)
print("Q2 μ=0.4、60 kg 的最大推進力 F=μN（牛頓）  =", round(q2, 2))
print("Q3 μ=0 時的最大推進力（牛頓）              =", q3)
print("Q4 以 1.5 m/s² 起步所需的最小 μ（掃描）     =", q4, "（解析解 a/g =", round(a_need / g, 4), "）")
print("--- 參考：μ 從 0 到 1 每 0.1 的 F_max：", [round(f_max(k / 10), 1) for k in range(11)])
