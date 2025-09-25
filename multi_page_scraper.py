from bs4 import BeautifulSoup
import json
import pandas as pd

html_files = ["listing_page1.html", "listing_page2.html", "listing_page3.html"]

all_reviews = []

for file_name in html_files:
    with open(file_name, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    business_name_el = soup.select_one(
        "body > yelp-react-root > div:nth-child(1) > div.y-css-vcnn65 > "
        "div.y-css-1d804v4 > div.photoHeader__09f24__nPvHp.y-css-mhg9c5 > "
        "div.photo-header-content-container__09f24__jDLBB.y-css-mhg9c5 > "
        "div.photo-header-content__09f24__q7rNO.y-css-84tjbt > div > div > "
        "div.headingLight__09f24__N86u1.y-css-74ugvt"
    )
    business_name = business_name_el.get_text(strip=True) if business_name_el else None

    total_reviews_el = soup.select_one(
        "body > yelp-react-root > div:nth-child(1) > div.y-css-vcnn65 > "
        "div.y-css-1d804v4 > div.photoHeader__09f24__nPvHp.y-css-mhg9c5 > "
        "div.photo-header-content-container__09f24__jDLBB.y-css-mhg9c5 > "
        "div.photo-header-content__09f24__q7rNO.y-css-84tjbt > div > div > "
        "div.arrange__09f24__LDfbs.gutter-1-5__09f24__vMtpw.vertical-align-middle__09f24__zU9sE.y-css-1pnalxe > "
        "div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.y-css-1n5biw7 > span.y-css-1q46f5r"
    )
    total_reviews_count = total_reviews_el.get_text(strip=True) if total_reviews_el else None

    review_blocks = soup.select("#reviews > section > div.y-css-mhg9c5 > ul > li")

    for block in review_blocks:
        reviewer_name_el = block.select_one(
            "div.y-css-9vtc3g div.y-css-8x4us div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.y-css-mhg9c5 "
            "div.user-passport-info.y-css-mhg9c5 > span > a"
        )
        reviewer_name = reviewer_name_el.get_text(strip=True) if reviewer_name_el else None

        location_el = block.select_one(
            "div.y-css-9vtc3g div.y-css-8x4us div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.y-css-mhg9c5 "
            "div.user-passport-info.y-css-mhg9c5 > div.y-css-14zpyii"
        )
        location = location_el.get_text(strip=True) if location_el else None

        date_el = block.select_one(
            "div.y-css-scqtta div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.y-css-mhg9c5"
        )
        reviewer_date = date_el.get_text(strip=True) if date_el else None

        text_el = block.select_one("div:nth-child(4) > p")
        reviewer_text = text_el.get_text(strip=True) if text_el else None

        all_reviews.append({
            "business_name": business_name,
            "total_reviews_count": total_reviews_count,
            "reviewer_name": reviewer_name,
            "location": location,
            "reviewer_date": reviewer_date,
            "reviewer_text": reviewer_text
        })

with open("blueprint_data.json", "w", encoding="utf-8") as f:
    json.dump(all_reviews, f, indent=2, ensure_ascii=False)

df = pd.DataFrame(all_reviews)
df.to_csv("blueprint_data.csv", index=False, encoding="utf-8")

print(f"Extracted {len(all_reviews)} reviews from all 3 pages into blueprint_data.json and blueprint_data.csv")
