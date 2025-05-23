# Spotify Charts Scraper

A simple Python scraper to fetch daily Spotify charts for any country from [kworb.net](https://kworb.net/spotify/).

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/alexakka/spotify-charts-scraper.git
   cd spotify-charts-scraper
   ```
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv spotify-scraper
   spotify-scraper\Scripts\activate
   ```
3. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Extending

* Add or update country codes in `CountryCodes.country_codes`.
* Modify CSS selectors in `parse_daily_chart` if the HTML structure changes.

## License

This project is licensed under the MIT License.

---

*Happy scraping!*
