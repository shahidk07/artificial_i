from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import threading
import json
import re

# ==========================================
# SETTINGS
# ==========================================

INPUT_FILE = "youtube_links_2.csv"

OUTPUT_FILE = "youtube_videos.csv"

MAX_THREADS = 10

# ==========================================
# LOAD CSV
# ==========================================

df = pd.read_csv(INPUT_FILE)

if "description" not in df.columns:
    df["description"] = ""

# ==========================================
# THREAD LOCK
# ==========================================

lock = threading.Lock()

# ==========================================
# GET DESCRIPTION USING REQUESTS
# ==========================================

def get_description(index, row):

    try:

        print(f"{index+1}. {row['title']}")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        }

        response = requests.get(
            row["url"],
            headers=headers,
            timeout=15
        )

        html = response.text

        # ==========================================
        # EXTRACT DESCRIPTION
        # ==========================================

        match = re.search(
            r'"shortDescription":"(.*?)","isCrawlable"',
            html
        )

        if match:

            description = match.group(1)

            # clean text
            description = (
                description
                .replace("\\n", "\n")
                .replace('\\"', '"')
                .replace("\\\\", "\\")
                .replace("\\u0026", "&")
            )

        else:

            description = "No description found"

        # ==========================================
        # THREAD SAFE SAVE
        # ==========================================

        with lock:

            df.at[index, "description"] = description

            # auto save progress
            df.to_csv(
                OUTPUT_FILE,
                index=False,
                encoding="utf-8"
            )

            print("Saved:", row["title"])

    except Exception as e:

        print("Error:", e)

# ==========================================
# MULTITHREADING
# ==========================================

with ThreadPoolExecutor(
    max_workers=MAX_THREADS
) as executor:

    futures = []

    for index, row in df.iterrows():

        futures.append(
            executor.submit(
                get_description,
                index,
                row
            )
        )

    for future in futures:
        future.result()

# ==========================================
# FINAL SAVE
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\nFinished everything.")