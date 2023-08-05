__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pandas
import os
from typing import Dict, List, Tuple, Any
from functools import reduce
from erlab_coat.meta import *
from datetime import date


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


def createUSHighResCOVID19SpreadDB(
        tables_root_directory: str,
        output_directory: str = '.'
) -> None:
    """
    The :func:`createUSHighResCOVID19SpreadDB` takes care of merging and preprocessing
    the integration of all the data resources on the US regions.

    Parameters
    ----------
    tables_root_directory: `str`, required
        The root directory to the dataset tables folder

    output_directory: `str`, optional(default='.')
        The path to the output directory

    """

    collection_path = tables_root_directory  # '/Volumes/samsung/erlab_us_covid_spread/erlab_covid19_glance/'
    collection = parse_erlab_covid19_glance_collection(collection_path=collection_path)

    ## preprocessing
    for key in preprocessings.keys():
        for table_name in preprocessings[key].keys():
            table = collection[key][table_name].copy()
            lambdas = preprocessings[key][table_name]['lambdas']
            renames = preprocessings[key][table_name]['rename']
            remove = preprocessings[key][table_name]['remove']
            for column in lambdas.keys():
                table[column] = table[column].apply(lambdas[column])
            table.rename(renames, inplace=True, axis="columns", errors="raise")
            table.drop(columns=remove, inplace=True)
            collection[key][table_name] = table.copy()
            table = None

    ## further preprocessing

    # income
    def income_check1(x):
        try:
            output = x.split(',')[1]
        except:
            output = 'bad'
        return output

    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['Location'].apply(
        income_check1)
    collection['county']['diversityindex'] = collection['county']['diversityindex'][
        collection['county']['diversityindex']['state'] != 'bad']
    collection['county']['diversityindex']['county'] = collection['county']['diversityindex']['Location'].apply(
        lambda x: x.split(', ')[0][:-7])
    collection['county']['diversityindex'].drop(columns=['Location'], inplace=True)

    # diversity
    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['state'].apply(
        lambda x: x.strip())

    # mortality
    def mortality_check1(x):
        try:
            output = x.split(', ')[1]
        except:
            output = 'bad'
        return output

    collection['county']['mortality']['state'] = collection['county']['mortality']['county'].apply(
        mortality_check1).copy()
    collection['county']['mortality'] = collection['county']['mortality'][
        collection['county']['mortality']['state'] != 'bad']
    collection['county']['mortality']['county'] = collection['county']['mortality']['county'].apply(
        lambda x: x.split(',')[0][:-7])
    collection['county']['mortality']['state'] = collection['county']['mortality']['state'].apply(
        lambda x: state_abbreviations[x])

    # election
    collection['county']['election'].drop(columns=['state_po'], inplace=True)
    collection['county']['election'] = collection['county']['election'][
        collection['county']['election']['year'] == 2016]
    collection['county']['election']['state'] = collection['county']['election']['state'].apply(
        lambda x: state_abbreviations[x])
    output = {
        'state': [],
        'county': [],
        'democrat': [],
        'republican': [],
        'other': [],
    }

    for i in range(collection['county']['election'].shape[0]):
        row = collection['county']['election'].iloc[i, :]
        output['state'] += [row['state']]
        output['county'] += [row['county']]
        if row['party'] == 'democrat':
            output['democrat'] += [row['candidatevotes']]
            output['republican'] += [0]
            output['other'] += [0]
        elif row['party'] == 'republican':
            output['republican'] += [row['candidatevotes']]
            output['democrat'] += [0]
            output['other'] += [0]
        else:
            output['republican'] += [0]
            output['democrat'] += [0]
            output['other'] += [row['candidatevotes']]

    collection['county']['election'] = pandas.DataFrame(output)

    ## icu beds
    collection['county']['icu_beds']['state'] = collection['county']['icu_beds']['state'].apply(
        lambda x: state_abbreviations[x])

    ## income
    collection['county']['income'] = collection['county']['income'].groupby(
        ['county', 'state']).mean().reset_index().copy()

    ## land and water
    collection['county']['land_and_water'] = collection['county']['land_and_water'].loc[:,
                                             ['state', 'county', 'ALAND', 'AWATER', 'ALAND_SQMI', 'AWATER_SQMI']]

    """
    Proceeding to merging and forming the final dataset
    """

    # cases
    cases = collection['county']['cases'].copy()
    aggregate_covid_by_country = {
        'sum': cases.groupby(['county', 'state']).sum().copy(),
        'mean': cases.groupby(['county', 'state']).mean().copy(),
        'median': cases.groupby(['county', 'state']).median().copy(),
        'max': cases.groupby(['county', 'state']).max().copy().drop(columns=['confirmed_date']),
        'min': cases.groupby(['county', 'state']).min().copy().drop(columns=['confirmed_date'])
    }

    for key in aggregate_covid_by_country.keys():
        aggregate_covid_by_country[key] = add_prefix_to_df_columns(df=aggregate_covid_by_country[key], prefix=key)

    aggregate_covid_county_table = merge_all_dfs_in_dict(aggregate_covid_by_country)

    income_table = collection['county']['income'].copy()

    aggregate_income_by_county = {
        'sum': income_table.groupby(['county', 'state']).sum().copy(),
        'mean': income_table.groupby(['county', 'state']).mean().copy(),
        'median': income_table.groupby(['county', 'state']).median().copy(),
        'max': income_table.groupby(['county', 'state']).max().copy().drop(columns=[]),
        'min': income_table.groupby(['county', 'state']).min().copy().drop(columns=[])
    }

    for key in aggregate_income_by_county.keys():
        aggregate_income_by_county[key] = add_prefix_to_df_columns(df=aggregate_income_by_county[key], prefix=key)
    aggregate_income_by_county = merge_all_dfs_in_dict(aggregate_income_by_county)

    # mortality

    mortality = collection['county']['mortality'].copy().drop(columns=[
        'Mortality Rate, 1980*',
        'Mortality Rate, 1980* (Min)',
        'Mortality Rate, 1980* (Max)',
        'Mortality Rate, 1985*',
        'Mortality Rate, 1985* (Min)',
        'Mortality Rate, 1985* (Max)',
        'Mortality Rate, 1990*',
        'Mortality Rate, 1990* (Min)',
        'Mortality Rate, 1990* (Max)',
        'Mortality Rate, 1995*',
        'Mortality Rate, 1995* (Min)',
        'Mortality Rate, 1995* (Max)',
        'Mortality Rate, 2000*',
        'Mortality Rate, 2000* (Min)',
        'Mortality Rate, 2000* (Max)',
        'Mortality Rate, 2005*',
        'Mortality Rate, 2005* (Min)',
        'Mortality Rate, 2005* (Max)',
        'Mortality Rate, 2010*',
        'Mortality Rate, 2010* (Min)',
        'Mortality Rate, 2010* (Max)'
    ]).rename({
        'Mortality Rate, 2014*': 'mortality_rate',
        'Mortality Rate, 2014* (Min)': 'min_mortality_rate',
        'Mortality Rate, 2014* (Max)': 'max_mortality_rate',
        '% Change in Mortality Rate, 1980-2014': "change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Min)': "min_change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Max)': "max_change_in_mortality_rate"
    }, inplace=False, axis="columns", errors="raise")
    mortality = mortality.groupby(['county', 'state']).mean().copy()

    # census
    census_full = collection['county']['census_full'].copy()
    census_full = census_full.groupby(['county', 'state']).mean()

    land_and_water = collection['county']['land_and_water'].copy()
    land_and_water = land_and_water.groupby(['county', 'state']).sum()

    election = collection['county']['election'].copy()
    election = election.groupby(['county', 'state']).sum()

    icu_beds = collection['county']['icu_beds'].copy()
    icu_beds = icu_beds.groupby(['county', 'state']).sum()

    diversity = collection['county']['diversityindex'].copy()
    diversity = diversity.groupby(['county', 'state']).sum()

    dataframes = [aggregate_covid_county_table, census_full, icu_beds, diversity, election, land_and_water,
                  aggregate_income_by_county, mortality]

    USHighResCOVID19SpreadDB = reduce(
        lambda left, right: pandas.merge(left, right, left_index=True, right_index=True, how='inner'), dataframes)

    USHighResCOVID19SpreadDB.to_csv(os.path.join(output_directory, 'USHighResCOVID19SpreadDB.csv'))


