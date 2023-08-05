__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import os, sys
import pandas
from typing import Dict


def preprocess_dataset_further(
        df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    The :func:`preprocess_dataset_further` takes care of further preprocessings such as normalizing election results.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The now modified output dataframe which is an instance of `pandas.DataFrame`.
    """
    df['democrat_percentage'] = df['democrat'] / (df['democrat'] + df['republican'] + df['other'])
    df['republican_percentage'] = df['republican'] / (df['democrat'] + df['republican'] + df['other'])
    df['other_than_democrat_or_republican_percentage'] = df['other'] / (df['democrat'] + df['republican'] + df['other'])

    df['population_density'] = df['total_population'] / df['sum_land_area']
    df = make_state_county_composite_index(df)
    return df


def make_state_county_composite_index(
        df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    The :func:`make_state_county_composite_index` takes care of creating and adding the composite index of
    state and county to the dataframe.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The now modified output dataframe which is an instance of `pandas.DataFrame`.
    """
    df['location'] = df['county'] + "_" + df['state']
    return df


def merge_all_dfs_in_dict(in_dict: Dict[str, pandas.DataFrame]) -> pandas.DataFrame:
    """
    The :func:`merge_all_dfs_in_dict` is for merging all the dataframes in a dict by their indexes.

    Parameters
    ----------
    in_dict: `Dict[str, pandas.DataFrame])`, required
        The input dictionary of dataframes

    Returns
    ----------
    The output dataframe will be returned.
    """
    state_table = None
    for key in in_dict.keys():
        if state_table is None:
            state_table = in_dict[key].copy()
        else:
            tmp1 = state_table.copy()
            tmp2 = in_dict[key].copy()
            state_table = pandas.merge(right=tmp1, left=tmp2, how="outer", left_index=True, right_index=True).copy()
            tmp1 = None
            tmp2 = None
    return state_table


def interpolate_by_location(df: pandas.DataFrame, column_to_interpolate_on: str = 'day_of_the_year') -> pandas.DataFrame:
    """
    The :func:`interpolate_by_location` helps with interpolating the values between the first and last
    day of events for our dataframes to have more consistent COVID-19 information.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The main pandas dataframe that is loaded.

    column_to_interpolate_on: `str`, required
        In COVID-19 case it is usually the day of the year column

    Returns
    -----------
    This method returns the now modified dataframe
    """
    if 'location' not in df.columns.tolist():
        df['location'] = (df['county'] + '_' + df['state']).copy()
    #df.reset_index(inplace=True)
    df.sort_values(by=['location', 'day_of_the_year'], inplace=True)
    min_day = int(df['day_of_the_year'].min())
    max_day = int(df['day_of_the_year'].max())
    unique_locations = df['location'].unique().tolist()
    rows_to_concat = []
    for location in unique_locations:
        tmp = df[df['location']==location].copy()
        try:
            first_day_in_location = int(tmp['day_of_the_year'].min())
        except:
            continue
        for day in range(first_day_in_location, max_day + 1):
            tmp2 = tmp[tmp['day_of_the_year'] == day].copy()
            if tmp2.shape[0] == 0:
                prev_row['day_of_the_year'] = day
                rows_to_concat.append(prev_row.copy())
            else:
                prev_row = tmp2.iloc[0, :].copy()

    df = pandas.concat([df.copy(), pandas.DataFrame(rows_to_concat)])
    return df


def add_prefix_to_df_columns(df: pandas.DataFrame, prefix: str) -> pandas.DataFrame:
    """
    Adding prefix to the columns using this method.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The resulting dataframe will be returned.
    """
    for column in df.columns.tolist():
        df.rename({column: prefix + "_" + column}, inplace=True, axis="columns", errors="raise")
    return df


def parse_erlab_covid19_glance_collection(collection_path: str) -> Dict[str, Dict[str, pandas.DataFrame]]:
    """
    The :func:`parse_erlab_covid19_glance_collection` parses and loads ERLab's collection of US counties and
    COVID-19 outbreak.

    Parameters
    ----------
    collection_path: `str`, required
        The path to the directory of collection, which is produced by the extraction of the file you have downloaded.

    Returns
    ----------
    The output is of `Dict[str, Dict[str, pandas.DataFrame]]`, and is composed of information both for counties and states
    along with needed metadata.
    """
    collection_path = os.path.abspath(collection_path)
    output = {
        'state': dict(),
        'county': dict(),
        'meta': dict()
    }
    for key in output.keys():
        tmp_path = os.path.join(collection_path, 'resolution', key)
        files = [e for e in os.listdir(tmp_path) if (e.endswith('.csv')) and (not e.startswith('.'))]
        for file in files:
            try:
                output[key][file.split('.')[0]] = pandas.read_csv(os.path.join(tmp_path, file))
            except Exception as e:
                output[key][file.split('.')[0]] = pandas.read_csv(os.path.join(tmp_path, file), encoding="ISO-8859-1")
    return output
