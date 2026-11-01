# Web Scraping Task

Maine Python ke BeautifulSoup aur requests libraries use karke books.toscrape.com (ek public website) se 1000 books ka data scrape kiya. Script HTML structure se title, price, rating, stock status aur URL nikalti hai, aur "next" button follow karke saare 50 pages cover karti hai. Data ko clean karke ek custom dataset (`books_dataset.csv`) banaya hai, jo price aur rating ke beech relation dekhne ke liye bana hai.

## Files
- `scrape_books.py`: scraping script
- `books_dataset.csv`: final dataset (1000 rows)

## Run
pip install requests beautifulsoup4
python scrape_books.py
