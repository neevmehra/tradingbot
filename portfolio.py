from typing import List, Dict, Union, Optional, Tuple
from td.client import TDClient
import numpy as np
from numpy import DataFrame

class Portfolio():
    def __init__(self, account_number: Optional[str]):
        
        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number
        self._td_client: TDClient = None

    def add_position(self, symbol: str, asset_type: str, purchase_date: Optional[str], quantity: int = 0, purchase_price: float = 0.0) -> dict:
        
        self.positions[symbol] = {}
        self.positions[symbol]['symbol'] = symbol
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

        return self.positions
    
    def add_positions(self, positions: List[dict]) -> dict:

        if isinstance(positions, list):
            
            for position in positions:

                self.add_position(
                    symbol=position['symbol'],
                    asset_type=position['asset_type'],
                    purchase_date=position.get['purchase_date', None],
                    purchase_price=position.get['purchase_price', 0.0],
                    quantity=position.get('quantity', 0)
                )

                return self.positions

        else:
            raise TypeError("Positions must be a list of dictionaries")
        
    def remove_position(self, symbol: str) -> Tuple[bool, str]:

        if symbol in self.positions:
            del self.positions[symbol]
            return (True, "{Symbol} was successfully removed".format(symbol=symbol))
        else:
            return (False, "{Symbol} did not exist in the portfolio".format(symbol=symbol))

    def in_portfolio(self, symbol: str) -> bool:
        
        if symbol in self.positions:
            return True
        else:
            return False
        
    def is_profitable(self, symbol: str, current_price: float) -> bool:

        # Grab the purchase price
        purchase_price = self.positions[symbol]['purchase_price']

        if (purchase_price <= current_price):
            return True
        elif (purchase_price > current_price):
            return False
        
    @property
    def td_client(self) -> TDClient:

        return self._td_client

    @td_client.setter
    def td_client(self, td_client: TDClient) -> None:

        self._td_client: TDClient = td_client
        

    def total_allocation(self) -> dict:

        total_allocation = {
            'stocks': [],
            'fixed_income': [],
            'options': [],
            'futures': [],
            'furex': []
        }

        if len(self.positions.keys()) > 0:
            for symbol in self.positions:
                total_allocation[self.positions[symbol]['asset_type']].append(self.positions[symbol])

    def portfolio_variance(self, weights: dict, covariance_matrix: DataFrame) -> dict:

        sorted_keys = list(weights.keys())
        sorted_keys.sort()

        sorted_weights = np.array([weights[symbol] for symbol in sorted_keys])
        portfolio_variance = np.dot(
            sorted_weights.T,
            np.dot(covariance_matrix, sorted_weights)
        )

        return portfolio_variance

    def portfolio_metrics(self) -> dict:

        if not self._stock_frame_daily:
            self._grab_daily_historical_prices()

        # Calculate the weights.
        porftolio_weights = self.portfolio_weights()

        # Calculate the Daily Returns (%)
        self._stock_frame_daily.frame['daily_returns_pct'] = self._stock_frame_daily.symbol_groups['close'].transform(
            lambda x: x.pct_change()
        )

        # Calculate the Daily Returns (Mean)
        self._stock_frame_daily.frame['daily_returns_avg'] = self._stock_frame_daily.symbol_groups['daily_returns_pct'].transform(
            lambda x: x.mean()
        )

        # Calculate the Daily Returns (Standard Deviation)
        self._stock_frame_daily.frame['daily_returns_std'] = self._stock_frame_daily.symbol_groups['daily_returns_pct'].transform(
            lambda x: x.std()
        )

        # Calculate the Covariance.
        returns_cov = self._stock_frame_daily.frame.unstack(
            level=0)['daily_returns_pct'].cov()

        # Take the other columns and get ready to add them to our dictionary.
        returns_avg = self._stock_frame_daily.symbol_groups['daily_returns_avg'].tail(
            n=1
        ).to_dict()

        returns_std = self._stock_frame_daily.symbol_groups['daily_returns_std'].tail(
            n=1
        ).to_dict()

        metrics_dict = {}

        portfolio_variance = self.portfolio_variance(
            weights=porftolio_weights,
            covariance_matrix=returns_cov
        )

        for index_tuple in returns_std:

            symbol = index_tuple[0]
            metrics_dict[symbol] = {}
            metrics_dict[symbol]['weight'] = porftolio_weights[symbol]
            metrics_dict[symbol]['average_returns'] = returns_avg[index_tuple]
            metrics_dict[symbol]['weighted_returns'] = returns_avg[index_tuple] * \
                metrics_dict[symbol]['weight']
            metrics_dict[symbol]['standard_deviation_of_returns'] = returns_std[index_tuple]
            metrics_dict[symbol]['variance_of_returns'] = returns_std[index_tuple] ** 2
            metrics_dict[symbol]['covariance_of_returns'] = returns_cov.loc[[
                symbol]].to_dict()

        metrics_dict['portfolio'] = {}
        metrics_dict['portfolio']['variance'] = portfolio_variance

        return metrics_dict

    def portfolio_weights(self) -> dict:

        weights = {}

        # First grab all the symbols.
        symbols = self.positions.keys()

        # Grab the quotes.
        quotes = self.td_client.get_quotes(instruments=list(symbols))

        # Grab the projected market value.
        projected_market_value_dict = self.projected_market_value(
            current_prices=quotes
        )

        # Loop through each symbol.
        for symbol in projected_market_value_dict:

            # Calculate the weights.
            if symbol != 'total':
                weights[symbol] = projected_market_value_dict[symbol]['total_market_value'] / \
                    projected_market_value_dict['total']['total_market_value']

        return weights
        

