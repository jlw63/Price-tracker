from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Price Tracker API is running"}

@app.get("/scrape")
def scrape(url: str):
    # We'll add real scraping here soon
    # For now just return the URL back so we can test the API works
    return {
        "url": url,
        "price": None,
        "status": "scraping not implemented yet"
    }