from celery import Celery
from database import SessionLocal, PriceRecord
from playwright.sync_api import sync_playwright

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def scrape_price(url: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            price = None
            try:
                customer_price = page.locator(".js-customer-price.ginc")
                dollars = customer_price.locator(".js-dollar").inner_text()
                cents = customer_price.locator(".js-cent").inner_text()
                price = f"${dollars}{cents}"
            except:
                pass

            browser.close()

        db = SessionLocal()
        record = PriceRecord(url=url, price=price)
        db.add(record)
        db.commit()
        db.close()

        return {"url": url, "price": price}

    except Exception as e:
        return {"error": str(e)}


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run scrape_price every 6 hours for tracked URLs
    sender.add_periodic_task(
        21600.0,  # 6 hours in seconds
        scrape_price.s("https://www.pbtech.co.nz/product/MONSAM72534/Samsung-Odyssey-G5-34-Ultrawide-QHD-165Hz-Curved-G"),
        name="scrape every 6 hours"
    )