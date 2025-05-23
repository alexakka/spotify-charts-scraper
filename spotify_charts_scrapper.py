import datetime
import re
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


class CountryCodes:
    country_codes = {
        "Argentina": "ar",
        "Australia": "au",
        "Austria": "at",
        "Belgium": "be",
        "Bolivia": "bo",
        "Brazil": "br",
        "Bulgaria": "bg",
        "Canada": "ca",
        "Chile": "cl",
        "Colombia": "co",
        "Costa Rica": "cr",
        "Cyprus": "cy",
        "Czech Republic": "cz",
        "Denmark": "dk",
        "Dominican Republic": "do",
        "Ecuador": "ec",
        "Egypt": "eg",
        "El Salvador": "sv",
        "Estonia": "ee",
        "Finland": "fi",
        "France": "fr",
        "Germany": "de",
        "Global": "global",
        "Greece": "gr",
        "Guatemala": "gt",
        "Honduras": "hn",
        "Hong Kong": "hk",
        "Hungary": "hu",
        "Iceland": "is",
        "India": "in",
        "Indonesia": "id",
        "Ireland": "ie",
        "Israel": "il",
        "Italy": "it",
        "Japan": "jp",
        "Kazakhstan": "kz",
        "Latvia": "lv",
        "Lithuania": "lt",
        "Luxembourg": "lu",
        "Malaysia": "my",
        "Malta": "mt",
        "Mexico": "mx",
        "Morocco": "ma",
        "Netherlands": "nl",
        "New Zealand": "nz",
        "Nicaragua": "ni",
        "Nigeria": "ng",
        "Norway": "no",
        "Pakistan": "pk",
        "Panama": "pa",
        "Paraguay": "py",
        "Peru": "pe",
        "Philippines": "ph",
        "Poland": "pl",
        "Portugal": "pt",
        "Romania": "ro",
        "Saudi Arabia": "sa",
        "Singapore": "sg",
        "Slovakia": "sk",
        "South Africa": "za",
        "South Korea": "kr",
        "Spain": "es",
        "Sweden": "se",
        "Switzerland": "ch",
        "Taiwan": "tw",
        "Thailand": "th",
        "Turkey": "tr",
        "Ukraine": "ua",
        "United Arab Emirates": "ae",
        "United Kingdom": "gb",
        "United States": "us",
        "Uruguay": "uy",
        "Venezuela": "ve",
        "Vietnam": "vn",
    }

    def get_country_code(self, country: str="Global") -> str:
        return self.country_codes.get(country.title())

    def get_countries_list(self):
        return list(self.country_codes.keys())


class SpotifyChartsScrapper:
    def __init__(self):
        self.country_codes = CountryCodes()

    def __get_daily_chart(self, country: str="Global") -> Dict[str, str]:
        code = self.country_codes.get_country_code(country)

        if not code:
            raise ValueError(f"No country code found for '{country}'")

        url = f"https://kworb.net/spotify/country/{code}_daily.html"

        response = requests.get(url)
        response.raise_for_status()

        return country, response.content

    def __parse_daily_chart(self, chart_page) -> pd.DataFrame:
        country, html = chart_page
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table.sortable tbody tr")

        title_text = soup.select_one("span.pagetitle").get_text(strip=True)
        date = re.findall(r"\d{4}/\d{2}/\d{2}", title_text)

        records = []
        for row in rows:
            pos_td = row.select_one("td:nth-of-type(1)")
            art_a = row.select_one("td.text.mp div a:nth-of-type(1)")
            song_a = row.select_one("td.text.mp div a:nth-of-type(2)")
            streams_td = row.select_one("td:nth-of-type(7)")

            # skip any malformed rows
            if not (pos_td and art_a and song_a and streams_td):
                continue

            position = pos_td.get_text(strip=True)
            artist = art_a.get_text(strip=True)
            song = song_a.get_text(strip=True)

            streams_raw = streams_td.get_text(strip=True).replace(",", "")
            streams = None

            if streams_raw:
                streams = streams_raw

            records.append({
                "date": date[0],
                "position": position,
                "artist": artist,
                "song": song,
                "streams": streams,
                "country": country
            })

        return pd.DataFrame(records)

    def get_daily_charts(self, countries=["Global"]):
        charts = []

        if len(countries) == 0:
            countries = self.country_codes.get_countries_list()

        for country in countries:
            country_chart = self.__get_daily_chart(country)
            chart = self.__parse_daily_chart(country_chart)

            charts.append(chart)

        return pd.concat(charts, ignore_index=True)
