"""This is the main scapper script."""
import requests
from bs4 import BeautifulSoup
import time
import csv
import urllib.parse

# Configuration
BASE_URL = "https://europeanyouthcard.gr/?city=0&offer_category=0&s=&post_type=offers"
output_dir = "data/"
output_csv = output_dir + "offers_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

label_greek_to_english = {
    "Διεύθυνση": "address",
    "Τηλέφωνο": "tel",
    "Πόλη": "city",
    "Κατηγορία": "category",
    "Ιστοσελίδα": "site",
    "Έκπτωση": "discount_desc",
}

page = requests.get(BASE_URL)
soup = BeautifulSoup(page.content, "html.parser")

# Fetch all offers
all_offers = soup.find_all("div", class_="post_search")
print("Found %d offers..." % len(all_offers))


all_offers_structured = []
for offer in all_offers:
    url = offer.find("a").get("href")
    title = offer.find("a").get("title")

    print("-Fetching offer %d of %d: \"%s\"" % (len(all_offers_structured) + 1,
                                                len(all_offers), title))
    print("Accessing url: \"%s\"" % urllib.parse.unquote(url))

    offer_page = requests.get(url)
    soup = BeautifulSoup(offer_page.content, "html.parser")
    offer_info = soup.find_all("p", class_="offer_data")

    offer_structured_info = {}
    for offer_info_piece in offer_info:
        label = offer_info_piece.find("strong").getText()
        # Labels might contain trailing whiterspace after colon,
        # remove it along with the colon
        label_clean = label.split(":")[0]

        # Try to retrieve the english name of the label
        try:
            label_eng = label_greek_to_english[label_clean]
        except KeyError as e:
            print("Label not know yet: %s. Skipping it..." % e)
            continue

        # Retrieve the offer info for the label
        text = offer_info_piece.getText().split(":")[1].strip()
        if label_eng == "discount_desc":
            print("%s : %s" % (label_eng, text[0:100] + "..."))
        else:
            print("%s : %s" % (label_eng, text))
        offer_structured_info[label_eng] = text
    all_offers_structured.append(offer_structured_info)

    # Sleep to avoid DOS
    time.sleep(5)

with open(output_csv, 'w') as csvfile:
    print("Writing data to CSV file: %s" % output_csv)
    keys = all_offers_structured[0].keys()
    dict_writer = csv.DictWriter(csvfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_offers_structured)
