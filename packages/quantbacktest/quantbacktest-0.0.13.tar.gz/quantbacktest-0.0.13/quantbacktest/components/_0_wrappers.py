"""Serves as a high-level caller."""

# For counting the number of result files in the "results" folder to allow for
# consistent file versioning when saving the results as a csv file.
import os
import os.path

# For managing dates
from datetime import datetime

# For vector operations
from numpy import array

# For plots (especially the heatmap)
import matplotlib.pyplot as plt

from _1_data_preparation import prepare_data, save_dataframe_to_csv
from _2_strategy_execution import test_strategies


def backtest(
        file_path_with_price_data,
        int_chosen_strategy,
        dict_crypto_options,
        float_budget_in_usd,
        margin_loan_rate,
        display_options,
        general_settings,
        constraints,
        start_time,
        comments,
        file_path_with_signal_data=None,
        file_path_with_token_data=None,# Only for multi-asset strategies.
        name_of_foreign_key_in_price_data_table=None,
        name_of_foreign_key_in_token_metadata_table=None,
        boolean_allow_shorting=False,
        list_trading_execution_delay_after_signal_in_hours={
            'delay_before_buying': 0,
            'delay_before_selling': 0
        },
        minimum_expected_mispricing_trigger_in_percent={
            'mispricing_when_buying': 0.0,
            'mispricing_when_selling': 0.0
        },
        strategy_hyperparameters=None,
        sell_at_the_end=True,
        list_times_of_split_for_robustness_test=None,
        benchmark_data_specifications={# Bitcoin as default benchmark
            'name_of_column_with_benchmark_primary_key': 'id',
            'benchmark_key': 'TP3B-248N-Q',
            'file_path_with_benchmark_data': 'raw_itsa_data/20190717_itsa_tokenbase_top600_wtd302_token_daily.csv'
        }
    ):
    """Backtests a user-defined strategy.

    With user-defined price data and possibly many other parameters.
    """
    # assert percentage_selling_fees_and_spread >= 0, "Please choose positive selling slippage."
    # assert percentage_buying_fees_and_spread >= 0, "Please choose positive buying slippage."
    # assert percentage_selling_fees_and_spread == 0, "Please choose a selling slippage greater than zero."
    # assert percentage_buying_fees_and_spread == 0, "Please choose a buying slippage greater than zero."
    assert float_budget_in_usd > 0, "Please choose positive budget."
    # assert list_trading_execution_delay_after_signal_in_hours >= 0, "Please choose an execution delay greater than zero."
    # assert list_trading_execution_delay_after_signal_in_hours == 0, "Please choose an exectution delay greater than zero."

    ## Check if exposure is > 0 and <= 100
    ## Check if margin is between 0.01 and 1
    ## Check if fees are >= 0 and warn if fees = 0

    df_prices = prepare_data(
        file_path_with_price_data=file_path_with_price_data,
        file_path_with_token_data=file_path_with_token_data,
        strategy_hyperparameters=strategy_hyperparameters,
        name_of_foreign_key_in_price_data_table=name_of_foreign_key_in_price_data_table,
        name_of_foreign_key_in_token_metadata_table=name_of_foreign_key_in_token_metadata_table,
    )

    if list_times_of_split_for_robustness_test is None:
        dfs_results = test_strategies(
            df_prices=df_prices,
            int_chosen_strategy=int_chosen_strategy,
            float_budget_in_usd=float_budget_in_usd,
            file_path_with_signal_data=file_path_with_signal_data,
            margin_loan_rate=margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
            strategy_hyperparameters=strategy_hyperparameters,
            sell_at_the_end=sell_at_the_end,
            benchmark_data_specifications=benchmark_data_specifications,
            display_options=display_options,
            general_settings=general_settings,
            start_time=start_time,
            comments=comments
        )

    else:
        for sell_parameter in strategy_hyperparameters['sell_parameter_space']:
            for buy_parameter in strategy_hyperparameters['buy_parameter_space']:
                strategy_hyperparameters['sell_parameter'] = sell_parameter/10
                strategy_hyperparameters['buy_parameter'] = buy_parameter/10

                for index, dates in enumerate(list_times_of_split_for_robustness_test):
                    strategy_hyperparameters['start_time'] = dates[0]
                    strategy_hyperparameters['end_time'] = dates[1]

                    dfs_intermediate_results = test_strategies(
                        df_prices,
                        int_chosen_strategy=int_chosen_strategy,
                        float_budget_in_usd=float_budget_in_usd,
                        file_path_with_signal_data=file_path_with_signal_data,
                        margin_loan_rate=margin_loan_rate,
                        boolean_allow_shorting=boolean_allow_shorting,
                        list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
                        dict_crypto_options=dict_crypto_options,
                        minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
                        strategy_hyperparameters=strategy_hyperparameters,
                        sell_at_the_end=sell_at_the_end,
                        benchmark_data_specifications=benchmark_data_specifications,
                        display_options=display_options,
                        constraints=constraints,
                        general_settings=general_settings,
                        start_time=start_time,
                        comments=comments
                    )

                    try:
                        dfs_results[0] = dfs_results[0].append(
                            dfs_intermediate_results[0]
                        )
                        dfs_results[1] = dfs_results[1].append(
                            dfs_intermediate_results[1]
                        )
                    except:
                        dfs_results = dfs_intermediate_results

    save_dataframe_to_csv(
        dfs_results[0],
        string_name='backtesting_result_metrics',
        string_directory=display_options['string_results_directory'],
    )

    comments = {
        **{
            'file_path_with_price_data': file_path_with_price_data,
            'file_path_with_token_data': file_path_with_token_data,
            'name_of_foreign_key_in_price_dat_table': name_of_foreign_key_in_price_data_table,
            'name_of_foreign_key_in_token_metadata_table': name_of_foreign_key_in_token_metadata_table,
            'float_budget_in_usd': float_budget_in_usd,
            'margin_loan_rate': margin_loan_rate,
            'boolean_allow_shorting': boolean_allow_shorting,
            'list_trading_execution_delay_after_signal_in_hours': list_trading_execution_delay_after_signal_in_hours,
            'dict_crypto_options': dict_crypto_options,
            'minimum_expected_mispricing_trigger_in_percent': minimum_expected_mispricing_trigger_in_percent,
            'strategy_hyperparameters': strategy_hyperparameters,
            'sell_at_the_end': sell_at_the_end,
        },
        **comments
    }


    return {
        'df_performance': dfs_results[0],
        'df_trading_journal': dfs_results[1],
        'comments': comments
    }

