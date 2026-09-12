import asyncio
import sys

from playwright.sync_api import Page, sync_playwright


def _ensure_event_loop_for_playwright() -> None:
    if sys.version_info >= (3, 10):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())


def test_bdjobs_login() -> None:
    _ensure_event_loop_for_playwright()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(
            "https://mybdjobs.bdjobs.com/",
            timeout=60000,
            wait_until="domcontentloaded",
        )

        page.wait_for_selector("//input[@id='TXTUSERNAME']")
        page.fill("//input[@id='TXTUSERNAME']", "test.20@gmail.com")
        page.click("//input[@value='Continue']")

        page.wait_for_selector("//input[@id='TXTPASS']")
        page.fill("//input[@id='TXTPASS']", "12345678")
        page.click("//input[@value='Sign in']")

        page.wait_for_timeout(5000)

        page.click("//span[normalize-space()='Invitations']")
        page.wait_for_timeout(3000)

        page.click("//span[normalize-space()='General Interview']")
        page.wait_for_timeout(3000)

        page.click("text=Upcoming")
        page.wait_for_timeout(3000)

        page.click("text=Expired")
        page.wait_for_timeout(3000)

        # Interview Details (same tab)
        page.wait_for_selector("text=interview Details")
        page.click("//div//div//div//div//div//div//div//div//div//div[1]//app-interview-list-card[1]//div[1]//div[1]//div[8]//a[2]")
        page.wait_for_timeout(5000)
        page.go_back()
        page.wait_for_timeout(3000)

        # Back to Upcoming
        page.click("text=Upcoming")
        page.wait_for_timeout(3000)

        # ✅ Job Details → new tab open → close
        with page.context.expect_page() as new_page_info:
            page.click("//div//div//div//div//div//div//div//div//div//div[1]//app-interview-list-card[1]//div[1]//div[1]//div[8]//a[1]")

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        new_page.close()

        page.bring_to_front()
        page.wait_for_timeout(5000)

        # browser.close() না দিলে browser খোলা থাকবে
        
        page.wait_for_selector("text=interview Details")
        page.click("//div//div//div//div//div//div//div//div//div//div[1]//app-interview-list-card[1]//div[1]//div[1]//div[8]//a[2]")
        page.wait_for_timeout(5000)
        # page.click("//span[@class='text-[#98A2B3] size-[14px] font-thin right-2.5 cursor-pointer']//*[name()='svg']")
        # page.wait_for_timeout(5000)
        # page.click("//*[name()='path' and contains(@d,'M10.0026 3')]")
        # page.wait_for_timeout(5000)
        
        # page.wait_for_selector("text=No,I can't attend")
        # page.click("//span[@class='text-sm font-semibold text-[#344054]']")
        # page.wait_for_timeout(5000)
        # page.click("#declineReason-1")
        # page.wait_for_timeout(5000)
        
        
        
        


if __name__ == "__main__":
    test_bdjobs_login()