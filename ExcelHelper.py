import math
import pandas as pd


def validate_excel_file(data_frame_path):
    try:
        DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")
        states = DataFrameToAnalyze["ESTADOS"][1:]
        any_non_string_state = states[states.apply(type) != str].any()

        if any_non_string_state:
            raise Exception("All States should be string values.")

        if "ERROR" in states:
            raise Exception("ERROR state isn't accpeted at this point, delete from the no deterministict automata.")

        zero_entrance_symbols = DataFrameToAnalyze.iloc[1:, 1].str.split(pat=',')

        for index, value in zero_entrance_symbols.items():

            if type(value) is float:
                continue

            for state in value:
                if state.isnumeric():
                    raise Exception(f"All states on input symbol 0 must be a string, state: {state} is not valid.")

                if not states.str.contains(state).any():
                    raise Exception(
                        f"All states on input symbol 0 must exists on state list, state: {state} is not valid.")

        one_entrance_symbols = DataFrameToAnalyze.iloc[1:, 2].str.split(pat=',')

        for index, value in one_entrance_symbols.items():

            if type(value) is float:
                continue

            for state in value:
                if state.isnumeric():
                    raise Exception(f"All states on input symbol 1 must be a string, state: {state} is not valid.")

                if not states.str.contains(state).any():
                    raise Exception(
                        f"All states on input symbol 1 must exists on state list, state: {state} is not valid.")

        result_states = DataFrameToAnalyze["ACEPTA (1) / RECHAZA (0)"][1:]

        any_non_integer_result_symbol = result_states[result_states.apply(type) != float].any()

        if any_non_integer_result_symbol:
            raise Exception("All state results must be a integer value.")

        all_result_symbols_are_valid = result_states.isin([0, 1]).all()

        if not all_result_symbols_are_valid:
            raise Exception("All state results must be a 0 or a 1 value.")

        return True

    except Exception as e:
        print(f"Error while trying to read file. Description: {e}")
        return False


def is_no_deterministic(data_frame_path):
    DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")[1:]
    DataFrameToAnalyze.columns = ['STATES', '0', '1', 'RESULT']
    inputs_splitted = DataFrameToAnalyze.iloc[:, 1:3]

    for index, row in inputs_splitted.iterrows():
        zero_input_states_length = 0 if type(row['0']) is float else len(row['0'].split(','))
        one_input_states_length = 0 if type(row['1']) is float else len(row['1'].split(','))
        if (zero_input_states_length == 0 or zero_input_states_length > 1) or (
                one_input_states_length == 0 or one_input_states_length > 1):
            return True

    return False


def generate_template():
    DataFrameTemplate = pd.DataFrame([['ESTADOS', 'SÍMBOLOS DE ENTRADA', '', 'ACEPTA (1) / RECHAZA (0)'],
                                      ['', 0, 1, '']
                                      ])
    DataFrameTemplate.to_excel(excel_writer="TEMPLATE.xlsx",
                               index=False,
                               header=False,
                               sheet_name='TEMPLATE')


def convert_to_deterministict(data_frame_path):
    DataFrameToAnalyze = pd.read_excel(io=data_frame_path, sheet_name="TEMPLATE")[1:]
    DataFrameToAnalyze.columns = ['STATES', '0', '1', 'RESULT']
    NewDF = pd.DataFrame({"STATES": [], "0": [], "1": [], "RESULT": []})
    states_created = pd.DataFrame(columns=["STATES", "COMBINED_STATES"])
    all_states = pd.concat([DataFrameToAnalyze['0'], DataFrameToAnalyze['1']], ignore_index=True)
    symbol_list = all_states.str.replace(',', '', regex=False).unique().tolist()
    symbol_list = [item for item in symbol_list if pd.notna(item)]
    is_first_loop = True
    states_to_be_deleted = []

    for row in DataFrameToAnalyze.itertuples(index=True):

        if not is_first_loop and row.STATES not in symbol_list:
            states_to_be_deleted.append(row.STATES)

        is_first_loop = False
        state_on_zero_input = row[2]
        state_on_zero_input = "" if type(row[2]) is float else state_on_zero_input.replace(',', '')

        state_on_one_input = row[3]
        state_on_one_input = "" if type(row[3]) is float else state_on_one_input.replace(',', '')

        if row.STATES not in NewDF["STATES"].values:
            NewDF.loc[len(NewDF)] = {"STATES": row.STATES, "0": state_on_zero_input,
                                     "1": state_on_one_input,
                                     "RESULT": row.RESULT}

        if state_on_zero_input != "" and state_on_zero_input not in NewDF["STATES"].values and state_on_zero_input not in DataFrameToAnalyze[
            "STATES"].values:
            states_created.loc[len(states_created)] = {"STATES": state_on_zero_input,
                                                       "COMBINED_STATES": list(state_on_zero_input)}
            NewDF.loc[len(NewDF), 'STATES'] = state_on_zero_input

        if state_on_one_input != "" and state_on_one_input not in NewDF["STATES"].values and state_on_one_input not in DataFrameToAnalyze[
            "STATES"].values:
            states_created.loc[len(states_created)] = {"STATES": state_on_one_input,
                                                       "COMBINED_STATES": list(state_on_one_input)}
            NewDF.loc[len(NewDF), 'STATES'] = state_on_one_input

    created_data_frame = create_new_states_on_automata(NewDF, states_created)
    created_data_frame = create_error_state_on_automata(created_data_frame)

    created_data_frame = created_data_frame[~created_data_frame['STATES'].isin(states_to_be_deleted)]

    return created_data_frame

