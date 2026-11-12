import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mcp_client import C
import rig
OUT = os.path.join(HERE, "out").replace("\\", "/"); os.makedirs(OUT, exist_ok=True)
ALL = rig.LAYERS + ["lines", "outline"]
c = C()
for which in sys.argv[1:]:
    t0 = time.time(); n, durs = rig.ANIMS[which]
    frames = [rig.rasterize(rig.build(rig.pose(which, i))) for i in range(n)]
    path = json.loads(c.call("create_canvas", {"width": rig.W, "height": rig.H, "color_mode": "rgb"}))["file_path"]
    c.call("set_palette", {"sprite_path": path, "colors": rig.palette()})
    for l in ALL: c.call("add_layer", {"sprite_path": path, "layer_name": l})
    for i in range(1, n): c.call("add_frame", {"sprite_path": path, "duration_ms": durs[i]})
    c.call("set_frame_duration", {"sprite_path": path, "frame_number": 1, "duration_ms": durs[0]})
    for i, b in enumerate(frames):
        for l in ALL:
            px = [{"x": x, "y": y, "color": col} for (x, y), col in sorted(b[l].items(), key=lambda t: (t[0][1], t[0][0]))]
            for k in range(0, len(px), 6000):
                c.call("draw_pixels", {"sprite_path": path, "layer_name": l, "frame_number": i + 1, "pixels": px[k:k + 6000]})
    c.call("create_tag", {"sprite_path": path, "tag_name": which, "from_frame": 1, "to_frame": n, "direction": "forward"})
    f = f"{OUT}/knight_{which}.aseprite"
    c.call("save_as", {"sprite_path": path, "output_path": f})
    c.call("export_sprite", {"sprite_path": f, "output_path": f"{OUT}/knight_{which}.gif", "format": "gif", "frame_number": 0})
    c.call("export_sprite", {"sprite_path": f, "output_path": f"{OUT}/knight_{which}_f1.png", "format": "png", "frame_number": 1})
    c.call("export_spritesheet", {"sprite_path": f, "output_path": f"{OUT}/knight_{which}_sheet.png", "layout": "horizontal", "padding": 0, "include_json": True})
    prev = f"{OUT}/knight_{which}_x3.aseprite"
    c.call("save_as", {"sprite_path": f, "output_path": prev})
    c.call("scale_sprite", {"sprite_path": prev, "scale_x": 3, "scale_y": 3, "algorithm": "nearest"})
    c.call("export_sprite", {"sprite_path": prev, "output_path": f"{OUT}/knight_{which}_x3.gif", "format": "gif", "frame_number": 0})
    os.remove(prev.replace("/", os.sep)) if os.path.exists(prev.replace("/", os.sep)) else None
    print(which, "done", round(time.time() - t0), "s", flush=True)
