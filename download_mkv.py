import os
import time
import requests
import libtorrent as lt

# -------------------------------
# 1️⃣ Configuration
# -------------------------------
TORRENT_URL = "https://raw.githubusercontent.com/pothabattulavinod/vs/refs/heads/main/www.1TamilMV.cool%20-%20Mirai%20(2025)%20Telugu%20HQ%20HDRip%20-%20x264%20-%20AAC%20-%20400MB%20-%20ESub.mkv.torrent"
TORRENT_FILE = "download/movie.torrent"
DOWNLOAD_DIR = "download/mkv"
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs("download", exist_ok=True)

# -------------------------------
# 2️⃣ Download torrent file
# -------------------------------
print("📥 Downloading torrent file...")
r = requests.get(TORRENT_URL)
if r.status_code == 200:
    with open(TORRENT_FILE, "wb") as f:
        f.write(r.content)
    print(f"✅ Torrent file downloaded: {TORRENT_FILE}")
else:
    print("❌ Failed to download torrent file")
    exit(1)

# -------------------------------
# 3️⃣ Download MKV from torrent
# -------------------------------
for attempt in range(1, MAX_RETRIES + 1):
    print(f"🚀 Attempt {attempt} to download MKV...")

    ses = lt.session()
    ses.listen_on(6881, 6891)
    info = lt.torrent_info(TORRENT_FILE)
    handle = ses.add_torrent({
        'ti': info,
        'save_path': DOWNLOAD_DIR
    })

    print(f"⏳ Downloading: {info.name()} ({info.total_size() / 1024 / 1024:.2f} MB)")

    while not handle.is_seed():
        s = handle.status()
        print(f"\rProgress: {s.progress * 100:.2f}% | "
              f"Down: {s.download_rate / 1000:.1f} kB/s | "
              f"Up: {s.upload_rate / 1000:.1f} kB/s | "
              f"Peers: {s.num_peers}", end="")
        time.sleep(1)
    print("\n✅ Download completed!")

    # Check for MKV
    mkv_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".mkv")]
    if mkv_files:
        print(f"✅ MKV file: {os.path.join(DOWNLOAD_DIR, mkv_files[0])}")
        break
    else:
        print(f"⚠️ MKV not found, retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)
else:
    print(f"❌ MKV download failed after {MAX_RETRIES} attempts.")
    exit(1)
