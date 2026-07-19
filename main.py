from dotenv import load_dotenv
import os

load_dotenv()

BUDGET = os.getenv('BUDGET')
PRODUCT_URL = os.getenv('PRODUCT_URL')

from playwright.sync_api import sync_playwright
import time
import asyncio
from threading import Thread

from monitor import approval_event, cancel_event

from discord_bot import start_bot, send_message, client

bot_thread = Thread(target=start_bot, daemon=True)
bot_thread.start()

def check_stock(page):
    stock = page.locator('[data-outofstock]')
    stock_value = stock.get_attribute("data-outofstock")

    if stock_value == "true":
        return False

    return True


def get_price(page):
    price = page.locator(".price div")
    price_text = price.inner_text()

    return int(price_text.replace("₹", ""))


def handle_cart_navigation(page):
    page.wait_for_timeout(2000)

    go_cart = page.get_by_text("Go to Cart")

    if go_cart.count() > 0 and go_cart.first.is_visible():
        print("Existing cart detected")
        go_cart.first.click()
    else:
        print("Product added directly, continuing")

    page.wait_for_load_state("networkidle")
    return


def prepare_checkout(page, price):
    # Click Order Now
    buttons = page.get_by_role("button", name="Order Now")
    buttons.last.click()

    handle_cart_navigation(page)

    # Cart page
    checkout_button = page.get_by_text("Place Order").first
    checkout_button.click()

    cod = page.locator('[data-testid="cod"]')
    cod.wait_for(state="attached", timeout=60000)
    cod.evaluate("(el)=>el.click()")

    approval_event.clear()
    cancel_event.clear()
    while True:
        if approval_event.is_set():
            final_order = page.locator("button.payment-method-solo-pay-button")

            final_order.wait_for(
                state="visible",
                timeout=60000
            )

            final_order.click()
            break

        if cancel_event.is_set():
            print("Order cancelled")
            return

        time.sleep(10)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state="state.json"
    )
    page = context.new_page()
    page.goto(PRODUCT_URL)

    try:
        while True:
            page.reload()

            if not check_stock(page):
                print("Out of stock. Checking again in 60 seconds...")
            else:
                price = get_price(page)
                print("Current price:", price)

                if price <= int(BUDGET):
                    asyncio.run_coroutine_threadsafe(send_message(
                        "Protein is available!\n"
                        f"Price: ₹{price}\n"
                        "Type YES to place the order."
                        ),
                    client.loop
                    )
                    prepare_checkout(page, price)
                    break

                else:
                    asyncio.run_coroutine_threadsafe(send_message(
                        f"Protein available but price is high.\n"
                        f"Current: ₹{price}\n"
                        f"Budget: ₹{BUDGET}"
                        f"Want to buy?\n"
                        ),
                    client.loop
                    )
                    prepare_checkout(page, price)
                    break

            page.wait_for_timeout(60000)

    except KeyboardInterrupt:
        print("\nStopping monitor...")

    finally:
        context.close()
        browser.close()

