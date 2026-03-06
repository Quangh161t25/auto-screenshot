import asyncio
from playwright.async_api import async_playwright
import datetime

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Truy cập link của bạn
        await page.goto('https://phanmem.wameli.vn/admin/')
        await page.wait_for_timeout(5000)
        
        # Đặt tên file theo ngày giờ
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"screenshot_{now}.png"
        
        await page.screenshot(path=filename, full_page=True)
        print(f"Đã chụp xong: {filename}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
