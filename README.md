# Spotify Charts Scraper

A simple Python scraper to fetch daily Spotify charts for any country from [kworb.net](https://kworb.net/spotify/).

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/spotify-charts-scraper.git
   cd spotify-charts-scraper
   ```
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from spotify_charts_scraper import SpotifyChartsScrapper

# Initialize scraper
scraper = SpotifyChartsScrapper()

# Fetch and parse daily chart for Ukraine
chart_page = scraper.get_daily_chart("Ukraine")
df = scraper.parse_daily_chart(chart_page)

# Display top 5 tracks
print(df.head())
```

## Classes

### `CountryCodes`

* Maintains a mapping of country names to Spotify chart codes (e.g., "United States" → `us`).
* Method: `get_country_code(country: str) -> str` (case-insensitive lookup).

### `SpotifyChartsScrapper`

* Methods:

  * `get_daily_chart(country: str) -> (country_name, html_bytes)`
  * `parse_daily_chart(chart_page) -> pandas.DataFrame`

## Extending

* Add or update country codes in `CountryCodes.country_codes`.
* Modify CSS selectors in `parse_daily_chart` if the HTML structure changes.

## License

This project is licensed under the MIT License.

---

*Happy scraping!*
