from .metrics_calculator import MetricsCalculator
from .risk_metrics_calculator import RiskMetricsCalculator
import logging
from typing import Dict, Any


class StockAnalyzer:
    def __init__(self, ticker: str, balance_sheet, financials, cashflow, info):
        self.ticker = ticker
        self.calculator = MetricsCalculator(balance_sheet, financials, cashflow, info)
        self.risk_calculator = RiskMetricsCalculator(ticker)

    def get_metrics(self) -> Dict[str, Any]:
        """Calculate and return all metrics for a stock ticker."""
        try:
            metrics = {
                "Ticker": self.ticker,
                # Basic Metrics
                "Revenue": self.calculator.get_revenue(),
                "Operating Income": self.calculator.get_operating_income(),
                "Net Income": self.calculator.get_net_income(),
                "Total Assets": self.calculator.get_total_assets(),
                "Total Liabilities": self.calculator.get_total_liabilities(),
                "Total Equity": self.calculator.get_total_equity(),
                # Profitability Metrics
                "Gross Margin": self.calculator.calculate_gross_margin(),
                "Operating Margin": self.calculator.calculate_operating_margin(),
                "Net Profit Margin": self.calculator.calculate_net_profit_margin(),
                "ROA": self.calculator.calculate_roa(),
                "ROE": self.calculator.calculate_roe(),
                "ROIC": self.calculator.calculate_roic(),
                # Leverage and Coverage Metrics
                "Debt to Equity": self.calculator.calculate_debt_to_equity(),
                "Interest Coverage": self.calculator.calculate_interest_coverage(),
                # Market Metrics
                "PE Ratio": self.calculator.calculate_pe_ratio(),
                "PEG Ratio": self.calculator.calculate_peg_ratio(),
                "Forward PE": self.calculator.calculate_forward_pe(),
                "Price to Sales": self.calculator.calculate_price_to_sales(),
                "Price to Book": self.calculator.calculate_price_to_book(),
                "Price to Free Cash Flow": self.calculator.calculate_price_to_free_cash_flow(),
                "EV/EBITDA": self.calculator.calculate_ev_to_ebitda(),
                # Growth and Value Metrics
                "Sustainable Growth Rate": self.calculator.calculate_sustainable_growth_rate(),
                "Altman Z-Score": self.calculator.calculate_altman_z_score(),
                # Other Important Metrics
                "Beta": self.calculator.get_beta(),
                "Dividend Yield": self.calculator.calculate_dividend_yield(),
                "Payout Ratio": self.calculator.calculate_payout_ratio(),
                "Asset Turnover": self.calculator.calculate_asset_turnover_ratio(),
                "Institutional Ownership": self.calculator.get_institutional_ownership(),
                "Insider Ownership": self.calculator.get_insider_transactions(),
            }

            try:
                print("Calculating Risk Metrics now")
                risk_metrics = self.risk_calculator.calculate_risk_metrics()
                metrics.update(risk_metrics)
            except Exception as e:
                logging.warning(
                    f"Failed to calculate risk metrics for {self.ticker}: {e}"
                )

            # Filter out None values and replace with "N/A"
            return {k: "N/A" if v is None else v for k, v in metrics.items()}

        except Exception as e:
            logging.error(f"Error in calculating metrics for {self.ticker}: {e}")
            return {"Ticker": self.ticker, "Error": str(e)}