def plot_robustness_heatmap(
        df_performance,
        display_options,
        boolean_save=True,
        boolean_show=False
    ):
    """Plots each row that is contained in the performance table.

    With the attributes 'start date' on the x-axis and 'duration' on the y-axis.
    """

    dict_heatmap = {
        'Begin time of tested interval': [],
        'Duration of the tested interval': [],
        'USD annualized ROI (from first to last trade)': []
    }

    for index, row in df_performance.iterrows():
        begin_date = row['Begin time of tested interval']
        strategy_duration_in_days = int(
            row['Duration of the tested interval'].days
        )
        roi = row['USD annualized ROI (from first to last trade)']
        dict_heatmap['Begin time of tested interval'].append(begin_date)
        dict_heatmap['Duration of the tested interval'].append(strategy_duration_in_days)
        dict_heatmap['USD annualized ROI (from first to last trade)'].append(roi)

    # x_axis = array(dict_heatmap['Begin time of tested interval'], dtype=datetime)
    x_axis = [i.to_pydatetime() for i in dict_heatmap['Begin time of tested interval']]
    y_axis = dict_heatmap['Duration of the tested interval']
    z_values = dict_heatmap['USD annualized ROI (from first to last trade)']

    figure, axis = plt.subplots()
    plt.ylabel('Duration (in days)')
    axis.set_xlabel('Begin time of tested interval')
    plt.xticks(rotation=70)
    plt.title('ROI heatmap (in percent)')
    points = axis.scatter(
        x_axis,
        y_axis,
        c=z_values,
        s=1300,# Size of scatters
        cmap='RdYlGn',# Taken from here: https://matplotlib.org/users/colormaps.html
        marker="s"
    )
    figure.colorbar(points)

    string_directory = display_options['string_results_directory']
    result_no = len(
        [name for name in os.listdir(string_directory) if os.path.isfile(
            os.path.join(
                string_directory,
                name
            )
        )]
    ) / 2

    number_of_result_files_plus_1 = 1 + int(result_no)

    if boolean_save:
        plt.savefig(string_directory + '/robustness_heatmap_' + str(number_of_result_files_plus_1) + '.png')

    if boolean_show:
        plt.show()

