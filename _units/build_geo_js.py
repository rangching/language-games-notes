"""產生 ../data/geo_europe.js（window.GEO_EUROPE）：EP01 生平地圖的底圖資料。

資料：Natural Earth 1:50m Cultural Vectors — Admin 0 Countries v5.1.1（公有領域），
讀本機快取 ~/.cache/geo-map-video/ne_50m_admin_0_countries.zip，不連外下載。
（晶片戰爭專案的 world_50m.json 是同一份資料合併成陸地、沒有國界，所以改讀含國界的原始 shapefile。）

做法：只用標準函式庫解析 .shp/.dbf → shapely 依範圍裁切 → Douglas–Peucker 簡化 →
座標量化成 0.01° 整數（lon×100, lat×100）存成扁平陣列。投影在頁面內計算。
執行：~/.manim-env/bin/python build_geo_js.py   （需要 shapely；~/.manim-env 已安裝）
"""
import io, json, struct, zipfile
from pathlib import Path
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.validation import make_valid

ZIP = Path.home() / ".cache/geo-map-video/ne_50m_admin_0_countries.zip"
OUT = Path(__file__).resolve().parent.parent / "data" / "geo_europe.js"

# 範圍與簡化容許度（度）
EUROPE_BOX = (-28.0, 33.0, 44.0, 72.5)      # lon0, lat0, lon1, lat1：歐洲＋愛爾蘭＋挪威＋義大利中部
EUROPE_TOL = 0.012                          # 約 1 km：下奧地利放大框也夠用
NA_BOX = (-100.0, 24.0, -50.0, 56.0)        # 北美東北部：只給「大西洋彼岸」定位小圖用
NA_TOL = 0.12
DROP_AREA = 0.004                           # 平方度：太小的島嶼略去


def read_dbf(b):
    n = struct.unpack("<I", b[4:8])[0]
    hlen, rlen = struct.unpack("<HH", b[8:12])
    fields, off = [], 32
    while b[off] != 0x0D:
        name = b[off:off + 11].split(b"\0")[0].decode()
        fields.append((name, b[off + 16]))
        off += 32
    recs = []
    for i in range(n):
        r = b[hlen + i * rlen: hlen + (i + 1) * rlen]
        p, d = 1, {}
        for name, ln in fields:
            d[name] = r[p:p + ln].decode("utf-8", "ignore").strip("\0 ")
            p += ln
        recs.append(d)
    return recs


def signed_area(ring):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1])) / 2


def read_shp(b):
    off, shapes = 100, []
    while off < len(b):
        clen = struct.unpack(">I", b[off + 4:off + 8])[0] * 2
        rec = b[off + 8: off + 8 + clen]
        off += 8 + clen
        st = struct.unpack("<i", rec[0:4])[0]
        if st != 5:
            shapes.append(None); continue
        nparts, npts = struct.unpack("<ii", rec[36:44])
        parts = list(struct.unpack(f"<{nparts}i", rec[44:44 + 4 * nparts])) + [npts]
        pts = struct.unpack(f"<{2 * npts}d", rec[44 + 4 * nparts: 44 + 4 * nparts + 16 * npts])
        rings = [[(pts[2 * k], pts[2 * k + 1]) for k in range(parts[j], parts[j + 1])] for j in range(nparts)]
        # shapefile：外環順時針（面積 < 0），內環逆時針
        polys = []
        for r in rings:
            if signed_area(r) <= 0:
                polys.append([r, []])
            elif polys:
                polys[-1][1].append(r)
        shapes.append(MultiPolygon([Polygon(s, h) for s, h in polys]))
    return shapes


def pack(geom, bbox, tol):
    g = make_valid(geom).intersection(box(*bbox))
    if g.is_empty:
        return []
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
    out = []
    for p in polys:
        if p.area < DROP_AREA:
            continue
        ring = list(p.exterior.coords)[:-1]
        flat = []
        for x, y in ring:
            flat += [round(x * 100), round(y * 100)]
        if len(flat) >= 6:
            out.append(flat)
    return out


def main():
    z = zipfile.ZipFile(ZIP)
    stem = "ne_50m_admin_0_countries"
    recs = read_dbf(z.read(stem + ".dbf"))
    shapes = read_shp(z.read(stem + ".shp"))
    version = z.read(stem + ".VERSION.txt").decode().strip()
    eu, na = [], []
    for d, g in zip(recs, shapes):
        if g is None:
            continue
        a3 = d.get("ADM0_A3")
        zh = d.get("NAME_ZHT") or d.get("NAME_ZH") or d.get("NAME")
        r = pack(g, EUROPE_BOX, EUROPE_TOL)
        if r:
            eu.append({"a3": a3, "zh": zh, "en": d.get("NAME"), "p": r})
        if a3 in ("USA", "CAN"):
            r2 = pack(g, NA_BOX, NA_TOL)
            if r2:
                na.append({"a3": a3, "zh": zh, "en": d.get("NAME"), "p": r2})
    data = {
        "src": f"Natural Earth 1:50m Admin 0 Countries v{version}（公有領域）；國界為現今國界",
        "q": 100, "box": EUROPE_BOX, "naBox": NA_BOX, "tol": [EUROPE_TOL, NA_TOL],
        "countries": eu, "na": na,
    }
    js = "// 由 _units/build_geo_js.py 產生，請勿手改。\nwindow.GEO_EUROPE = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(js, encoding="utf-8")
    npts = sum(len(f) // 2 for c in eu + na for f in c["p"])
    print(f"{OUT.name}: {len(eu)} 國（歐洲範圍）＋ {len(na)} 國（北美定位），{npts} 點，{len(js.encode()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
