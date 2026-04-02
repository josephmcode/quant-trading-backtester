import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Backtester:
    def __init__(self, data):
        self.data = data
        self.results = None

    def sma_strategy(self, short_window, long_window):
        self.data['Short_SMA'] = self.data['Close'].rolling(window=short_window).mean()
        self.data['Long_SMA'] = self.data['Close'].rolling(window=long_window).mean()
        self.data['Signal'] = 0.0
        self.data['Signal'][short_window:] = np.where(self.data['Short_SMA'][short_window:] > self.data['Long_SMA'][short_window:], 1.0, 0.0)
        self.data['Position'] = self.data['Signal'].diff()

    def run_backtest(self):
        self.data['Returns'] = self.data['Close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Signal'].shift(1)
        self.data['Cumulative_Returns'] = (1 + self.data['Strategy_Returns']).cumprod()
        return self.data['Cumulative_Returns']

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['Cumulative_Returns'], label='Strategy Returns')
        plt.title('Backtest Results')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Example usage with dummy data
    dates = pd.date_range(start='2023-01-01', periods=100)
    prices = np.random.randn(100).cumsum() + 100
    df = pd.DataFrame({'Close': prices}, index=dates)
    
    bt = Backtester(df)
    bt.sma_strategy(short_window=10, long_window=30)
    bt.run_backtest()
    print("Backtest completed. Cumulative Returns calculated.")

