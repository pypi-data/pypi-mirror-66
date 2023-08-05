__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from functools import reduce
from erlab_coat.dataset import *
from erlab_coat.meta import *
from datetime import date


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
