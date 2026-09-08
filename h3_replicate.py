#!/usr/bin/env python3
"""Submit a localized product-video recreation to the Compshare MiniMax H3 API.

The source clip is used only as a visual/camera reference.  The supplied
product image is the identity anchor and the supplied audio is the only final
voice track.  Local files are sent as Data URLs because the Compshare model
key does not authorize the separate file-upload endpoint.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import requests

API_MANAGER = Path(r"C:\Users\Administrator\.codex\skills\api-manager\scripts")
sys.path.insert(0, str(API_MANAGER))
from api_manager import resolve_provider  # noqa: E402


ROOT = Path(__file__).resolve().parent
PROVIDER = "compshare_mmh3"
SUCCESS = {"succeeded", "success", "completed", "done"}
FAILED = {"failed", "fail", "cancelled", "canceled", "expired", "error"}


def cfg():
    c = resolve_provider(PROVIDER)
    if not c.get("api_key"):
        raise RuntimeError("COMPSHARE_MMH3_API_KEY is not set")
    return c


def headers(c):
    return {
        "Authorization": f"Bearer {c['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def data_url(path: Path) -> str:
    kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{kind};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def query_points(c):
    p = c["endpoints"]["query_points"]["path"]
    r = requests.get(c["base_url"].rstrip("/") + p,
                     headers={"Authorization": f"Bearer {c['api_key']}", "Accept": "application/json"},
                     timeout=60)
    r.raise_for_status()
    return r.json()


def submit(c, item, product_url, video_url, audio_url, resolution="768P", visual_mode="product_first"):
    content = [{"type": "text", "text": item["prompt"]}]
    # The API forbids mixing first/last-frame inputs with reference videos.
    # Product-first is the safer mode for a brand swap: it protects the real
    # package artwork, while the prompt reconstructs the source shot rhythm.
    if visual_mode == "reference_video":
        content.append({"type": "image_url", "image_url": {"url": product_url}, "role": "reference_image"})
        content.append({"type": "video_url", "video_url": {"url": video_url}, "role": "reference_video"})
    elif visual_mode == "image_only":
        content.append({"type": "image_url", "image_url": {"url": product_url}, "role": "reference_image"})
    else:
        content.append({"type": "image_url", "image_url": {"url": product_url}, "role": "first_frame"})
    # Compshare currently rejects first_frame + reference_audio together.  In
    # first_frame mode the narration is muxed back after visual generation.
    if visual_mode != "first_frame":
        content.append({"type": "audio_url", "audio_url": {"url": audio_url}, "role": "reference_audio"})
    body = {
        "model": "MiniMax-H3",
        "content": content,
        "resolution": resolution,
        "duration": int(item["duration"]),
        "ratio": "3:4",
        "use_context_ir": False,
        "mute_audio": False,
        "aigc_watermark": False,
    }
    endpoint = c["base_url"].rstrip("/") + c["endpoints"]["create_video"]["path"]
    # A unique idempotency key makes retries safe without accidentally
    # returning an earlier task from another run.
    h = dict(headers(c))
    h["Idempotency-Key"] = f"h3-replica-20260907-{item.get('run_tag', 'default')}-{item['id']}"
    r = requests.post(endpoint, headers=h, json=body, timeout=180)
    if r.status_code >= 400:
        raise RuntimeError(f"{item['id']} submit HTTP {r.status_code}: {r.text[:500]}")
    j = r.json()
    tid = j.get("task_id") or (j.get("task") or {}).get("id")
    if not tid:
        raise RuntimeError(f"{item['id']} submit returned no task_id: {json.dumps(j, ensure_ascii=False)[:500]}")
    return str(tid)


def query(c, task_id):
    path = c["endpoints"]["query_video"]["path"].replace("{task_id}", task_id)
    r = requests.get(c["base_url"].rstrip("/") + path,
                     headers={"Authorization": f"Bearer {c['api_key']}", "Accept": "application/json"},
                     timeout=60)
    r.raise_for_status()
    return r.json()


def wait_task(c, item, task_id, out_path: Path, timeout_s=1800):
    started = time.time()
    last_status = None
    while time.time() - started < timeout_s:
        j = query(c, task_id)
        task = j.get("task") or j
        status = str(task.get("status", "")).lower()
        url = (task.get("content") or {}).get("url")
        if status != last_status:
            print(f"[{item['id']}] status={status or 'unknown'} task={task_id}", flush=True)
            last_status = status
        if url:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, out_path)
            if out_path.stat().st_size < 10240:
                raise RuntimeError(f"{item['id']} result is unexpectedly small")
            meta = {"task_id": task_id, "task": task}
            out_path.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            return
        if status in FAILED:
            raise RuntimeError(f"{item['id']} failed: {json.dumps(task.get('error'), ensure_ascii=False)}")
        time.sleep(10)
    raise TimeoutError(f"{item['id']} still pending after {timeout_s}s; task={task_id}")


def ffmpeg_cmd(*args):
    exe = ROOT / "tools" / "ffmpeg" / "bin" / "ffmpeg.exe"
    if not exe.exists():
        exe = Path("ffmpeg")
    return [str(exe), *map(str, args)]


def run_ffprobe(path: Path):
    exe = ROOT / "tools" / "ffmpeg" / "bin" / "ffprobe.exe"
    if not exe.exists():
        exe = Path("ffprobe")
    r = subprocess.run([str(exe), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def make_source_segment(source: Path, start: float, end: float, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(ffmpeg_cmd("-y", "-ss", start, "-to", end, "-i", source,
                              "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", out),
                   check=True, capture_output=True)


def make_audio_segment(mp3: Path, target: int, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    # Pad each narration to the requested H3 duration.  This keeps visual
    # timing stable while retaining the complete spoken copy in the master.
    # The bundled FFmpeg is an older build; use apad=whole_len (samples)
    # rather than the newer pad_dur option.
    subprocess.run(ffmpeg_cmd("-y", "-i", mp3, "-af", f"apad=whole_len={target * 44100},atrim=0:{target}",
                              "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", out),
                   check=True, capture_output=True)


def concat_video(clips: list[Path], out: Path):
    list_file = out.with_suffix(".concat.txt")
    list_file.write_text("\n".join("file '" + str(p).replace("'", "'\\''") + "'" for p in clips), encoding="utf-8")
    subprocess.run(ffmpeg_cmd("-y", "-f", "concat", "-safe", "0", "-i", list_file,
                              "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out),
                   check=True, capture_output=True)


def concat_audio(audios: list[Path], out: Path):
    list_file = out.with_suffix(".concat.txt")
    list_file.write_text("\n".join("file '" + str(p).replace("'", "'\\''") + "'" for p in audios), encoding="utf-8")
    subprocess.run(ffmpeg_cmd("-y", "-f", "concat", "-safe", "0", "-i", list_file,
                              "-c:a", "pcm_s16le", out), check=True, capture_output=True)


def mux(video: Path, audio: Path, out: Path):
    subprocess.run(ffmpeg_cmd("-y", "-i", video, "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
                              "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out),
                   check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=Path(r"D:\企微存储\WXWork\1688855633891784\Cache\Video\2026-09\video.mp4"))
    ap.add_argument("--out-dir", type=Path, default=ROOT / "run" / "h3_20260907")
    ap.add_argument("--only", nargs="*", default=None, help="only submit these segment ids")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--skip-submit", action="store_true")
    ap.add_argument("--visual-mode", choices=["first_frame", "image_only", "reference_video"], default="image_only",
                    help="image_only protects the supplied package image; reference_video follows the source motion more closely")
    args = ap.parse_args()

    out = args.out_dir
    source = args.source
    product = ROOT / "run" / "source_20260907" / "assets" / "changwang-parrot-feed.png"
    if not source.exists() or not product.exists():
        raise FileNotFoundError("source video or Changwang product anchor is missing")

    # Boundaries follow the localized shotlist: opening/nature, ecology, grain
    # claims, feeding, and brand close.  The last segment is allowed to expand
    # so the complete closing line is audible instead of being cut off.
    specs = [
        ("H1", 0.00, 6.50, "从林间枝头的自在啄食，到居家日常喂养，选择鹦鹉专用粮。"),
        ("H2", 6.50, 12.67, "无抗配方，益生菌营养。"),
        ("H3", 12.67, 18.71, "100亿益生菌，8种维生素，2重必需氨基酸，6种微量元素。"),
        ("H4", 18.71, 23.75, "0添加色素及抗生素，真材实料一眼可见。"),
        ("H5", 23.75, 29.88, "益生菌营养鹦鹉专用粮，从幼鸟到成鸟，做好日常喂养。"),
        ("H6", 29.88, 33.17, "新希望六和·畅旺，益生菌营养鹦鹉专用粮，做好鹦鹉日常喂养。"),
    ]
    base_prompt = (
        "subject_definitions: The supplied reference video is the exact camera, cut and action reference. "
        "Image 1 is the only product identity anchor: New Hope Liuhe Changwang probiotic nutrition parrot food, "
        "a green and pale-blue 500 g stand-up bag. Preserve its real Chinese packaging, logo, bird illustration and nutrition panel exactly. "
        "Never show the original brown jar, ZaiZai/再再 branding, 虎皮粮 label, or any other package.\n"
        "summary: Recreate this vertical 3:4 ecommerce nature-film sequence with the same shot order and calm premium pacing, "
        "but replace every product appearance with the supplied Changwang bag and its real food grains.\n"
        "retention_analysis: Retain the reference video's fixed-camera compositions, hard cuts, gentle pushes, tropical forest light, "
        "parrot perching and feeding, grain macro photography, and final product hero framing. Product identity and all on-screen product claims come only from Image 1.\n"
        "detailed_description: {segment}\n"
        "overall_soundscape: Audio 1 is the complete supplied Mandarin narration track. Reuse it directly as the only spoken audio; "
        "do not invent dialogue, subtitles, extra voices or lip-sync speech.\n"
        "non_diegetic_music: No added music, sound effects or watermark. Keep the natural ambience subtle under Audio 1."
    )
    segments = []
    for sid, start, end, text in specs:
        # H3 duration is integer seconds; the final line is intentionally
        # allowed to determine its own longer duration after TTS is rendered.
        requested = max(4, int(math.ceil(end - start)))
        segments.append({"id": sid, "start": start, "end": end, "duration": requested, "text": text,
                         "prompt": base_prompt.format(segment=(
                             f"[Shot A] At 00:00.000, reproduce the opening material from {start:.2f}s to {end:.2f}s of the reference: "
                             "use the same nature, parrot or grain actions and camera movement, with clean green-gold natural light. "
                             "Use only the supplied Changwang package whenever a package or food product appears."
                         ))})
    if args.only:
        wanted = set(args.only)
        segments = [s for s in segments if s["id"] in wanted]
    for s in segments:
        s["run_tag"] = out.name
    (out / "segments.json").parent.mkdir(parents=True, exist_ok=True)
    (out / "segments.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")

    source_dir = out / "reference_video"
    audio_dir = out / "audio"
    source_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    for s in segments:
        src = source_dir / f"{s['id']}.mp4"
        mp3 = audio_dir / f"{s['id']}.mp3"
        wav = audio_dir / f"{s['id']}.wav"
        if not src.exists():
            make_source_segment(source, s["start"], s["end"], src)
        if not mp3.exists() or mp3.stat().st_size < 1024:
            # edge-tts is used only as a local TTS fallback when CosyVoice is
            # unavailable; the resulting audio is still passed to H3 as the
            # reference_audio track and muxed into the final output.
            subprocess.run([sys.executable, "-m", "edge_tts", "--voice", "zh-CN-XiaoxiaoNeural",
                            "--rate", "+0%", "--text", s["text"], "--write-media", str(mp3)], check=True)
        # Keep the complete spoken line.  The reference picture duration is
        # only a floor; a longer closing line is allowed to extend its H3
        # segment instead of being truncated.
        s["duration"] = max(int(s["duration"]), int(math.ceil(run_ffprobe(mp3))))
        wav_duration = run_ffprobe(wav) if wav.exists() and wav.stat().st_size >= 1024 else 0
        if wav_duration < s["duration"] - 0.05 or wav_duration > s["duration"] + 0.05:
            make_audio_segment(mp3, s["duration"], wav)
        s["source_video"] = str(src)
        s["audio"] = str(wav)
    (out / "segments.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.prepare_only:
        print(f"Prepared {len(segments)} segments in {out}")
        return

    c = cfg()
    points = query_points(c)
    print(f"provider={c['base_url']} model=MiniMax-H3 available_points={points.get('available_points')}")
    # 10 points/sec at 768P; input reference video usage is reported by the
    # service separately.  Stop before submitting if the documented output
    # estimate alone cannot fit the available balance.
    estimated = sum(int(s["duration"]) for s in segments) * 10
    if int(points.get("available_points", 0)) < estimated:
        raise RuntimeError(f"available points {points.get('available_points')} < output estimate {estimated}")
    product_url = data_url(product)
    for s in segments:
        if args.skip_submit:
            continue
        meta_path = out / "clips" / f"{s['id']}.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            s["task_id"] = meta["task_id"]
            continue
        tid = submit(c, s, product_url, data_url(Path(s["source_video"])), data_url(Path(s["audio"])),
                     visual_mode=args.visual_mode)
        s["task_id"] = tid
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps({"task_id": tid, "segment": s["id"]}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{s['id']}] submitted task_id={tid}")
    (out / "segments.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.skip_submit:
        return

    clips = []
    audios = []
    for s in segments:
        clip = out / "clips" / f"{s['id']}.mp4"
        if not clip.exists():
            wait_task(c, s, s["task_id"], clip)
        clips.append(clip)
        audios.append(Path(s["audio"]))
    video_only = out / "video_only.mp4"
    master_audio = out / "master_audio.wav"
    final = out / "minimax_h3_replica.mp4"
    concat_video(clips, video_only)
    concat_audio(audios, master_audio)
    mux(video_only, master_audio, final)
    manifest = {"model": "MiniMax-H3", "provider": c["base_url"], "segments": segments,
                "available_points_before": points.get("available_points"),
                "output_estimate_points": estimated, "final": str(final),
                "final_duration_s": run_ffprobe(final)}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"DONE final={final} duration={manifest['final_duration_s']:.3f}s")


if __name__ == "__main__":
    main()
