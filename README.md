I got tired of checking my favourite protein powder's website every day.
The one I wanted has been out of stock for what feels like forever.
Apparently that's a lifestyle now.

So I wrote a bot. Now it suffers instead of me.

<br>

-> What it does
- Watches the product page like it has nothing better to do.
- Refreshes it over and over so I don't have to.
- The moment **"Notify Me"** becomes **"Order Now"**, it wakes up.
- Checks the current price.
- Sends me a Discord notification when the product becomes available.
- Lets me decide whether I actually want to buy it.
  *(I'm financially fragile. The bot understands.)*
- Automatically prepares checkout.
- Selects Cash on Delivery.
- Waits for my approval:
  - YES -> places the order.
  - NO -> cancels.

<br>

-> Tech Stack
- Python
- Playwright
- Discord.py
- Threading Events

<br>

I just want my protein powder.

> *ding* **Order placed.**

<br>

### Disclaimer

This project was built for personal use to monitor a specific product on **Only What's Needed**.

*(Plant Protein has been out of stock for ages!)*

It is not intended to be a general-purpose shopping bot, bypass website restrictions, or automate purchases across different platforms.

The goal was simply to stop manually refreshing a product page every day and experiment with browser automation, Discord bots, and human-in-the-loop approval workflows.
