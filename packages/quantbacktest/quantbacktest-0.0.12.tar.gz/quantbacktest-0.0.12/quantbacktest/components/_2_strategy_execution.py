"""Contains strategies and order execution functionality."""

# For deep-copied dictionaries
from copy import deepcopy

# For managing dates
from datetime import datetime, timedelta

# For managing tables properly
from numpy import where
from pandas import DataFrame, read_csv, read_excel, date_range, Timedelta, Timestamp

# For mathematical operations
from math import isnan

# For nice-looking progress bars
from tqdm import tqdm

# For white noise strategy
from random import choice

from _helper_functions import find_dataframe_value_with_keywords, \
    find_price, calculate_portfolio_value, calculate_relative_gross_exposure
from _1_data_preparation import save_dataframe_to_csv
from _3_performance_evaluation import evaluate_performance


def initialize_trading_journal():
    """Initializes a pandas DataFrame that serves as a trading journal.

    Initialization is important for determining the column order.
    """
    df_trading_journal = DataFrame(columns=[
        'datetime',
        'Cash',
        'Cash before',
        'Asset',
        'Buy or sell',
        'Number bought',
        'Price (quote without any fees)',
        'Value bought',
        'Portfolio value',
        'Dict of assets in portfolio',
        'Absolute fees (as absolute)',
        'Current equity margin',
        'Exposure (in currency)',
        'Exposure (number)',
        'Gross exposure',
        'Interest paid',
        'Money spent',
        'Relative fees (as absolute)',
        'Relative fees (as relative)',
        'Strategy ID',
        'Total exposure',
        'Total fees (as absolute)',
        'Total fees (as relative)'
    ])

    return df_trading_journal

