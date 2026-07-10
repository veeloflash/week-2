# Week 2 Company Information System

## Overview
This project implements a simple CLI-based company information system using JSON files. It allows users to store companies, search them, and maintain a watchlist.

## Files
- company_system.py: CLI and storage logic
- companies.json: sample company database
- watchlist.json: watchlist data
- config.json: configuration file
- engineering_answers.txt: answers to the engineering questions

## Usage
Run the CLI with Python:

```bash
python company_system.py list
python company_system.py add --company "Apple Inc." --ticker AAPL --industry "Consumer Electronics" --country US --description "Consumer electronics company" --market-cap "3.0T"
python company_system.py search --keyword apple
python company_system.py watchlist --ticker AAPL
python company_system.py config
```
