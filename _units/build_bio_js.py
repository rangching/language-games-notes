"""source/bio_places.json → ../data/bio_places.js（window.BIO = {places, events}）。
執行：python3 build_bio_js.py"""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
src = here.parent.parent / "source" / "bio_places.json"
out = here.parent / "data" / "bio_places.js"
d = json.loads(src.read_text(encoding="utf-8"))
ids = {p["id"] for p in d["places"]}
for e in d["events"]:
    assert e["place"] is None or e["place"] in ids, f"未知地點 {e['place']}"
    assert (e["y0"], e.get("m0", 1)) <= (e["y1"], e.get("m1", 12)), f"年代顛倒：{e['zh']}"
places = [{k: p[k] for k in ("id", "zh", "en", "lat", "lon", "country_now")} for p in d["places"]]
events = sorted(d["events"], key=lambda e: (e["y0"], e.get("m0", 1)))
js = "// 由 _units/build_bio_js.py 從 source/bio_places.json 產生，請勿手改。\nwindow.BIO = " + json.dumps(
    {"places": places, "events": events}, ensure_ascii=False, indent=1) + ";\n"
out.parent.mkdir(exist_ok=True)
out.write_text(js, encoding="utf-8")
print(f"{out.name}: {len(places)} 個地點、{len(events)} 段經歷")
