import logging
from financial_analysis.multi_stock_analyzer import MultiStockAnalyzer


def setup_logging():
    """Configure logging to write to stdout."""
    logging.basicConfig(
        level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    # Set up logging
    setup_logging()

    # List of stock tickers to analyze
    tickers = [
        "AAPL",
        "ADBE",
        "AMZN",
        "BRK.B",
        "COST",
        "TGT",
        "WMT",
        "GOOGL",
        "META",
        "MSFT",
        "NFLX",
        "NVDA",
        "TSLA",
        "UBER",
        "LYFT",
        "TSM",
        "INTC",
        "DLTR",
        "OLLI",
        "DG",
    ]

    # Initialize the MultiStockAnalyzer with the tickers
    analyzer = MultiStockAnalyzer(tickers)

    # Analyze the stocks and return the results
    results_df = analyzer.analyze_stocks()

    # Print out the results
    print(results_df)


if __name__ == "__main__":
    main()
