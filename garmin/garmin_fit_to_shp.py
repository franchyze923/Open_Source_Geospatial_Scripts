#!/usr/bin/env python3
# FIT -> Shapefile (points) with lat/lon, altitude (m & ft), per-record timestamp, zipped

import argparse, os, zipfile
from fitparse import FitFile
import geopandas as gpd
from shapely.geometry import Point

def semi_to_deg(v):
    if v is None:
        return None
    return (v * 180.0 / (2**31)) if isinstance(v, (int, float)) and abs(v) > 1000 else v

def meters_to_feet(m):
    return m * 3.28084 if m is not None else None

def main():
    ap = argparse.ArgumentParser(description="FIT -> Shapefile (points with lat/lon/alt m+ft), zipped")
    ap.add_argument("fit_path", help="Path to .FIT file")
    ap.add_argument("-o", "--out", default="activity_points.shp", help="Output .shp path")
    args = ap.parse_args()

    ff = FitFile(args.fit_path)

    rows = []
    for rec in ff.get_messages("record"):
        row = {f.name: f.value for f in rec}
        ts  = row.get("timestamp")
        lat = semi_to_deg(row.get("position_lat"))
        lon = semi_to_deg(row.get("position_long"))
        alt_m = row.get("altitude") or row.get("enhanced_altitude")
        alt_ft = meters_to_feet(alt_m)

        if lat is None or lon is None:
            continue

        rows.append({
            "ts": str(ts),
            "lat": float(lat),
            "lon": float(lon),
            "alt_m": float(alt_m) if alt_m is not None else None,
            "alt_ft": float(alt_ft) if alt_ft is not None else None,
            "hr": row.get("heart_rate"),
            "cad": row.get("cadence"),
            "spd_m_s": row.get("speed") or row.get("enhanced_speed"),
            "pwr": row.get("power"),
            "geometry": Point(float(lon), float(lat)),
        })

    if not rows:
        raise SystemExit("No GPS records found in this FIT file.")

    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
    out_shp = args.out
    gdf.to_file(out_shp, driver="ESRI Shapefile")

    base = os.path.splitext(out_shp)[0]
    zip_path = f"{base}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for ext in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
            f = base + ext
            if os.path.exists(f):
                zf.write(f, os.path.basename(f))

    print(f"✅ Wrote & zipped -> {zip_path} (CRS: EPSG:4326)")

if __name__ == "__main__":
    main()
