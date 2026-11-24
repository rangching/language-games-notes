"""EP01 練習題答案：翻桌子，推翻自己的哲學家。
年代取自 source/bio_places.json 與系列大綱；距離用 haversine 大圓公式（地球平均半徑 6371 km）。
執行：python3 calc_u01.py（只用標準函式庫）"""
import json, math
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
bio = json.loads((ROOT / "source" / "bio_places.json").read_text(encoding="utf-8"))
P = {p["id"]: p for p in bio["places"]}
R = 6371.0

def age_on(birth, day):
    return day.year - birth.year - ((day.month, day.day) < (birth.month, birth.day))

def haversine(a, b):
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dp, dl = p2 - p1, math.radians(b["lon"] - a["lon"])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

birth = date(1889, 4, 26)
q1 = age_on(birth, date(1929, 1, 18))          # 回到劍橋那天（凱因斯的信）
q2 = 1953 - 1921                               # 《邏輯哲學論》德文版 1921 → 《哲學研究》出版 1953
q3 = haversine(P["vienna"], P["cambridge"])
q4 = haversine(P["cambridge"], P["skjolden"])

print("Q1 1929-01-18 回到劍橋時的年齡（歲）          =", q1)
print("Q2 1921 → 1953 相隔幾年                         =", q2)
print(f"Q3 維也納 → 劍橋 大圓距離（km）                 = {q3:.0f}")
print(f"Q4 劍橋 → 斯寇爾登 大圓距離（km）               = {q4:.0f}")
# 參考：過世時年齡；序言落款（1945-01）時距離回劍橋幾年；依 events 順序串起來的總移動距離
print("--- 參考：1951-04-29 過世時年齡 =", age_on(birth, date(1951, 4, 29)))
seq, prev, total = [], None, 0.0
for e in sorted(bio["events"], key=lambda e: (e["y0"], e.get("m0", 1))):
    if e["place"] and e["place"] != prev:
        if prev:
            total += haversine(P[prev], P[e["place"]])
        prev = e["place"]
print(f"--- 參考：依年表把地點串成路線，大圓總長約 {total:.0f} km（與動手玩的「累計移動」一致）")
print(f"--- 參考：特拉騰巴赫 → 奧特塔 {haversine(P['trattenbach'], P['otterthal']):.1f} km；都柏林 → 綺色佳 {haversine(P['dublin'], P['ithaca']):.0f} km")