def backtest_visualizer(
        file_path_with_price_data,
        int_chosen_strategy,
        dict_crypto_options,
        benchmark_data_specifications,
        display_options,
        strategy_hyperparameters,
        constraints,
        general_settings,
        margin_loan_rate,
        file_path_with_token_data=None, # Only for multi-asset strategies.
        name_of_foreign_key_in_price_data_table=None,
        name_of_foreign_key_in_token_metadata_table=None,
        float_budget_in_usd=10000,
        boolean_allow_shorting=False,
        list_trading_execution_delay_after_signal_in_hours={
            'delay_before_buying': 24,
            'delay_before_selling': 24
        },
        minimum_expected_mispricing_trigger_in_percent={
            'mispricing_when_buying': 0.0,
            'mispricing_when_selling': 0.0
        },
        sell_at_the_end=True,
        list_times_of_split_for_robustness_test=None,
        file_path_with_signal_data=None,
        comments={}
    ):
    """Prints and plots results from the performance table."""

    start_time = datetime.now()
    dict_backtesting = backtest(
        file_path_with_price_data=file_path_with_price_data,
        file_path_with_token_data=file_path_with_token_data,
        name_of_foreign_key_in_price_data_table=name_of_foreign_key_in_price_data_table,
        name_of_foreign_key_in_token_metadata_table=name_of_foreign_key_in_token_metadata_table,
        float_budget_in_usd=float_budget_in_usd,
        margin_loan_rate=margin_loan_rate,
        boolean_allow_shorting=boolean_allow_shorting,
        list_trading_execution_delay_after_signal_in_hours=list_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options=dict_crypto_options,
        minimum_expected_mispricing_trigger_in_percent=minimum_expected_mispricing_trigger_in_percent,
        strategy_hyperparameters=strategy_hyperparameters,
        sell_at_the_end=sell_at_the_end,
        list_times_of_split_for_robustness_test=list_times_of_split_for_robustness_test,
        benchmark_data_specifications=benchmark_data_specifications,
        int_chosen_strategy=int_chosen_strategy,
        file_path_with_signal_data=file_path_with_signal_data,
        display_options=display_options,
        constraints=constraints,
        general_settings=general_settings,
        start_time=start_time,
        comments=comments
    )
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    asset_name = list(dict_crypto_options.keys())[0]
    print("\n")
    print("Execution started at: " + str(start_time) + ", finished at: " + str(end_time) + ", elapsed time:", str(elapsed_time.total_seconds()) + "s")
    print("****  Performance overview ->", asset_name, "<- ****")
    print("Key metrics")
    print("*USD annualized ROI (from first to last trade):", "{0:.2%}".format(dict_backtesting['df_performance']['USD annualized ROI (from first to last trade)'].iloc[-1]))
    if type(dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1]) is str:
        print("*Cryptocurrency annualized ROI delta (from first to last trade):", dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1])
    else:
        print("*Cryptocurrency annualized ROI delta (from first to last trade):", "{0:.2%}".format(dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1]))
    print("Number of trades:", len(dict_backtesting['df_trading_journal']))
    print("Other metrics")
    print("**** Assumptions ****")
    print("*Budget:", dict_backtesting['comments']['float_budget_in_usd'])
    print("*Check arguments and parameter defaults for a full list of assumptions.*")

    plot_robustness_heatmap(
        dict_backtesting['df_performance'],
        display_options=display_options,
        boolean_show=display_options['boolean_plot_heatmap']
    )

    return dict_backtesting
