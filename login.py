from playwright.sync_api import sync_playwright

def create_login_session():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()

        page.goto("https://onlywhatsneeded.in")

        input("Login manually, then press ENTER...")

        context.storage_state(path="state.json")

        print("Session saved!")

        browser.close()


if __name__ == "__main__":
    create_login_session()