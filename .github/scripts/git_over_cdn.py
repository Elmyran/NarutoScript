import argparse
import json
import os
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path

# Cloudflare Worker 单文件上限 25MB，24MB 留出余量
MAX_PACK_BYTES = 24 * 1024 * 1024


def run_git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def fmt_bytes(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def build_pack(latest, old, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    pack = output_dir / f"pack-{latest}.pack"
    idx = output_dir / f"pack-{latest}.idx"
    zip_path = output_dir / f"{old}.zip"

    revs = f"{latest}\n^{old}\n".encode("ascii")
    with pack.open("wb") as f:
        subprocess.run(
            ["git", "pack-objects", "--revs", "--stdout"],
            input=revs,
            stdout=f,
            check=True,
        )

    subprocess.run(
        ["git", "index-pack", "-o", str(idx), str(pack)],
        stdout=subprocess.DEVNULL,
        check=True,
    )

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        zipped.write(pack, pack.name)
        zipped.write(idx, idx.name)

    size = zip_path.stat().st_size
    if size > MAX_PACK_BYTES:
        # 超出 Worker 单文件存储上限，生成也无法上传，直接清理
        for path in (zip_path, pack, idx):
            path.chmod(stat.S_IWRITE)
            path.unlink()
        print(f"  skip {old}.zip ({fmt_bytes(size)} > {fmt_bytes(MAX_PACK_BYTES)})")
        return None

    return zip_path


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path):
    shutil.rmtree(path, onerror=remove_readonly)


def cleanup_pack_artifacts(output_dir):
    for pattern in ("pack-*.pack", "pack-*.idx", "pack-*.rev"):
        for path in output_dir.glob(pattern):
            path.chmod(stat.S_IWRITE)
            path.unlink()


def main():
    parser = argparse.ArgumentParser(description="Build git-over-cdn update packs.")
    parser.add_argument("--branch", default="master")
    parser.add_argument("--history", type=int, default=1)
    parser.add_argument("--output", default="dist/git-over-cdn")
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists():
        remove_tree(output)
    output.mkdir(parents=True)

    latest = run_git("rev-parse", args.branch)
    commits = run_git("rev-list", "--first-parent", f"--max-count={args.history + 1}", args.branch).splitlines()
    old_commits = [commit for commit in commits if commit != latest]

    (output / "latest.json").write_text(
        json.dumps({"commit": latest}, indent=2) + "\n",
        encoding="utf-8",
    )

    latest_dir = output / latest
    skipped = 0
    for old in old_commits:
        latest_dir.mkdir(parents=True, exist_ok=True)
        if build_pack(latest=latest, old=old, output_dir=latest_dir) is None:
            skipped += 1
    cleanup_pack_artifacts(latest_dir)

    print(f"Generated {len(old_commits) - skipped} update pack(s)")
    if skipped > 0:
        print(
            f"Skipped {skipped} update pack(s) larger than "
            f"{fmt_bytes(MAX_PACK_BYTES)} (Cloudflare Worker file limit)"
        )
    print("*" * 20)


if __name__ == "__main__":
    main()
