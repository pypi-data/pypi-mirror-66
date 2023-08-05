__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import os, sys
import pandas
from typing import Dict
from erlab_coat.preprocessing import add_cumsums_to_cases_table


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


def combine_dynamic_and_static_datasets(
        commute_dataset_filepath: str = '/Volumes/samsung/erlab_us_covid_spread/erlab_covid19_glance/resolution/state/commute.csv',
        cases_dataset_filepath: str = '/Volumes/samsung/erlab_us_covid_spread/erlab_covid19_glance/resolution/county/cases.csv',
        us_region_features_filepath: str = '/Users/mednet_machine/PHOENIX/er_covid_projects/erlab_covid19/app/static/aggregate_db/USHighResCOVID19SpreadDB.csv',
        interpolate_in_days: bool = False
) -> pandas.DataFrame:
    """
    The :func:`combine_dynamic_and_static_datasets` combines the static datasets including the state regions
    mentioned in our article with the dynamically changing datasets (commute and covid-19) to form the
    dataframes.

    Parameters
    ----------
    commute_dataset_filepath: `str`, required
        The filepath for the dataset

    cases_dataset_filepath: `str`, required
        The filepath for the dataset

    us_region_features_filepath: `str`, required
        The filepath for the dataset

    interpolate_in_days: `bool`, optional (default=False)
        If this is true, the values will be interpolated for days. Be cautious that in the cases
        of static plots this might lead to invalid interpretations (you do not want to add new cases
        to the dates with no new cases, but for animation, this helps smoothing the frames)

    Returns
    ----------
    The new dataframe will be returned.
    """
    commute = pandas.read_csv(commute_dataset_filepath)
    commute.rename({
        'State': 'state'
    }, inplace=True, axis="columns", errors="raise")
    commute['average_change_in_commute'] = (1 / 6.0) * (commute['change_in_commute_for_retail'] +
                                                        commute['change_in_commute_for_grocery_and_pharmacy'] + commute[
                                                            'change_in_commute_for_park'] + commute[
                                                            'change_in_commute_for_transit_stations']
                                                        + commute['change_in_commute_for_workplace'] + commute[
                                                            'change_in_commute_for_residential']).copy()

    commute['compliance'] = commute['average_change_in_commute'].apply(lambda x: -1 - (x - (100.0)) / 100.0).copy()
    commute = commute.loc[:, ['state', 'compliance']].copy()

    us_region_features = pandas.read_csv(us_region_features_filepath)
    us_region_features.fillna(0, inplace=True)

    us_region_features.set_index(['county', 'state'], inplace=True)

    if cases_dataset_filepath is not None:
        cases = pandas.read_csv(cases_dataset_filepath)
        cases.rename({
            'state_name': 'state',
            'county_name': 'county'
        }, inplace=True, axis="columns", errors="raise")
        cases = add_cumsums_to_cases_table(cases)
        cases.set_index(['county', 'state'], inplace=True)
        full = pandas.merge(right=cases, left=us_region_features, how="outer", left_index=True, right_index=True).copy()
        full['normalized_confirmed_count_cumsum'] = 1000.0 * full['confirmed_count_cumsum'] / full['total_population']
        full['normalized_death_count_cumsum'] = 1000.0 * full['death_count_cumsum'] / full['total_population']
    else:
        full = us_region_features.copy()

    full = pandas.merge(left=full.reset_index(), right=commute, on='state', how='outer').copy()
    full['compliance'].fillna(0, inplace=True)

    if interpolate_in_days:
        full = interpolate_by_location(full)

    full.dropna(inplace=True)

    return full
