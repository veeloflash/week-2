import argparse
import json
import logging
import os
from typing import List, Dict, Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="company_system.log",
)


class CompanyStore:
    def __init__(self, db_path: str = "companies.json", watchlist_path: str = "watchlist.json", config_path: str = "config.json"):
        self.db_path = db_path
        self.watchlist_path = watchlist_path
        self.config_path = config_path
        self._ensure_file(self.db_path, [])
        self._ensure_file(self.watchlist_path, [])
        self._ensure_file(self.config_path, {"log_level": "INFO"})
        self.config = self._load_json(self.config_path)

    def _ensure_file(self, path: str, default: Any) -> None:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(default, handle, ensure_ascii=False, indent=2)

    def _load_json(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_json(self, path: str, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def list_companies(self) -> List[Dict[str, Any]]:
        return self._load_json(self.db_path)

    def add_company(self, company: Dict[str, Any]) -> None:
        companies = self.list_companies()
        ticker = company.get("Ticker", "").upper()
        company = dict(company)
        company["Ticker"] = ticker
        companies.append(company)
        self._write_json(self.db_path, companies)
        logging.info("Added company: %s", company.get("Company"))

    def search_companies(self, keyword: str) -> List[Dict[str, Any]]:
        keyword = keyword.lower().strip()
        companies = self.list_companies()
        return [company for company in companies if keyword in company.get("Company", "").lower() or keyword in company.get("Ticker", "").lower() or keyword in company.get("Industry", "").lower()]

    def add_to_watchlist(self, ticker: str) -> None:
        ticker = ticker.upper().strip()
        watchlist = self._load_json(self.watchlist_path)
        if ticker not in watchlist:
            watchlist.append(ticker)
            self._write_json(self.watchlist_path, watchlist)
            logging.info("Added ticker to watchlist: %s", ticker)

    def list_watchlist(self) -> List[str]:
        return self._load_json(self.watchlist_path)

    def show_config(self) -> Dict[str, Any]:
        return self.config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Company Information System")
    parser.add_argument("command", choices=["list", "add", "search", "watchlist", "config"], help="Action to perform")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--ticker", help="Ticker symbol")
    parser.add_argument("--industry", help="Industry")
    parser.add_argument("--country", help="Country")
    parser.add_argument("--description", help="Description")
    parser.add_argument("--market-cap", dest="market_cap", help="Market cap")
    parser.add_argument("--keyword", help="Search keyword")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    store = CompanyStore()

    if args.command == "list":
        companies = store.list_companies()
        for company in companies:
            print(json.dumps(company, ensure_ascii=False, indent=2))
    elif args.command == "add":
        if not args.company or not args.ticker:
            raise SystemExit("Company and ticker are required for add")
        store.add_company(
            {
                "Company": args.company,
                "Ticker": args.ticker,
                "Industry": args.industry or "",
                "Country": args.country or "",
                "Description": args.description or "",
                "Market Cap": args.market_cap or "",
            }
        )
        print(f"Added {args.company} ({args.ticker})")
    elif args.command == "search":
        if not args.keyword:
            raise SystemExit("Keyword is required for search")
        results = store.search_companies(args.keyword)
        for company in results:
            print(json.dumps(company, ensure_ascii=False, indent=2))
    elif args.command == "watchlist":
        if args.ticker:
            store.add_to_watchlist(args.ticker)
            print(f"Added {args.ticker} to watchlist")
        else:
            for ticker in store.list_watchlist():
                print(ticker)
    elif args.command == "config":
        print(json.dumps(store.show_config(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
