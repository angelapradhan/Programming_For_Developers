def max_profit_trading(max_trades, daily_prices):
    """
    Calculates maximum profit in Chitwan market given transaction limits.
    """
    n = len(daily_prices)
    if n < 2 or max_trades == 0:
        return 0

    dp = [[0] * n for _ in range(max_trades + 1)]

    for i in range(1, max_trades + 1):

        max_diff = -daily_prices[0]
        for j in range(1, n):

            dp[i][j] = max(dp[i][j-1], daily_prices[j] + max_diff)

            max_diff = max(max_diff, dp[i-1][j] - daily_prices[j])

    return dp[max_trades][n-1]

# Test Execution
prices1 = [2000, 4000, 1000]
print(f"Example 1 Profit: {max_profit_trading(2, prices1)} NPR")

prices2 = [1500, 3000, 2000, 5000]
print(f"Example 2 Profit: {max_profit_trading(2, prices2)} NPR")