def execute_order(
        boolean_buy,
        index,
        date,
        crypto_key,
        number_to_be_bought,
        strategy_id,
        df_prices,
        df_trading_journal,
        margin_loan_rate,
        fees,
        float_budget_in_usd,
        price,
        display_options,
        constraints,
        general_settings,
        boolean_allow_partially_filled_orders
    ):
    """Executes all kinds of orders.

    Can handle more than one order per point in time by subsequently calling
    this function.
    """
    if boolean_buy and (number_to_be_bought < 0) or not boolean_buy and (number_to_be_bought > 0):
        raise ValueError(f'boolean_buy: {boolean_buy} and number_to_be_bought: {number_to_be_bought} is contradictory.')

    order = {
        'datetime': date,
        'Strategy ID': strategy_id,
        'Asset': crypto_key,
        'Buy or sell': boolean_buy
    }

    if len(df_trading_journal) > 0:
        available_funds = df_trading_journal['Cash'].iloc[-1] - constraints['minimum_cash']
        order['Dict of assets in portfolio'] = deepcopy(df_trading_journal['Dict of assets in portfolio'].iloc[-1])
        order['Cash before'] = df_trading_journal['Cash'].iloc[-1]
    else:
        available_funds = float_budget_in_usd
        order['Dict of assets in portfolio'] = {crypto_key: 0}
        order['Cash before'] = float_budget_in_usd

    def reduce_quantity_until_max_gross_exposure_is_met(
            number_to_be_bought,
            df_prices,
            dict_of_assets_in_portfolio,
            time,
            display_options,
            constraints,
            rounding_accuracy,
            cash_value,
            general_settings,
            crypto_key
        ):
        # Checks if the maximum_gross_exposure constraint is violated and
        # reduces the order volumne step-by-step in case of a violation
        # until the exposure falls within the constraint.
        initial_number_to_be_bought = number_to_be_bought
        dict_of_assets_in_portfolio[crypto_key] = dict_of_assets_in_portfolio[crypto_key] + number_to_be_bought
        for reduction_step in range(1, 100):
            dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)
            relative_gross_exposure = calculate_relative_gross_exposure(
                df_prices=df_prices,
                dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
                time=time,
                display_options=display_options,
                constraints=constraints,
                rounding_accuracy=rounding_accuracy,
                cash_value=cash_value,
                general_settings=general_settings
            )

            # Stop reduction as soon as constraint is met, reduce if
            # constraint is violated.
            if relative_gross_exposure <= constraints['maximum_gross_exposure']:
                break
            else:
                dict_of_assets_in_portfolio[crypto_key] = ((100 - reduction_step) / 100) * initial_number_to_be_bought

        return initial_number_to_be_bought

    def quantity_that_can_be_bought_given_budget(order, dict_of_assets_in_portfolio, boolean_allow_partially_filled_orders, number_to_be_bought, available_funds, general_settings, display_options, date):
        initial_number_to_be_bought = number_to_be_bought

        number_to_be_bought = min(
            max(round(available_funds / price, general_settings['rounding_decimal_places_for_security_quantities']), 0),
            number_to_be_bought
        )

        # Todo: Individual asset constraints.
        # constraints['maximum_individual_asset_exposure_all']
        dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)
        number_to_be_bought = reduce_quantity_until_max_gross_exposure_is_met(
            number_to_be_bought=number_to_be_bought,
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            time=date,
            display_options=display_options,
            constraints=constraints,
            rounding_accuracy=general_settings['rounding_decimal_places'],
            cash_value=order['Cash before'] - (number_to_be_bought * price) - fees['absolute_fee_buy_order'] - round(
                fees['percentage_buying_fees_and_spread'] * price * number_to_be_bought,
                general_settings['rounding_decimal_places']
            ),
            general_settings=general_settings,
            crypto_key=crypto_key
        )

        if boolean_allow_partially_filled_orders:
            if number_to_be_bought == 0 and initial_number_to_be_bought != 0:
                if display_options['warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy order for {initial_number_to_be_bought} units of {crypto_key} could not be filled.')
            elif number_to_be_bought < initial_number_to_be_bought:
                if display_options['warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy order for {initial_number_to_be_bought} units of {crypto_key} could only partially be filled: {number_to_be_bought} units bought.')
            elif number_to_be_bought > initial_number_to_be_bought:
                raise ValueError(f'It is not possible that the signal quantity {initial_number_to_be_bought} is lower than the final quantity {number_to_be_bought} for {order["Asset"]}.')
            return number_to_be_bought
        else:
            if initial_number_to_be_bought != number_to_be_bought:
                raise InputError('Quantity {number_to_be_bought} for {crypto_key} cannot be covered with the given budget or constraints. Maximum {max_possible_quantity} units can be bought.')
            else:
                return number_to_be_bought

    def quantity_that_can_be_sold_given_portfolio(order, dict_of_assets_in_portfolio, boolean_allow_partially_filled_orders, number_to_be_bought, df_trading_journal, general_settings, display_options, date):
        initial_number_to_be_bought = number_to_be_bought

        # Todo: Individual asset constraints.
        # constraints['maximum_individual_asset_exposure_all']

        positive_quantity = (-1) * number_to_be_bought
        try:
            number_to_be_bought = (-1) * min(
                positive_quantity,
                df_trading_journal['Dict of assets in portfolio'].iloc[-1][crypto_key]
            )
        except IndexError:
            number_to_be_bought = 0

        dict_of_assets_in_portfolio = deepcopy(order['Dict of assets in portfolio'])
        number_to_be_bought = reduce_quantity_until_max_gross_exposure_is_met(
            number_to_be_bought=number_to_be_bought,
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            time=date,
            display_options=display_options,
            constraints=constraints,
            rounding_accuracy=general_settings['rounding_decimal_places'],
            cash_value=order['Cash before'] - (number_to_be_bought * price) - fees['absolute_fee_buy_order'] - round(
                fees['percentage_buying_fees_and_spread'] * price * number_to_be_bought,
                general_settings['rounding_decimal_places']
            ),
            general_settings=general_settings,
            crypto_key=crypto_key
        )

        if boolean_allow_partially_filled_orders:
            if number_to_be_bought == 0 and initial_number_to_be_bought != 0:
                if display_options['warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy order for {number_to_be_bought} units of {crypto_key} could not be filled.')
            elif number_to_be_bought > initial_number_to_be_bought:
                if display_options['warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy order for {number_to_be_bought} units of {crypto_key} could not be filled.')
            elif number_to_be_bought < initial_number_to_be_bought:
                raise ValueError('It is not possible that the signal quantity {initial_number_to_be_bought} is higher (less assets sold) than the final quantity {number_to_be_bought} for {order["Asset"]}.')
            return number_to_be_bought
        else:
            if number_to_be_bought != initial_number_to_be_bought:
                raise InputError('Quantity {number_to_be_bought} for {crypto_key} cannot be sold with the given assets or constraints. Maximum {number_to_be_bought} units can be sold.')
            else:
                return number_to_be_bought

    if boolean_buy:
        number_to_be_bought = quantity_that_can_be_bought_given_budget(
            order=order,
            dict_of_assets_in_portfolio=order['Dict of assets in portfolio'],
            boolean_allow_partially_filled_orders=boolean_allow_partially_filled_orders,
            number_to_be_bought=number_to_be_bought,
            available_funds=available_funds,
            general_settings=general_settings,
            display_options=display_options,
            date=date
        )
    else:
        number_to_be_bought = quantity_that_can_be_sold_given_portfolio(
            order=order,
            dict_of_assets_in_portfolio=order['Dict of assets in portfolio'],
            boolean_allow_partially_filled_orders=boolean_allow_partially_filled_orders,
            number_to_be_bought=number_to_be_bought,
            df_trading_journal=df_trading_journal,
            general_settings=general_settings,
            display_options=display_options,
            date=date
        )

    if isnan(price):
        number_to_be_bought = 0
        price = 0

    order['Dict of assets in portfolio'][crypto_key] = order['Dict of assets in portfolio'][crypto_key] + number_to_be_bought

    if number_to_be_bought != 0:
        if boolean_buy:
            order['Absolute fees (as absolute)'] = fees['absolute_fee_buy_order']
            order['Relative fees (as absolute)'] = round(
                fees['percentage_buying_fees_and_spread'] * price * number_to_be_bought,
                general_settings['rounding_decimal_places']
            )
            order['Relative fees (as relative)'] = fees['percentage_buying_fees_and_spread']
            order['Total fees (as absolute)'] = fees['absolute_fee_buy_order'] + order['Relative fees (as absolute)']
            order['Total fees (as relative)'] = round(
                order['Total fees (as absolute)'] / (number_to_be_bought * price),
                general_settings['rounding_decimal_places']
            )
        else:
            order['Absolute fees (as absolute)'] = fees['absolute_fee_sell_order']
            order['Relative fees (as absolute)'] = round(
                fees['percentage_selling_fees_and_spread'] * price * number_to_be_bought * (-1),
                general_settings['rounding_decimal_places']
            )
            order['Relative fees (as relative)'] = fees['percentage_selling_fees_and_spread']
            order['Total fees (as absolute)'] = fees['absolute_fee_sell_order'] + order['Relative fees (as absolute)']
            order['Total fees (as relative)'] = round(
                order['Total fees (as absolute)'] / (number_to_be_bought * price) * (-1),
                general_settings['rounding_decimal_places']
            )
    else:
        order['Absolute fees (as absolute)'] = 0
        order['Relative fees (as absolute)'] = 0
        order['Relative fees (as relative)'] = 0
        order['Total fees (as absolute)'] = 0
        order['Total fees (as relative)'] = 0

    if len(df_trading_journal) > 0:
        # Date conversion from string to date format; datetime is in microsecond format
        previous_time = df_trading_journal['datetime'].iloc[-1]
        days_since_last_order = date - previous_time

        order['Number bought'] = number_to_be_bought
        order['Value bought'] = round(price * number_to_be_bought, general_settings['rounding_decimal_places'])
        if days_since_last_order == timedelta(seconds=0):
            order['Interest paid'] = 0
        else:
            order['Interest paid'] = round(
                (
                    (1 - df_trading_journal['Current equity margin'].iloc[-1])
                    * (
                        df_trading_journal['Portfolio value'].iloc[-1]
                        * margin_loan_rate
                    )
                ) ** (
                    (
                        days_since_last_order.total_seconds() / 86400
                    ) / 365
                ),
                general_settings['rounding_decimal_places']
            ) # "/ 86400" because one day has 86400 seconds

        order['Money spent'] = round(
            number_to_be_bought * (
                price
            ) + (
                order['Total fees (as absolute)'] + order['Interest paid']
            ), general_settings['rounding_decimal_places']
        ) # Todo But everything that can be bought minus fees and other costs

        order['Cash'] = round(
            df_trading_journal['Cash'].iloc[-1] - order['Money spent'],
            general_settings['rounding_decimal_places']
        )

    else:
        # For initial row
        order['Number bought'] = number_to_be_bought
        order['Value bought'] = price * number_to_be_bought
        order['Interest paid'] = 0.0
        order['Money spent'] = number_to_be_bought * (
            price
        ) + (
            + order['Total fees (as absolute)']
            + order['Interest paid']
        ) # Todo But everything that can be bought minus fees and other costs

        order['Cash'] = round(
            float_budget_in_usd - order['Money spent'],
            general_settings['rounding_decimal_places']
        )

    order['Price (quote without any fees)'] = price

    # Todo: For now just 1
    order['Current equity margin'] = 1

    order['Exposure (number)'] = order['Dict of assets in portfolio'][order['Asset']]

    order['Exposure (in currency)'] = round(
        price * order['Exposure (number)'],
        general_settings['rounding_decimal_places']
    )

    order['Portfolio value'] = calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=order['Dict of assets in portfolio'],
        time=order['datetime'],
        display_options=display_options,
        constraints=constraints,
        cash_value=order['Cash'],
        rounding_accuracy=general_settings['rounding_decimal_places']
    )

    order['Total exposure'] = round(
        order['Portfolio value'] - order['Cash'],
        general_settings['rounding_decimal_places']
    )

    assert round(order['Total exposure'], 2) == round(calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=order['Dict of assets in portfolio'],
        time=order['datetime'],
        display_options=display_options,
        constraints=constraints,
        rounding_accuracy=general_settings['rounding_decimal_places']
    ), 2)

    order['Gross exposure'] = calculate_relative_gross_exposure(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=order['Dict of assets in portfolio'],
        time=order['datetime'],
        display_options=display_options,
        constraints=constraints,
        rounding_accuracy=general_settings['rounding_decimal_places'],
        cash_value=order['Cash'],
        general_settings=general_settings
    )

    return order

