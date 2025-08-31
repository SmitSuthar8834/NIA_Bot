import asyncio
import sys
from playwright.async_api import async_playwright

async def run(meet_link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(meet_link)

        # Try disabling mic/camera (if buttons exist)
        try:
            await page.click("button[aria-label='Turn off microphone']")
            await page.click("button[aria-label='Turn off camera']")
        except:
            pass  

        # Try clicking Join
        try:
            await page.click("text=Join now")
            print("✅ Nia joined the meeting!")
        except:
            print("⚠️ Could not auto-click 'Join now'. Please check UI selectors.")

        await page.wait_for_timeout(600000)  # stay 10 mins

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ No meeting link provided")
    else:
        asyncio.run(run(sys.argv[1]))
