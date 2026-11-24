"""EP03 練習題答案：語言遊戲，說話是做事的一部分。
Q1 §23 的清單：本程式內附依第 4 版原文自己數過的轉述清單（15 行，最後一行含 5 種）；
   若 source/pi_sections.json 已有鍵 23a 的 list 欄位，就一併比對。
Q2 動手玩「這句話在玩哪一種遊戲？」的同一套分數模型（權重與網頁相同），列舉情境計算。
執行：python3 calc_u03.py（只用標準函式庫）"""
import json, math
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

L23 = ["下命令，並照命令去做", "依外觀或量測描述一個東西", "照描述（或圖）做出一個東西", "報告一件事的經過",
       "對事情的經過做推測", "提出假說並檢驗", "用表格與圖呈現實驗結果", "編故事；讀故事", "演戲", "唱輪唱曲",
       "猜謎", "編笑話；講笑話", "解一道應用算術題", "把一種語言翻成另一種", "請求、道謝、咒罵、問候、祈禱"]
q1 = len(L23)
q1_split = len(L23) - 1 + len(L23[-1].split("、"))      # 把最後一行的五種拆開算
other = None
f = ROOT / "source" / "pi_sections.json"
if f.exists():
    try:
        for r in json.loads(f.read_text(encoding="utf-8")):
            if r.get("k") == "23a" and r.get("list"):
                other = len(r["list"])
    except Exception as e:
        other = f"讀取失敗：{e}"

# 「門開著。」的分數模型（與 sims/u03.html 相同）：z = b + Σ w·x
FEATS = 6
GAMES = {
    "命令": (-1.0, [2.6, 1.6, -2.0, 0, 0, -2.5]),
    "報告": (0.6, [0, 0, 3.0, 0, 0, -1.5]),
    "抱怨": (-0.8, [-1.8, 2.4, -1.0, 0, 0, -2]),
    "提醒": (-1.2, [0, 0, -0.5, 2.0, 2.4, -2]),
    "邀請": (-1.6, [-0.5, -1, -1, 0, 0, 4.2]),
}
PRESETS = {"冬天的辦公室，主管說": (1, 1, 0, 0, 0, 0), "保全問：門關了嗎？": (0, 0, 1, 0, 0, 0),
           "室友縮在沙發上說": (0, 1, 0, 0, 0, 0), "正要出門，家裡有貓": (0, 0, 0, 1, 1, 0),
           "店員對路人說": (0, 0, 0, 0, 0, 1)}

def play(x):
    z = {g: b + sum(w * v for w, v in zip(ws, x)) for g, (b, ws) in GAMES.items()}
    m = max(z.values()); s = sum(math.exp(v - m) for v in z.values())
    p = {g: math.exp(v - m) / s for g, v in z.items()}
    return max(p, key=p.get), p

preset_games = {name: play(x)[0] for name, x in PRESETS.items()}
q2 = len(set(preset_games.values()))
all_x = list(product([0, 1], repeat=FEATS))
q2_all = len({play(x)[0] for x in all_x})

TOOLS = ["槌子", "鉗子", "鋸子", "螺絲起子", "尺", "膠鍋", "膠", "釘子", "螺絲"]   # §11
HANDLES = ["曲柄", "開關", "煞車桿", "幫浦"]                                       # §12

print("Q1 §23 清單共幾行（每行一種）                   =", q1, f"（若把最後一行的五種拆開算：{q1_split}）")
print("   pi_sections.json 的 23a.list 項數           =", other if other is not None else "（檔案或欄位尚未建立，未比對）")
print("Q2 「門開著。」× 5 張情境卡，玩出幾種不同遊戲   =", q2, preset_games)
print("   列舉全部 2^6 =", len(all_x), "種情境，最可能的遊戲共幾種 =", q2_all)
print("Q3 §11 工具箱裡列了幾樣東西（釘子、螺絲分開）   =", len(TOOLS))
print("Q4 §12 火車頭駕駛室裡描述了幾種把手             =", len(HANDLES))