def prepare_signal_list_ii(
        file_path_with_signal_data,
        strategy_hyperparameters
    ):
    try:
        try:
            df_signals = read_csv(
                file_path_with_signal_data,
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'id']
            )
        except UnicodeDecodeError:
            df_signals = read_excel(
                file_path_with_signal_data,
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'id']
            )
    except:
        try:
            df_signals = read_csv(
                'backtesting/' + file_path_with_signal_data,
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'id']
            )
        except:
            raise ValueError("Please setup a signal table. A signal table needs the following columns: 'datetime', 'id' (hexadecimal ERC20 token identifier), 'signal_strength' (numeric that is used to infer buy or sell orders)")

    # Only use top 50 tokens
    print(f'\nNumber of signals before dropping non-top-50 tokens: {len(df_signals)}')
    comments['Number of signals before dropping non-top-50 tokens'] = len(df_signals)
    print(f'Number of unique eth IDs before: {len(df_signals["id"].unique())}')
    comments['Number of unique eth IDs before'] = len(df_signals['id'].unique())
    df_top50 = read_csv('strategy_tables/Top50Tokens.csv', sep=',')
    list_top50 = df_top50['a.ID'].values.tolist()
    df_signals = df_signals[df_signals['id'].isin(list_top50)]
    print(f'Number of signals after dropping non-top-50 tokens: {len(df_signals)}')
    comments['Number of signals after dropping non-top-50 tokens'] = len(df_signals)
    print(f'Number of unique eth IDs after: {len(df_signals["id"].unique())}')
    comments['Number of unique eth IDs after'] = len(df_signals['id'].unique())

    # Drop weak signals
    print(f'\nNumber of signals before dropping weak signals: {len(df_signals)}')
    comments['Number of signals before dropping weak signals'] = len(df_signals)
    df_signals['signal_type'] = where(df_signals["rawSignal"]<=strategy_hyperparameters['sell_parameter'], "SELL", where(df_signals["rawSignal"]>=strategy_hyperparameters['buy_parameter'], "BUY", "HODL"))
    #indexNames = df_signals[(df_signals['rawSignal'] >= strategy_hyperparameters['sell_parameter']) & (df_signals['rawSignal'] <= strategy_hyperparameters['buy_parameter']) ].index # FOr testing purposes: 0.03 and 12.0
    #df_signals.drop(indexNames, inplace=True)
    df_signals = df_signals[~df_signals['signal_type'].isin(["HODL"])]
    print(f'Number of signals after dropping weak signals: {len(df_signals)}')
    comments['Number of signals after dropping weak signals'] = len(df_signals)

    # Drop signals that are not covered by ITSA
    print(f'\nNumber of signals before dropping unavailable data: {len(df_signals)}')
    comments['Number of signals before dropping unavailable data'] = len(df_signals)
    df_signals = df_signals[
        df_signals['id'].isin(df_prices['token_address_eth'].unique())
    ]
    print(f'Number of signals after dropping unavailable data: {len(df_signals)}')
    comments['Number of signals after dropping unavailable data'] = len(df_signals)

    # Drop data that is not needed
    print(f'\nNumber of data points before dropping unnecessary data: {len(df_prices)}')
    comments['Number of data points before dropping unnecessary data'] = len(df_prices)
    df_prices = df_prices[
        df_prices['token_address_eth'].isin(df_signals['id'].unique())
    ]
    print(f'Number of data points after dropping unnecessary data: {len(df_prices)}')
    comments['Number of data points after dropping unnecessary data'] = len(df_prices)

    # Drop signals that have assets that have no prices for the last day. This
    # is necessary because for the final portfolio valuation, there has to be a
    # price for the last day.
    print(f'\nNumber of signals before dropping unavailable prices: {len(df_signals)}')
    comments['Number of signals before dropping unavailable prices'] = len(df_signals)
    print(f'Number of unique eth IDs before: {len(df_signals["id"].unique())}')
    comments['Number of unique eth IDs before'] = len(df_signals['id'].unique())

    last_signal_date = df_signals['datetime'].iloc[-1]
    price = None

    list_of_assets_dropped_due_to_price_lag_at_last_day = []

    for asset_in_signal_table in df_prices['token_address_eth'].unique():
        price = find_price(
            df_prices,
            desired_index=index,
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=display_options['warning_no_price_for_last_day'],
            boolean_errors=False
        )

        if price is None:
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if display_options['warning_no_price_for_last_day']:
                print(f'{asset_in_signal_table} was dropped because there is no price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )
        elif isnan(price):
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if display_options['warning_no_price_for_last_day']:
                print(f'{asset_in_signal_table} was dropped because there is only a NaN price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )
        elif price == 0:
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if display_options['warning_no_price_for_last_day']:
                print(f'asset_in_signal_table was dropped because there is only a 0 price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )

    df_signals = df_signals[~df_signals['id'].isin(list_of_assets_dropped_due_to_price_lag_at_last_day)]

    print(f'Number of assets that do not have a price on the last day: {len(list_of_assets_dropped_due_to_price_lag_at_last_day)}')
    comments['Number of assets that do not have a price on the last day'] = len(
        list_of_assets_dropped_due_to_price_lag_at_last_day
    )

    print(f'Number of signals after dropping unavailable prices: {len(df_signals)}')
    comments['Number of signals after dropping unavailable prices'] = len(df_signals)

    print(f'Number of unique eth IDs after: {len(df_signals["id"].unique())}')
    comments['Number of unique eth IDs after'] = len(df_signals['id'].unique())

    id_column_name = 'token_address_eth'

    for asset_with_possible_later_price in list_of_assets_dropped_due_to_price_lag_at_last_day:
        price = find_price(
            df_prices,
            asset_with_possible_later_price,
            time=datetime(2019, 7, 1),
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=True,
            boolean_warnings=display_options['warning_no_price_for_last_day']
        )
        if price is None:
            list_of_assets_dropped_due_to_price_lag_at_last_day.remove(
                asset_with_possible_later_price
            )

    print(f'Number of assets that do not have a price on the last day, but on a later day: {len(list_of_assets_dropped_due_to_price_lag_at_last_day)}')
    comments['Number of assets that do not have a price on the last day, but on a later day'] = len(list_of_assets_dropped_due_to_price_lag_at_last_day)

    return df_signals, id_column_name

def prepare_signal_list_san(
        file_path_with_signal_data,
        strategy_hyperparameters
    ):
    try:
        df_signals = read_csv(
            file_path_with_signal_data,
            sep=',',
            parse_dates=True,
            infer_datetime_format=True,
            index_col=['datetime', 'id']
        )
    except:
        raise ValueError("Please set up a signal table. A signal table needs the following columns: 'date' (yyyy-mm-dd), 'signal_strength' (numeric that is used to infer buy or sell orders), 'id' (hexadecimal ERC20 token identifier or ITIN). You can change the column names in the Excel/CSV file to fit this convention or in main.py so that the program adjusts to the naming in the table.")

    df_signals['signal_type'] = where(df_signals['signal_strength']<=strategy_hyperparameters['sell_parameter'],'SELL',where(df_signals['signal_strength']>=strategy_hyperparameters['buy_parameter'],'BUY','HODL'))
    df_signals = df_signals[~df_signals['signal_type'].isin(['HODL'])]

    return df_signals

def execute_strategy_multi_asset(
        df_prices,
        int_chosen_strategy,
        float_budget_in_usd,
        margin_loan_rate,
        boolean_allow_shorting,
        list_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options,
        minimum_expected_mispricing_trigger_in_percent,
        strategy_hyperparameters,
        sell_at_the_end,
        file_path_with_signal_data,
        display_options,
        constraints,
        general_settings,
        comments
    ):
    """Filters signals and executes all remaining signals."""

    df_signals = prepare_signal_list_san(
        file_path_with_signal_data,
        strategy_hyperparameters
    )

    df_signals = df_signals.loc[strategy_hyperparameters['start_time']:strategy_hyperparameters['end_time'], ]

    if display_options['boolean_test']:
        # Drop non-test signals
        print('Warning: Test run!')
        print(f'\nNumber of signals before dropping non-test signals: {len(df_signals)}')
        comments['Number of signals before dropping non-test signals'] = len(df_signals)
        list_indexes_to_be_dropped = []
        df_signals = df_signals.sample(frac=0.05, random_state=0)
        df_signals.sort_index(inplace=True)
        print(f'Number of signals after dropping non-test signals: {len(df_signals)}')
        comments['Number of signals after dropping non-test signals'] = len(df_signals)

    df_trading_journal = initialize_trading_journal()

    for index, row in tqdm(df_signals.iterrows(), desc='Going through signals', unit='signal'):
        boolean_buy = None

        crypto_key = index[1]

        price = find_price(
            df_prices,
            desired_index=index,
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=display_options['warning_no_price_during_execution']
        )

        if price is not None and price > 0:
            if row['signal_type'] == "BUY":
                boolean_buy = True

                # Check if minimum is already crossed
                if len(df_trading_journal) > 0:
                    if df_trading_journal['Cash'].iloc[-1] <= constraints['minimum_cash']:
                        allow_buy_orders = False

                    else:
                        allow_buy_orders = True

                else:
                    allow_buy_orders = True

                if allow_buy_orders:
                    try:
                        float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
                    except:
                        pass

                    number_to_be_bought = round(
                        (
                            float_budget_in_usd
                            - constraints['minimum_cash']
                        ) / price,
                        general_settings['rounding_decimal_places_for_security_quantities']
                    )

                else:
                    number_to_be_bought = None

                if number_to_be_bought is not None:
                    number_to_be_bought = number_to_be_bought * strategy_hyperparameters['maximum_relative_exposure_per_buy']

            elif row['signal_type'] == "SELL":
                boolean_buy = False
                # Check if exposure for this asset is zero and skip order if so

                if not (
                    (
                        boolean_buy == False
                    ) and (
                        find_dataframe_value_with_keywords(
                            df_trading_journal,
                            search_term_1=crypto_key,
                            search_column_name_1='Asset'
                        )
                    ) is None
                ):
                    number_to_be_bought = (-1) * (
                        find_dataframe_value_with_keywords(
                            df_trading_journal,
                            search_term_1=crypto_key,
                            search_column_name_1='Asset',
                            output_column_name='Exposure (number)',
                            first_last_or_all_elements='Last'
                        )
                    )

                else:
                    number_to_be_bought = None

            else:
                raise ValueError('Ambiguous signal:', row['signal_type'])

            try:
                amount = df_trading_journal['Cash'].iloc[-1]
            except:
                amount = float_budget_in_usd

            if number_to_be_bought is None:
                number_to_be_bought = 0

            number_to_be_bought = round(number_to_be_bought, general_settings['rounding_decimal_places_for_security_quantities'])

            dataseries_trading_journal = execute_order(
                boolean_buy=boolean_buy,
                index=index,
                date=index[0],
                strategy_id=int_chosen_strategy,
                crypto_key=crypto_key,
                number_to_be_bought=number_to_be_bought,
                df_prices=df_prices,
                df_trading_journal=df_trading_journal,
                margin_loan_rate=margin_loan_rate,
                float_budget_in_usd=float_budget_in_usd,
                price=price,
                fees={
                    'absolute_fee_buy_order':dict_crypto_options['general']['absolute_fee_buy_order'],
                    'absolute_fee_sell_order':dict_crypto_options['general']['absolute_fee_sell_order'],
                    'percentage_buying_fees_and_spread':dict_crypto_options['general']['percentage_buying_fees_and_spread'],
                    'percentage_selling_fees_and_spread':dict_crypto_options['general']['percentage_selling_fees_and_spread']
                },
                display_options=display_options,
                constraints=constraints,
                general_settings=general_settings,
                boolean_allow_partially_filled_orders=strategy_hyperparameters['boolean_allow_partially_filled_orders']
            )

            df_trading_journal = df_trading_journal.append(
                dataseries_trading_journal,
                ignore_index=True
            )

    comments['constraints'] = constraints
    comments['general_settings'] = general_settings

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': '3',
        'Strategy label': 'X',
        'strategy_hyperparameters': strategy_hyperparameters,
        'comments': comments
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=display_options['string_results_directory'],
    )

    return dict_return

def execute_strategy_white_noise(
        df_prices,
        int_chosen_strategy,
        float_budget_in_usd,
        margin_loan_rate,
        list_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options,
        minimum_expected_mispricing_trigger_in_percent,
        strategy_hyperparameters,
        display_options,
        constraints,
        general_settings,
        sell_at_the_end,
        comments,
        boolean_allow_shorting=False,
    ):
    """Executes buy and sell orders in alternating order.

    Has positive average exposure and is therefore not expected to yield a gross
    return of zero.
    """
    df_prices = df_prices.loc[(slice(strategy_hyperparameters['start_time'], strategy_hyperparameters['end_time']), strategy_hyperparameters['id']), :]

    df_trading_journal = initialize_trading_journal()

    usd_safety_buffer = 100

    # Single-asset only
    crypto_key = strategy_hyperparameters['id']

    for index, row in df_prices.iterrows():
        try:
            amount = df_trading_journal['Cash'].iloc[-1]
        except:
            amount = float_budget_in_usd

        if choice(['buy', 'sell']) == 'buy':
            # Determine the number of assets to be bought or sold
            try:
                float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
            except:
                pass

            number_to_be_bought = round(
                (
                    float_budget_in_usd - usd_safety_buffer
                ) / row['price'],
                general_settings['rounding_decimal_places_for_security_quantities']
            )

            if number_to_be_bought < 0:
                number_to_be_bought = 0

            boolean_buy = True

        else:
            # Determine the number of assets to be bought or sold
            try:
                number_to_be_bought = (-1) * df_trading_journal[
                    'Exposure (number)'
                ].iloc[-1]
            except:
                number_to_be_bought = 0

            boolean_buy = False

        dataseries_trading_journal = execute_order(
            df_prices=df_prices,
            df_trading_journal=df_trading_journal,
            boolean_buy=boolean_buy,
            index=index,
            date=index[0],
            strategy_id=int_chosen_strategy,
            crypto_key=crypto_key,
            number_to_be_bought=number_to_be_bought,
            margin_loan_rate=margin_loan_rate,
            float_budget_in_usd=float_budget_in_usd,
            price=row['price'],
            fees={
                'absolute_fee_buy_order':dict_crypto_options['general']['absolute_fee_buy_order'],
                'absolute_fee_sell_order':dict_crypto_options['general']['absolute_fee_sell_order'],
                'percentage_buying_fees_and_spread':dict_crypto_options['general']['percentage_buying_fees_and_spread'],
                'percentage_selling_fees_and_spread':dict_crypto_options['general']['percentage_selling_fees_and_spread']
            },
            display_options=display_options,
            constraints=constraints,
            general_settings=general_settings,
            boolean_allow_partially_filled_orders=strategy_hyperparameters['boolean_allow_partially_filled_orders']
        )

        df_trading_journal = df_trading_journal.append(
            dataseries_trading_journal,
            ignore_index=True
        )

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': int_chosen_strategy,
        'Strategy label': 'White Noise',
        'strategy_hyperparameters': strategy_hyperparameters,
        'comments': ''
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=display_options['string_results_directory'],
    )

    return dict_return

def execute_strategy_ma_crossover(
        df_prices,
        int_chosen_strategy,
        float_budget_in_usd,
        margin_loan_rate,
        boolean_allow_shorting,
        list_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options,
        general_settings,
        minimum_expected_mispricing_trigger_in_percent,
        strategy_hyperparameters,
        sell_at_the_end,
        file_path_with_signal_data,
        display_options,
        constraints,
        comments
    ):
    """Filters signals and executes all remaining signals."""
    df_prices['moving_average'] = df_prices.groupby(
        level='id'
    )['price'].transform(
        lambda x: round(
            x.rolling(
                window=strategy_hyperparameters['moving_average_window_in_days'],
                # on='datetime'
            ).mean(),
            general_settings['rounding_decimal_places']
        )
    )

    df_trading_journal = initialize_trading_journal()

    price = None

    current_time = strategy_hyperparameters['start_time']
    previous_time = Timestamp(current_time) - strategy_hyperparameters['frequency']

    times_to_loop_over = date_range(start=strategy_hyperparameters['start_time'], end=strategy_hyperparameters['end_time'], freq=strategy_hyperparameters['frequency']).to_series()
    for current_time in times_to_loop_over:
    #for time_elapsed in tqdm(range(strategy_hyperparameters['frequency'], ((strategy_hyperparameters['end_time'] - strategy_hyperparameters['start_time']) + strategy_hyperparameters['frequency'])), desc='Going through signals', unit='signal'):

        boolean_buy = None
        number_to_be_bought = 0

        # CONTINUE HERE
        previous_time = current_time - Timedelta(strategy_hyperparameters['frequency'])
        # This intermediate step is used to erase the frequency from the Timestamp
        previous_time = Timestamp(str(previous_time))

        old_row = df_prices.loc[(previous_time, strategy_hyperparameters['id']), : ]
        previous_ma = old_row['moving_average']
        old_price = old_row['price']

        new_ma = df_prices.loc[(current_time, strategy_hyperparameters['id']), 'moving_average']

        price = find_price(
            df_prices,
            desired_index=(current_time, strategy_hyperparameters['id']),
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=display_options['warning_no_price_during_execution']
        )

        if (previous_ma < old_price) and (new_ma > price):
            moving_average_crossover = 'Upside breach'
        elif (previous_ma > old_price) and (new_ma < price):
            moving_average_crossover = 'Downside breach'
        elif new_ma < price:
            moving_average_crossover = 'Above'
        elif new_ma > price:
            moving_average_crossover = 'Below'
        else:
            moving_average_crossover = None

        if moving_average_crossover == 'Upside breach' or moving_average_crossover == 'Above':
            boolean_buy = True
        elif moving_average_crossover == 'Downside breach' or moving_average_crossover == 'Below':
            boolean_buy = False
        else:
            boolean_buy = None

        if price is not None and price > 0:
            if boolean_buy:
                try:
                    float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
                except:
                    pass

                number_to_be_bought = round(
                    (
                        float_budget_in_usd
                        - constraints['minimum_cash']
                    ) / price,
                    general_settings['rounding_decimal_places_for_security_quantities']
                )

                if number_to_be_bought is not None:
                    number_to_be_bought = round(
                        number_to_be_bought * strategy_hyperparameters['maximum_relative_exposure_per_buy'],
                        general_settings['rounding_decimal_places_for_security_quantities']
                    )

            elif boolean_buy == False:
                if len(df_trading_journal) > 0:
                    number_to_be_bought = (-1) * round(
                        df_trading_journal.iloc[-1]['Dict of assets in portfolio'][strategy_hyperparameters['id']],
                        general_settings['rounding_decimal_places_for_security_quantities']
                    )
                else:
                    number_to_be_bought = 0
            else:
                number_to_be_bought = 0

            if number_to_be_bought != 0:
                dataseries_trading_journal = execute_order(
                    boolean_buy=boolean_buy,
                    index=current_time,
                    date=current_time,
                    strategy_id=int_chosen_strategy,
                    crypto_key=strategy_hyperparameters['id'],
                    number_to_be_bought=number_to_be_bought,
                    df_prices=df_prices,
                    df_trading_journal=df_trading_journal,
                    margin_loan_rate=margin_loan_rate,
                    float_budget_in_usd=float_budget_in_usd,
                    price=price,
                    fees={
                        'absolute_fee_buy_order': dict_crypto_options['general']['absolute_fee_buy_order'],
                        'absolute_fee_sell_order': dict_crypto_options['general']['absolute_fee_sell_order'],
                        'percentage_buying_fees_and_spread': dict_crypto_options['general']['percentage_buying_fees_and_spread'],
                        'percentage_selling_fees_and_spread': dict_crypto_options['general']['percentage_selling_fees_and_spread']
                    },
                    display_options=display_options,
                    constraints=constraints,
                    general_settings=general_settings,
                    boolean_allow_partially_filled_orders=strategy_hyperparameters['boolean_allow_partially_filled_orders']
                )

                df_trading_journal = df_trading_journal.append(
                    dataseries_trading_journal,
                    ignore_index=True
                )

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': '4',
        'Strategy label': 'Moving Average Crossover',
        'strategy_hyperparameters': strategy_hyperparameters,
        'comments': comments
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=display_options['string_results_directory'],
    )

    return dict_return

