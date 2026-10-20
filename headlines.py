
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )
}


def main():
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=15
        )

        # Check the status before parsing HTML.
        print(f"HTTP Status: {response.status_code}")

        if response.status_code != 200:
            print("Error: Could not fetch the news page.",
                  file=sys.stderr)
            return

        # Parse the HTML only after a successful response.
        soup = BeautifulSoup(response.text, "html.parser")

        # Inspect the current BBC HTML to verify this selector.
        headline_elements = soup.select(
            'h2[data-testid="card-headline"]'
        )

        # Fallback for pages using article h2 elements.
        if not headline_elements:
            headline_elements = soup.select("article h2")

        headlines = []
        seen = set()

        for element in headline_elements:
            headline = element.get_text(" ", strip=True)
            headline = " ".join(headline.split())

            if not headline or headline in seen:
                continue

            seen.add(headline)
            headlines.append(headline)

            if len(headlines) == 5:
                break

        # Print the available headlines, up to five.
        for index, headline in enumerate(headlines, start=1):
            print(f"{index}. {headline}")

        if len(headlines) < 5:
            print(
                f"Warning: Found only {len(headlines)} "
                "unique headlines. Check the HTML selector "
                "or try again later.",
                file=sys.stderr
            )

    except requests.RequestException as error:
        print(f"Request failed: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
