#!/usr/bin/env python3
"""compshare_gen.py — 模型广场(compshare) MiniMax H3 视频生成脚本
直接调用官方规范 API，参考图+参考音频模式，提交→轮询→下载。
"""
import json, os, sys, time, urllib.request

BASE = "https://cp.compshare.cn"
API_KEY = "sk-ml-5RGa2lXhtLeS8W0Y2Ju-v4MtJiOq8riOVzCq-sSbRWg"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def submit(prompt, image_urls, audio_url, duration=5, ratio="9:16"):
    content = [{"type": "text", "text": prompt}]
    for url in image_urls:
        content.append({"type": "image_url", "image_url": {"url": url}, "role": "reference_image"})
    if audio_url:
        content.append({"type": "audio_url", "audio_url": {"url": audio_url}, "role": "reference_audio"})
    body = {
        "model": "MiniMax-H3",
        "content": content,
        "resolution": "768P",
        "duration": duration,
        "ratio": ratio,
        "aigc_watermark": False,
    }
    req = urllib.request.Request(f"{BASE}/minimax/v2/video_generation",
                                  data=json.dumps(body).encode(), headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())
    return resp.get("task_id")

def query(task_id):
    req = urllib.request.Request(f"{BASE}/minimax/v2/query/video_generation/{task_id}",
                                  headers=HEADERS, method="GET")
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
    return resp.get("task", {})

def download(url, dst):
    urllib.request.urlretrieve(url, dst)
    return os.path.getsize(dst)

def wait_and_download(task_id, dst, max_wait=600, gap=10):
    start = time.time()
    while time.time() - start < max_wait:
        task = query(task_id)
        status = task.get("status")
        elapsed = int(time.time() - start)
        print(f"  [{elapsed}s] status={status}", flush=True)
        if status in ("succeeded", "completed", "done"):
            url = task.get("content", {}).get("url")
            if url:
                size = download(url, dst)
                print(f"  下载完成: {dst} ({size} bytes)", flush=True)
                return size
            else:
                print("  成功但无视频URL", flush=True)
                return None
        if status in ("failed", "error", "cancelled"):
            err = task.get("error", {})
            print(f"  失败: {err}", flush=True)
            return None
        time.sleep(gap)
    print(f"  超时({max_wait}s)，task_id={task_id} 可后续手动查询", flush=True)
    return None

if __name__ == "__main__":
    # T01 配置
    prompt = """subject_definitions: The reference images define the exact same grey-and-pale-blue parrot, the same white round ceramic bowl, the orange-red flower-shaped grain scoop, the brown monogram patterned tabletop and the wooden cabinet background. Preserve this individual bird and every object identity.
summary: Recreate the original indoor tabletop opening in a vertical 9:16 frame. The orange-red scoop pours a colorful mixed bird-food blend into the white round bowl while the unchanged grey-and-pale-blue parrot stands beside it and begins pecking.
retention_analysis: Preserve the source framing, shallow depth of field, warm indoor light, hand motion, scoop angle, bowl shape, tabletop pattern and the bird's exact plumage and scale. Do not replace the parrot, bowl, scoop or room. Do not add a new package, text, captions, logo or watermark.
detailed_description: [Shot 1] At 00:00.000, show the white round bowl on the brown patterned tabletop and the orange-red scoop entering from the upper left. [Shot 2] At 00:01.500, pour mixed grains into the bowl with believable falling motion. [Shot 3] At 00:03.200, cut to the same grey-and-pale-blue parrot lowering its head toward the bowl and pecking naturally. Keep the cabinet and indoor background softly blurred. Hold until 00:05.000.
overall_soundscape: Use the supplied reference audio as the only voice track; no invented dialogue or subtitles.
non_diegetic_music: Preserve the source's quiet indoor ambience. No added music, watermark or platform overlay."""

    image_urls = [
        "https://aka.doubaocdn.com/s/rrZn9geOiF",  # source_01.50.png
        "https://aka.doubaocdn.com/s/3UcEq48yUi",  # source_03.20.png
    ]
    audio_url = "https://aka.doubaocdn.com/s/EmPTmUFGXz"  # T01.wav

    out_dir = r"D:\vibe 电商\一键复刻爆款视频\豆包专属工作区\redo_20260908\clips"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "T01.mp4")

    print("=== 提交 T01 ===", flush=True)
    print(f"  时长: 5s, 比例: 9:16, 参考图: {len(image_urls)}张, 音频: 有", flush=True)
    task_id = submit(prompt, image_urls, audio_url, duration=5, ratio="9:16")
    print(f"  task_id: {task_id}", flush=True)
    print("=== 轮询中 ===", flush=True)
    size = wait_and_download(task_id, dst, max_wait=600, gap=10)
    if size:
        print(f"\n=== T01 生成完成 ===")
        print(f"  文件: {dst}")
        print(f"  大小: {size} bytes")
    else:
        print(f"\n=== T01 生成失败或超时 ===")
        print(f"  task_id: {task_id}")
        sys.exit(1)