def test_strategies(
        df_prices,
        int_chosen_strategy,
        float_budget_in_usd,
        margin_loan_rate,
        boolean_allow_shorting,
        list_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options,
        minimum_expected_mispricing_trigger_in_percent,
        strategy_hyperparameters,
        sell_at_the_end,
        benchmark_data_specifications,
        display_options,
        constraints,
        general_settings,
        start_time,
        file_path_with_signal_data=None,
        comments={}
    ):
    """Calls user-defined strategy.

    Chooses the correct strategy (as per user input) and returns
    the performance metrics and the trading journal of that strategy.
    """

    if int_chosen_strategy == 1:
        dict_execution_results = execute_strategy_white_noise(
            df_prices=df_prices,
            float_budget_in_usd=float_budget_in_usd,
            margin_loan_rate=margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
            int_chosen_strategy=int_chosen_strategy,
            dict_crypto_options=dict_crypto_options,
            minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
            strategy_hyperparameters=strategy_hyperparameters,
            display_options=display_options,
            constraints=constraints,
            general_settings=general_settings,
            sell_at_the_end=sell_at_the_end,
            comments=comments
        )
    elif int_chosen_strategy == 2:
        raise NotImplementedError('Strategy 2 is not implemented.')
    elif int_chosen_strategy == 3:
        dict_execution_results = execute_strategy_multi_asset(
            df_prices=df_prices,
            file_path_with_signal_data=file_path_with_signal_data,
            float_budget_in_usd=float_budget_in_usd,
            int_chosen_strategy=int_chosen_strategy,
            margin_loan_rate=margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
            strategy_hyperparameters=strategy_hyperparameters,
            sell_at_the_end=sell_at_the_end,
            display_options=display_options,
            constraints=constraints,
            general_settings=general_settings,
            comments=comments
        )
    elif int_chosen_strategy == 4:
        dict_execution_results = execute_strategy_ma_crossover(
            df_prices=df_prices,
            file_path_with_signal_data=file_path_with_signal_data,
            int_chosen_strategy=int_chosen_strategy,
            float_budget_in_usd=float_budget_in_usd,
            margin_loan_rate=margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
            strategy_hyperparameters=strategy_hyperparameters,
            sell_at_the_end=sell_at_the_end,
            display_options=display_options,
            constraints=constraints,
            general_settings=general_settings,
            comments=comments
        )

    save_dataframe_to_csv(
        dict_execution_results['df_trading_journal'],
        string_name='trading_journal',
        string_directory=display_options['string_results_directory'],
    )

    df_performance = evaluate_performance(
        df_prices=df_prices,
        dict_execution_results=dict_execution_results,
        float_budget_in_usd=float_budget_in_usd,
        benchmark_data_specifications=benchmark_data_specifications,
        strategy_hyperparameters=strategy_hyperparameters,
        display_options=display_options,
        constraints=constraints,
        general_settings=general_settings,
        start_time=start_time,
    )

    return [df_performance, dict_execution_results['df_trading_journal']]
