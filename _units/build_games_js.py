"""source/games_features.json → learning_site/data/games.js（window.GAMES）。
用法：python3 build_games_js.py"""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parent.parent
src = root / "source" / "games_features.json"
out = here.parent / "data" / "games.js"

d = json.loads(src.read_text(encoding="utf-8"))
features = [{k: f[k] for k in ("id", "zh", "en")} for f in d["features"]]
items = [{k: it[k] for k in ("id", "zh", "en", "kind", "f")} for it in d["items"]]
n = len(features)
for it in items:
    assert len(it["f"]) == n and all(v in (0, 1) for v in it["f"]), f"{it['id']} 特徵數不對"
common = [features[j]["zh"] for j in range(n) if all(it["f"][j] for it in items)]

body = json.dumps({"features": features, "items": items}, ensure_ascii=False, separators=(",", ":"))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(
    "// 由 _units/build_games_js.py 產生，請勿手改。來源：source/games_features.json\n"
    "// 家族相似（PI §66–§67）示範資料：本系列自訂的教學資料，不是原書內容。\n"
    f"window.GAMES = {body};\n",
    encoding="utf-8",
)
print(f"games.js ← {len(items)} 種活動 × {n} 項特徵；全部共有的特徵：{len(common)} 項 {common}")
