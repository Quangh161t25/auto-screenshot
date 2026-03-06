import asyncio
from playwright.async_api import async_playwright
import datetime

async def run():
    async with async_playwright() as p:
        # Khởi tạo trình duyệt
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800} # Đặt kích thước màn hình
        )
        page = await context.new_page()
        
        print("Đang truy cập trang quản trị...")
        await page.goto('https://phanmem.wameli.vn/admin/')
        
        # Đợi các ô nhập liệu xuất hiện
        await page.wait_for_selector('input[name="username"]', timeout=10000)
        
        # Điền thông tin đăng nhập
        print("Đang điền thông tin đăng nhập...")
        await page.fill('input[name="username"]', "Admin")
        await page.fill('input[name="password"]', "anhtuyen123321")
        
        # Nhấn nút Đăng nhập (thường là button type="submit")
        # Nếu nút có tên khác, Playwright sẽ cố gắng tìm nút Click được
        await page.click('button[type="submit"]')
        
        # Đợi 5 giây để trang load sau khi đăng nhập thành công
        print("Đăng nhập thành công, đang đợi tải dữ liệu...")
        await page.wait_for_timeout(5000)
        
        # Đặt tên file theo ngày giờ Việt Nam (UTC+7)
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%Y-%m-%d_%H-%M")
        filename = f"admin_dashboard_{now}.png"
        
        # Chụp toàn bộ trang
        await page.screenshot(path=filename, full_page=True)
        print(f"Đã lưu ảnh: {filename}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