def add_day_of_the_year_to_cases_table(
        cases_dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the day of the year for cases table this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the day of the year field
    """

    def get_day_of_the_year(x: str):
        year, month, day = [int(e) for e in x.split('-')]
        the_date = date(year, month, day)
        first_date = date(2020, 1, 1)
        delta = the_date - first_date
        return delta.days

    cases_dataframe['day_of_the_year'] = cases_dataframe['confirmed_date'].apply(get_day_of_the_year)
    return cases_dataframe


def add_cumsums_to_cases_table(
        cases: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the cumsum values for death count and confirmed count, this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the cumsum values for cases added to it.
    """
    if not 'location' in cases.columns.tolist():
        cases = add_location_to_cases_table(cases)

    if not 'day_of_the_year' in cases.columns.tolist():
        cases = add_day_of_the_year_to_cases_table(cases)

    cases.sort_values(by=['state', 'county', 'day_of_the_year'], inplace=True)

    cases.reset_index(inplace=True)

    cases['death_count_cumsum'] = cases['death_count'].copy()
    cases['confirmed_count_cumsum'] = cases['confirmed_count'].copy()

    val1 = 0
    val2 = 0
    prev_state = 'wrong'
    prev_county = 'wrong'
    for i in range(cases.shape[0]):
        row = cases.iloc[i, :]
        state = row['state']
        county = row['county']
        death_count = int(row['death_count'])
        confirmed_count = int(row['confirmed_count'])
        if not ((state == prev_state) and (county == prev_county)):
            prev_state = state
            prev_county = county
            val1 = death_count
            val2 = confirmed_count
        else:
            val1 += death_count
            val2 += confirmed_count
        cases['death_count_cumsum'][i] = val1
        cases['confirmed_count_cumsum'][i] = val2

    return cases


def add_location_to_cases_table(
        cases: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the location for cases table this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the location field
    """
    cases['location'] = cases['county'] + '_' + cases['state']
    return cases
