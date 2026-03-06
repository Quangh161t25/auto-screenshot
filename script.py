import asyncio
from playwright.async_api import async_playwright
import datetime

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            print("Đang truy cập: https://phanmem.wameli.vn/admin/")
            await page.goto('https://phanmem.wameli.vn/admin/', timeout=60000)
            
            # Đợi trang ổn định
            await page.wait_for_load_state("networkidle")

            # 1. Tìm và điền Username (thử nhiều cách)
            # Tìm ô input có chữ "Tài khoản", "Username" hoặc là ô nhập liệu đầu tiên
            user_input = page.locator('input[name*="user"], input[name*="login"], input[type="text"]').first
            await user_input.fill("Admin")
            print("Đã điền Username")

            # 2. Tìm và điền Password
            pass_input = page.locator('input[name*="pass"], input[type="password"]').first
            await pass_input.fill("anhtuyen123321")
            print("Đã điền Password")

            # 3. Tìm nút Đăng nhập và Click
            # Tìm nút có chữ "Đăng nhập", "Login" hoặc nút Submit
            login_button = page.locator('button:has-text("Đăng nhập"), button[type="submit"], input[type="submit"]').first
            await login_button.click()
            print("Đã nhấn nút Đăng nhập")

            # Đợi chuyển trang
            await page.wait_for_timeout(7000) 
            
            # Chụp ảnh kết quả
            now = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%Y-%m-%d_%H-%M")
            filename = f"admin_check_{now}.png"
            await page.screenshot(path=filename, full_page=True)
            print(f"Thành công! Đã lưu: {filename}")

        except Exception as e:
            # Nếu lỗi, chụp ảnh màn hình lỗi để bạn biết nó đang đứng ở đâu
            print(f"Lỗi xảy ra: {e}")
            await page.screenshot(path="error_debug.png")
            print("Đã lưu ảnh lỗi 'error_debug.png' để kiểm tra.")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
