import asyncio
import csv
import re
from playwright.async_api import async_playwright

CITIES = [
    "new-york-ny",
    "philadelphia-pa",
    "austin-tx"
]

BASE_URL = "https://www.zocdoc.com"
SPECIALTY_ID = 153 


async def extract_doctor_data(card):
    """Extract structured doctor data from a result card."""

    
    link_el = await card.query_selector("a")
    profile_url = await link_el.get_attribute("href") if link_el else ""
    if profile_url and not profile_url.startswith("http"):
        profile_url = BASE_URL + profile_url

   
    name_el = await card.query_selector("h2")
    name = (await name_el.inner_text()).strip() if name_el else ""

    
    img_el = await card.query_selector("img")
    pic_url = await img_el.get_attribute("src") if img_el else ""

  
    specialty = ""
    specialty_el = await card.query_selector("span")
    if specialty_el:
        specialty = (await specialty_el.inner_text()).strip()

   
    rating = ""
    rating_el = await card.query_selector('[aria-label*="star"]')
    if rating_el:
        rating_text = await rating_el.get_attribute("aria-label")
        match = re.search(r"\d+(\.\d+)?", rating_text or "")
        rating = match.group() if match else ""

  
    review_count = ""
    review_el = await card.query_selector("text=reviews")
    if review_el:
        review_text = await review_el.inner_text()
        match = re.search(r"\d+", review_text)
        review_count = match.group() if match else ""

    return [
        pic_url,
        name,
        profile_url,
        specialty,
        rating,
        review_count
    ]


async def scrape_city(page, city, seen, results):
    """Scrape all pages for a given city."""

    page_number = 1

    while True:
        url = f"{BASE_URL}/search?address={city}&dr_specialty={SPECIALTY_ID}&page={page_number}"
        print(f"Scraping: {url}")

        await page.goto(url, timeout=60000)

        content = await page.content()
        if "Verification Required" in content:
            print("Blocked by anti-bot protection. Stopping scraping.")
            return

        try:
            await page.wait_for_selector("article", timeout=15000)
        except:
            print("No more results found.")
            break

        cards = await page.query_selector_all("article")
        if not cards:
            break

        for card in cards:
            try:
                doctor_data = await extract_doctor_data(card)

                profile_url = doctor_data[2]
                if profile_url and profile_url not in seen:
                    seen.add(profile_url)
                    results.append(doctor_data)

            except Exception as e:
                print("Error extracting card:", e)
                continue

        print(f"Completed page {page_number}")
        page_number += 1

        await page.wait_for_timeout(2000)


async def main():
    seen = set()
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        page = await context.new_page()

        for city in CITIES:
            await scrape_city(page, city, seen, results)

        await browser.close()

    
    with open("zocdoc_doctors.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow([
            "pic_url",
            "Name",
            "Profile URL",
            "Specialty",
            "Rating",
            "Review Count"
        ])
        writer.writerows(results)

    print("Scraping complete. Data saved to zocdoc_doctors.csv")


if __name__ == "__main__":
    asyncio.run(main())