def create_error_state_on_automata(created_data_frame):
    nan_rows_on_zero_input = created_data_frame[created_data_frame["0"] == ""]
    nan_rows_on_one_input = created_data_frame[created_data_frame["1"] == ""]

    for index, row in nan_rows_on_zero_input.iterrows():
        row_index_on_created_DF = created_data_frame[created_data_frame["STATES"] == row["STATES"]].index[0]
        created_data_frame.at[row_index_on_created_DF, "0"] = "ERROR"

    for index, row in nan_rows_on_one_input.iterrows():
        row_index_on_created_DF = created_data_frame[created_data_frame["STATES"] == row["STATES"]].index[0]
        created_data_frame.at[row_index_on_created_DF, "1"] = "ERROR"

    if len(nan_rows_on_zero_input) > 0 or len(nan_rows_on_one_input) > 0:
        created_data_frame.loc[len(created_data_frame)] = {"STATES": "ERROR", "0": "ERROR",
                                 "1": "ERROR",
                                 "RESULT": 0}

    return created_data_frame

def create_new_states_on_automata(created_data_frame, states_created):
    nan_rows = created_data_frame[pd.isna(created_data_frame["RESULT"])]
    for index, row in nan_rows.iterrows():

        if row["STATES"] in states_created["STATES"].values:
            row_index_on_created_DF = created_data_frame[created_data_frame["STATES"] == row["STATES"]].index[0]
            combined_states = states_created[states_created["STATES"] == row["STATES"]]["COMBINED_STATES"].values
            first_original_row = created_data_frame[created_data_frame["STATES"] == combined_states[0][0]]
            second_original_row = created_data_frame[created_data_frame["STATES"] == combined_states[0][1]]

            # Setting up Result value
            any_state_accept = first_original_row["RESULT"].values == 1 or second_original_row["RESULT"].values

            if any_state_accept:
                created_data_frame.at[row_index_on_created_DF, "RESULT"] = 1.0
            else:
                created_data_frame.at[row_index_on_created_DF, "RESULT"] = 0.0

            # Setting up Zero Input State
            first_row_zero_input = "" if type(first_original_row["0"].values[0]) is float else first_original_row["0"].values[0].replace(",", "")
            second_row_zero_input = "" if type(second_original_row["0"].values[0]) is float else second_original_row["0"].values[0].replace("", "")
            zero_input_combined = f"{first_row_zero_input}{second_row_zero_input}"
            zero_input_combined = ''.join(sorted(set(zero_input_combined)))
            created_data_frame.at[row_index_on_created_DF, "0"] = zero_input_combined

            if zero_input_combined != "" and zero_input_combined not in created_data_frame["STATES"].values:
                states_created.loc[len(states_created)] = {"STATES": zero_input_combined,
                                                           "COMBINED_STATES": [first_row_zero_input,
                                                                               second_row_zero_input]}
                created_data_frame.loc[len(created_data_frame), 'STATES'] = zero_input_combined

            # Setting up One Input State
            first_row_one_input = "" if type(first_original_row["1"].values[0]) is float else first_original_row["1"].values[0].replace(",", "")
            second_row_one_input = "" if type(second_original_row["1"].values[0]) is float else second_original_row["1"].values[0].replace("", "")
            one_input_combined = f"{first_row_one_input}{second_row_one_input}"
            one_input_combined = ''.join(sorted(set(one_input_combined)))
            created_data_frame.at[row_index_on_created_DF, "1"] = one_input_combined

            if one_input_combined != "" and one_input_combined not in created_data_frame["STATES"].values:
                states_created.loc[len(states_created)] = {"STATES": one_input_combined,
                                                           "COMBINED_STATES": [first_row_one_input,
                                                                               second_row_one_input]}
                created_data_frame.loc[len(created_data_frame), 'STATES'] = one_input_combined

        else:
            raise Exception(f"State {row["STATES"]} is invalid on this step.")

    if created_data_frame["RESULT"].isna().any():
        created_data_frame = create_new_states_on_automata(created_data_frame, states_created)

    return created_data_frame
