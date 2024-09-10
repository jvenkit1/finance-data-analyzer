from financial_analysis.multi_stock_analyzer import MultiStockAnalyzer

if __name__ == "__main__":
    tickers = ["AAPL", "ADBE", "AMZN", "BRK.B", "COST", "TGT", "WMT", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA", "UBER", "LYFT", "TSM", "INTC", "DLTR", "OLLI", "DG"]  

    analyzer = MultiStockAnalyzer(tickers)
    result_df = analyzer.analyze_stocks("First")

    print(result_df)
    result_df.to_csv("stock_analysis.csv", index=False)