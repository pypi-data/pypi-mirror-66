#%%

""" Just copy of inner content of main function. Developing is much faster
having all variables in variable explorer and all plots in jupyter cell because code is not in fuction but declarative.
After finishing developing, just copy result back in main.

"""



if __name__ == "__main__":

    from pathlib import Path
    import sys

    jupyter = 0
    this_path = Path(__file__).resolve().parents[1]
    this_path_string = str(this_path)

    from pathlib import Path
    import numpy as np
    #import matplotlib.pyplot as plt
    from prettytable import PrettyTable
    import time
    import pandas as pd
    import warnings
    import inspect
    import argparse

    this_path = Path(__file__).resolve().parents[1]
    this_path_string = str(this_path)

    if 'predictit' not in sys.modules:

        # If used not as a library but as standalone framework, add path to be able to import predictit if not opened in folder
        sys.path.insert(0, this_path_string)

        import predictit

    from predictit.config import config, presets
    from predictit.misc import traceback_warning, user_warning, _GUI

    def update_gui(content, id):
        try:
            gui_start.edit_gui_py(content, id)
        except Exception:
            pass




    data_complete = pd.DataFrame()

    # for file in list(glob.glob(f'{lib_path_str}/*.txt')):
    #     data_complete = pd.concat([data_complete, pd.read_csv(file, index_col=False, sep='\t', decimal=',', encoding='cp1250')])

    data_complete = pd.read_csv(r"C:\Users\truton\ownCloud\Github\Oxy_data\Dan\data\20160125.txt", index_col=False, sep='\t', decimal=',', encoding='cp1250')[10: -100]
    config = predictit.config.config

    config.update({
        'used_function': 'compare_models',

        'data_all': {
            'data 1': data_complete[:-20],
            'data 2': data_complete[:-100],
            'data 3': data_complete[:-200],
            'data 4': data_complete[:-300],
            'data 5': data_complete[:-400],
            'data 6': data_complete[:-500],
        },
        'data': data_complete[-1000:],
        'predicted_column': 'CO2 (%)',
        'datetime_index': 'čas',  # Index of dataframe datetime column or it's name if it has datetime column. If there already is index in input data, it will be used automatically.

        'debug': 1,
        'freq': '10S',
        'default_n_steps_in': 15,
        'datalength': 0,
        'other_columns': 0,
        'default_other_columns_length': 2,
        'standardize': 'standardize',
        'remove_outliers': 0,
        'correlation_threshold': 0,
        'data_transform': 0,

        'optimizeit': 0,
        'optimizeit_limit': 10,
        'optimizeit_details': 3,

        'predicts': 12,
        'compareit': 20,
        'repeatit': 50,
        'return_type': 'best',







    })



    config['standardize'] = 0



    _GUI = predictit.misc._GUI
    # Add everything printed + warnings to variable to be able to print in GUI
    if _GUI:
        import io

        stdout = sys.stdout
        sys.stdout = io.StringIO()

    if config["use_config_preset"] and config["use_config_preset"] != 'none':
        config.update(presets[config["use_config_preset"]])

    # Parse all functions parameters and it's values
    args, _, _, values = inspect.getargvalues(inspect.currentframe())

    # Edit config.py default values with arguments values if exist
    config.update({key: value for key, value in values.items() if key in args & values.keys() and value is not None})

    # Do not repeat actually mean evaluate once
    if not config['repeatit']:
        config['repeatit'] = 1

    # Some config values are derived from other values. If it has been changed, it has to be updated.
    predictit.config.update_references_1()
    predictit.config.update_references_2()

    # Find difference between original config and set values and if there are any differences, raise error
    config_errors = set(config.keys()) - predictit.config.config_check_set
    if config_errors:
        raise KeyError(f"Some config values: {config_errors} was named incorrectly. Check config.py for more informations")

    # Definition of the table for spent time on code parts
    time_parts_table = PrettyTable()
    time_parts_table.field_names = ["Part", "Time"]

    def update_time_table(time_last):
        time_parts_table.add_row([progress_phase, time.time() - time_last])
        return time.time()
    time_point = time_begin = time.time()

    #######################################
    ############## LOAD DATA ####### ANCHOR Data
    #######################################

    progress_phase = "Data loading and preprocessing"
    update_gui(progress_phase, 'progress_phase')

    if config['data'] is None:

        ############# Load CSV data #############
        if config['data_source'] == 'csv':
            if config['csv_test_data_relative_path']:
                try:
                    data_location = this_path / 'predictit' / 'test_data'
                    csv_path = data_location / config['csv_test_data_relative_path']
                    config['csv_full_path'] = Path(csv_path).as_posix()
                except Exception:
                    print(f"\n ERROR - Test data load failed - Setup CSV adress and column name in config \n\n")
                    raise
            try:
                config['data'] = pd.read_csv(config['csv_full_path'], header=0).iloc[-config['datalength']:, :]
            except Exception:
                print("\n ERROR - Data load failed - Setup CSV adress and column name in config \n\n")
                raise

        ############# Load SQL data #############
        elif config['data_source'] == 'sql':
            try:
                config['data'] = predictit.database.database_load(server=config['server'], database=config['database'], freq=config['freq'],
                                                                  data_limit=config['datalength'], last=config['last_row'])
            except Exception:
                print("\n ERROR - Data load from SQL server failed - Setup server, database and predicted column name in config \n\n")
                raise

        elif config['data_source'] == 'test':
            config['data'] = predictit.test_data.generate_test_data.gen_random(config['datalength'])
            user_warning("Test data was used. Setup config.py where are possible options with comments. Data can be insert as function parameters, with editing config.py or with CLI.")

    ##############################################
    ############ DATA PREPROCESSING ###### ANCHOR Preprocessing
    #############################################

    if not config['predicted_column']:
        config['predicted_column'] = 0

    ### Data are used in shape (n_features, n_samples)!!! - other way that usual convention... if iterate data_for_predictions[i] - you have columns

    data_for_predictions, data_for_predictions_df, predicted_column_name = predictit.data_preprocessing.data_consolidation(config['data'])

    if config['mode'] == 'validate':
        data_for_predictions, test = predictit.data_preprocessing.split(data_for_predictions, predicts=config['predicts'])
        data_for_predictions_df, test_df = predictit.data_preprocessing.split(data_for_predictions_df, predicts=config['predicts'])

    predicted_column_index = 0

    multicolumn = 0 if data_for_predictions.shape[0] == 1 else 1

    if config['analyzeit'] == 1 or config['analyzeit'] == 3:
        predictit.analyze.analyze_data(data_for_predictions.T, window=30)

    ########################################
    ############# Data analyze ###### ANCHOR Analyze
    ########################################

    if config['remove_outliers']:
        data_for_predictions = predictit.data_preprocessing.remove_outliers(data_for_predictions, predicted_column_index=predicted_column_index, threshold=config['remove_outliers'])

    if config['correlation_threshold'] and multicolumn:
        data_for_predictions = predictit.data_preprocessing.keep_corelated_data(data_for_predictions, threshold=config['correlation_threshold'])

    ### Data preprocessing, common for all datatypes ###

    column_for_predictions_dataframe = data_for_predictions_df[data_for_predictions_df.columns[0]].to_frame()
    column_for_plot = column_for_predictions_dataframe.iloc[-7 * config['predicts']:]

    last_value = column_for_plot.iloc[-1]

    try:
        number_check = int(last_value)
    except Exception:
        raise ValueError(f"\n ERROR - Predicting not a number datatype. Maybe bad config['predicted_columns'] setup.\n Predicted datatype is {type(last_value[1])} \n\n")

    if config['data_transform'] == 'difference':

        for i in range(len(data_for_predictions)):
            data_for_predictions[i, 1:] = predictit.data_preprocessing.do_difference(data_for_predictions[i])

    if config['standardize']:
        data_for_predictions, final_scaler = predictit.data_preprocessing.standardize(data_for_predictions, used_scaler=config['standardize'])

    column_for_predictions = data_for_predictions[predicted_column_index]

    ############# Processed data analyze ############

    data_shape = np.shape(data_for_predictions)
    data_length = len(column_for_predictions)

    data_std = np.std(data_for_predictions[0, -30:])
    data_mean = np.mean(data_for_predictions[0, -30:])
    data_abs_max = max(abs(column_for_predictions.min()), abs(column_for_predictions.max()))

    multicolumn = 0 if data_shape[0] == 1 else 1

    if config['analyzeit'] == 2 or config['analyzeit'] == 3:
        predictit.analyze.analyze_data(data_for_predictions.T, window=30)

        # TODO repair decompose
        #predictit.analyze.decompose(column_for_predictions_dataframe, freq=36, model='multiplicative')

    min_data_length = 3 * config['predicts'] + config['default_n_steps_in']

    if data_length < min_data_length:
        config['repeatit'] = 1
        min_data_length = 3 * config['predicts'] + config['repeatit'] * config['predicts'] + config['default_n_steps_in']

    assert (min_data_length < data_length), 'To few data - set up less repeat value in settings or add more data'

    if config['lengths']:
        data_lengths = [data_length, int(data_length / 2), int(data_length / 4), min_data_length + 50, min_data_length]
        data_lengths = [k for k in data_lengths if k >= min_data_length]
    else:
        data_lengths = [data_length]

    data_number = len(data_lengths)

    models_names = list(config['used_models'].keys())
    models_number = len(models_names)

    for i in models_names:

        # If no parameters or parameters details, add it so no index errors later
        if i not in config['models_parameters']:
            config['models_parameters'][i] = {}

    # Empty boxes for results definition
    # The final result is - [repeated, model, data, results]
    test_results_matrix = np.zeros((config['repeatit'], models_number, data_number, config['predicts']))
    evaluated_matrix = np.zeros((config['repeatit'], models_number, data_number))
    reality_results_matrix = np.zeros((models_number, data_number, config['predicts']))
    test_results_matrix.fill(np.nan)
    evaluated_matrix.fill(np.nan)
    reality_results_matrix.fill(np.nan)

    models_time = {}
    models_optimizations_time = {}

    time_point = update_time_table(time_point)
    progress_phase = "Predict"
    update_gui(progress_phase, 'progress_phase')

    trained_models = {}

    models_test_outputs = np.zeros((config['repeatit'], config['predicts']))

    for i in range(config['repeatit']):

        models_test_outputs[i] = column_for_predictions[-config['predicts'] - i: - i] if i > 0 else column_for_predictions[-config['predicts'] - i:]

    models_test_outputs = models_test_outputs[::-1]

    data_end = -config['predicts'] - config['repeatit'] - 100 if config['mode'] == 'validate' else None

    used_input_types = []
    for i in models_names:
        used_input_types.append(config['models_input'][i])
    used_input_types = set(used_input_types)

    #######################################
    ############# Main loop ######## ANCHOR Main loop
    #######################################

    for data_length_index, data_length_iteration in enumerate(data_lengths):

        for input_type in used_input_types:
            try:
                used_sequention = predictit.define_inputs.create_inputs(input_type, data_for_predictions, predicted_column_index=predicted_column_index)
            except Exception:
                traceback_warning(f"Error in creating sequentions on input type: {input_type} model on data length: {data_length_iteration}")
                continue

            for iterated_model_index, (iterated_model_name, iterated_model) in enumerate(config['used_models'].items()):
                if config['models_input'][iterated_model_name] == input_type:

                    if config['models_input'][iterated_model_name] in ['one_step', 'one_step_constant']:
                        if multicolumn and config['predicts'] > 1:

                            user_warning(f"""Warning in model {iterated_model_name} \n\nOne-step prediction on multivariate data (more columns).
                                             Use batch (y lengt equals to predict) or do use some one column data input in config models_input or predict just one value.""")
                            continue

                    if isinstance(used_sequention, tuple):
                        model_train_input = (used_sequention[0][data_length - data_length_iteration: data_end, :], used_sequention[1][data_length - data_length_iteration: data_end, :])
                        model_predict_input = used_sequention[2]
                        model_test_inputs = used_sequention[3]

                    elif used_sequention.ndim == 1:
                        model_train_input = used_sequention[data_length - data_length_iteration: data_end]
                        model_predict_input = used_sequention[data_length - data_length_iteration:]
                        model_test_inputs = []
                        for i in range(config['repeatit']):
                            model_test_inputs.append(used_sequention[data_length - data_length_iteration: - config['predicts'] - config['repeatit'] + i + 1])

                    else:
                        model_train_input = used_sequention[:, data_length - data_length_iteration: data_end]
                        model_predict_input = used_sequention[:, data_length - data_length_iteration:]
                        model_test_inputs = []
                        for i in range(config['repeatit']):
                            model_test_inputs.append(used_sequention[:, data_length - data_length_iteration: - config['predicts'] - config['repeatit'] + i + 1])

                    if config['optimizeit'] and data_length_index == 0:
                        if iterated_model_name in config['models_parameters_limits']:

                            try:
                                start_optimization = time.time()

                                best_kwargs = predictit.best_params.optimize(iterated_model, config['models_parameters'][iterated_model_name], config['models_parameters_limits'][iterated_model_name],
                                                                             model_train_input=model_train_input, model_test_inputs=model_test_inputs, models_test_outputs=models_test_outputs,
                                                                             fragments=config['fragments'], iterations=config['iterations'], time_limit=config['optimizeit_limit'],
                                                                             error_criterion=config['error_criterion'], name=iterated_model_name, details=config['optimizeit_details'])

                                for k, l in best_kwargs.items():

                                    config['models_parameters'][iterated_model_name][k] = l

                            except Exception:
                                traceback_warning("Optimization didn't finished")

                            finally:
                                stop_optimization = time.time()
                                models_optimizations_time[iterated_model_name] = (stop_optimization - start_optimization)

                    try:
                        start = time.time()

                        # Train all models
                        trained_models[iterated_model_name] = iterated_model.train(model_train_input, **config['models_parameters'][iterated_model_name])

                        # Create predictions - out of sample
                        one_reality_result = iterated_model.predict(model_predict_input, trained_models[iterated_model_name], predicts=config['predicts'])

                        if np.isnan(np.sum(one_reality_result)) or one_reality_result is None:
                            continue

                        # Remove wrong values out of scope to not be plotted

                        one_reality_result[abs(one_reality_result) > 3 * data_abs_max] = np.nan

                        # Do inverse data preprocessing
                        if config['power_transformed'] == 1:
                            one_reality_result = predictit.data_preprocessing.fitted_power_transform(one_reality_result, data_std, data_mean)

                        if config['standardize']:
                            one_reality_result = final_scaler.inverse_transform(one_reality_result.reshape(-1, 1)).ravel()

                        if config['data_transform'] == 'difference':
                            one_reality_result = predictit.data_preprocessing.inverse_difference(one_reality_result, last_value)

                        reality_results_matrix[iterated_model_index, data_length_index] = one_reality_result

                        # Predict many values in test inputs to evaluate which models are best - do not inverse data preprocessing, because test data are processed
                        for repeat_iteration in range(config['repeatit']):

                            # Create in-sample predictions to evaluate if model is good or not

                            test_results_matrix[repeat_iteration, iterated_model_index, data_length_index] = iterated_model.predict(model_test_inputs[repeat_iteration], trained_models[iterated_model_name], predicts=config['predicts'])

                            if config['power_transformed'] == 2:
                                test_results_matrix[repeat_iteration, iterated_model_index, data_length_index] = predictit.data_preprocessing.fitted_power_transform(test_results_matrix[repeat_iteration, iterated_model_index, data_length_index], data_std, data_mean)

                            evaluated_matrix[repeat_iteration, iterated_model_index, data_length_index] = predictit.evaluate_predictions.compare_predicted_to_test(test_results_matrix[repeat_iteration, iterated_model_index, data_length_index],
                                                                                                                                                                   models_test_outputs[repeat_iteration], error_criterion=config['error_criterion'])

                    except Exception:
                        traceback_warning(f"Error in {iterated_model_name} model on data length {data_length_iteration}")

                    finally:
                        models_time[iterated_model_name] = (time.time() - start)

    #############################################
    ############# Evaluate models ######## ANCHOR Evaluate
    #############################################

    # Criterion is the best of average from repetitions
    time_point = update_time_table(time_point)
    progress_phase = "Evaluation"
    update_gui(progress_phase, 'progress_phase')

    repeated_average = np.mean(evaluated_matrix, axis=0)

    model_results = []

    for i in repeated_average:
        model_results.append(np.nan if np.isnan(i).all() else np.nanmin(i))

    sorted_results = np.argsort(model_results)

    if config['compareit']:
        sorted_results = sorted_results[:config['compareit']]
    else:
        sorted_results = sorted_results[0]

    predicted_models = {}

    for i, j in enumerate(sorted_results):
        this_model = list(config['used_models'].keys())[j]

        if i == 0:
            best_model_name = this_model

        predicted_models[this_model] = {'order': i + 1, 'error_criterion': model_results[j], 'predictions': reality_results_matrix[j, np.argmin(repeated_average[j])], 'data_length': np.argmin(repeated_average[j])}

    best_model_predicts = predicted_models[best_model_name]['predictions'] if best_model_name in predicted_models else "Best model had an error"

    complete_dataframe = column_for_plot.copy()

    if config['confidence_interval'] == 'default':
        try:
            lower_bound, upper_bound = predictit.misc.confidence_interval(column_for_plot, predicts=config['predicts'], confidence=config['confidence_interval'])
            complete_dataframe['Lower bound'] = complete_dataframe['Upper bound'] = None
            bounds = True
        except Exception:
            bounds = False
            traceback_warning("Error in compute confidence interval")

    else:
        bounds = False

    last_date = column_for_plot.index[-1]

    if isinstance(last_date, (pd.core.indexes.datetimes.DatetimeIndex, pd._libs.tslibs.timestamps.Timestamp)):
        date_index = pd.date_range(start=last_date, periods=config['predicts'] + 1, freq=column_for_plot.index.freq)[1:]
        date_index = pd.to_datetime(date_index)

    else:
        date_index = list(range(last_date + 1, last_date + config['predicts'] + 1))

    results_dataframe = pd.DataFrame(data={'Lower bound': lower_bound, 'Upper bound': upper_bound}, index=date_index) if bounds else pd.DataFrame(index=date_index)

    for i, j in predicted_models.items():
        if 'predictions' in j:
            results_dataframe[f"{j['order']} - {i}"] = j['predictions']
            complete_dataframe[f"{j['order']} - {i}"] = None
            if j['order'] == 1:
                best_model_name_plot = f"{j['order']} - {i}"

    if config['mode'] == 'validate':
        best_model_name_plot = 'Test'
        results_dataframe['Test'] = test

    last_value = float(column_for_plot.iloc[-1])

    complete_dataframe = pd.concat([complete_dataframe, results_dataframe], sort=False)
    complete_dataframe.iloc[-config['predicts'] - 1] = last_value

    #######################################
    ############# Plot ############# ANCHOR Plot
    #######################################

    time_point = update_time_table(time_point)
    progress_phase = "plot"
    update_gui(progress_phase, 'progress_phase')

    if config['plot']:

        plot_return = 'div' if _GUI else ''
        div = predictit.plot.plotit(complete_dataframe, plot_type=config['plot_type'], show=config['show_plot'], save=config['save_plot'], save_path=config['save_plot_path'],
                                    plot_return=plot_return, best_model_name=best_model_name_plot, predicted_column_name=predicted_column_name)


    ####################################
    ############# Results ####### ANCHOR Results
    ####################################

    if config['print']:
        if config['print_result']:
            print(f"\n Best model is {best_model_name} \n\t with results {best_model_predicts} \n\t with model error {config['error_criterion']} = {predicted_models[best_model_name]['error_criterion']}")
            print(f"\n\t with data length {data_lengths[predicted_models[best_model_name]['data_length']]} \n\t with paramters {config['models_parameters'][best_model_name]} \n")


        # Table of results
        models_table = PrettyTable()
        models_table.field_names = ['Model', f"Average {config['error_criterion']} error", "Time"]
        # Fill the table
        for i, j in predicted_models.items():
            if i in models_time:
                models_table.add_row([i, j['error_criterion'], models_time[i]])

        if config['print_table']:
            print(f'\n {models_table} \n')

        time_parts_table.add_row(['Complete time', time.time() - time_begin])

        if config['print_time_table']:
            print(f'\n {time_parts_table} \n')

        ### Print detailed resuts ###
        if config['print_detailed_result']:

            for i, j in enumerate(models_names):
                print(models_names[i])

                for k in range(data_number):
                    print(f"\t With data length: {data_lengths[k]}  {config['error_criterion']} = {repeated_average[i, k]}")

                if config['optimizeit']:
                    if j in models_optimizations_time:
                        print(f"\t Time to optimize {models_optimizations_time[j]} \n")
                    print("Best models parameters", config['models_parameters'][j])

    time_point = update_time_table(time_point)
    progress_phase = 'finished'
    update_gui(progress_phase, 'progress_phase')

    # Return stdout and stop collect warnings and printed output
    if _GUI:
        output = sys.stdout.getvalue()
        sys.stdout = stdout

        print(output)
