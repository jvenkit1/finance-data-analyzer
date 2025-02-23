from dataclasses import dataclass
from typing import Optional, Dict, Any
import numpy as np
import pandas as pd
from scipy import stats
import yfinance as yf
from .utils import handle_api_errors


class RiskMetricsCalculator:
    def __init__(
        self,
        ticker: str,
        confidence_level: float = 0.95,
        risk_free_rate: float = 0.02,
        period: str = "1y",
    ):
        self.ticker = ticker
        self.confidence_level = confidence_level
        self.risk_free_rate = risk_free_rate
        self.period = period
        self._price_history = None
        self._market_data = None
        self._daily_returns = None
        self._market_returns = None

    def _fetch_data(self) -> None:
        """Fetch historical price data for stock and market index."""
        if self._price_history is None:
            try:
                stock = yf.Ticker(self.ticker)
                market = yf.Ticker("^GSPC")  # S&P 500

                self._price_history = stock.history(period=self.period)
                self._market_data = market.history(period=self.period)

                # Calculate returns
                self._daily_returns = self._price_history["Close"].pct_change().dropna()
                self._market_returns = self._market_data["Close"].pct_change().dropna()

            except Exception as e:
                raise ValueError(f"Failed to fetch data for {self.ticker}: {e}")

    @handle_api_errors
    def calculate_risk_metrics(self) -> Dict[str, float]:
        """Calculate all risk metrics for the stock."""
        self._fetch_data()

        if self._daily_returns is None or self._daily_returns.empty:
            return {}

        # Historical VaR
        var_historical = np.percentile(
            self._daily_returns, (1 - self.confidence_level) * 100
        )

        # Parametric VaR
        z_score = stats.norm.ppf(1 - self.confidence_level)
        var_parametric = (
            self._daily_returns.mean() - z_score * self._daily_returns.std()
        )

        # CVaR
        tail_returns = self._daily_returns[self._daily_returns <= var_historical]
        cvar = tail_returns.mean()

        # Sharpe Ratio
        daily_rf = (1 + self.risk_free_rate) ** (1 / 252) - 1
        excess_returns = self._daily_returns - daily_rf
        sharpe = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())

        # Sortino Ratio
        negative_returns = excess_returns[excess_returns < 0]
        downside_std = np.sqrt(np.mean(negative_returns**2))
        sortino = np.sqrt(252) * (excess_returns.mean() / downside_std)

        # Beta and Correlation
        aligned_returns = pd.concat(
            [self._daily_returns, self._market_returns], axis=1
        ).dropna()

        covariance = aligned_returns.cov().iloc[0, 1]
        market_variance = aligned_returns.iloc[:, 1].var()
        beta = covariance / market_variance
        correlation = aligned_returns.corr().iloc[0, 1]

        return {
            "Value at Risk (Historical)": var_historical,
            "Value at Risk (Parametric)": var_parametric,
            "Conditional VaR": cvar,
            "Sharpe Ratio": sharpe,
            "Sortino Ratio": sortino,
            "Beta": beta,
            "Market Correlation": correlation,
        }
