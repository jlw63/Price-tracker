import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Price Tracker API is running"}

@app.get("/scrape")
def scrape(url: str):
    try:
        # Fetch the webpage
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try to find a price on the page
        # This looks for common ways websites display prices
        price = None
        for tag in soup.find_all(True):
            if any(word in tag.get("class", []) for word in ["price", "Price", "product-price"]):
                price = tag.get_text(strip=True)
                break
        
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