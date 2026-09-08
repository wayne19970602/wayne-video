"""Generate the v2 per-segment keyframes with the local imagegen skill only."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "run" / "target_20260907_v2" / "source_frames"
OUT = ROOT / "output" / "imagegen" / "target_20260907_v2"
PRODUCT = ROOT / "run" / "target_20260907_v2" / "assets" / "changwang-parrot-feed.png"
CLI = Path(r"C:\Users\Administrator\.codex\skills\imagegen\scripts\image_gen.py")

PRODUCT_PROMPT = (
    "编辑这张源视频帧，保留原始森林、树枝、植物、鹦鹉、食盆、机位、景别、光线和构图。"
    "把画面中旧的 ZaiZai/再再/虎皮鹦鹉粮罐、旧品牌、旧字幕和旧卖点全部替换掉；"
    "用第二张用户真实产品图中的同一款新希望六和·畅旺益生菌营养鹦鹉专用粮袋替换，"
    "产品袋的颜色、形状、logo、包装印刷和品牌文字必须来自用户参考图，保持清晰完整，"
    "不要让产品消失，不要重新设计包装，不要生成新的宣传语、功效、价格、logo、水印或其他品牌。"
    "画面外的旧字幕全部清除，保留自然电商摄影质感，3:4 竖幅。"
)

SCENE_PROMPT = (
    "编辑这张源视频帧，保留原片真实的场景主体、动作状态、镜位、景别、光线、颜色和空间关系。"
    "清除画面中所有旧品牌、旧产品、旧字幕、旧卖点、logo 和水印；这是一段不需要产品出镜的场景，"
    "绝对不要出现任何产品包装、品牌标识或商业文字。不要添加新文字，不要改成棚拍，不要改变鸟、"
    "树枝、城市、溪流、谷物或种子本身的真实内容。自然写实，3:4 竖幅。"
)

PRODUCT_JOBS = [
    ("V01", "start", "source_00.08.png"),
    ("V01", "end", "source_02.92.png"),
    ("V04", "start", "source_10.38.png"),
    ("V04", "end", "source_12.58.png"),
    ("V09", "start", "source_29.98.png"),
    ("V09", "end", "source_33.08.png"),
]
SCENE_JOBS = [
    ("V02", "start", "source_03.08.png"),
    ("V02", "end", "source_04.55.png"),
    ("V03", "start", "source_06.58.png"),
    ("V03", "end", "source_10.20.png"),
    ("V05", "start", "source_12.76.png"),
    ("V05", "end", "source_18.86.png"),
    ("V06", "start", "source_19.18.png"),
    ("V06", "end", "source_23.65.png"),
    ("V07", "start", "source_23.90.png"),
    ("V07", "end", "source_26.02.png"),
    ("V08", "start", "source_26.25.png"),
    ("V08", "end", "source_29.78.png"),
]

def run_job(job, product=False):
    seg, edge, source_name = job
    source = SOURCE / source_name
    out = OUT / f"{seg}-{edge}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    prompt = PRODUCT_PROMPT if product else SCENE_PROMPT
    cmd = [sys.executable, str(CLI), "edit", "--image", str(source)]
    if product:
        cmd += ["--image", str(PRODUCT)]
    cmd += [
        "--prompt", prompt, "--aspect-ratio", "3:4", "--out", str(out),
        "--max-attempts", "2", "--timeout", "240", "--force",
    ]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{seg}-{edge} failed ({result.returncode}): {result.stderr[-1200:]}")
    return seg, edge, out, result.stdout[-800:]

def main():
    jobs = [(j, True) for j in PRODUCT_JOBS] + [(j, False) for j in SCENE_JOBS]
    missing = [str(SOURCE / j[2]) for j, _ in jobs if not (SOURCE / j[2]).exists()]
    if missing or not PRODUCT.exists():
        raise SystemExit(f"missing inputs: {missing}; product={PRODUCT.exists()}")
    print(f"[imagegen-v2] jobs={len(jobs)} out={OUT}", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run_job, j, product) for j, product in jobs]
        for fut in as_completed(futures):
            seg, edge, out, tail = fut.result()
            print(f"[imagegen-v2] done {seg}-{edge}: {out} ({out.stat().st_size} bytes)", flush=True)
    print("[imagegen-v2] complete", flush=True)

if __name__ == "__main__":
    main()
