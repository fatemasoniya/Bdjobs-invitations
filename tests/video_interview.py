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
        page.fill("//input[@id='TXTUSERNAME']", "kejih25003@idwager.com")
        page.click("//input[@value='Continue']")
        
        page.wait_for_selector("//input[@id='TXTPASS']")
        page.fill("//input[@id='TXTPASS']", "@Aa12345")
        page.click("//input[@value='Sign in']")

        page.wait_for_timeout(5000)
        
        page.click("//span[normalize-space()='Invitations']")
        page.wait_for_timeout(3000)

        page.click("//span[normalize-space()='Video Interview']")
        page.wait_for_timeout(3000)
        
        page.click("text=Upcoming")
        page.wait_for_timeout(3000)
        
        page.wait_for_selector("text=interview Details")
        page.click("//div//div//div//div//div//div//div//div//div//div[1]//app-interview-list-card[1]//div[1]//div[1]//div[8]//a[2]")
        page.wait_for_timeout(5000)
        page.go_back()
        page.wait_for_timeout(3000)
        
        # job Details
        page.wait_for_selector("text=job Details")
        page.click("//div//div//div//div//div//div//div//div//div//div[1]//app-interview-list-card[1]//div[1]//div[1]//div[8]//a[1]")
        page.wait_for_timeout(5000)
        
        
        
if __name__ == "__main__":
    test_bdjobs_login()