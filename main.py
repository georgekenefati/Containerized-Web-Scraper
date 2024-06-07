import requests
from bs4 import BeautifulSoup
import pandas as pd

class CompanyDataScraper:
    URL = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
    COLUMN_TYPES = {
        "Rank": "int32",
        "Name": "string",
        "Industry": "string",
        "Revenue (USD millions)": "float64",
        "Revenue growth": "float64",
        "Employees": "float64",
        "Headquarters": "string",
    }

    def __init__(self):
        self.soup = None
        self.headers = []
        self.data = []

    def fetch_page_content(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, "html.parser")

    def extract_table_headers(self):
        table = self.soup.find("table", class_="wikitable sortable")
        if not table:
            raise ValueError("No table found on the webpage")
        
        headers = table.find_all("th")
        self.headers = [header.text.strip() for header in headers]

    def clean_data(self, cell: str) -> str:
        if cell and cell[0].isnumeric():
            cell = cell.split("[")[0]  # Remove references
            cell = cell.replace(',', '')  # Remove commas in numbers
        if '%' in cell:
            cell = cell.replace('%', '')  # Remove percentage signs
        return cell.strip()

    def extract_table_data(self):
        table = self.soup.find("table", class_="wikitable sortable")
        rows = table.find_all("tr")[1:]  # Skip header row
        self.data = []
        for row in rows:
            cells = row.find_all("td")
            cleaned_cells = [self.clean_data(cell.text) for cell in cells]
            self.data.append(cleaned_cells)

    def create_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data, columns=self.headers)
        return df.astype(self.COLUMN_TYPES)

    def run(self):
        self.fetch_page_content()
        self.extract_table_headers()
        self.extract_table_data()
        df = self.create_dataframe()
        return df

def main():
    scraper = CompanyDataScraper()
    df = scraper.run()
    print(df.info())
    print(df.describe())

if __name__ == "__main__":
    main()