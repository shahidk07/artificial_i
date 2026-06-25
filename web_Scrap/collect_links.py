from playwright.sync_api import sync_playwright
import csv
import time

# ==========================================
# SETTINGS
# ==========================================

CHANNEL_URL = "https://www.youtube.com/@PocketTV_Ind/videos"
OUTPUT_FILE = "youtube_links_2.csv"

all_videos = []

# ==========================================
# START
# ==========================================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening channel...")

    page.goto(CHANNEL_URL)

    time.sleep(5)

    # ==========================================
    # AUTO SCROLL
    # ==========================================

    print("\nScrolling until all videos load...\n")

    last_count = 0

    while True:

        page.mouse.wheel(0, 50000)

        time.sleep(3)

        links = page.query_selector_all(
            'a.ytLockupMetadataViewModelTitle'
        )

        current_count = len(links)

        print("Videos loaded:", current_count)

        if current_count == last_count:

            print("\nFinished scrolling.\n")

            break

        last_count = current_count

    # ==========================================
    # COLLECT TITLES + LINKS
    # ==========================================

    print("\nCollecting links...\n")

    links = page.query_selector_all(
        'a.ytLockupMetadataViewModelTitle'
    )

    visited = set()

    for link in links:

        try:

            title = link.inner_text().strip()

            href = link.get_attribute("href")

            if not title or not href:
                continue

            video_url = "https://www.youtube.com" + href

            if video_url in visited:
                continue

            visited.add(video_url)

            print(title)

            all_videos.append({
                "title": title,
                "url": video_url
            })

        except Exception as e:

            print("Error:", e)

    # ==========================================
    # SAVE CSV
    # ==========================================

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["title", "url"]
        )

        writer.writeheader()

        writer.writerows(all_videos)

    browser.close()

print(f"\nSaved {len(all_videos)} videos to {OUTPUT_FILE}")