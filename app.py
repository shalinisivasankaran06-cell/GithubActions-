import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Random Quote Generator API")

quotes = [
    {"id": 1, "text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation"},
    {"id": 2, "text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "life"},
    {"id": 3, "text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "category": "motivation"},
    {"id": 4, "text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "category": "tech"},
    {"id": 5, "text": "First, solve the problem. Then, write the code.", "author": "John Johnson", "category": "tech"},
    {"id": 6, "text": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu", "category": "life"},
]


class Quote(BaseModel):
    text: str
    author: str
    category: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the Random Quote Generator API", "endpoints": ["/quote", "/quote/{category}", "/quotes", "/quote (POST)"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/quote")
def get_random_quote():
    return random.choice(quotes)


@app.get("/quote/{category}")
def get_quote_by_category(category: str):
    filtered = [q for q in quotes if q["category"].lower() == category.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail=f"No quotes found for category '{category}'")
    return random.choice(filtered)


@app.get("/quotes")
def get_all_quotes():
    return {"count": len(quotes), "quotes": quotes}


@app.post("/quote")
def add_quote(quote: Quote):
    new_id = max(q["id"] for q in quotes) + 1
    new_quote = {"id": new_id, **quote.dict()}
    quotes.append(new_quote)
    return new_quote
