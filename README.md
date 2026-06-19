# **Imovirtual Rental Scraper & Form Auto‑Submitter**

This project automates the extraction of rental listings from **Imovirtual** and submits the collected data into a web form using **Selenium**.

It combines:

- **Requests + BeautifulSoup** → to scrape listing data  
- **Selenium WebDriver** → to fill and submit the form  
- **Environment variables** → to store URLs securely  

---

## **Features**

- Scrapes rental listings from Imovirtual:
  - Title  
  - Price  
  - Location  
  - Typology  
  - Area  
  - Listing URL  

- Automatically fills and submits a form for each listing  
- Uses a persistent Chrome profile for stable Selenium sessions  
- Includes informative console logs for debugging  

---

## **Environment Variables**

Create a `.env` file with:

```
RENTAL_URL=https://...
FORM_URL=https://...
```

---

## **How It Works**

### **1. Setup**
Initializes Selenium with a custom Chrome profile and loads environment variables.

### **2. Scraping**
Fetches the rental page, parses the HTML, and extracts all listing fields using CSS selectors.

### **3. Form Submission**
For each listing, Selenium:
- Opens the form  
- Fills all fields  
- Submits the entry  
- Waits before processing the next one  

---

## **Project Structure**

- `setup()`  
  Initializes Selenium and loads configuration.

- `scrape_ads()`  
  Scrapes all rental listings and returns structured data.

- `submit_to_form()`  
  Automates form submission for each listing.

- Main execution  
  Runs setup → scraping → submission.

---

## **Requirements**

- Python 3.10+  
- Google Chrome  
- ChromeDriver  
- Required packages:

```
pip install requests beautifulsoup4 python-dotenv selenium
```

---

## **Usage**

Run the script:

```
python main.py
```

The script will:

1. Scrape all listings from the URL in `RENTAL_URL`
2. Submit each listing to the form defined in `FORM_URL`
3. Log progress in the terminal

---

## **Notes**

- XPaths may need adjustment depending on your form structure.  
- The script uses a persistent Chrome profile to avoid repeated logins.  
- Imovirtual HTML structure may change; selectors can be updated easily.