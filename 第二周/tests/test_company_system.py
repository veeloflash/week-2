import os
import tempfile
import unittest

from company_system import CompanyStore


class CompanyStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "companies.json")
        self.watchlist_path = os.path.join(self.temp_dir.name, "watchlist.json")
        self.config_path = os.path.join(self.temp_dir.name, "config.json")
        self.store = CompanyStore(
            db_path=self.db_path,
            watchlist_path=self.watchlist_path,
            config_path=self.config_path,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_loads_empty_database(self):
        self.assertEqual(self.store.list_companies(), [])

    def test_add_and_search_companies(self):
        self.store.add_company(
            {
                "Company": "Apple Inc.",
                "Ticker": "AAPL",
                "Industry": "Consumer Electronics",
                "Country": "US",
                "Description": "Consumer electronics company",
                "Market Cap": "3.0T",
            }
        )
        companies = self.store.search_companies("apple")
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0]["Ticker"], "AAPL")

    def test_watchlist_adds_ticker(self):
        self.store.add_company(
            {
                "Company": "Apple Inc.",
                "Ticker": "AAPL",
                "Industry": "Consumer Electronics",
                "Country": "US",
                "Description": "Consumer electronics company",
                "Market Cap": "3.0T",
            }
        )
        self.store.add_to_watchlist("AAPL")
        self.assertEqual(self.store.list_watchlist(), ["AAPL"])


if __name__ == "__main__":
    unittest.main()
