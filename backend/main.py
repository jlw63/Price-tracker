from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, PriceRecord
from playwright.sync_api import sync_playwright

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Price Tracker API is running"}

@app.get("/scrape")
def scrape(url: str, db: Session = Depends(get_db)):
    try:
        with sync_playwright() as p:
            # Launch a real browser (invisible)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Visit the URL and wait for it to fully load
            page.goto(url, wait_until="networkidle")
            
            # Try to find the price on PB Tech
            price = None
            try:
                price_element = page.locator(".price, .product-price, [class*='price']").first
                price = price_element.inner_text()
            except:
                pass
            
            browser.close()

        # Save to database
        record = PriceRecord(url=url, price=price)
        db.add(record)
        db.commit()

        return {
            "url": url,
            "price": price,
            "status": "success" if price else "price not found"
        }
    
    except Exception as e:
        return {
            "url": url,
            "price": None,
            "status": f"error: {str(e)}"
        }

@app.get("/history")
def history(url: str, db: Session = Depends(get_db)):
    records = db.query(PriceRecord).filter(PriceRecord.url == url).all()
    return [
        {"price": r.price, "scraped_at": r.scraped_at}
        for r in records
    ]