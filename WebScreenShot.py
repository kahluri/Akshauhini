import asyncio
import os
from pyppeteer import launch

async def screenshot(url, output_path):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': output_path})
    await browser.close()

# Read URLs from url.txt
with open("url.txt", "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# Directory to save screenshots
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

# Take screenshots
for url in urls:
    try:
        full_url = f"https://{url}" if not url.startswith("http") else url
        output_path = f"{output_dir}/{url.replace('.', '_')}.png"
        asyncio.get_event_loop().run_until_complete(screenshot(full_url, output_path))
        print(f"Screenshot saved: {output_path}")
    except Exception as e:
        print(f"Failed to capture screenshot for {url}: {e}")

