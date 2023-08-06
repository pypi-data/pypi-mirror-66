"""Provides individual metrics calculations.

This module is more low-level than _3_performance_evaluation."""

# For mathematical operations
from math import sqrt, exp, log

# For tensor calculations
from numpy import cov

# For managing tables properly
from pandas import to_datetime

from _helper_functions import find_dataframe_value_with_keywords, \
    datetime_to_string

def calculate_volatility(df_daily_returns, time_adjustment_in_days=None):
    """Calculates the volatility of a portfolio using daily portfolio returns.

    Outputs the volatility over the given time series by default; can also be
    adjusted for any arbitrary time using the time_adjustment_in_days parameter.
    """
    if time_adjustment_in_days is None:
        time_adjustment_in_days = len(df_daily_returns)

    volatility = df_daily_returns['relative_portfolio_return'].std() * sqrt(
        time_adjustment_in_days
    ) / sqrt(len(df_daily_returns))

    if round(volatility, 4) == 0:
        raise ValueError('Volatility cannot be zero or close to zero. Please check if daily returns are correctly calculated and if any trades were made. \n{df_daily_returns}')

    return volatility

def calculate_roi_math(
        end_value,
        start_value,
        end_time,
        start_time
    ):
    unadjusted_return_factor = end_value / start_value
    time_duration = (end_time - start_time).total_seconds() / 86400

    roi = exp(
        log(
            unadjusted_return_factor
        ) * 365 / (time_duration)
    ) - 1

    return roi

def calculate_roi(
        df_trading_journal,
        float_budget_in_usd,
        df_benchmark=None,
        df_price_column_name='price',
        df_time_column_name='datetime',
        df_benchmark_price_column_name='price',
        df_benchmark_time_column_name='datetime',
        df_trading_journal_price_column_name='Portfolio value',
        df_trading_journal_time_column_name='datetime'
    ):
    """Calculates annualized returns (on equity, not total assets).

    It can calculate standalone returns without benchmarking (in USD/fiat) or
    returns in relation to a benchmark. It can also use different start and end
    points for calculating the time frame, i.e., the duration between the first
    and the last trade OR the duration between the first and the last data point
    of the price data.
    """
    start_time = df_trading_journal[
        df_trading_journal_time_column_name
    ].iloc[0]
    end_time = df_trading_journal[
        df_trading_journal_time_column_name
    ].iloc[-1]

    portfolio_roi = calculate_roi_math(
        end_value=df_trading_journal[
            df_trading_journal_price_column_name
    ].iloc[-1],
        start_value=float_budget_in_usd,
        end_time=end_time,
        start_time=start_time
    )

    roi_delta_compared_to_benchmark = None
    benchmark_roi = None

    if df_benchmark is not None:
        end_value_benchmark = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=end_time,
            search_column_name_1=df_benchmark_time_column_name,
            search_term_2=None,
            search_column_name_2=None,
            output_column_name=df_benchmark_price_column_name,
            first_last_or_all_elements='First'
        )

        begin_value_benchmark = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=start_time,
            search_column_name_1=df_benchmark_time_column_name,
            search_term_2=None,
            search_column_name_2=None,
            output_column_name=df_benchmark_price_column_name,
            first_last_or_all_elements='First'
        )

        benchmark_roi = calculate_roi_math(
            end_value=end_value_benchmark,
            start_value=begin_value_benchmark,
            end_time=end_time,
            start_time=start_time
        )

        roi_delta_compared_to_benchmark = portfolio_roi - benchmark_roi

    return {
        'portfolio_roi': portfolio_roi,
        'benchmark_roi': benchmark_roi,
        'roi_delta_compared_to_benchmark': roi_delta_compared_to_benchmark
    }

def calculate_sharpe_ratio(
        df_daily_returns,
        portfolio_roi_usd,
        days=None,
        risk_free_rate=None
    ):
    """Calculates the Sharpe ratio of a given set of returns."""
    volatility = calculate_volatility(df_daily_returns, days)

    if risk_free_rate is None:
        sharpe_ratio = portfolio_roi_usd / volatility
    else:
        sharpe_ratio = (portfolio_roi_usd - risk_free_rate) / volatility
    return sharpe_ratio

def calculate_maximum_drawdown(
        df_daily_returns,
        column_with_portfolio_values
    ):
    """Calculates the maximum_drawdown of a portfolio using portfolio_value from df_daily_returns.

    Outputs the maximum_drawdown ratio.
    """
    dict_peak_tracking = {
        'first_peak': {
            'peak': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            },
            'trough': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            }
        },
        'second_peak': {
            'peak': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            },
            'trough': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            }
        }
    }

    for datetime, row in df_daily_returns.iterrows():
        if row[column_with_portfolio_values] > dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values]:
            dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['peak']['datetime'] = datetime
            dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['trough']['datetime'] = datetime
        if row[column_with_portfolio_values] < dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values]:
            dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['trough']['datetime'] = datetime
        if row[column_with_portfolio_values] < dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values]:
            dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['first_peak']['trough']['datetime'] = datetime

        drawdown_second = (
            dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values] - dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values]
        ) / dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values]
        drawdown_first = (
            dict_peak_tracking['first_peak']['peak'][column_with_portfolio_values] - dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values]
        ) / dict_peak_tracking['first_peak']['peak'][column_with_portfolio_values]
        if drawdown_second > drawdown_first:
            dict_peak_tracking['first_peak'] = dict_peak_tracking['second_peak']

    maximum_drawdown_duration = dict_peak_tracking['first_peak']['trough']['datetime'] - dict_peak_tracking['first_peak']['peak']['datetime']
    peak_date = dict_peak_tracking['first_peak']['peak']['datetime']
    trough_date = dict_peak_tracking['first_peak']['trough']['datetime']

    return drawdown_first, maximum_drawdown_duration, peak_date, trough_date

def calculate_transaction_cost(df_trading_journal):
    return round(
        sum(df_trading_journal["Total fees (as absolute)"]),
        2
    )

def calculate_beta(df_daily_returns, df_daily_benchmark_returns):
    """Calculates the beta of a portfolio against a benchmark."""
    portfolio_returns = df_daily_returns['relative_portfolio_return'].to_numpy()
    benchmark_returns = df_daily_benchmark_returns['benchmark_relative_return'].to_numpy()

    covariance_matrix = cov(portfolio_returns, benchmark_returns)

    benchmark_portfolio_covariance = covariance_matrix[0][1]
    benchmark_variance = covariance_matrix[1][1]

    return benchmark_portfolio_covariance / benchmark_variance

def calculate_alpha(
        annualized_portfolio_return,
        risk_free_rate,
        beta_exposure,
        annualized_market_return
    ):
    """Calculates the Jensen's alpha of a portfolio against a benchmark."""
    market_risk_premium = annualized_market_return - risk_free_rate

    alpha = annualized_portfolio_return - (
        risk_free_rate + beta_exposure * market_risk_premium
    )

    return alpha
