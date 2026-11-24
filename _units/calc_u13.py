"""EP13 練習題答案：代理人的劇本：Agent、MCP 與狀態機。
狀態機定義讀自 ROOT/source/ep13_fsm.json（sims/u13.html 內嵌同一份）；只用標準函式庫。
執行：python3 calc_u13.py
"""
import json
from collections import deque
from pathlib import Path

FSM = json.loads((Path(__file__).resolve().parents[2] / "source" / "ep13_fsm.json").read_text(encoding="utf-8"))
EV = {e["id"]: e for e in FSM["events"]}


def full_scripts():
    """每位角色的劇本＝它身為收件者的所有事件。"""
    s = {r: set() for r in FSM["roles"]}
    for e in FSM["events"]:
        s[e["to"]].add(e["id"])
    return s


def reachable(scripts):
    """BFS：只走收件者劇本裡有的事件。"""
    seen, q = {FSM["start"]}, deque([FSM["start"]])
    while q:
        s = q.popleft()
        for e in FSM["events"]:
            if s in e["src"] and e["id"] in scripts[e["to"]] and e["dst"] not in seen:
                seen.add(e["dst"])
                q.append(e["dst"])
    return seen


def run(scripts, rounds, stock=None):
    """照 sim 的規則跑訊息佇列：A 連喊 rounds 次「石板！」（每輪完成後送「下一輪」）。回傳處理的訊息數、最後狀態、紀錄。"""
    stock = FSM["stock"]["initial"] if stock is None else stock
    state, queue, log, handled = FSM["start"], deque(), [], 0
    for k in range(rounds):
        queue.append("order")
        while queue:
            mid = queue[0]
            e = EV[mid]
            if mid not in scripts[e["to"]]:
                log.append(f"卡住：{e['to']} 的劇本沒有「{e['zh']}」")
                return handled, state, log
            queue.popleft()
            if state not in e["src"]:
                log.append(f"退回：{e['zh']}（狀態 {state}）")
                continue
            handled += 1
            state = e["dst"]
            log.append(f"{e['from']}→{e['to']} {e['zh']} ⇒ {state}")
            for em in e["emit"]:
                if em == "handover|short":
                    if stock > 0:
                        stock -= 1
                        queue.append("handover")
                    else:
                        queue.append("short")
                elif em == "handover" and mid == "restock":
                    stock += FSM["stock"]["restock_amount"] - 1
                    queue.append("handover")
                else:
                    queue.append(em)
        if k < rounds - 1:
            queue.append("next")
            while queue:
                mid = queue.popleft(); e = EV[mid]
                if mid in scripts[e["to"]] and state in e["src"]:
                    handled += 1; state = e["dst"]; log.append(f"{e['from']}→{e['to']} {e['zh']} ⇒ {state}")
    return handled, state, log


S = full_scripts()
q1 = len(reachable(S))
S2 = full_scripts(); S2["C"].discard("restock")
q2 = len(reachable(S2))
S3 = full_scripts(); S3["B"].discard("order")
q3_ref = len(reachable(S3))
n = 10
q3 = n * (n - 1) // 2
q3_hub = n
# Q4 一次工具呼叫的最少訊息數。定義：一則訊息＝一位參與者傳給另一位參與者的一次傳送。
# 參與者：模型、主機裡的用戶端、工具伺服器。工具清單已事先取得。
hops = [("模型", "用戶端", "工具呼叫請求（名稱＋參數）"),
        ("用戶端", "伺服器", "tools/call 請求"),
        ("伺服器", "用戶端", "執行結果（回應）"),
        ("用戶端", "模型", "把結果交回模型")]
q4 = len(hops)
h5, st5, log5 = run(S, 2)

print("狀態：", "、".join(FSM["states"]), f"（共 {len(FSM['states'])} 個）")
print("Q1 劇本齊全時，從「待命」可到達的狀態數（含待命）  =", q1, sorted(reachable(S), key=FSM["states"].index))
print("Q2 拿掉倉管 C 劇本裡的「補貨」後，可到達的狀態數     =", q2, sorted(reachable(S2), key=FSM["states"].index))
print("--- 參考：拿掉搬運 B 劇本裡的「石板！」（B 沒受訓）  =", q3_ref)
print(f"Q3 {n} 個代理人兩兩直連的連線數 n(n−1)/2            =", q3, f"；經單一協調者只要 n = {q3_hub} 條，少 {q3 - q3_hub} 條")
for k in (3, 5, 20):
    print(f"    參考 n={k}：兩兩直連 {k*(k-1)//2} 條，經協調者 {k} 條")
print("Q4 一次工具呼叫的最少訊息數                         =", q4)
for a, b, m in hops:
    print(f"    {a} → {b}：{m}")
print("    參考：若還要先問伺服器有哪些工具（tools/list 請求＋回應），再加 2 則 =", q4 + 2)
print(f"--- 參考：庫存 {FSM['stock']['initial']}，連喊兩輪「石板！」共處理 {h5} 則訊息，最後狀態 {st5}")
for line in log5:
    print("    ", line)
