import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, PriceRecord

app = FastAPI()

# This gives us a database connection for each request
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
        # Fetch the webpage
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try to find a price
        price = None
        for tag in soup.find_all(True):
            if any(word in tag.get("class", []) for word in ["price", "Price", "product-price"]):
                price = tag.get_text(strip=True)
                break

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