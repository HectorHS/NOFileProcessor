import click
# import csv
import numpy as np
import pandas as pd
import math


@click.command()
@click.argument('input')
@click.argument('processtype')
def cli(input, processtype):
    """ File processor to reduce file sizes

    First argument is input file, second the type of processing

    Valid processing types are: death-tree, death-map, death-bars, migration-bubbles,
    sustainability-area, covid19, covid19-time """

    click.echo('Starting ' + processtype + " processing of file " + input)
    if processtype == 'covid19-week':
        click.echo("custom process")
        loaded = pd.read_csv(
            input, skiprows=2, delimiter=',', encoding='latin1')
        click.echo('file loaded')
    elif processtype not in ['covid19', 'cclab-covid-time']:
        loaded = pd.read_csv(input, delimiter=',', encoding='latin1')
        click.echo('file loaded')

    if processtype == 'death-tree':
        output = pd.pivot_table(loaded, values='val', columns=['cause'],
                                index=['measure', 'location', 'sex', 'age'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'death-causes':
        # get rid of float points
        loaded['val'] = loaded['val'].astype(int)
        # expand ages so we can combine them in 10 year buckets instead of 5
        ages = pd.pivot_table(loaded, values='val', columns=['age'],
                              index=['location', 'cause', 'sex'],
                              aggfunc=lambda x: x)
        ages = ages.reset_index()

        # fill empty values otherwise operations fail
        ages = ages.fillna(0)
        # combine ages
        ages['0 to 9'] = (ages['<1 year'] +
                          ages['1 to 4'] + ages['5 to 9'])
        ages['10 to 19'] = ages['10 to 14'] + ages['15 to 19']
        ages['20 to 29'] = ages['20 to 24'] + ages['25 to 29']
        ages['30 to 39'] = ages['30 to 34'] + ages['35 to 39']
        ages['40 to 49'] = ages['40 to 44'] + ages['45 to 49']
        ages['50 to 59'] = ages['50 to 54'] + ages['55 to 59']
        ages['60 to 69'] = ages['60 to 64'] + ages['65 to 69']
        ages['70 to 79'] = ages['70 to 74'] + ages['75 to 79']
        ages['80 to 89'] = ages['80 to 84'] + ages['85 to 89']
        ages['90+'] = ages['90 to 94'] + ages['95 plus']

        # get rid of older brackets / columns
        del ages['<1 year']
        del ages['1 to 4']
        del ages['10 to 14']
        del ages['20 to 24']
        del ages['30 to 34']
        del ages['40 to 44']
        del ages['50 to 54']
        del ages['60 to 64']
        del ages['70 to 74']
        del ages['80 to 84']
        del ages['90 to 94']
        del ages['5 to 9']
        del ages['15 to 19']
        del ages['25 to 29']
        del ages['35 to 39']
        del ages['45 to 49']
        del ages['55 to 59']
        del ages['65 to 69']
        del ages['75 to 79']
        del ages['85 to 89']
        del ages['95 plus']

        # convert ages to single column
        ages = pd.melt(ages,
                       id_vars=['cause', 'sex', 'location'],
                       # list of days of the week
                       value_vars=list(ages.columns[3:]),
                       var_name='age',
                       value_name='val')

        # expand location to multiple columns to reduce rows and file size
        output = pd.pivot_table(ages, values='val', columns=['location'],
                                index=['cause', 'sex', 'age'],
                                aggfunc=lambda x: x)

        output = output.replace(0, np.nan)

        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)

    elif processtype == 'death-causes-percent':
        # reduce floating points to reduce file size. Making them ints also helps a lot with size
        # loaded['value'] = (loaded['val'] * 10000)
        # del loaded['val']
        # loaded['val'] = loaded['value'].astype(int)
        # del loaded['value']
        # get rid of float points
        loaded['val'] = loaded['val'].astype(int)
        # expand ages so we can combine them in 10 year buckets instead of 5
        ages = pd.pivot_table(loaded, values='val', columns=['age'],
                              index=['location', 'cause', 'sex'],
                              aggfunc=lambda x: x)
        ages = ages.reset_index()

        # fill empty values otherwise operations fail
        ages = ages.fillna(0)
        # combine ages
        ages['0 to 9'] = (ages['<1 year'] +
                          ages['1 to 4'] + ages['5 to 9'])
        ages['10 to 19'] = ages['10 to 14'] + ages['15 to 19']
        ages['20 to 29'] = ages['20 to 24'] + ages['25 to 29']
        ages['30 to 39'] = ages['30 to 34'] + ages['35 to 39']
        ages['40 to 49'] = ages['40 to 44'] + ages['45 to 49']
        ages['50 to 59'] = ages['50 to 54'] + ages['55 to 59']
        ages['60 to 69'] = ages['60 to 64'] + ages['65 to 69']
        ages['70 to 79'] = ages['70 to 74'] + ages['75 to 79']
        ages['80 to 89'] = ages['80 to 84'] + ages['85 to 89']
        ages['90+'] = ages['90 to 94'] + ages['95 plus']

        # get rid of older brackets / columns
        del ages['<1 year']
        del ages['1 to 4']
        del ages['10 to 14']
        del ages['20 to 24']
        del ages['30 to 34']
        del ages['40 to 44']
        del ages['50 to 54']
        del ages['60 to 64']
        del ages['70 to 74']
        del ages['80 to 84']
        del ages['90 to 94']
        del ages['5 to 9']
        del ages['15 to 19']
        del ages['25 to 29']
        del ages['35 to 39']
        del ages['45 to 49']
        del ages['55 to 59']
        del ages['65 to 69']
        del ages['75 to 79']
        del ages['85 to 89']
        del ages['95 plus']

        # convert ages to single column
        ages = pd.melt(ages,
                       id_vars=['cause', 'sex', 'location'],
                       # list of days of the week
                       value_vars=list(ages.columns[3:]),
                       var_name='age',
                       value_name='val')

        # exapnd by cause to calculate percentages
        output = pd.pivot_table(ages, values='val', columns=['cause'],
                                index=['location', 'age', 'sex'],
                                aggfunc=lambda x: x)
        output = output.reset_index()

        #  calculate an all causes column
        output['All causes'] = output.sum(axis=1, numeric_only=True)

        allCauses = output.columns[3:]
        allCauses = allCauses.drop('All causes')
        output = output.fillna(0)

        # convert values to percentages
        for cause in allCauses:
            output[cause] = (
                (output[cause] / output['All causes']) * 10000)
            output = output.fillna(0)
            output[cause] = output[cause].astype(int)
            output[cause] = output[cause] / 100

        del output['All causes']
        # convert causes to single column
        output = pd.melt(output,
                         id_vars=['age', 'sex', 'location'],
                         # list of days of the week
                         value_vars=list(output.columns[3:]),
                         var_name='cause',
                         value_name='val')

        # expand location to multiple columns to reduce rows and file size
        output = pd.pivot_table(output, values='val', columns=['location'],
                                index=['cause', 'sex', 'age'],
                                aggfunc=lambda x: x)

        output = output.replace(0, np.nan)

        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
        click.echo('outpout exported')

        # allAges = output.age.unique()
        allSexes = output.sex.unique()

        top_causes = pd.DataFrame(
            columns=['location', 'sex', 'age', 'cause', 'value'])

        allLocation = output.columns[3:]
        for location in allLocation:
            # for age in allAges:
            for sex in allSexes:
                top_value0 = 0
                top_cause0 = ""
                top_value1 = 0
                top_cause1 = ""
                top_value2 = 0
                top_cause2 = ""
                top_value3 = 0
                top_cause3 = ""
                top_value4 = 0
                top_cause4 = ""
                top_value5 = 0
                top_cause5 = ""
                top_value6 = 0
                top_cause6 = ""
                top_value7 = 0
                top_cause7 = ""
                top_value8 = 0
                top_cause8 = ""
                top_value9 = 0
                top_cause9 = ""
                top_value10 = 0
                top_cause10 = ""

                for (idx, row) in output.iterrows():
                    if row.sex == sex and row.age == '0 to 9' and row[location] > top_value0 and row.cause != 'All causes':
                        top_value0 = float(row[location])
                        top_cause0 = row.cause
                    elif row.sex == sex and row.age == '10 to 19' and row[location] > top_value1 and row.cause != 'All causes':
                        top_value1 = float(row[location])
                        top_cause1 = row.cause
                    elif row.sex == sex and row.age == '20 to 29' and row[location] > top_value2 and row.cause != 'All causes':
                        top_value2 = float(row[location])
                        top_cause2 = row.cause
                    elif row.sex == sex and row.age == '30 to 39' and row[location] > top_value3 and row.cause != 'All causes':
                        top_value3 = float(row[location])
                        top_cause3 = row.cause
                    elif row.sex == sex and row.age == '40 to 49' and row[location] > top_value4 and row.cause != 'All causes':
                        top_value4 = float(row[location])
                        top_cause4 = row.cause
                    elif row.sex == sex and row.age == '50 to 59' and row[location] > top_value5 and row.cause != 'All causes':
                        top_value5 = float(row[location])
                        top_cause5 = row.cause
                    elif row.sex == sex and row.age == '60 to 69' and row[location] > top_value6 and row.cause != 'All causes':
                        top_value6 = float(row[location])
                        top_cause6 = row.cause
                    elif row.sex == sex and row.age == '70 to 79' and row[location] > top_value7 and row.cause != 'All causes':
                        top_value7 = float(row[location])
                        top_cause7 = row.cause
                    elif row.sex == sex and row.age == '80 to 89' and row[location] > top_value8 and row.cause != 'All causes':
                        top_value8 = float(row[location])
                        top_cause8 = row.cause
                    elif row.sex == sex and row.age == '90+' and row[location] > top_value9 and row.cause != 'All causes':
                        top_value9 = float(row[location])
                        top_cause9 = row.cause
                    elif row.sex == sex and row.age == 'All Ages' and row[location] > top_value10 and row.cause != 'All causes':
                        top_value10 = float(row[location])
                        top_cause10 = row.cause

                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '0 to 9', 'cause': top_cause0,
                                                'value': top_value0}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '10 to 19', 'cause': top_cause1,
                                                'value': top_value1}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '20 to 29', 'cause': top_cause2,
                                                'value': top_value2}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '30 to 39', 'cause': top_cause3,
                                                'value': top_value3}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '40 to 49', 'cause': top_cause4,
                                                'value': top_value4}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '50 to 59', 'cause': top_cause5,
                                                'value': top_value5}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '60 to 69', 'cause': top_cause6,
                                                'value': top_value6}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '70 to 79', 'cause': top_cause7,
                                                'value': top_value7}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '80 to 89', 'cause': top_cause8,
                                                'value': top_value8}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': '90+', 'cause': top_cause9,
                                                'value': top_value9}, ignore_index=True)
                top_causes = top_causes.append({'location': location, 'sex': sex, 'age': 'All Ages', 'cause': top_cause10,
                                                'value': top_value10}, ignore_index=True)

        top_causes = top_causes.reset_index()
        top_causes.to_csv(r'output2.csv', index=None, header=True)
        click.echo('output2 exported')

    elif processtype == 'death-risks':
        # get rid of float points
        loaded['val'] = loaded['val'].astype(int)
        # expand ages so we can combine them in 10 year buckets instead of 5
        ages = pd.pivot_table(loaded, values='val', columns=['age'],
                              index=['location', 'cause', 'sex', 'rei'],
                              aggfunc=lambda x: x)
        ages = ages.reset_index()

        # fill empty values otherwise operations fail
        ages = ages.fillna(0)
        # combine ages
        ages['0 to 9'] = (ages['<1 year'] +
                          ages['1 to 4'] + ages['5 to 9'])
        ages['10 to 19'] = ages['10 to 14'] + ages['15 to 19']
        ages['20 to 29'] = ages['20 to 24'] + ages['25 to 29']
        ages['30 to 39'] = ages['30 to 34'] + ages['35 to 39']
        ages['40 to 49'] = ages['40 to 44'] + ages['45 to 49']
        ages['50 to 59'] = ages['50 to 54'] + ages['55 to 59']
        ages['60 to 69'] = ages['60 to 64'] + ages['65 to 69']
        ages['70 to 79'] = ages['70 to 74'] + ages['75 to 79']
        ages['80 to 89'] = ages['80 to 84'] + ages['85 to 89']
        ages['90+'] = ages['90 to 94'] + ages['95 plus']

        # get rid of older brackets / columns
        del ages['<1 year']
        del ages['1 to 4']
        del ages['10 to 14']
        del ages['20 to 24']
        del ages['30 to 34']
        del ages['40 to 44']
        del ages['50 to 54']
        del ages['60 to 64']
        del ages['70 to 74']
        del ages['80 to 84']
        del ages['90 to 94']
        del ages['5 to 9']
        del ages['15 to 19']
        del ages['25 to 29']
        del ages['35 to 39']
        del ages['45 to 49']
        del ages['55 to 59']
        del ages['65 to 69']
        del ages['75 to 79']
        del ages['85 to 89']
        del ages['95 plus']

        # convert ages to single column
        ages = pd.melt(ages,
                       id_vars=['cause', 'sex', 'location', 'rei'],
                       # list of days of the week
                       value_vars=list(ages.columns[4:]),
                       var_name='age',
                       value_name='val')

        # expand location to multiple columns to reduce rows and file size
        output = pd.pivot_table(ages, values='val', columns=['location'],
                                index=['cause', 'sex', 'age', 'rei'],
                                aggfunc=lambda x: x)

        output = output.replace(0, np.nan)

        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'death-map':
        output = pd.pivot_table(loaded, values='val', columns=['location'],
                                index=['cause', 'sex', 'age', 'year'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'death-bars':
        output = pd.pivot_table(loaded, values='val', columns=['cause'],
                                index=['measure', 'location', 'sex', 'rei'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'migration-bubbles':
        output = pd.pivot_table(loaded, values='population', columns=['year'],
                                index=['country_host', 'country_origin'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'sustainability-area':
        output = pd.pivot_table(loaded, values='value', columns=['year'],
                                index=['country', 'record', 'type'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)
    elif processtype == 'life-map':
        output = pd.pivot_table(loaded, values='Value', columns=['Country'],
                                index=['Year', 'Parameter'],
                                aggfunc=lambda x: x)
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)

    elif processtype == 'covid19':
        day = int(input[:2])
        month = int(input[3:5])
        year = int(input[6:10])
        targerDate = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2) 

        cases = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/total_cases.csv', delimiter=',', encoding='latin1')
        deaths = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/total_deaths.csv', delimiter=',', encoding='latin1')
        weekly_cases = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/weekly_cases_per_million.csv', delimiter=',', encoding='latin1')
        weekly_cases_abs = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/weekly_cases.csv', delimiter=',', encoding='latin1')
        weekly_deaths = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/weekly_deaths_per_million.csv', delimiter=',', encoding='latin1')     
        click.echo("cases and deaths loaded")
        vaccinations = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', delimiter=',', encoding='latin1')
        click.echo('vaccination data loaded')
        historical = pd.read_csv('resources/covid-historical.csv', delimiter=',', encoding='latin1')

        countries = cases.columns.tolist()
        del countries[0]

        # Remove possible newer records
        allDates = cases['date'].tolist()
        dateIndex = allDates.index(targerDate)
        cases = cases.iloc[:dateIndex+1]
        deaths = deaths.iloc[:dateIndex+1]
        weekly_cases = weekly_cases.iloc[:dateIndex+1]
        weekly_cases_abs = weekly_cases_abs.iloc[:dateIndex+1]
        weekly_deaths = weekly_deaths.iloc[:dateIndex+1]

        # latest 10 dates
        datesList = cases['date'].tolist()[-10:]
        datesList = list(reversed(datesList))
        datesListLonger = cases['date'].tolist()[-180:]
        datesListLonger = list(reversed(datesListLonger))

        # filter out uneeded rows - we keep 10 in case the target date is not available
        cases = cases[cases.date.isin(datesList)]
        deaths = deaths[deaths.date.isin(datesList)]
        weekly_cases = weekly_cases[weekly_cases.date.isin(datesList)]
        weekly_cases_abs = weekly_cases_abs[weekly_cases_abs.date.isin(datesList)]
        weekly_deaths = weekly_deaths[weekly_deaths.date.isin(datesList)]
        vaccinations = vaccinations[vaccinations.date.isin(datesListLonger)]

        testing = pd.read_csv(
             'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv', delimiter=',', encoding='latin1')
        testing.columns = [c.strip().lower().replace(' ', '_')
                           for c in testing.columns]
        testing.columns = [c.strip().lower().replace('-', '_')
                           for c in testing.columns]
        testing.columns = [c.strip().lower().replace('7', 'seven')
                           for c in testing.columns]
        click.echo('testing data loaded')

        output = pd.DataFrame(
            columns=['Country', 'Cases', 'Cases_2020', 'Cases_2021', 'Cases_2022', 'Cases_week', 'Deaths', 'Deaths_2020', 'Deaths_2021', 'Deaths_2022', 'Deaths_week', 'Positive_rate', 'Fully_vaccinated', 'Vaccinated_booster'])

        def getTestingCountryName(country):
            countryName = {
                "Albania": "Albania - tests performed",
                "Andorra": "Andorra - tests performed",
                "Antigua and barbuda": "Antigua and Barbuda - tests performed",
                "Argentina": "Argentina - tests performed",
                "Armenia": "Armenia - tests performed",
                "Azerbaijan": "Azerbaijan - tests performed",
                "Australia": "Australia - tests performed",
                "Austria": "Austria - tests performed",
                "Bahamas": "Bahamas - tests performed",
                "Bahrain": "Bahrain - units unclear",
                "Bangladesh": "Bangladesh - tests performed",
                "Belarus": "Belarus - tests performed",
                "Belgium": "Belgium - tests performed",
                "Belize": "Belize - tests performed",
                "Benin": "Benin - tests performed",
                "Bhutan": "Bhutan - samples tested",
                "Bolivia": "Bolivia - tests performed",
                "Bosnia and Herzegovina": "Bosnia and Herzegovina - tests performed",
                "Botswana": "Botswana - tests performed",
                "Brazil": "Brazil - tests performed",
                "Bulgaria": "Bulgaria - tests performed",
                "Cambodia": "Cambodia - tests performed",
                "Canada": "Canada - tests performed",
                "Cape Verde": "Cape Verde - tests performed",
                "Chile": "Chile - tests performed",
                "China": "China - tests performed",
                "Colombia": "Colombia - tests performed",
                "Costa Rica": "Costa Rica - people tested",
                "Cote d'Ivoire": "Cote d'Ivoire - tests performed",
                "Croatia": "Croatia - people tested",
                "Cuba": "Cuba - tests performed",
                "Cyprus": "Cyprus - tests performed",
                "Czechia": "Czechia - tests performed",
                "Democratic Republic of Congo": "Democratic Republic of Congo - samples tested",
                "Denmark": "Denmark - tests performed",
                "Dominican Republic": "Dominican Republic - samples tested",
                "Ecuador": "Ecuador - people tested",
                "El_salvador": "El Salvador - tests performed",
                "Equatorial Guinea": "Equatorial Guinea - tests performed",
                "Estonia": "Estonia - tests performed",
                "Ethiopia": "Ethiopia - tests performed",
                "Faeroe Islands": "Faeroe Islands - people tested",
                "Fiji": "Fiji - tests performed",
                "Finland": "Finland - tests performed",
                "France": "France - people tested",
                "Gabon": "Gabon - tests performed",
                "Gambia": "Gambia - tests performed",
                "Georgia": "Georgia - tests performed",
                "Germany": "Germany - tests performed",
                "Ghana": "Ghana - tests performed",
                "Greece": "Greece - samples tested",
                "Guatemala": "Guatemala - people tested",
                "Haiti": "Haiti - tests performed",
                "Hong Kong": "Hong Kong - tests performed",
                "Hungary": "Hungary - tests performed",
                "Iceland": "Iceland - tests performed",
                "India": "India - samples tested",
                "Indonesia": "Indonesia - people tested",
                "Iran": "Iran - tests performed",
                "Iraq": "Iraq - tests performed",
                "Ireland": "Ireland - tests performed",
                "Israel": "Israel - people tested",
                "Italy": "Italy - tests performed",
                "Jamaica": "Jamaica - samples tested",
                "Japan": "Japan - people tested",
                "Jordan": "Jordan - tests performed",
                "Kazakhstan": "Kazakhstan - tests performed",
                "Kenya": "Kenya - tests performed",
                "Kosovo": "Kosovo - tests performed",
                "Kuwait": "Kuwait - tests performed",
                "Laos": "Laos - tests performed",
                "Latvia": "Latvia - tests performed",
                "Lebanon": "Lebanon - tests performed",
                "Libya": "Libya - samples tested",
                "Liechtenstein": "Liechtenstein - tests performed",
                "Lithuania": "Lithuania - tests performed",
                "Luxembourg": "Luxembourg - tests performed",
                "Madagascar": "Madagascar - tests performed",
                "Malawi": "Malawi - tests performed",
                "Malaysia": "Malaysia - people tested",
                "Malta": "Malta - tests performed",
                "Mauritania": "Mauritania - tests performed",
                "Mexico": "Mexico - people tested",
                "Maldives": "Maldives - samples tested",
                "Moldova": "Moldova - tests performed",
                "Mongolia": "Mongolia - samples tested",
                "Morocco": "Morocco - people tested",
                "Mozambique": "Mozambique - tests performed",
                "Myanmar": "Myanmar - samples tested",
                "Namibia": "Namibia - tests performed",
                "Nepal": "Nepal - samples tested",
                "Netherlands": "Netherlands - tests performed",
                "New Zealand": "New Zealand - tests performed",
                "Nigeria": "Nigeria - tests performed",
                "North Macedonia": "North Macedonia - tests performed",
                "Norway": "Norway - people tested",
                "Oman": "Oman - tests performed",
                "Palestine": "Palestine - tests performed",
                "Pakistan": "Pakistan - tests performed",
                "Panama": "Panama - tests performed",
                "Papua New Guinea": "Papua New Guinea - people tested",
                "Paraguay": "Paraguay - tests performed",
                "Peru": "Peru - tests performed",
                "Philippines": "Philippines - people tested",
                "Poland": "Poland - tests performed",
                "Portugal": "Portugal - tests performed",
                "Qatar": "Qatar - tests performed",
                "Romania": "Romania - tests performed",
                "Russia": "Russia - tests performed",
                "Rwanda": "Rwanda - samples tested",
                "Saint Kitts and Nevis": "Saint Kitts and Nevis - people tested",
                "Saint Vincent and the Grenadines": "Saint Vincent and the Grenadines - tests performed",
                "Saudi Arabia": "Saudi Arabia - tests performed",
                "Senegal": "Senegal - tests performed",
                "Serbia": "Serbia - people tested",
                "Singapore": "Singapore - samples tested",
                "Slovakia": "Slovakia - tests performed",
                "Slovenia": "Slovenia - tests performed",
                "South Africa": "South Africa - people tested",
                "South Korea": "South Korea - people tested",
                "South Sudan": "South Sudan - tests performed",
                "Spain": "Spain - tests performed",
                "Sri Lanka": "Sri Lanka - tests performed",
                "Sweden": "Sweden - tests performed",
                "Switzerland": "Switzerland - tests performed",
                "Taiwan": "Taiwan - people tested",
                "Thailand": "Thailand - tests performed",
                "Timor": "Timor - tests performed",
                "Togo": "Togo - tests performed",
                "Trinidad and Tobago": "Trinidad and Tobago - people tested",
                "Tunisia": "Tunisia - people tested",
                "Turkey": "Turkey - tests performed",
                "Uganda": "Uganda - tests performed",
                "Ukraine": "Ukraine - tests performed",
                "United Arab Emirates": "United Arab Emirates - tests performed",
                "United Kingdom": "United Kingdom - tests performed",
                "United States": "United States - tests performed",
                "Uruguay": "Uruguay - people tested",
                "Vietnam": "Vietnam - people tested",
                "Zambia": "Zambia - tests performed",
                "Zimbabwe": "Zimbabwe - tests performed"
            }

            name = countryName[country] if country in countryName else ""
            return name

        def getPositiveRate(testingCountryName, country):
            # click.echo("got in positive rate")
            nonlocal testing
            sliced = testing[testing.entity == testingCountryName]
            if len(sliced.index) > 0:  
                rate = sliced.iloc[0]['short_term_positive_rate']
                # for row in testing.itertuples():
                #     if row.entity == testingCountryName:
                #         rate = row.short_term_positive_rate
                        if not (math.isnan(rate)):
                    rate = rate*100
                    rate = '%.2f'%(rate)
                            return rate
                        
            # we didnt get one, so let's try to calculate it
                weeklyCases = getWeeklyCasesAbsolute(country)
                weeklyTests = getWeeklyTestsAbsolute(testingCountryName)
                if weeklyCases > 0 and weeklyTests > 0:
                rate = ((weeklyCases/7)/weeklyTests)*100
                rate = '%.2f'%(rate)
                    return rate
            
            click.echo('Positive test rate for ' + str(testingCountryName) + ' not found')
            return ""
                
        def getWeeklyCasesAbsolute(country):
             # we repeat the process in case the latest values are not available
            for date in datesList:
                sliced = weekly_cases_abs[weekly_cases_abs.date == date]
                val = sliced.iloc[0][country]
                if not(math.isnan(val)):
                    return val
                # for row in weekly_cases_abs.itertuples():
                #     if row.date == date:
                #         val = getattr(row, country)
                #         if not(math.isnan(val)):
                #             return val
            
            click.echo("no absolute weekly cases data found for " + country)
            return 0

        def getWeeklyTestsAbsolute(testingCountryName):
            # click.echo("got in weekly tests absolute")
            nonlocal testing
            sliced = testing[testing.entity == testingCountryName]
            if len(sliced.index) > 0:  
                val = sliced.iloc[0]['seven_day_smoothed_daily_change']
            # return val
                # for row in testing.itertuples():
                #     if row.entity == testingCountryName:
                #         val = row.seven_day_smoothed_daily_change
                    if not (math.isnan(val)):
                        return val

            click.echo("no absolute weekly tests data found for " + testingCountryName)
            return 0

        def getVaccination(country):
            nonlocal vaccinations
            # click.echo(vaccinations)
            # filter out uneeded rows
            subset = vaccinations[vaccinations.location == country]
            # click.echo(subset)

            for date in datesListLonger:
                sliced = subset[subset.date == date]
                # for row in subset.itertuples():
                #     if row.date == date:
                        # val = row.people_fully_vaccinated_per_hundred
                if len(sliced.index) > 0:      
                    val = sliced.iloc[0]['people_fully_vaccinated_per_hundred']
                        if not(math.isnan(val)):
                            return val

            click.echo("No vaccination rows found for " + country)
            return 0

        def getVaccinationBooster(country):
            nonlocal vaccinations

            # filter out uneeded rows
            subset = vaccinations[vaccinations.location == country]

            for date in datesListLonger:
                sliced = subset[subset.date == date]
                # for row in subset.itertuples():
                    # if row.date == date:
                        # val = row.total_boosters_per_hundred
                if len(sliced.index) > 0: 
                    val = sliced.iloc[0]['total_boosters_per_hundred']
                        if not(math.isnan(val)):
                            return val
            return 0

        def getCases(country):
            sliced = cases[cases.date == targerDate]
            val = sliced.iloc[0][country]
            return val

        def getDeaths(country):
            sliced = deaths[deaths.date == targerDate]
            val = sliced.iloc[0][country]
            return val

        def getWeeklyDeaths(country):
             # we repeat the process in case the latest values are not available
            for date in datesList:
                sliced = weekly_deaths[weekly_deaths.date == date]
                val = sliced.iloc[0][country]
                if not(math.isnan(val)):
                    return '%.4f'%(val/7)

            click.echo("no weekly death data found for " + country)
            return 0

        def getWeeklyCases(country):
            # we repeat the process in case the latest values are not available
            for date in datesList:
                sliced = weekly_cases[weekly_cases.date == date]
                val = sliced.iloc[0][country]
                if not(math.isnan(val)):
                    return '%.4f'%(val/7)

            click.echo("no weekly cases data found for " + country)
            return 0
        def getHistoricalData(country, measure, year):
            # click.echo("got in historical data" + country + measure + year)
            sliced = historical[historical.location == country]
            val = 0
            meas = measure + "_" + year
            try:
                val = sliced.iloc[0][meas]
            except:
                click.echo("Unable to get historical data for " + country + measure + year)
            else:
                if not(math.isnan(val)):
                    return val
            
            return 0

        for country in countries:
            if country not in ['Africa', 'Asia', 'Europe', 'European Union', 'High income', 'International', 'Low income', 'Lower middle income', 'North America', 'Oceania', 'South America', 'Summer Olympics 2020', 'Upper middle income']:
                weekDea = 0

                cas = getCases(country)
                cas2020 = getHistoricalData(country, "cases", "2020")
                cas2021 = getHistoricalData(country, "cases", "2021")
                cas2022 = cas - cas2020 - cas2021

                dea = getDeaths(country)
                dea2020 = getHistoricalData(country, "deaths", "2020")
                dea2021 = getHistoricalData(country, "deaths", "2021")
                dea2022 = dea - dea2020 - dea2021

                weekCas = getWeeklyCases(country)
                if dea > 0:
                    weekDea = getWeeklyDeaths(country)

                postiveRate = 0

                testingCountryName = getTestingCountryName(country)
                if (testingCountryName):
                    postiveRate = getPositiveRate(testingCountryName, country)

                vacc = getVaccination(country)
                vaccBoost = getVaccinationBooster(country)
                
                output = output.append({'Country': country, 'Cases': cas, 'Cases_2020': cas2020, 'Cases_2021': cas2021, 'Cases_2022': cas2022, 
                    'Cases_week': weekCas, 'Deaths': dea, 'Deaths_2020': dea2020, 'Deaths_2021':dea2021, 'Deaths_2022': dea2022, 'Deaths_week': weekDea,
                                    'Positive_rate': postiveRate, 'Fully_vaccinated': vacc, 'Vaccinated_booster': vaccBoost}, ignore_index=True)

        # Sort by country, but because sorting in python with mixed cases is messy, do all this
        output['country_lower'] = output['Country'].str.lower()
        output = output.sort_values(by=['country_lower'])
        output.drop('country_lower', axis=1, inplace=True)

        output = output.reset_index()
        output.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-map.csv', index=None, header=True)
        click.echo('covid-map.csv exported')

        # Update covid-time.csv
        click.echo('processing covid-time started')
        time = pd.read_csv(
            '../NavigateObscurity/static/worlddata/csv/covid-time.csv', delimiter=',', encoding='latin1')
        click.echo('time series data loaded')
        testingFull = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv', delimiter=',', encoding='latin1')
        click.echo('testing data loaded')
        new_cases = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv', delimiter=',', encoding='latin1')
        new_deaths = pd.read_csv(
            'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv', delimiter=',', encoding='latin1')

        # only keep 10 latest dates 
        testingFull = testingFull[testingFull.Date.isin(datesList)]
        new_cases = new_cases[new_cases.date.isin(datesList)]
        new_deaths = new_deaths[new_deaths.date.isin(datesList)]

        timeCases = time[time.Parameter == "Cases"]
        timeDeaths = time[time.Parameter == "Deaths"]
        timeTests = time[time.Parameter == "Tests"]
        timeRates = time[time.Parameter == "Tests_rate"]

        # remove latest 10 days from existing covid time file. We do this to attempt to have more updated data as this data is not always up to latest date
        datesList = list(reversed(datesList))
        newDateList = []
        for date in datesList:
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:10])
            newDate = str(day).zfill(2) + "/" + str(month).zfill(2) + "/" + str(year)
            newDateList.append(newDate)

        for date in newDateList:
            if date in time.columns.tolist():
                time.drop(date, axis=1, inplace=True)

        def getTimeNewCases(country, date):
            sliced = new_cases[new_cases.date == date]
            val = sliced.iloc[0][country]
            if not(math.isnan(val)):
                return val
            return 0

        def getTimeNewDeaths(country, date):
            sliced = new_deaths[new_deaths.date == date]
            val = sliced.iloc[0][country]
            if not(math.isnan(val)):
                return val
            return 0

        def getTimeTest(country, date):
            country = getTestingCountryName(country)
            subset = testingFull[testingFull.Entity == country]
            subset = subset[subset.Date == date]
            if len(subset.index) > 0:
                val = subset.iloc[0]['7-day smoothed daily change']
                if not(math.isnan(val)):
                    return val
            return ""
        def getTimeTestRate(country, date):
            testingCountryName = getTestingCountryName(country)
            subset = testingFull[testingFull.Entity == testingCountryName]
            subset = subset[subset.Date == date]
            if len(subset.index) > 0:
                val = subset.iloc[0]['Short-term positive rate']
                if not(math.isnan(val)):
                    return val*100
                # we didnt get one, so let's try to calculate it
                weeklyCases = getTimeWeeklyCases(country, date)
                weeklyTests = getTimeTest(country, date)
                if weeklyTests == "":
                    weeklyTests = 0
                if weeklyCases > 0 and weeklyTests > 0:
                    rate = ((weeklyCases/7)/weeklyTests)*100
                    rate = '%.2f'%(rate)
                    return rate
            return ""
        def getTimeWeeklyCases(country, date):
            sliced = weekly_cases_abs[weekly_cases_abs.date == date]
            val = sliced.iloc[0][country]
            if not(math.isnan(val)):
                return val
            return 0

        # for each date, create a new column to covid time file
        for i in range(len(datesList)):
        today = []
            click.echo("processing for: " + datesList[i])
            for row in timeCases.itertuples():
                today.append(getTimeNewCases(row.Country, datesList[i]))

            for row in timeDeaths.itertuples():
                today.append(getTimeNewDeaths(row.Country, datesList[i]))

            for row in timeTests.itertuples():
                today.append(getTimeTest(row.Country, datesList[i]))
            for row in timeRates.itertuples():
                today.append(getTimeTestRate(row.Country, datesList[i]))

            time = time.assign(**{newDateList[i]: today})

        time.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-time.csv', index=None, header=True)
        click.echo('covid-time.csv exported')

    elif processtype == 'covid19-week':
        countries = {
            "Austria",
            "Belgium",
            "Bulgaria",
            "Switzerland",
            "Czech Republic",
            "Denmark",
            "Spain",
            "Estonia",
            "Finland",
            "France",
            "Croatia",
            "Hungary",
            "Iceland",
            "Israel",
            "Italy",
            "Lithuania",
            "Luxembourg",
            "Latvia",
            "Netherlands",
            "Norway",
            "Poland",
            "Portugal",
            "Russia",
            "Slovakia",
            "Slovenia",
            "Sweden",
            "USA",
            "Germany",
            "Greece",
            "Korea, South",
            "New Zealand",
            "Australia",
            "Canada",
            "Chile",
            "Taiwan"}

        years = {2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022}
        weeks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53}
        uk = {"GBRTENW", "GBR_NIR", "GBR_SCO"}

        def getCountryCode(country):
            countryCode = {
                "Austria": "AUT",
                "Belgium": "BEL",
                "Bulgaria": "BGR",
                "Switzerland": "CHE",
                "Czech Republic": "CZE",
                "Denmark": "DNK",
                "Spain": "ESP",
                "Estonia": "EST",
                "Finland": "FIN",
                "France": "FRATNP",
                "Croatia": "HRV",
                "Hungary": "HUN",
                "Iceland": "ISL",
                "Israel": "ISR",
                "Italy": "ITA",
                "Lithuania": "LTU",
                "Luxembourg": "LUX",
                "Latvia": "LVA",
                "Netherlands": "NLD",
                "Norway": "NOR",
                "Poland": "POL",
                "Portugal": "PRT",
                "Russia": "RUS",
                "Slovakia": "SVK",
                "Slovenia": "SVN",
                "Sweden": "SWE",
                "USA": "USA",
                "Germany": "DEUTNP",
                "Greece": "GRC",
                "Korea, South": "KOR",
                "New Zealand": "NZL_NP",
                "Australia": "AUS2",
                "Canada": "CAN",
                "Chile": "CHL",
                "Taiwan": "TWN"}

            return countryCode[country]

        output = pd.DataFrame(
            columns=['Country', 'Week', 'Deaths_old', 'Deaths_2020', 'Deaths_2021', 'Deaths_2022'])

        # filter out uneeded rows
        loaded = loaded[loaded.Sex == 'b']
        loaded = loaded[loaded['Year'].isin(years)]

        for country in countries:
            for week in weeks:
                loadedFiltered = loaded[loaded.Week == week]
                loadedFiltered = loadedFiltered[loadedFiltered.CountryCode ==
                                                getCountryCode(country)]
                oldSum = 0
                sum20 = 0
                sum21 = 0
                sum22 = 0
                for row in loadedFiltered.itertuples():
                    if row.Year == 2020:
                        sum20 = row.DTotal
                    elif row.Year == 2021:
                        sum21 = row.DTotal
                    elif row.Year == 2022:
                        sum22 = row.DTotal
                    else:
                        oldSum += row.DTotal
                if week == 53:
                    oldAverage = oldSum
                else:
                    oldAverage = oldSum / 5
                countryName = country
                if country == 'USA':
                    countryName = 'United States'
                if country == 'Korea, South':
                    countryName = 'South Korea'
                output = output.append(
                    {'Country': countryName, 'Week': week, 'Deaths_old': oldAverage, 'Deaths_2020': sum20, 'Deaths_2021': sum21, 'Deaths_2022': sum22}, ignore_index=True)

        for week in weeks:
            loadedFiltered = loaded[loaded.Week == week]
            loadedFiltered = loadedFiltered[loadedFiltered['CountryCode'].isin(
                uk)]
            oldSum = 0
            sum20 = 0
            sum21 = 0
            sum22 = 0
            i = 0
            j = 0
            k = 0
            for row in loadedFiltered.itertuples():
                if row.Year == 2020:
                    sum20 += row.DTotal
                    i += 1
                elif row.Year == 2021:
                    sum21 += row.DTotal
                    j += 1
                elif row.Year == 2022:
                    sum22 += row.DTotal
                    k += 1
                else:
                    oldSum += row.DTotal

            if week == 53:
                oldAverage = oldSum
            else:
                oldAverage = oldSum / 5

            if i < 3:
                sum20 = 0
            if j < 3:
                sum21 = 0
            if k < 3:
                sum22 = 0

            output = output.append({'Country': "United Kingdom", 'Week': week,
                                    'Deaths_old': oldAverage, 'Deaths_2020': sum20, 'Deaths_2021': sum21, 'Deaths_2022': sum22}, ignore_index=True)
        output = output.reset_index()
        output.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-excess-deaths.csv', index=None, header=True)

    elif processtype == 'cclab-covid':
        # Run processor cclab-covid.csv cclab-covid

         # Load covid data files
        # location_01 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/09-26-2020.csv'
        # location_02 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/10-27-2020.csv'
        # location_03 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/11-28-2020.csv'
        # location_04 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/12-28-2020.csv'
        # location_05 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/01-27-2021.csv'
        # location_06 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/02-26-2021.csv'
        # location_07 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/03-28-2021.csv'
        # location_08 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/04-27-2021.csv'
        # location_09 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/05-27-2021.csv'
        # location_10 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/06-26-2021.csv'
        # location_11 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/07-26-2021.csv'
        # location_12 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/08-25-2021.csv'
        # location_13 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/10-25-2021.csv'
        # location_14 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/12-16-2021.csv'
        # location_15 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/02-24-2022.csv'
        location_16 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/04-25-2022.csv'
        location_hospital = 'hospitalizations.csv'
        # loaded01 = pd.read_csv(location_01, delimiter=',', encoding='latin1')
        # loaded02 = pd.read_csv(location_02, delimiter=',', encoding='latin1')
        # loaded03 = pd.read_csv(location_03, delimiter=',', encoding='latin1')
        # loaded04 = pd.read_csv(location_04, delimiter=',', encoding='latin1')
        # loaded05 = pd.read_csv(location_05, delimiter=',', encoding='latin1')
        # loaded06 = pd.read_csv(location_06, delimiter=',', encoding='latin1')
        # loaded07 = pd.read_csv(location_07, delimiter=',', encoding='latin1')
        # loaded08 = pd.read_csv(location_08, delimiter=',', encoding='latin1')
        # loaded09 = pd.read_csv(location_09, delimiter=',', encoding='latin1')
        # loaded10 = pd.read_csv(location_10, delimiter=',', encoding='latin1')
        # loaded11 = pd.read_csv(location_11, delimiter=',', encoding='latin1')
        # loaded12 = pd.read_csv(location_12, delimiter=',', encoding='latin1')
        # loaded13 = pd.read_csv(location_13, delimiter=',', encoding='latin1')
        # loaded14 = pd.read_csv(location_14, delimiter=',', encoding='latin1')
        # loaded15 = pd.read_csv(location_15, delimiter=',', encoding='latin1')
        loaded16 = pd.read_csv(location_16, delimiter=',', encoding='latin1')
        loadedHospital = pd.read_csv(location_hospital, delimiter=',', encoding='latin1')

        click.echo('covid data loaded')

        # initialise columns
        # loaded['Incident_Rate.01'] = ''
        # loaded['Case-Fatality_Ratio.01'] = ''
        # loaded['Hospitalizations.01'] = ''
        # loaded['Incident_Rate.02'] = ''
        # loaded['Case-Fatality_Ratio.02'] = ''
        # loaded['Hospitalizations.02'] = ''
        # loaded['Incident_Rate.03'] = ''
        # loaded['Case-Fatality_Ratio.03'] = ''
        # loaded['Hospitalizations.03'] = ''
        # loaded['Incident_Rate.04'] = ''
        # loaded['Case-Fatality_Ratio.04'] = ''
        # loaded['Hospitalizations.04'] = ''
        # loaded['Incident_Rate.05'] = ''
        # loaded['Case-Fatality_Ratio.05'] = ''
        # loaded['Hospitalizations.05'] = ''
        # loaded['Incident_Rate.06'] = ''
        # loaded['Case-Fatality_Ratio.06'] = ''
        # loaded['Hospitalizations.06'] = ''
        # loaded['Incident_Rate.07'] = ''
        # loaded['Case-Fatality_Ratio.07'] = ''
        # loaded['Hospitalizations.07'] = ''
        # loaded['Incident_Rate.08'] = ''
        # loaded['Case-Fatality_Ratio.08'] = ''
        # loaded['Hospitalizations.08'] = ''
        # loaded['Incident_Rate.09'] = ''
        # loaded['Case-Fatality_Ratio.09'] = ''
        # loaded['Hospitalizations.09'] = ''
        # loaded['Incident_Rate.10'] = ''
        # loaded['Case-Fatality_Ratio.10'] = ''
        # loaded['Hospitalizations.10'] = ''
        # loaded['Incident_Rate.11'] = ''
        # loaded['Case-Fatality_Ratio.11'] = ''
        # loaded['Hospitalizations.11'] = ''
        # loaded['Incident_Rate.12'] = ''
        # loaded['Case-Fatality_Ratio.12'] = ''
        # loaded['Hospitalizations.12'] = ''
        # loaded['Incident_Rate.13'] = ''
        # loaded['Case-Fatality_Ratio.13'] = ''
        # loaded['Hospitalizations.13'] = ''
        # loaded['Incident_Rate.14'] = ''
        # loaded['Case-Fatality_Ratio.14'] = ''
        # loaded['Hospitalizations.14'] = ''
        # loaded['Incident_Rate.15'] = ''
        # loaded['Case-Fatality_Ratio.15'] = ''
        # loaded['Hospitalizations.15'] = ''
        loaded['Incident_Rate.16'] = ''
        loaded['Case-Fatality_Ratio.16'] = ''
        loaded['Hospitalizations.16'] = ''

        for i in range(len(loaded)):
            # for row in loaded01.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.01'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.01'] = row.Mortality_Rate
            #         break
            # for row in loaded02.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.02'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.02'] = row.Mortality_Rate
            #         break
            # for row in loaded03.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.03'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded04.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.04'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded05.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.05'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded06.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.06'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded07.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.07'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded08.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.08'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.08'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded09.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.09'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.09'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded10.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.10'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.10'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded11.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.11'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.11'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded12.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.12'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.12'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded13.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.13'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.13'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded14.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.14'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.14'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded15.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.15'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.15'] = row.Case_Fatality_Ratio
            #         break
            # for row in loaded16.itertuples():
            #     if loaded.at[i, 'State_full'] == row.Province_State:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incident_Rate.16'] = row.Incident_Rate
            #             loaded.at[i, 'Case-Fatality_Ratio.16'] = row.Case_Fatality_Ratio
            #         break

            hospSlice01 = loadedHospital[loadedHospital.Date == "2020-09-26"]
            hospSlice02 = loadedHospital[loadedHospital.Date == "2020-10-27"]
            hospSlice03 = loadedHospital[loadedHospital.Date == "2020-11-28"]
            hospSlice04 = loadedHospital[loadedHospital.Date == "2020-12-28"]
            hospSlice05 = loadedHospital[loadedHospital.Date == "2021-01-27"]
            hospSlice06 = loadedHospital[loadedHospital.Date == "2021-02-26"]
            hospSlice07 = loadedHospital[loadedHospital.Date == "2021-03-28"]
            hospSlice08 = loadedHospital[loadedHospital.Date == "2021-04-27"]
            hospSlice09 = loadedHospital[loadedHospital.Date == "2021-05-27"]
            hospSlice10 = loadedHospital[loadedHospital.Date == "2021-06-26"]
            hospSlice11 = loadedHospital[loadedHospital.Date == "2021-07-26"]
            hospSlice12 = loadedHospital[loadedHospital.Date == "2021-08-25"]
            hospSlice13 = loadedHospital[loadedHospital.Date == "2021-10-25"]
            hospSlice14 = loadedHospital[loadedHospital.Date == "2021-12-16"]
            hospSlice15 = loadedHospital[loadedHospital.Date == "2022-02-24"]
            hospSlice16 = loadedHospital[loadedHospital.Date == "2022-04-25"]

            for row in hospSlice01.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.01'] = row.CurrentHospitalizations
            for row in hospSlice02.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.02'] = row.CurrentHospitalizations
            for row in hospSlice03.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.03'] = row.CurrentHospitalizations
            for row in hospSlice04.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.04'] = row.CurrentHospitalizations
            for row in hospSlice05.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.05'] = row.CurrentHospitalizations
            for row in hospSlice06.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.06'] = row.CurrentHospitalizations
            for row in hospSlice07.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.07'] = row.CurrentHospitalizations
            for row in hospSlice08.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.08'] = row.CurrentHospitalizations
            for row in hospSlice09.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.09'] = row.CurrentHospitalizations
            for row in hospSlice10.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.10'] = row.CurrentHospitalizations
            for row in hospSlice11.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.11'] = row.CurrentHospitalizations
            for row in hospSlice12.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.12'] = row.CurrentHospitalizations
            for row in hospSlice13.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.13'] = row.CurrentHospitalizations
            for row in hospSlice14.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.14'] = row.CurrentHospitalizations
            for row in hospSlice15.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.15'] = row.CurrentHospitalizations
            for row in hospSlice16.itertuples():
                if loaded.at[i, 'State_full'] == row.StateName:
                    if (row.CurrentHospitalizations > 0):
                        loaded.at[i, 'Hospitalizations.16'] = row.CurrentHospitalizations


            


        loaded = loaded.reset_index()
        loaded.to_csv(r'output.csv', index=None, header=True)
        
        click.echo('output file exported')
    elif processtype == 'cclab-covid-time':
        # used on us dashboard, back to normal etc. thios calculates daily values, but in the dashboards we usually use
        # 7 day averages - so calculate a few days around target date and then manually get the averages

        month = input[:2]
        day = input[3:5]
        year = input[6:10]

        loaded_location = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/' + \
            month + '-' + day + '-' + year + '.csv'

        loaded = pd.read_csv(loaded_location, delimiter=',', encoding='latin1')
        click.echo('newer data loaded')

        oldData_location = '../../Work/Athena/new data/covid-latest-data.csv'
        oldData = pd.read_csv(
            oldData_location, delimiter=',', encoding='latin1')
        click.echo('older data loaded')

        timeData_location = '../../Work/Athena/new data/covid-time-data.csv'
        timeData = pd.read_csv(
            timeData_location, delimiter=',', encoding='latin1')
        click.echo('time series data loaded')

        # create new data
        newData = pd.DataFrame(
            columns=['state', 'confirmed', 'deaths'])

        for row in loaded.itertuples():
            newData = newData.append(
                {'state': row.Province_State, 'confirmed': row.Confirmed, 'deaths': row.Deaths}, ignore_index=True)

        newData.to_csv(
            r'../../Work/Athena/new data/covid-latest-data.csv', index=False, header=True)
        click.echo('latest data exported')

        today = []
        # for row in newData.itertuples():
        #     today.append(row.confirmed)
        # for row in newData.itertuples():
        #     today.append(row.deaths)

        for i in range(len(newData)):
            today.append(newData.at[i, 'confirmed'] -
                         oldData.at[i, 'confirmed'])

        for i in range(len(newData)):
            today.append(newData.at[i, 'deaths'] - oldData.at[i, 'deaths'])

        timeData = timeData.assign(**{input: today})
        timeData.to_csv(
            r'../../Work/Athena/new data/covid-time-data.csv', index=False, header=True)
        click.echo('time data exported')

    elif processtype == 'cclab-old-covid':
        # Load covid data files
        # location_01 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/03-06-2020.csv'
        # location_02 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/03-14-2020.csv'
        location_03 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/03-24-2020.csv'
        location_04 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/04-03-2020.csv'
        location_05 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/04-17-2020.csv'
        location_06 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/05-02-2020.csv'
        location_07 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/05-16-2020.csv'
        location_08 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/05-30-2020.csv'
        location_09 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/06-13-2020.csv'
        location_10 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/06-27-2020.csv'
        location_11 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/07-11-2020.csv'
        location_12 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/07-25-2020.csv'
        location_13 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/08-08-2020.csv'
        location_14 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/08-22-2020.csv'
        population_loc = 'resources/jhu_population.csv'
        # loaded01 = pd.read_csv(location_01, delimiter=',', encoding='latin1')
        # loaded02 = pd.read_csv(location_02, delimiter=',', encoding='latin1')
        loaded03 = pd.read_csv(location_03, delimiter=',', encoding='latin1')
        loaded04 = pd.read_csv(location_04, delimiter=',', encoding='latin1')
        loaded05 = pd.read_csv(location_05, delimiter=',', encoding='latin1')
        loaded06 = pd.read_csv(location_06, delimiter=',', encoding='latin1')
        loaded07 = pd.read_csv(location_07, delimiter=',', encoding='latin1')
        loaded08 = pd.read_csv(location_08, delimiter=',', encoding='latin1')
        loaded09 = pd.read_csv(location_09, delimiter=',', encoding='latin1')
        loaded10 = pd.read_csv(location_10, delimiter=',', encoding='latin1')
        loaded11 = pd.read_csv(location_11, delimiter=',', encoding='latin1')
        loaded12 = pd.read_csv(location_12, delimiter=',', encoding='latin1')
        loaded13 = pd.read_csv(location_13, delimiter=',', encoding='latin1')
        loaded14 = pd.read_csv(location_14, delimiter=',', encoding='latin1')
        population = pd.read_csv(
            population_loc, delimiter=',', encoding='latin1')
        click.echo('covid data loaded')

        # initialise columns
        loaded['Incidence_Rate.01'] = ''
        loaded['Case-Fatality_Ratio.01'] = ''
        loaded['Incidence_Rate.02'] = ''
        loaded['Case-Fatality_Ratio.02'] = ''
        loaded['Incidence_Rate.03'] = ''
        loaded['Case-Fatality_Ratio.03'] = ''
        loaded['Incidence_Rate.04'] = ''
        loaded['Case-Fatality_Ratio.04'] = ''
        loaded['Incidence_Rate.05'] = ''
        loaded['Case-Fatality_Ratio.05'] = ''
        loaded['Incidence_Rate.06'] = ''
        loaded['Case-Fatality_Ratio.06'] = ''
        loaded['Incidence_Rate.07'] = ''
        loaded['Case-Fatality_Ratio.07'] = ''
        loaded['Incidence_Rate.08'] = ''
        loaded['Case-Fatality_Ratio.08'] = ''
        loaded['Incidence_Rate.09'] = ''
        loaded['Case-Fatality_Ratio.09'] = ''
        loaded['Incidence_Rate.10'] = ''
        loaded['Case-Fatality_Ratio.10'] = ''
        loaded['Incidence_Rate.11'] = ''
        loaded['Case-Fatality_Ratio.11'] = ''
        loaded['Incidence_Rate.12'] = ''
        loaded['Case-Fatality_Ratio.12'] = ''
        loaded['Incidence_Rate.13'] = ''
        loaded['Case-Fatality_Ratio.13'] = ''
        loaded['Incidence_Rate.14'] = ''
        loaded['Case-Fatality_Ratio.14'] = ''

        # change default column name of Case-Fatality_Ratio to Case_Fatality_Ratio
        # loaded01.columns = [c.strip().replace('/', '_')
        #                     for c in loaded01.columns]
        # loaded02.columns = [c.strip().replace('/', '_')
        #                     for c in loaded02.columns]
        loaded03.columns = [c.strip().replace('-', '_')
                            for c in loaded03.columns]
        loaded04.columns = [c.strip().replace('-', '_')
                            for c in loaded04.columns]
        loaded05.columns = [c.strip().replace('-', '_')
                            for c in loaded05.columns]
        loaded06.columns = [c.strip().replace('-', '_')
                            for c in loaded06.columns]
        loaded07.columns = [c.strip().replace('-', '_')
                            for c in loaded07.columns]
        loaded08.columns = [c.strip().replace('-', '_')
                            for c in loaded08.columns]
        loaded09.columns = [c.strip().replace('-', '_')
                            for c in loaded09.columns]
        loaded10.columns = [c.strip().replace('-', '_')
                            for c in loaded10.columns]
        loaded11.columns = [c.strip().replace('-', '_')
                            for c in loaded11.columns]
        loaded12.columns = [c.strip().replace('-', '_')
                            for c in loaded12.columns]
        loaded13.columns = [c.strip().replace('-', '_')
                            for c in loaded13.columns]
        loaded14.columns = [c.strip().replace('-', '_')
                            for c in loaded14.columns]

        # def getPopulation(country, state, admin):
        #     nonlocal population
        #     click.echo(str(country) +
        #                str(state) + str(admin))
        #     for row in population.itertuples():
        #         if row.Country_Region == country and row.Province_State == state and row.Admin2 == admin:
        #             click.echo("All")
        #             return int(row.Population)
        #     for row in population.itertuples():
        #         if row.Country_Region == country and row.Province_State == state and math.isnan(row.Admin2):
        #             click.echo("No admin")
        #             return int(row.Population)
        #     for row in population.itertuples():
        #         if row.Country_Region == country and math.isnan(row.Province_State) and math.isnan(row.Admin2):
        #             click.echo("No state")
        #             return int(row.Population)
        #     click.echo('population for ' + str(country) +
        #                str(state) + str(admin) + ' not found')
        #     return 0

        # Populate columns. one loop for each time point
        for i in range(len(loaded)):
            pop = getPopulation(loaded.at[i, 'CurrentCountry'],
                                loaded.at[i, 'CovidArea'], loaded.at[i, 'CovidAreaSmaller'])

            # for row in loaded03.itertuples():

            #     if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
            #         click.echo(row.Confirmed)
            #         click.echo(pop)
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
            #             loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
            #                 row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
            #         loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
            #             row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
            #         loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
            #             row.Confirmed*100
            #         break

            # for row in loaded04.itertuples():
            #     if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
            #             loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
            #                 row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
            #         loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
            #             row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
            #         loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
            #             row.Confirmed*100
            #         break

            # for row in loaded05.itertuples():
            #     if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
            #             loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
            #                 row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
            #         loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
            #             row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
            #         loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
            #             row.Confirmed*100
            #         break

            # for row in loaded06.itertuples():
            #     if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
            #             loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
            #                 row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
            #         loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
            #             row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
            #         loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
            #             row.Confirmed*100
            #         break

            # for row in loaded07.itertuples():
            #     if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
            #         if (row.Confirmed > 0):
            #             loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
            #             loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
            #                 row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
            #         loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
            #             row.Confirmed*100
            #         break
            #     elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
            #         loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
            #         loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
            #             row.Confirmed*100
            #         break

            for row in loaded08.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.08'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.08'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.08'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.08'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.08'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.08'] = row.Case_Fatality_Ratio
                    break

            for row in loaded09.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.09'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.09'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.09'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.09'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.09'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.09'] = row.Case_Fatality_Ratio
                    break

            for row in loaded10.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.10'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.10'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.10'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.10'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.10'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.10'] = row.Case_Fatality_Ratio
                    break

            for row in loaded11.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.11'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.11'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.11'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.11'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.11'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.11'] = row.Case_Fatality_Ratio
                    break

            for row in loaded12.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.12'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.12'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.12'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.12'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.12'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.12'] = row.Case_Fatality_Ratio
                    break

            for row in loaded13.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.13'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.13'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.13'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.13'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.13'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.13'] = row.Case_Fatality_Ratio
                    break

            for row in loaded14.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.14'] = row.Incidence_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.14'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.14'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.14'] = row.Case_Fatality_Ratio
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.14'] = row.Incidence_Rate
                    loaded.at[i, 'Case-Fatality_Ratio.14'] = row.Case_Fatality_Ratio
                    break

            click.echo('row ' + str(i) + ' done')
            if (i == 10):
                # loaded = loaded.reset_index()
                loaded.to_csv(r'output1.csv', index=None, header=True)
                click.echo('sample exported')
            if (i == 75):
                # loaded = loaded.reset_index()
                loaded.to_csv(r'output2.csv', index=None, header=True)
                click.echo('sample exported')
            if (i == 500):
                # loaded = loaded.reset_index()
                loaded.to_csv(r'output3.csv', index=None, header=True)
                click.echo('sample exported')

        loaded = loaded.reset_index()
        loaded.to_csv(r'output.csv', index=None, header=True)

    elif processtype == "preprint3-aggregate":

        #load aditional files
        recAge = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-age-scat_data.csv', delimiter=',', encoding='latin1')
        recCovid = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-covid-scat_data.csv', delimiter=',', encoding='latin1')
        recEducation = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-education-scat_data.csv', delimiter=',', encoding='latin1')
        recFuture = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-future-scat_data.csv', delimiter=',', encoding='latin1')
        recImmediate = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-immediate-scat_data.csv', delimiter=',', encoding='latin1')
        recMask1 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-mask1-scat_data.csv', delimiter=',', encoding='latin1')
        recMask2 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-mask2-scat_data.csv', delimiter=',', encoding='latin1')
        recMask3 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-mask3-scat_data.csv', delimiter=',', encoding='latin1')
        recMask4 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-mask4-scat_data.csv', delimiter=',', encoding='latin1')
        recMask5 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-mask5-scat_data.csv', delimiter=',', encoding='latin1')
        recPolitical = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-political-scat_data.csv', delimiter=',', encoding='latin1')
        recRisk = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-risk-scat_data.csv', delimiter=',', encoding='latin1')
        recSes = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-ses-scat_data.csv', delimiter=',', encoding='latin1')
        recSex = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-sex-scat_data.csv', delimiter=',', encoding='latin1')
        recStress = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/recreational-stress-scat_data.csv', delimiter=',', encoding='latin1')

        rouAge = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-age_data.csv', delimiter=',', encoding='latin1')
        rouCovid = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-covid_data.csv', delimiter=',', encoding='latin1')
        rouEducation = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-education_data.csv', delimiter=',', encoding='latin1')
        rouFuture = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-future_data.csv', delimiter=',', encoding='latin1')
        rouImmediate = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-immediate_data.csv', delimiter=',', encoding='latin1')
        rouMask1 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-mask1_data.csv', delimiter=',', encoding='latin1')
        rouMask2 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-mask2_data.csv', delimiter=',', encoding='latin1')
        rouMask3 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-mask3_data.csv', delimiter=',', encoding='latin1')
        rouMask4 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-mask4_data.csv', delimiter=',', encoding='latin1')
        rouMask5 = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-mask5_data.csv', delimiter=',', encoding='latin1')
        rouPolitical = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-political_data.csv', delimiter=',', encoding='latin1')
        rouRisk = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-risk_data.csv', delimiter=',', encoding='latin1')
        rouSes = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-ses_data.csv', delimiter=',', encoding='latin1')
        rouSex = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-sex_data.csv', delimiter=',', encoding='latin1')
        rouStress = pd.read_csv(
            'C:/Users/Hecto/OneDrive/Desktop/aggregates/routine-stress_data.csv', delimiter=',', encoding='latin1')

        click.echo("additional files loaded")
        #initialise columns
        loaded['recAgeAggr'] = ''
        loaded['recCovidAggr'] = ''
        loaded['recEducationAggr'] = ''
        loaded['recEducationJit'] = ''
        loaded['recFutureAggr'] = ''
        loaded['recImmediateAggr'] = ''
        loaded['recMask1Aggr'] = ''
        loaded['recMask1Jit'] = ''
        loaded['recMask2Aggr'] = ''
        loaded['recMask2Jit'] = ''
        loaded['recMask3Aggr'] = ''
        loaded['recMask3Jit'] = ''
        loaded['recMask4Aggr'] = ''
        loaded['recMask4Jit'] = ''
        loaded['recMask5Aggr'] = ''
        loaded['recMask5Jit'] = ''
        loaded['recPoliticalAggr'] = ''
        loaded['recPoliticalJit'] = ''
        loaded['recRiskAggr'] = ''
        loaded['recRiskJit'] = ''
        loaded['recSesAggr'] = ''
        loaded['recSesJit'] = ''
        loaded['recSexAggr'] = ''
        loaded['recSexJit'] = ''
        loaded['recStressAggr'] = ''
        loaded['recStressJit'] = ''
        loaded['rouAgeAggr'] = ''
        loaded['rouCovidAggr'] = ''
        loaded['rouEducationAggr'] = ''
        loaded['rouEducationJit'] = ''
        loaded['rouFutureAggr'] = ''
        loaded['rouImmediateAggr'] = ''
        loaded['rouMask1Aggr'] = ''
        loaded['rouMask1Jit'] = ''
        loaded['rouMask2Aggr'] = ''
        loaded['rouMask2Jit'] = ''
        loaded['rouMask3Aggr'] = ''
        loaded['rouMask3Jit'] = ''
        loaded['rouMask4Aggr'] = ''
        loaded['rouMask4Jit'] = ''
        loaded['rouMask5Aggr'] = ''
        loaded['rouMask5Jit'] = ''
        loaded['rouPoliticalAggr'] = ''
        loaded['rouPoliticalJit'] = ''
        loaded['rouRiskAggr'] = ''
        loaded['rouRiskJit'] = ''
        loaded['rouSesAggr'] = ''
        loaded['rouSesJit'] = ''
        loaded['rouSexAggr'] = ''
        loaded['rouSexJit'] = ''
        loaded['rouStressAggr'] = ''
        loaded['rouStressJit'] = ''
       
        for i in range(len(loaded)):
            # click.echo(loaded.at[i, 'Age'])
            for row in recAge.itertuples():
                if str(loaded.at[i, 'Age']) == str(row.Age) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recAgeAggr'] = row.Count
                    break

            for row in recCovid.itertuples():
                if str(loaded.at[i, 'Covid']) == str(row.Covid) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recCovidAggr'] = row.Count
                    break
            
            for row in recEducation.itertuples():
                if str(loaded.at[i, 'Education']) == str(row.Education) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recEducationAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Education + jit
                    loaded.at[i, 'recEducationJit'] = value
                    break

            for row in recFuture.itertuples():
                if str(loaded.at[i, 'CFCcompositeFuture']) == str(row.CFCcompositeFuture) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recFutureAggr'] = row.Count
                    break

            for row in recImmediate.itertuples():
                if str(loaded.at[i, 'CFCcompositeImmediate']) == str(row.CFCcompositeImmediate) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recImmediateAggr'] = row.Count
                    break

            for row in recMask1.itertuples():
                if str(loaded.at[i, 'Mask1']) == str(row.Mask1) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recMask1Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask1 + jit
                    loaded.at[i, 'recMask1Jit'] = value
                    break

            for row in recMask2.itertuples():
                if str(loaded.at[i, 'Mask2']) == str(row.Mask2) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recMask2Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask2 + jit
                    loaded.at[i, 'recMask2Jit'] = value
                    break

            for row in recMask3.itertuples():
                if str(loaded.at[i, 'Mask3']) == str(row.Mask3) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recMask3Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask3 + jit
                    loaded.at[i, 'recMask3Jit'] = value
                    break

            for row in recMask4.itertuples():
                if str(loaded.at[i, 'Mask4']) == str(row.Mask4) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recMask4Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask4 + jit
                    loaded.at[i, 'recMask4Jit'] = value
                    break

            for row in recMask5.itertuples():
                if str(loaded.at[i, 'Mask5']) == str(row.Mask5) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recMask5Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask5 + jit
                    loaded.at[i, 'recMask5Jit'] = value
                    break

            for row in recPolitical.itertuples():
                if str(loaded.at[i, 'Political']) == str(row.Political) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recPoliticalAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Political + jit
                    loaded.at[i, 'recPoliticalJit'] = value
                    break

            for row in recRisk.itertuples():
                if str(loaded.at[i, 'Risk']) == str(row.Risk) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recRiskAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Risk + jit
                    loaded.at[i, 'recRiskJit'] = value
                    break

            for row in recSes.itertuples():
                if str(loaded.at[i, 'SubjectiveSES']) == str(row.SubjectiveSES) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recSesAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.SubjectiveSES + jit
                    loaded.at[i, 'recSesJit'] = value
                    break

            for row in recSex.itertuples():
                if str(loaded.at[i, 'Sex']) == str(row.Sex) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recSexAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Sex + jit
                    loaded.at[i, 'recSexJit'] = value
                    break

            for row in recStress.itertuples():
                if str(loaded.at[i, 'Stress']) == str(row.Stress) and str(loaded.at[i, 'Recreational']) == str(row.Recreational):
                    loaded.at[i, 'recStressAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Stress + jit
                    loaded.at[i, 'recStressJit'] = value
                    break

            for row in rouAge.itertuples():
                if str(loaded.at[i, 'Age']) == str(row.Age) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouAgeAggr'] = row.Count
                    break

            for row in rouCovid.itertuples():
                if str(loaded.at[i, 'Covid']) == str(row.Covid) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouCovidAggr'] = row.Count
                    break

            for row in rouEducation.itertuples():
                if str(loaded.at[i, 'Education']) == str(row.Education) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouEducationAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Education + jit
                    loaded.at[i, 'rouEducationJit'] = value
                    break

            for row in rouFuture.itertuples():
                if str(loaded.at[i, 'CFCcompositeFuture']) == str(row.CFCcompositeFuture) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouFutureAggr'] = row.Count
                    break

            for row in rouImmediate.itertuples():
                if str(loaded.at[i, 'CFCcompositeImmediate']) == str(row.CFCcompositeImmediate) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouImmediateAggr'] = row.Count
                    break

            for row in rouMask1.itertuples():
                if str(loaded.at[i, 'Mask1']) == str(row.Mask1) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouMask1Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask1 + jit
                    loaded.at[i, 'rouMask1Jit'] = value
                    break

            for row in rouMask2.itertuples():
                if str(loaded.at[i, 'Mask2']) == str(row.Mask2) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouMask2Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask2 + jit
                    loaded.at[i, 'rouMask2Jit'] = value
                    break

            for row in rouMask3.itertuples():
                if str(loaded.at[i, 'Mask3']) == str(row.Mask3) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouMask3Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask3 + jit
                    loaded.at[i, 'rouMask3Jit'] = value
                    break

            for row in rouMask4.itertuples():
                if str(loaded.at[i, 'Mask4']) == str(row.Mask4) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouMask4Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask4 + jit
                    loaded.at[i, 'rouMask4Jit'] = value
                    break

            for row in rouMask5.itertuples():
                if str(loaded.at[i, 'Mask5']) == str(row.Mask5) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouMask5Aggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Mask5 + jit
                    loaded.at[i, 'rouMask5Jit'] = value
                    break

            for row in rouPolitical.itertuples():
                if str(loaded.at[i, 'Political']) == str(row.Political) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouPoliticalAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Political + jit
                    loaded.at[i, 'rouPoliticalJit'] = value
                    break

            for row in rouRisk.itertuples():
                if str(loaded.at[i, 'Risk']) == str(row.Risk) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouRiskAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Risk + jit
                    loaded.at[i, 'rouRiskJit'] = value
                    break

            for row in rouSes.itertuples():
                if str(loaded.at[i, 'SubjectiveSES']) == str(row.SubjectiveSES) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouSesAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.SubjectiveSES + jit
                    loaded.at[i, 'rouSesJit'] = value
                    break

            for row in rouSex.itertuples():
                if str(loaded.at[i, 'Sex']) == str(row.Sex) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouSexAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Sex + jit
                    loaded.at[i, 'rouSexJit'] = value
                    break

            for row in rouStress.itertuples():
                if str(loaded.at[i, 'Stress']) == str(row.Stress) and str(loaded.at[i, 'Routine']) == str(row.Routine):
                    loaded.at[i, 'rouStressAggr'] = row.Count
                    jit = row.jitter/4 - 0.125
                    value = row.Stress + jit
                    loaded.at[i, 'rouStressJit'] = value
                    break


        loaded = loaded.reset_index()
        loaded.to_csv(r'output.csv', index=None, header=True)

    elif processtype == "cclab-dashboard-us":

        measures = ["PerceptionRisk", "PFINeigh1", "PFINeigh6", "PFIcountry1", 
        "PFIcountry6", "WillingnessNeigh", "NBTneigh", "WillingnessCountry", "NBTcountry"]

        measures_b = ["PerceptionRisk", "PFINeigh1", "PFINeigh6", "PFIcountry1", 
        "PFIcountry6", "WillingnessNeigh", "NBTneigh", "WillingnessCountry", "NBTcountry"]

        # get states
        states = loaded.State_full.unique()

        output_vars = pd.DataFrame(
            columns=['State', 'Measure', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12'])

        output_breakdown = pd.DataFrame(
            columns=['State', 'Measure', 'subclass', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12'])
        
        output_map = pd.DataFrame(
            columns=['State_full', 'State', 'Count', 'Sex', 'Covid_infected', 'Age'])

        # For each variable calculate averages by state and date
        for msr in measures:
            total_all_t1 = 0
            count_all_t1 = 0
            total_all_t2 = 0
            count_all_t2 = 0
            total_all_t3 = 0
            count_all_t3 = 0
            total_all_t4 = 0
            count_all_t4 = 0
            total_all_t5 = 0
            count_all_t5 = 0
            total_all_t6 = 0
            count_all_t6 = 0
            total_all_t7 = 0
            count_all_t7 = 0
            total_all_t8 = 0
            count_all_t8 = 0
            total_all_t9 = 0
            count_all_t9 = 0
            total_all_t10 = 0
            count_all_t10 = 0
            total_all_t11 = 0
            count_all_t11 = 0
            total_all_t12 = 0
            count_all_t12 = 0
            for state in states: 
                t1_total = 0
                t1_count = 0
                t2_total = 0
                t2_count = 0
                t3_total = 0
                t3_count = 0
                t4_total = 0
                t4_count = 0
                t5_total = 0
                t5_count = 0
                t6_total = 0
                t6_count = 0
                t7_total = 0
                t7_count = 0
                t8_total = 0
                t8_count = 0
                t9_total = 0
                t9_count = 0
                t10_total = 0
                t10_count = 0
                t11_total = 0
                t11_count = 0
                t12_total = 0
                t12_count = 0
                avg1 = np.nan
                avg2 = np.nan
                avg3 = np.nan
                avg4 = np.nan
                avg5 = np.nan
                avg6 = np.nan
                avg7 = np.nan
                avg8 = np.nan
                avg9 = np.nan
                avg10 = np.nan
                avg11 = np.nan
                avg12 = np.nan

                for i in range(len(loaded)):
                    val = float(loaded.at[i, msr])
                   
                    if state == loaded.at[i, "State_full"] and math.isnan(val) == False:
                        if loaded.at[i, "Date"] == "09/26/2020":
                            t1_total += val
                            t1_count += 1
                        elif  loaded.at[i, "Date"] == "10/27/2020":
                            t2_total += val
                            t2_count += 1
                        elif  loaded.at[i, "Date"] == "11/28/2020":
                            t3_total += val
                            t3_count += 1
                        elif loaded.at[i, "Date"] == "12/28/2020":
                            t4_total += val
                            t4_count += 1
                        elif  loaded.at[i, "Date"] == "01/27/2021":
                            t5_total += val
                            t5_count += 1
                        elif  loaded.at[i, "Date"] == "02/26/2021":
                            t6_total += val
                            t6_count += 1
                        elif  loaded.at[i, "Date"] == "03/28/2021":
                            t7_total += val
                            t7_count += 1
                        elif  loaded.at[i, "Date"] == "04/27/2021":
                            t8_total += val
                            t8_count += 1
                        elif  loaded.at[i, "Date"] == "05/27/2021":
                            t9_total += val
                            t9_count += 1
                        elif  loaded.at[i, "Date"] == "06/26/2021":
                            t10_total += val
                            t10_count += 1
                        elif  loaded.at[i, "Date"] == "07/26/2021":
                            t11_total += val
                            t11_count += 1
                        elif  loaded.at[i, "Date"] == "08/25/2021":
                            t12_total += val
                            t12_count += 1
                
                if t1_total > 0:
                    avg1 = t1_total/t1_count
                
                if t2_total > 0:    
                    avg2 = t2_total/t2_count
                
                if t3_total > 0:
                    avg3 = t3_total/t3_count
                
                if t4_total > 0:
                    avg4 = t4_total/t4_count
                
                if t5_total > 0:
                    avg5 = t5_total/t5_count
                
                if t6_total > 0:
                    avg6 = t6_total/t6_count
                
                if t7_total > 0:
                    avg7 = t7_total/t7_count
                
                if t8_total > 0:
                    avg8 = t8_total/t8_count
                
                if t9_total > 0:
                    avg9 = t9_total/t9_count
                
                if t10_total > 0:
                    avg10 = t10_total/t10_count
                
                if t11_total > 0:
                    avg11 = t11_total/t11_count
                
                if t12_total > 0:
                    avg12 = t12_total/t12_count
                
                output_vars = output.append({'State': state, 'Measure': msr, 't1': avg1, 't2': avg2, 't3': avg3, 't4': avg4, 't5': avg5,
                                't6': avg6, 't7': avg7, 't8': avg8, 't9': avg9, 't10': avg10, 't11': avg11, 't12': avg12}, ignore_index=True)

                total_all_t1 += t1_total
                count_all_t1 += t1_count
                total_all_t2 += t2_total
                count_all_t2 += t2_count
                total_all_t3 += t3_total
                count_all_t3 += t3_count
                total_all_t4 += t4_total
                count_all_t4 += t4_count
                total_all_t5 += t5_total
                count_all_t5 += t5_count
                total_all_t6 += t6_total
                count_all_t6 += t6_count
                total_all_t7 += t7_total
                count_all_t7 += t7_count
                total_all_t8 += t8_total
                count_all_t8 += t8_count
                total_all_t9 += t9_total
                count_all_t9 += t9_count
                total_all_t10 += t10_total
                count_all_t10 += t10_count
                total_all_t11 += t11_total
                count_all_t11 += t11_count
                total_all_t12 += t12_total
                count_all_t12 += t12_count
                
            
            tot_avg1 = total_all_t1/count_all_t1
            tot_avg2 = total_all_t2/count_all_t2
            tot_avg3 = total_all_t3/count_all_t3
            tot_avg4 = total_all_t4/count_all_t4
            tot_avg5 = total_all_t5/count_all_t5
            tot_avg6 = total_all_t6/count_all_t6
            tot_avg7 = total_all_t7/count_all_t7
            tot_avg8 = total_all_t8/count_all_t8
            tot_avg9 = total_all_t9/count_all_t9
            tot_avg10 = total_all_t10/count_all_t10
            tot_avg11 = total_all_t11/count_all_t11
            tot_avg12 = total_all_t12/count_all_t12

            output_vars = output_vars.append({'State': "All states", 'Measure': msr, 't1': tot_avg1, 't2': tot_avg2, 't3': tot_avg3, 't4': tot_avg4, 't5': tot_avg5,
                                    't6': tot_avg6, 't7': tot_avg7, 't8': tot_avg8, 't9': tot_avg9, 't10': tot_avg10, 't11': tot_avg11, 't12': tot_avg12}, ignore_index=True)
            click.echo("processing for " + msr + " completed")
        
        output_vars = output_vars.reset_index()
        output_vars.to_csv(r'output_vars.csv', index=None, header=True)
        click.echo("output_vars.csv exported")
        
        # sex & covid
        sex_total_all = 0
        sex_count_all = 0
        covid_total_all = 0
        age_total_all = 0
        age_count_all = 0
        count_all = 0
        for state in states: 
            sex_total = 0
            sex_count = 0
            covid_total = 0
            age_total = 0
            age_count = 0
            state_code = ''
            count = 0

            for i in range(len(loaded)):
                 if state == loaded.at[i, "State_full"] and loaded.at[i, "Date"] == "09/26/2020":
                sex = float(loaded.at[i, "Sex"])
                covid = float(loaded.at[i, "InfectedCovidLatest"])
                    age = float(loaded.at[i, "Age"])
                    state_code = loaded.at[i, "State"]
                    count += 1
                
                    if math.isnan(sex) == False:
                        if sex == 2:
                            sex_total += 1
                        sex_count += 1
                
                    if math.isnan(covid) == False:
                        if covid == 3:
                            covid_total += 1
                 
                    if math.isnan(age) == False:
                        age_total += age
                        age_count += 1
                        
            
            sex_per = sex_total/sex_count
            age_avg = age_total/age_count

            output_map = output_map.append({'State_full': state, 'State': state_code, 'Count': count, 'Sex': sex_per, 
                'Covid_infected': covid_total, 'Age': age_avg}, ignore_index=True)
            
            sex_total_all += sex_total
            sex_count_all += sex_count
            covid_total_all += covid_total
            age_total_all += age_total
            age_count_all += age_count
            count_all += count

            sex_per_all = sex_total_all/sex_count_all
            age_avg_all = age_total_all/age_count_all
        
        output_map = output_map.append({'State_full': 'All state', 'State': '', 'Count': count_all, 'Sex': sex_per_all, 
                'Covid_infected': covid_total_all, 'Age': age_avg_all}, ignore_index=True)


        output_map = output_map.reset_index()
        output_map.to_csv(r'output_map.csv', index=None, header=True)
        click.echo("output_map.csv exported")

    elif processtype == "cclab-dashboard-us-detail":

        loaded["Age"] = pd.to_numeric(loaded["Age"])
        loaded["Sex"] = pd.to_numeric(loaded["Sex"])
        loaded["InfectedCovidLatest"] = pd.to_numeric(loaded["InfectedCovidLatest"])
        loaded["t1"] = pd.to_numeric(loaded["t1"])
        loaded["t2"] = pd.to_numeric(loaded["t2"])
        loaded["t3"] = pd.to_numeric(loaded["t3"])
        loaded["t4"] = pd.to_numeric(loaded["t4"])
        loaded["t5"] = pd.to_numeric(loaded["t5"])
        loaded["t6"] = pd.to_numeric(loaded["t6"])
        loaded["t7"] = pd.to_numeric(loaded["t7"])
        loaded["t8"] = pd.to_numeric(loaded["t8"])
        loaded["t9"] = pd.to_numeric(loaded["t9"])
        loaded["t10"] = pd.to_numeric(loaded["t10"])
        loaded["t11"] = pd.to_numeric(loaded["t11"])
        loaded["t12"] = pd.to_numeric(loaded["t12"])

        measures = ["PerceptionRisk", "PFINeigh1", "PFINeigh6", "PFIcountry1", 
        "PFIcountry6", "WillingnessNeigh", "NBTneigh", "WillingnessCountry", "NBTcountry"]

        # get states
        states = loaded.State_full.unique()

        output_vars = pd.DataFrame(
            columns=['State', 'Measure', 'Category', 'Subcategory', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12'])

        # For each variable calculate averages by state and date
        for msr in measures:
            measureSubset = loaded[loaded.Measure == msr]
            agesubset1 = measureSubset[measureSubset.Age.isin([18, 19, 20, 21, 22, 23, 24])]
            agesubset2 = measureSubset[measureSubset.Age.isin([25, 26, 27, 28, 29, 30, 31, 32, 33, 34])]
            agesubset3 = measureSubset[measureSubset.Age.isin([35, 36, 37, 38, 39, 40, 41, 42, 43, 44])]
            agesubset4 = measureSubset[measureSubset.Age.isin([45, 46, 47, 48, 49, 50, 51, 52, 53, 54])]
            agesubset5 = measureSubset[measureSubset.Age.isin([55, 56, 57, 58, 59, 60, 61, 62, 63, 64])]
            agesubset6 = measureSubset[measureSubset.Age.isin([65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88])]

            maleSubset =  measureSubset[measureSubset.Sex == 1]
            femaleSubset =  measureSubset[measureSubset.Sex == 2]
            otherSubset =  measureSubset[measureSubset.Sex == 3]

            covidYesSubset = measureSubset[measureSubset.InfectedCovidLatest == 3]
            covidNoSubset = measureSubset[measureSubset.InfectedCovidLatest == 1]
            covidMaybeSubset = measureSubset[measureSubset.InfectedCovidLatest == 2]

            age1Avgt1 = agesubset1.t1.mean()
            age1Avgt2 = agesubset1.t2.mean()
            age1Avgt3 = agesubset1.t3.mean()
            age1Avgt4 = agesubset1.t4.mean()
            age1Avgt5 = agesubset1.t5.mean()
            age1Avgt6 = agesubset1.t6.mean()
            age1Avgt7 = agesubset1.t7.mean()
            age1Avgt8 = agesubset1.t8.mean()
            age1Avgt9 = agesubset1.t9.mean()
            age1Avgt10 = agesubset1.t10.mean()
            age1Avgt11 = agesubset1.t11.mean()
            age1Avgt12 = agesubset1.t12.mean()

            age2Avgt1 = agesubset2.t1.mean()
            age2Avgt2 = agesubset2.t2.mean()
            age2Avgt3 = agesubset2.t3.mean()
            age2Avgt4 = agesubset2.t4.mean()
            age2Avgt5 = agesubset2.t5.mean()
            age2Avgt6 = agesubset2.t6.mean()
            age2Avgt7 = agesubset2.t7.mean()
            age2Avgt8 = agesubset2.t8.mean()
            age2Avgt9 = agesubset2.t9.mean()
            age2Avgt10 = agesubset2.t10.mean()
            age2Avgt11 = agesubset2.t11.mean()
            age2Avgt12 = agesubset2.t12.mean()

            age3Avgt1 = agesubset3.t1.mean()
            age3Avgt2 = agesubset3.t2.mean()
            age3Avgt3 = agesubset3.t3.mean()
            age3Avgt4 = agesubset3.t4.mean()
            age3Avgt5 = agesubset3.t5.mean()
            age3Avgt6 = agesubset3.t6.mean()
            age3Avgt7 = agesubset3.t7.mean()
            age3Avgt8 = agesubset3.t8.mean()
            age3Avgt9 = agesubset3.t9.mean()
            age3Avgt10 = agesubset3.t10.mean()
            age3Avgt11 = agesubset3.t11.mean()
            age3Avgt12 = agesubset3.t12.mean()

            age4Avgt1 = agesubset4.t1.mean()
            age4Avgt2 = agesubset4.t2.mean()
            age4Avgt3 = agesubset4.t3.mean()
            age4Avgt4 = agesubset4.t4.mean()
            age4Avgt5 = agesubset4.t5.mean()
            age4Avgt6 = agesubset4.t6.mean()
            age4Avgt7 = agesubset4.t7.mean()
            age4Avgt8 = agesubset4.t8.mean()
            age4Avgt9 = agesubset4.t9.mean()
            age4Avgt10 = agesubset4.t10.mean()
            age4Avgt11 = agesubset4.t11.mean()
            age4Avgt12 = agesubset4.t12.mean()

            age5Avgt1 = agesubset5.t1.mean()
            age5Avgt2 = agesubset5.t2.mean()
            age5Avgt3 = agesubset5.t3.mean()
            age5Avgt4 = agesubset5.t4.mean()
            age5Avgt5 = agesubset5.t5.mean()
            age5Avgt6 = agesubset5.t6.mean()
            age5Avgt7 = agesubset5.t7.mean()
            age5Avgt8 = agesubset5.t8.mean()
            age5Avgt9 = agesubset5.t9.mean()
            age5Avgt10 = agesubset5.t10.mean()
            age5Avgt11 = agesubset5.t11.mean()
            age5Avgt12 = agesubset5.t12.mean()

            age6Avgt1 = agesubset6.t1.mean()
            age6Avgt2 = agesubset6.t2.mean()
            age6Avgt3 = agesubset6.t3.mean()
            age6Avgt4 = agesubset6.t4.mean()
            age6Avgt5 = agesubset6.t5.mean()
            age6Avgt6 = agesubset6.t6.mean()
            age6Avgt7 = agesubset6.t7.mean()
            age6Avgt8 = agesubset6.t8.mean()
            age6Avgt9 = agesubset6.t9.mean()
            age6Avgt10 = agesubset6.t10.mean()
            age6Avgt11 = agesubset6.t11.mean()
            age6Avgt12 = agesubset6.t12.mean()

            maleAvgt1 = maleSubset.t1.mean()
            maleAvgt2 = maleSubset.t2.mean()
            maleAvgt3 = maleSubset.t3.mean()
            maleAvgt4 = maleSubset.t4.mean()
            maleAvgt5 = maleSubset.t5.mean()
            maleAvgt6 = maleSubset.t6.mean()
            maleAvgt7 = maleSubset.t7.mean()
            maleAvgt8 = maleSubset.t8.mean()
            maleAvgt9 = maleSubset.t9.mean()
            maleAvgt10 = maleSubset.t10.mean()
            maleAvgt11 = maleSubset.t11.mean()
            maleAvgt12 = maleSubset.t12.mean()

            femaleAvgt1 = femaleSubset.t1.mean()
            femaleAvgt2 = femaleSubset.t2.mean()
            femaleAvgt3 = femaleSubset.t3.mean()
            femaleAvgt4 = femaleSubset.t4.mean()
            femaleAvgt5 = femaleSubset.t5.mean()
            femaleAvgt6 = femaleSubset.t6.mean()
            femaleAvgt7 = femaleSubset.t7.mean()
            femaleAvgt8 = femaleSubset.t8.mean()
            femaleAvgt9 = femaleSubset.t9.mean()
            femaleAvgt10 = femaleSubset.t10.mean()
            femaleAvgt11 = femaleSubset.t11.mean()
            femaleAvgt12 = femaleSubset.t12.mean()

            otherAvgt1 = otherSubset.t1.mean()
            otherAvgt2 = otherSubset.t2.mean()
            otherAvgt3 = otherSubset.t3.mean()
            otherAvgt4 = otherSubset.t4.mean()
            otherAvgt5 = otherSubset.t5.mean()
            otherAvgt6 = otherSubset.t6.mean()
            otherAvgt7 = otherSubset.t7.mean()
            otherAvgt8 = otherSubset.t8.mean()
            otherAvgt9 = otherSubset.t9.mean()
            otherAvgt10 = otherSubset.t10.mean()
            otherAvgt11 = otherSubset.t11.mean()
            otherAvgt12 = otherSubset.t12.mean()

            covidYesAvgt1 = covidYesSubset.t1.mean()
            covidYesAvgt2 = covidYesSubset.t2.mean()
            covidYesAvgt3 = covidYesSubset.t3.mean()
            covidYesAvgt4 = covidYesSubset.t4.mean()
            covidYesAvgt5 = covidYesSubset.t5.mean()
            covidYesAvgt6 = covidYesSubset.t6.mean()
            covidYesAvgt7 = covidYesSubset.t7.mean()
            covidYesAvgt8 = covidYesSubset.t8.mean()
            covidYesAvgt9 = covidYesSubset.t9.mean()
            covidYesAvgt10 = covidYesSubset.t10.mean()
            covidYesAvgt11 = covidYesSubset.t11.mean()
            covidYesAvgt12 = covidYesSubset.t12.mean()

            covidNoAvgt1 = covidNoSubset.t1.mean()    
            covidNoAvgt2 = covidNoSubset.t2.mean()    
            covidNoAvgt3 = covidNoSubset.t3.mean()    
            covidNoAvgt4 = covidNoSubset.t4.mean()    
            covidNoAvgt5 = covidNoSubset.t5.mean()    
            covidNoAvgt6 = covidNoSubset.t6.mean()    
            covidNoAvgt7 = covidNoSubset.t7.mean()    
            covidNoAvgt8 = covidNoSubset.t8.mean()    
            covidNoAvgt9 = covidNoSubset.t9.mean()    
            covidNoAvgt10 = covidNoSubset.t10.mean()    
            covidNoAvgt11 = covidNoSubset.t11.mean()    
            covidNoAvgt12 = covidNoSubset.t12.mean()

            covidMaybeAvgt1 = covidMaybeSubset.t1.mean()    
            covidMaybeAvgt2 = covidMaybeSubset.t2.mean()    
            covidMaybeAvgt3 = covidMaybeSubset.t3.mean()    
            covidMaybeAvgt4 = covidMaybeSubset.t4.mean()    
            covidMaybeAvgt5 = covidMaybeSubset.t5.mean()    
            covidMaybeAvgt6 = covidMaybeSubset.t6.mean()    
            covidMaybeAvgt7 = covidMaybeSubset.t7.mean()    
            covidMaybeAvgt8 = covidMaybeSubset.t8.mean()    
            covidMaybeAvgt9 = covidMaybeSubset.t9.mean()    
            covidMaybeAvgt10 = covidMaybeSubset.t10.mean()    
            covidMaybeAvgt11 = covidMaybeSubset.t11.mean()    
            covidMaybeAvgt12 = covidMaybeSubset.t12.mean()    

            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '18-24', 't1': age1Avgt1, 't2': age1Avgt2, 't3': age1Avgt3, 't4': age1Avgt4, 't5': age1Avgt5,
                            't6': age1Avgt6, 't7': age1Avgt7, 't8': age1Avgt8, 't9': age1Avgt9, 't10': age1Avgt10, 't11': age1Avgt11, 't12': age1Avgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '25-34', 't1': age2Avgt1, 't2': age2Avgt2, 't3': age2Avgt3, 't4': age2Avgt4, 't5': age2Avgt5,
                            't6': age2Avgt6, 't7': age2Avgt7, 't8': age2Avgt8, 't9': age2Avgt9, 't10': age2Avgt10, 't11': age2Avgt11, 't12': age2Avgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '35-44', 't1': age3Avgt1, 't2': age3Avgt2, 't3': age3Avgt3, 't4': age3Avgt4, 't5': age3Avgt5,
                            't6': age3Avgt6, 't7': age3Avgt7, 't8': age3Avgt8, 't9': age3Avgt9, 't10': age3Avgt10, 't11': age3Avgt11, 't12': age3Avgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '45-54', 't1': age4Avgt1, 't2': age4Avgt2, 't3': age4Avgt3, 't4': age4Avgt4, 't5': age4Avgt5,
                            't6': age4Avgt6, 't7': age4Avgt7, 't8': age4Avgt8, 't9': age4Avgt9, 't10': age4Avgt10, 't11': age4Avgt11, 't12': age4Avgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '55-64', 't1': age5Avgt1, 't2': age5Avgt2, 't3': age5Avgt3, 't4': age5Avgt4, 't5': age5Avgt5,
                            't6': age5Avgt6, 't7': age5Avgt7, 't8': age5Avgt8, 't9': age5Avgt9, 't10': age5Avgt10, 't11': age5Avgt11, 't12': age5Avgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Age', 'Subcategory': '65+', 't1': age6Avgt1, 't2': age6Avgt2, 't3': age6Avgt3, 't4': age6Avgt4, 't5': age6Avgt5,
                            't6': age6Avgt6, 't7': age6Avgt7, 't8': age6Avgt8, 't9': age6Avgt9, 't10': age6Avgt10, 't11': age6Avgt11, 't12': age6Avgt12}, ignore_index=True)

            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Male', 't1': maleAvgt1, 't2': maleAvgt2, 't3': maleAvgt3, 't4': maleAvgt4, 't5': maleAvgt5,
                            't6': maleAvgt6, 't7': maleAvgt7, 't8': maleAvgt8, 't9': maleAvgt9, 't10': maleAvgt10, 't11': maleAvgt11, 't12': maleAvgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Female', 't1': femaleAvgt1, 't2': femaleAvgt2, 't3': femaleAvgt3, 't4': femaleAvgt4, 't5': femaleAvgt5,
                            't6': femaleAvgt6, 't7': femaleAvgt7, 't8': femaleAvgt8, 't9': femaleAvgt9, 't10': femaleAvgt10, 't11': femaleAvgt11, 't12': femaleAvgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Other', 't1': otherAvgt1, 't2': otherAvgt2, 't3': otherAvgt3, 't4': otherAvgt4, 't5': otherAvgt5,
                            't6': otherAvgt6, 't7': otherAvgt7, 't8': otherAvgt8, 't9': otherAvgt9, 't10': otherAvgt10, 't11': otherAvgt11, 't12': otherAvgt12}, ignore_index=True)
        
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_yes', 't1': covidYesAvgt1, 't2': covidYesAvgt2, 't3': covidYesAvgt3, 't4': covidYesAvgt4, 't5': covidYesAvgt5,
                            't6': covidYesAvgt6, 't7': covidYesAvgt7, 't8': covidYesAvgt8, 't9': covidYesAvgt9, 't10': covidYesAvgt10, 't11': covidYesAvgt11, 't12': covidYesAvgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_no', 't1': covidNoAvgt1, 't2': covidNoAvgt2, 't3': covidNoAvgt3, 't4': covidNoAvgt4, 't5': covidNoAvgt5,
                            't6': covidNoAvgt6, 't7': covidNoAvgt7, 't8': covidNoAvgt8, 't9': covidNoAvgt9, 't10': covidNoAvgt10, 't11': covidNoAvgt11, 't12': covidNoAvgt12}, ignore_index=True)
            output_vars = output_vars.append({'State': 'All states', 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_maybe', 't1': covidMaybeAvgt1, 't2': covidMaybeAvgt2, 't3': covidMaybeAvgt3, 't4': covidMaybeAvgt4, 't5': covidMaybeAvgt5,
                            't6': covidMaybeAvgt6, 't7': covidMaybeAvgt7, 't8': covidMaybeAvgt8, 't9': covidMaybeAvgt9, 't10': covidMaybeAvgt10, 't11': covidMaybeAvgt11, 't12': covidMaybeAvgt12}, ignore_index=True)

            for state in states:
                stateAgesubset1 = agesubset1[agesubset1.State_full == state]
                stateAgesubset2 = agesubset2[agesubset2.State_full == state]
                stateAgesubset3 = agesubset3[agesubset3.State_full == state]
                stateAgesubset4 = agesubset4[agesubset4.State_full == state]
                stateAgesubset5 = agesubset5[agesubset5.State_full == state]
                stateAgesubset6 = agesubset6[agesubset6.State_full == state]

                stateMaleSubset = maleSubset[maleSubset.State_full == state]
                stateFemaleSubset = femaleSubset[femaleSubset.State_full == state]
                stateOtherSubset = otherSubset[otherSubset.State_full == state]

                stateCovidYesSubset = covidYesSubset[covidYesSubset.State_full == state]
                stateCovidNoSubset = covidNoSubset[covidNoSubset.State_full == state]
                stateCovidMaybeSubset = covidMaybeSubset[covidMaybeSubset.State_full == state]
                
                stateAge1Avgt1 = stateAgesubset1.t1.mean()
                stateAge1Avgt2 = stateAgesubset1.t2.mean()
                stateAge1Avgt3 = stateAgesubset1.t3.mean()
                stateAge1Avgt4 = stateAgesubset1.t4.mean()
                stateAge1Avgt5 = stateAgesubset1.t5.mean()
                stateAge1Avgt6 = stateAgesubset1.t6.mean()
                stateAge1Avgt7 = stateAgesubset1.t7.mean()
                stateAge1Avgt8 = stateAgesubset1.t8.mean()
                stateAge1Avgt9 = stateAgesubset1.t9.mean()
                stateAge1Avgt10 = stateAgesubset1.t10.mean()
                stateAge1Avgt11 = stateAgesubset1.t11.mean()
                stateAge1Avgt12 = stateAgesubset1.t12.mean()

                stateAge2Avgt1 = stateAgesubset2.t1.mean()
                stateAge2Avgt2 = stateAgesubset2.t2.mean()
                stateAge2Avgt3 = stateAgesubset2.t3.mean()
                stateAge2Avgt4 = stateAgesubset2.t4.mean()
                stateAge2Avgt5 = stateAgesubset2.t5.mean()
                stateAge2Avgt6 = stateAgesubset2.t6.mean()
                stateAge2Avgt7 = stateAgesubset2.t7.mean()
                stateAge2Avgt8 = stateAgesubset2.t8.mean()
                stateAge2Avgt9 = stateAgesubset2.t9.mean()
                stateAge2Avgt10 = stateAgesubset2.t10.mean()
                stateAge2Avgt11 = stateAgesubset2.t11.mean()
                stateAge2Avgt12 = stateAgesubset2.t12.mean()

                stateAge3Avgt1 = stateAgesubset3.t1.mean()
                stateAge3Avgt2 = stateAgesubset3.t2.mean()
                stateAge3Avgt3 = stateAgesubset3.t3.mean()
                stateAge3Avgt4 = stateAgesubset3.t4.mean()
                stateAge3Avgt5 = stateAgesubset3.t5.mean()
                stateAge3Avgt6 = stateAgesubset3.t6.mean()
                stateAge3Avgt7 = stateAgesubset3.t7.mean()
                stateAge3Avgt8 = stateAgesubset3.t8.mean()
                stateAge3Avgt9 = stateAgesubset3.t9.mean()
                stateAge3Avgt10 = stateAgesubset3.t10.mean()
                stateAge3Avgt11 = stateAgesubset3.t11.mean()
                stateAge3Avgt12 = stateAgesubset3.t12.mean()

                stateAge4Avgt1 = stateAgesubset4.t1.mean()
                stateAge4Avgt2 = stateAgesubset4.t2.mean()
                stateAge4Avgt3 = stateAgesubset4.t3.mean()
                stateAge4Avgt4 = stateAgesubset4.t4.mean()
                stateAge4Avgt5 = stateAgesubset4.t5.mean()
                stateAge4Avgt6 = stateAgesubset4.t6.mean()
                stateAge4Avgt7 = stateAgesubset4.t7.mean()
                stateAge4Avgt8 = stateAgesubset4.t8.mean()
                stateAge4Avgt9 = stateAgesubset4.t9.mean()
                stateAge4Avgt10 = stateAgesubset4.t10.mean()
                stateAge4Avgt11 = stateAgesubset4.t11.mean()
                stateAge4Avgt12 = stateAgesubset4.t12.mean()

                stateAge5Avgt1 = stateAgesubset5.t1.mean()
                stateAge5Avgt2 = stateAgesubset5.t2.mean()
                stateAge5Avgt3 = stateAgesubset5.t3.mean()
                stateAge5Avgt4 = stateAgesubset5.t4.mean()
                stateAge5Avgt5 = stateAgesubset5.t5.mean()
                stateAge5Avgt6 = stateAgesubset5.t6.mean()
                stateAge5Avgt7 = stateAgesubset5.t7.mean()
                stateAge5Avgt8 = stateAgesubset5.t8.mean()
                stateAge5Avgt9 = stateAgesubset5.t9.mean()
                stateAge5Avgt10 = stateAgesubset5.t10.mean()
                stateAge5Avgt11 = stateAgesubset5.t11.mean()
                stateAge5Avgt12 = stateAgesubset5.t12.mean()

                stateAge6Avgt1 = stateAgesubset6.t1.mean()
                stateAge6Avgt2 = stateAgesubset6.t2.mean()
                stateAge6Avgt3 = stateAgesubset6.t3.mean()
                stateAge6Avgt4 = stateAgesubset6.t4.mean()
                stateAge6Avgt5 = stateAgesubset6.t5.mean()
                stateAge6Avgt6 = stateAgesubset6.t6.mean()
                stateAge6Avgt7 = stateAgesubset6.t7.mean()
                stateAge6Avgt8 = stateAgesubset6.t8.mean()
                stateAge6Avgt9 = stateAgesubset6.t9.mean()
                stateAge6Avgt10 = stateAgesubset6.t10.mean()
                stateAge6Avgt11 = stateAgesubset6.t11.mean()
                stateAge6Avgt12 = stateAgesubset6.t12.mean()

                stateMaleAvgt1 = stateMaleSubset.t1.mean()
                stateMaleAvgt2 = stateMaleSubset.t2.mean()
                stateMaleAvgt3 = stateMaleSubset.t3.mean()
                stateMaleAvgt4 = stateMaleSubset.t4.mean()
                stateMaleAvgt5 = stateMaleSubset.t5.mean()
                stateMaleAvgt6 = stateMaleSubset.t6.mean()
                stateMaleAvgt7 = stateMaleSubset.t7.mean()
                stateMaleAvgt8 = stateMaleSubset.t8.mean()
                stateMaleAvgt9 = stateMaleSubset.t9.mean()
                stateMaleAvgt10 = stateMaleSubset.t10.mean()
                stateMaleAvgt11 = stateMaleSubset.t11.mean()
                stateMaleAvgt12 = stateMaleSubset.t12.mean()

                stateFemaleAvgt1 = stateFemaleSubset.t1.mean()
                stateFemaleAvgt2 = stateFemaleSubset.t2.mean()
                stateFemaleAvgt3 = stateFemaleSubset.t3.mean()
                stateFemaleAvgt4 = stateFemaleSubset.t4.mean()
                stateFemaleAvgt5 = stateFemaleSubset.t5.mean()
                stateFemaleAvgt6 = stateFemaleSubset.t6.mean()
                stateFemaleAvgt7 = stateFemaleSubset.t7.mean()
                stateFemaleAvgt8 = stateFemaleSubset.t8.mean()
                stateFemaleAvgt9 = stateFemaleSubset.t9.mean()
                stateFemaleAvgt10 = stateFemaleSubset.t10.mean()
                stateFemaleAvgt11 = stateFemaleSubset.t11.mean()
                stateFemaleAvgt12 = stateFemaleSubset.t12.mean()

                stateOtherAvgt1 = stateOtherSubset.t1.mean()
                stateOtherAvgt2 = stateOtherSubset.t2.mean()
                stateOtherAvgt3 = stateOtherSubset.t3.mean()
                stateOtherAvgt4 = stateOtherSubset.t4.mean()
                stateOtherAvgt5 = stateOtherSubset.t5.mean()
                stateOtherAvgt6 = stateOtherSubset.t6.mean()
                stateOtherAvgt7 = stateOtherSubset.t7.mean()
                stateOtherAvgt8 = stateOtherSubset.t8.mean()
                stateOtherAvgt9 = stateOtherSubset.t9.mean()
                stateOtherAvgt10 = stateOtherSubset.t10.mean()
                stateOtherAvgt11 = stateOtherSubset.t11.mean()
                stateOtherAvgt12 = stateOtherSubset.t12.mean()

                stateCovidYesAvgt1 = stateCovidYesSubset.t1.mean()
                stateCovidYesAvgt2 = stateCovidYesSubset.t2.mean()
                stateCovidYesAvgt3 = stateCovidYesSubset.t3.mean()
                stateCovidYesAvgt4 = stateCovidYesSubset.t4.mean()
                stateCovidYesAvgt5 = stateCovidYesSubset.t5.mean()
                stateCovidYesAvgt6 = stateCovidYesSubset.t6.mean()
                stateCovidYesAvgt7 = stateCovidYesSubset.t7.mean()
                stateCovidYesAvgt8 = stateCovidYesSubset.t8.mean()
                stateCovidYesAvgt9 = stateCovidYesSubset.t9.mean()
                stateCovidYesAvgt10 = stateCovidYesSubset.t10.mean()
                stateCovidYesAvgt11 = stateCovidYesSubset.t11.mean()
                stateCovidYesAvgt12 = stateCovidYesSubset.t12.mean()

                stateCovidNoAvgt1 = stateCovidNoSubset.t1.mean()
                stateCovidNoAvgt2 = stateCovidNoSubset.t2.mean()
                stateCovidNoAvgt3 = stateCovidNoSubset.t3.mean()
                stateCovidNoAvgt4 = stateCovidNoSubset.t4.mean()
                stateCovidNoAvgt5 = stateCovidNoSubset.t5.mean()
                stateCovidNoAvgt6 = stateCovidNoSubset.t6.mean()
                stateCovidNoAvgt7 = stateCovidNoSubset.t7.mean()
                stateCovidNoAvgt8 = stateCovidNoSubset.t8.mean()
                stateCovidNoAvgt9 = stateCovidNoSubset.t9.mean()
                stateCovidNoAvgt10 = stateCovidNoSubset.t10.mean()
                stateCovidNoAvgt11 = stateCovidNoSubset.t11.mean()
                stateCovidNoAvgt12 = stateCovidNoSubset.t12.mean()

                stateCovidMaybeAvgt1 = stateCovidMaybeSubset.t1.mean()
                stateCovidMaybeAvgt2 = stateCovidMaybeSubset.t2.mean()
                stateCovidMaybeAvgt3 = stateCovidMaybeSubset.t3.mean()
                stateCovidMaybeAvgt4 = stateCovidMaybeSubset.t4.mean()
                stateCovidMaybeAvgt5 = stateCovidMaybeSubset.t5.mean()
                stateCovidMaybeAvgt6 = stateCovidMaybeSubset.t6.mean()
                stateCovidMaybeAvgt7 = stateCovidMaybeSubset.t7.mean()
                stateCovidMaybeAvgt8 = stateCovidMaybeSubset.t8.mean()
                stateCovidMaybeAvgt9 = stateCovidMaybeSubset.t9.mean()
                stateCovidMaybeAvgt10 = stateCovidMaybeSubset.t10.mean()
                stateCovidMaybeAvgt11 = stateCovidMaybeSubset.t11.mean()
                stateCovidMaybeAvgt12 = stateCovidMaybeSubset.t12.mean()

                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '18-24', 't1': stateAge1Avgt1, 't2': stateAge1Avgt2, 't3': stateAge1Avgt3, 't4': stateAge1Avgt4, 't5': stateAge1Avgt5,
                                't6': stateAge1Avgt6, 't7': stateAge1Avgt7, 't8': stateAge1Avgt8, 't9': stateAge1Avgt9, 't10': stateAge1Avgt10, 't11': stateAge1Avgt11, 't12': stateAge1Avgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '25-34', 't1': stateAge2Avgt1, 't2': stateAge2Avgt2, 't3': stateAge2Avgt3, 't4': stateAge2Avgt4, 't5': stateAge2Avgt5,
                                't6': stateAge2Avgt6, 't7': stateAge2Avgt7, 't8': stateAge2Avgt8, 't9': stateAge2Avgt9, 't10': stateAge2Avgt10, 't11': stateAge2Avgt11, 't12': stateAge2Avgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '35-44', 't1': stateAge3Avgt1, 't2': stateAge3Avgt2, 't3': stateAge3Avgt3, 't4': stateAge3Avgt4, 't5': stateAge3Avgt5,
                                't6': stateAge3Avgt6, 't7': stateAge3Avgt7, 't8': stateAge3Avgt8, 't9': stateAge3Avgt9, 't10': stateAge3Avgt10, 't11': stateAge3Avgt11, 't12': stateAge3Avgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '45-54', 't1': stateAge4Avgt1, 't2': stateAge4Avgt2, 't3': stateAge4Avgt3, 't4': stateAge4Avgt4, 't5': stateAge4Avgt5,
                                't6': stateAge4Avgt6, 't7': stateAge4Avgt7, 't8': stateAge4Avgt8, 't9': stateAge4Avgt9, 't10': stateAge4Avgt10, 't11': stateAge4Avgt11, 't12': stateAge4Avgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '55-64', 't1': stateAge5Avgt1, 't2': stateAge5Avgt2, 't3': stateAge5Avgt3, 't4': stateAge5Avgt4, 't5': stateAge5Avgt5,
                                't6': stateAge5Avgt6, 't7': stateAge5Avgt7, 't8': stateAge5Avgt8, 't9': stateAge5Avgt9, 't10': stateAge5Avgt10, 't11': stateAge5Avgt11, 't12': stateAge5Avgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Age', 'Subcategory': '65+', 't1': stateAge6Avgt1, 't2': stateAge6Avgt2, 't3': stateAge6Avgt3, 't4': stateAge6Avgt4, 't5': stateAge6Avgt5,
                                't6': stateAge6Avgt6, 't7': stateAge6Avgt7, 't8': stateAge6Avgt8, 't9': stateAge6Avgt9, 't10': stateAge6Avgt10, 't11': stateAge6Avgt11, 't12': stateAge6Avgt12}, ignore_index=True)

                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Male', 't1': stateMaleAvgt1, 't2': stateMaleAvgt2, 't3': stateMaleAvgt3, 't4': stateMaleAvgt4, 't5': stateMaleAvgt5,
                                't6': stateMaleAvgt6, 't7': stateMaleAvgt7, 't8': stateMaleAvgt8, 't9': stateMaleAvgt9, 't10': stateMaleAvgt10, 't11': stateMaleAvgt11, 't12': stateMaleAvgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Female', 't1': stateFemaleAvgt1, 't2': stateFemaleAvgt2, 't3': stateFemaleAvgt3, 't4': stateFemaleAvgt4, 't5': stateFemaleAvgt5,
                                't6': stateFemaleAvgt6, 't7': stateFemaleAvgt7, 't8': stateFemaleAvgt8, 't9': stateFemaleAvgt9, 't10': stateFemaleAvgt10, 't11': stateFemaleAvgt11, 't12': stateFemaleAvgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Other', 't1': stateOtherAvgt1, 't2': stateOtherAvgt2, 't3': stateOtherAvgt3, 't4': stateOtherAvgt4, 't5': stateOtherAvgt5,
                                't6': stateOtherAvgt6, 't7': stateOtherAvgt7, 't8': stateOtherAvgt8, 't9': stateOtherAvgt9, 't10': stateOtherAvgt10, 't11': stateOtherAvgt11, 't12': stateOtherAvgt12}, ignore_index=True)

                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_yes', 't1': stateCovidYesAvgt1, 't2': stateCovidYesAvgt2, 't3': stateCovidYesAvgt3, 't4': stateCovidYesAvgt4, 't5': stateCovidYesAvgt5,
                                't6': stateCovidYesAvgt6, 't7': stateCovidYesAvgt7, 't8': stateCovidYesAvgt8, 't9': stateCovidYesAvgt9, 't10': stateCovidYesAvgt10, 't11': stateCovidYesAvgt11, 't12': stateCovidYesAvgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_no', 't1': stateCovidNoAvgt1, 't2': stateCovidNoAvgt2, 't3': stateCovidNoAvgt3, 't4': stateCovidNoAvgt4, 't5': stateCovidNoAvgt5,
                                't6': stateCovidNoAvgt6, 't7': stateCovidNoAvgt7, 't8': stateCovidNoAvgt8, 't9': stateCovidNoAvgt9, 't10': stateCovidNoAvgt10, 't11': stateCovidNoAvgt11, 't12': stateCovidNoAvgt12}, ignore_index=True)
                output_vars = output_vars.append({'State': state, 'Measure': msr, 'Category': 'Infected', 'Subcategory': 'Covid_maybe', 't1': stateCovidMaybeAvgt1, 't2': stateCovidMaybeAvgt2, 't3': stateCovidMaybeAvgt3, 't4': stateCovidMaybeAvgt4, 't5': stateCovidMaybeAvgt5,
                                't6': stateCovidMaybeAvgt6, 't7': stateCovidMaybeAvgt7, 't8': stateCovidMaybeAvgt8, 't9': stateCovidMaybeAvgt9, 't10': stateCovidMaybeAvgt10, 't11': stateCovidMaybeAvgt11, 't12': stateCovidMaybeAvgt12}, ignore_index=True)

            click.echo("processing for " + msr + " completed")
        
        output_vars = output_vars.reset_index()
        output_vars.to_csv(r'output_vars.csv', index=None, header=True)
        click.echo("output_vars.csv exported")

    elif processtype == "cclab-dashboard-glo":

        measures = ["PerceptionsRisk", "PFIHumanitySharedFate", "PFIHumanityEmpathy", "PFINeighEmpathy", 
        "PFINeighSharedFate", "NBTNeigh", "WillingnessNeigh", "NBTHumanity", "WillingnessHumanity"]

        # get states
        countries = loaded.CurrentCountry.unique()

        output_vars = pd.DataFrame(
            columns=['Country', 'Measure', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14'])
        
        # output_map = pd.DataFrame(
        #     columns=['Country', 'Count', 'Sex', 'Covid_infected', 'Age'])

        # For each variable calculate averages by country and date
        for msr in measures:
            total_all_t1 = 0
            count_all_t1 = 0
            total_all_t2 = 0
            count_all_t2 = 0
            total_all_t3 = 0
            count_all_t3 = 0
            total_all_t4 = 0
            count_all_t4 = 0
            total_all_t5 = 0
            count_all_t5 = 0
            total_all_t6 = 0
            count_all_t6 = 0
            total_all_t7 = 0
            count_all_t7 = 0
            total_all_t8 = 0
            count_all_t8 = 0
            total_all_t9 = 0
            count_all_t9 = 0
            total_all_t10 = 0
            count_all_t10 = 0
            total_all_t11 = 0
            count_all_t11 = 0
            total_all_t12 = 0
            count_all_t12 = 0
            total_all_t13 = 0
            count_all_t13 = 0
            total_all_t14 = 0
            count_all_t14 = 0
            for country in countries: 
                t1_total = 0
                t1_count = 0
                t2_total = 0
                t2_count = 0
                t3_total = 0
                t3_count = 0
                t4_total = 0
                t4_count = 0
                t5_total = 0
                t5_count = 0
                t6_total = 0
                t6_count = 0
                t7_total = 0
                t7_count = 0
                t8_total = 0
                t8_count = 0
                t9_total = 0
                t9_count = 0
                t10_total = 0
                t10_count = 0
                t11_total = 0
                t11_count = 0
                t12_total = 0
                t12_count = 0
                t13_total = 0
                t13_count = 0
                t14_total = 0
                t14_count = 0
                avg1 = np.nan
                avg2 = np.nan
                avg3 = np.nan
                avg4 = np.nan
                avg5 = np.nan
                avg6 = np.nan
                avg7 = np.nan
                avg8 = np.nan
                avg9 = np.nan
                avg10 = np.nan
                avg11 = np.nan
                avg12 = np.nan
                avg13 = np.nan
                avg14 = np.nan

                for i in range(len(loaded)):
                    val = float(loaded.at[i, msr])
                   
                    if country == loaded.at[i, "CurrentCountry"] and math.isnan(val) == False:
                        if loaded.at[i, "Date"] == "06/03/2020":
                            t1_total += val
                            t1_count += 1
                        elif  loaded.at[i, "Date"] == "14/03/2020":
                            t2_total += val
                            t2_count += 1
                        elif  loaded.at[i, "Date"] == "24/03/2020":
                            t3_total += val
                            t3_count += 1
                        elif loaded.at[i, "Date"] == "03/04/2020":
                            t4_total += val
                            t4_count += 1
                        elif  loaded.at[i, "Date"] == "17/04/2020":
                            t5_total += val
                            t5_count += 1
                        elif  loaded.at[i, "Date"] == "02/05/2020":
                            t6_total += val
                            t6_count += 1
                        elif  loaded.at[i, "Date"] == "16/05/2020":
                            t7_total += val
                            t7_count += 1
                        elif  loaded.at[i, "Date"] == "30/05/2020":
                            t8_total += val
                            t8_count += 1
                        elif  loaded.at[i, "Date"] == "13/06/2020":
                            t9_total += val
                            t9_count += 1
                        elif  loaded.at[i, "Date"] == "27/06/2020":
                            t10_total += val
                            t10_count += 1
                        elif  loaded.at[i, "Date"] == "11/07/2020":
                            t11_total += val
                            t11_count += 1
                        elif  loaded.at[i, "Date"] == "25/07/2020":
                            t12_total += val
                            t12_count += 1
                        elif  loaded.at[i, "Date"] == "08/08/2020":
                            t13_total += val
                            t13_count += 1
                        elif  loaded.at[i, "Date"] == "22/08/2020":
                            t14_total += val
                            t14_count += 1
                
                if t1_count > 0:
                    avg1 = t1_total/t1_count
                
                if t2_count > 0:    
                    avg2 = t2_total/t2_count
                
                if t3_count > 0:
                    avg3 = t3_total/t3_count
                
                if t4_count > 0:
                    avg4 = t4_total/t4_count
                
                if t5_count > 0:
                    avg5 = t5_total/t5_count
                
                if t6_count > 0:
                    avg6 = t6_total/t6_count
                
                if t7_count > 0:
                    avg7 = t7_total/t7_count
                
                if t8_count > 0:
                    avg8 = t8_total/t8_count
                
                if t9_count > 0:
                    avg9 = t9_total/t9_count
                
                if t10_count > 0:
                    avg10 = t10_total/t10_count
                
                if t11_count > 0:
                    avg11 = t11_total/t11_count
                
                if t12_count > 0:
                    avg12 = t12_total/t12_count
                
                if t13_count > 0:
                    avg13 = t13_total/t13_count
                
                if t14_count > 0:
                    avg14 = t14_total/t14_count
                
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 't1': avg1, 't2': avg2, 't3': avg3, 't4': avg4, 't5': avg5,
                                't6': avg6, 't7': avg7, 't8': avg8, 't9': avg9, 't10': avg10, 't11': avg11, 't12': avg12, 't13': avg13, 't14': avg14}, ignore_index=True)

                total_all_t1 += t1_total
                count_all_t1 += t1_count
                total_all_t2 += t2_total
                count_all_t2 += t2_count
                total_all_t3 += t3_total
                count_all_t3 += t3_count
                total_all_t4 += t4_total
                count_all_t4 += t4_count
                total_all_t5 += t5_total
                count_all_t5 += t5_count
                total_all_t6 += t6_total
                count_all_t6 += t6_count
                total_all_t7 += t7_total
                count_all_t7 += t7_count
                total_all_t8 += t8_total
                count_all_t8 += t8_count
                total_all_t9 += t9_total
                count_all_t9 += t9_count
                total_all_t10 += t10_total
                count_all_t10 += t10_count
                total_all_t11 += t11_total
                count_all_t11 += t11_count
                total_all_t12 += t12_total
                count_all_t12 += t12_count
                total_all_t13 += t13_total
                count_all_t13 += t13_count
                total_all_t14 += t14_total
                count_all_t14 += t14_count
                
            tot_avg1 = total_all_t1/count_all_t1
            tot_avg2 = total_all_t2/count_all_t2
            tot_avg3 = total_all_t3/count_all_t3
            tot_avg4 = total_all_t4/count_all_t4
            tot_avg5 = total_all_t5/count_all_t5
            tot_avg6 = total_all_t6/count_all_t6
            tot_avg7 = total_all_t7/count_all_t7
            tot_avg8 = total_all_t8/count_all_t8
            tot_avg9 = total_all_t9/count_all_t9
            tot_avg10 = total_all_t10/count_all_t10
            tot_avg11 = total_all_t11/count_all_t11
            tot_avg12 = total_all_t12/count_all_t12
            tot_avg13 = total_all_t13/count_all_t13
            tot_avg14 = total_all_t14/count_all_t14

            output_vars = output_vars.append({'Country': "World", 'Measure': msr, 't1': tot_avg1, 't2': tot_avg2, 't3': tot_avg3, 't4': tot_avg4, 't5': tot_avg5,
                                    't6': tot_avg6, 't7': tot_avg7, 't8': tot_avg8, 't9': tot_avg9, 't10': tot_avg10, 't11': tot_avg11, 't12': tot_avg12, 't13': tot_avg13, 't14': tot_avg14}, ignore_index=True)
            click.echo("processing for " + msr + " completed")
        
        output_vars = output_vars.reset_index()
        output_vars.to_csv(r'output_vars.csv', index=None, header=True)
        click.echo("output_vars.csv exported")

    elif processtype == "cclab-dashboard-glo-detail":

        loaded["Age"] = pd.to_numeric(loaded["Age"])
        loaded["Sex"] = pd.to_numeric(loaded["Sex"])
        loaded["Preexisting"] = pd.to_numeric(loaded["Preexisting"])
        loaded["t1"] = pd.to_numeric(loaded["t1"])
        loaded["t2"] = pd.to_numeric(loaded["t2"])
        loaded["t3"] = pd.to_numeric(loaded["t3"])
        loaded["t4"] = pd.to_numeric(loaded["t4"])
        loaded["t5"] = pd.to_numeric(loaded["t5"])
        loaded["t6"] = pd.to_numeric(loaded["t6"])
        loaded["t7"] = pd.to_numeric(loaded["t7"])
        loaded["t8"] = pd.to_numeric(loaded["t8"])
        loaded["t9"] = pd.to_numeric(loaded["t9"])
        loaded["t10"] = pd.to_numeric(loaded["t10"])
        loaded["t11"] = pd.to_numeric(loaded["t11"])
        loaded["t12"] = pd.to_numeric(loaded["t12"])
        loaded["t13"] = pd.to_numeric(loaded["t13"])
        loaded["t14"] = pd.to_numeric(loaded["t14"])

        measures = ["PerceptionsRisk", "PFIHumanitySharedFate", "PFIHumanityEmpathy", "PFINeighEmpathy", 
        "PFINeighSharedFate", "NBTNeigh", "WillingnessNeigh", "NBTHumanity", "WillingnessHumanity"]

        # get countries
        countries = loaded.CurrentCountry.unique()

        output_vars = pd.DataFrame(
            columns=['Country', 'Measure', 'Category', 'Subcategory', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14'])

        # For each variable calculate averages by state and date
        for msr in measures:
            measureSubset = loaded[loaded.Measure == msr]
            agesubset1 = measureSubset[measureSubset.Age.isin([18, 19, 20, 21])]
            agesubset2 = measureSubset[measureSubset.Age.isin([22, 23, 24, 25])]
            agesubset3 = measureSubset[measureSubset.Age.isin([26, 27, 28, 29, 30, 31, 32, 33, 34, 35])]
            agesubset4 = measureSubset[measureSubset.Age.isin([36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])]
            agesubset5 = measureSubset[measureSubset.Age.isin([51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80])]

            maleSubset =  measureSubset[measureSubset.Sex == 1]
            femaleSubset =  measureSubset[measureSubset.Sex == 2]
            otherSubset =  measureSubset[measureSubset.Sex == 3]

            preexistingYesSubset = measureSubset[measureSubset.Preexisting == 1]
            preexistingNoSubset = measureSubset[measureSubset.Preexisting == 2]

            age1Avgt1 = agesubset1.t1.mean()
            age1Avgt2 = agesubset1.t2.mean()
            age1Avgt3 = agesubset1.t3.mean()
            age1Avgt4 = agesubset1.t4.mean()
            age1Avgt5 = agesubset1.t5.mean()
            age1Avgt6 = agesubset1.t6.mean()
            age1Avgt7 = agesubset1.t7.mean()
            age1Avgt8 = agesubset1.t8.mean()
            age1Avgt9 = agesubset1.t9.mean()
            age1Avgt10 = agesubset1.t10.mean()
            age1Avgt11 = agesubset1.t11.mean()
            age1Avgt12 = agesubset1.t12.mean()
            age1Avgt13 = agesubset1.t13.mean()
            age1Avgt14 = agesubset1.t14.mean()

            age2Avgt1 = agesubset2.t1.mean()
            age2Avgt2 = agesubset2.t2.mean()
            age2Avgt3 = agesubset2.t3.mean()
            age2Avgt4 = agesubset2.t4.mean()
            age2Avgt5 = agesubset2.t5.mean()
            age2Avgt6 = agesubset2.t6.mean()
            age2Avgt7 = agesubset2.t7.mean()
            age2Avgt8 = agesubset2.t8.mean()
            age2Avgt9 = agesubset2.t9.mean()
            age2Avgt10 = agesubset2.t10.mean()
            age2Avgt11 = agesubset2.t11.mean()
            age2Avgt12 = agesubset2.t12.mean()
            age2Avgt13 = agesubset2.t13.mean()
            age2Avgt14 = agesubset2.t14.mean()

            age3Avgt1 = agesubset3.t1.mean()
            age3Avgt2 = agesubset3.t2.mean()
            age3Avgt3 = agesubset3.t3.mean()
            age3Avgt4 = agesubset3.t4.mean()
            age3Avgt5 = agesubset3.t5.mean()
            age3Avgt6 = agesubset3.t6.mean()
            age3Avgt7 = agesubset3.t7.mean()
            age3Avgt8 = agesubset3.t8.mean()
            age3Avgt9 = agesubset3.t9.mean()
            age3Avgt10 = agesubset3.t10.mean()
            age3Avgt11 = agesubset3.t11.mean()
            age3Avgt12 = agesubset3.t12.mean()
            age3Avgt13 = agesubset3.t13.mean()
            age3Avgt14 = agesubset3.t14.mean()

            age4Avgt1 = agesubset4.t1.mean()
            age4Avgt2 = agesubset4.t2.mean()
            age4Avgt3 = agesubset4.t3.mean()
            age4Avgt4 = agesubset4.t4.mean()
            age4Avgt5 = agesubset4.t5.mean()
            age4Avgt6 = agesubset4.t6.mean()
            age4Avgt7 = agesubset4.t7.mean()
            age4Avgt8 = agesubset4.t8.mean()
            age4Avgt9 = agesubset4.t9.mean()
            age4Avgt10 = agesubset4.t10.mean()
            age4Avgt11 = agesubset4.t11.mean()
            age4Avgt12 = agesubset4.t12.mean()
            age4Avgt13 = agesubset4.t13.mean()
            age4Avgt14 = agesubset4.t14.mean()

            age5Avgt1 = agesubset5.t1.mean()
            age5Avgt2 = agesubset5.t2.mean()
            age5Avgt3 = agesubset5.t3.mean()
            age5Avgt4 = agesubset5.t4.mean()
            age5Avgt5 = agesubset5.t5.mean()
            age5Avgt6 = agesubset5.t6.mean()
            age5Avgt7 = agesubset5.t7.mean()
            age5Avgt8 = agesubset5.t8.mean()
            age5Avgt9 = agesubset5.t9.mean()
            age5Avgt10 = agesubset5.t10.mean()
            age5Avgt11 = agesubset5.t11.mean()
            age5Avgt12 = agesubset5.t12.mean()
            age5Avgt13 = agesubset5.t13.mean()
            age5Avgt14 = agesubset5.t14.mean()

            maleAvgt1 = maleSubset.t1.mean()
            maleAvgt2 = maleSubset.t2.mean()
            maleAvgt3 = maleSubset.t3.mean()
            maleAvgt4 = maleSubset.t4.mean()
            maleAvgt5 = maleSubset.t5.mean()
            maleAvgt6 = maleSubset.t6.mean()
            maleAvgt7 = maleSubset.t7.mean()
            maleAvgt8 = maleSubset.t8.mean()
            maleAvgt9 = maleSubset.t9.mean()
            maleAvgt10 = maleSubset.t10.mean()
            maleAvgt11 = maleSubset.t11.mean()
            maleAvgt12 = maleSubset.t12.mean()
            maleAvgt13 = maleSubset.t13.mean()
            maleAvgt14 = maleSubset.t14.mean()

            femaleAvgt1 = femaleSubset.t1.mean()
            femaleAvgt2 = femaleSubset.t2.mean()
            femaleAvgt3 = femaleSubset.t3.mean()
            femaleAvgt4 = femaleSubset.t4.mean()
            femaleAvgt5 = femaleSubset.t5.mean()
            femaleAvgt6 = femaleSubset.t6.mean()
            femaleAvgt7 = femaleSubset.t7.mean()
            femaleAvgt8 = femaleSubset.t8.mean()
            femaleAvgt9 = femaleSubset.t9.mean()
            femaleAvgt10 = femaleSubset.t10.mean()
            femaleAvgt11 = femaleSubset.t11.mean()
            femaleAvgt12 = femaleSubset.t12.mean()
            femaleAvgt13 = femaleSubset.t13.mean()
            femaleAvgt14 = femaleSubset.t14.mean()

            otherAvgt1 = otherSubset.t1.mean()
            otherAvgt2 = otherSubset.t2.mean()
            otherAvgt3 = otherSubset.t3.mean()
            otherAvgt4 = otherSubset.t4.mean()
            otherAvgt5 = otherSubset.t5.mean()
            otherAvgt6 = otherSubset.t6.mean()
            otherAvgt7 = otherSubset.t7.mean()
            otherAvgt8 = otherSubset.t8.mean()
            otherAvgt9 = otherSubset.t9.mean()
            otherAvgt10 = otherSubset.t10.mean()
            otherAvgt11 = otherSubset.t11.mean()
            otherAvgt12 = otherSubset.t12.mean()
            otherAvgt13 = otherSubset.t13.mean()
            otherAvgt14 = otherSubset.t14.mean()

            preexistingYesAvgt1 = preexistingYesSubset.t1.mean()
            preexistingYesAvgt2 = preexistingYesSubset.t2.mean()
            preexistingYesAvgt3 = preexistingYesSubset.t3.mean()
            preexistingYesAvgt4 = preexistingYesSubset.t4.mean()
            preexistingYesAvgt5 = preexistingYesSubset.t5.mean()
            preexistingYesAvgt6 = preexistingYesSubset.t6.mean()
            preexistingYesAvgt7 = preexistingYesSubset.t7.mean()
            preexistingYesAvgt8 = preexistingYesSubset.t8.mean()
            preexistingYesAvgt9 = preexistingYesSubset.t9.mean()
            preexistingYesAvgt10 = preexistingYesSubset.t10.mean()
            preexistingYesAvgt11 = preexistingYesSubset.t11.mean()
            preexistingYesAvgt12 = preexistingYesSubset.t12.mean()
            preexistingYesAvgt13 = preexistingYesSubset.t13.mean()
            preexistingYesAvgt14 = preexistingYesSubset.t14.mean()

            preexistingNoAvgt1 = preexistingNoSubset.t1.mean()    
            preexistingNoAvgt2 = preexistingNoSubset.t2.mean()    
            preexistingNoAvgt3 = preexistingNoSubset.t3.mean()    
            preexistingNoAvgt4 = preexistingNoSubset.t4.mean()    
            preexistingNoAvgt5 = preexistingNoSubset.t5.mean()    
            preexistingNoAvgt6 = preexistingNoSubset.t6.mean()    
            preexistingNoAvgt7 = preexistingNoSubset.t7.mean()    
            preexistingNoAvgt8 = preexistingNoSubset.t8.mean()    
            preexistingNoAvgt9 = preexistingNoSubset.t9.mean()    
            preexistingNoAvgt10 = preexistingNoSubset.t10.mean()    
            preexistingNoAvgt11 = preexistingNoSubset.t11.mean()    
            preexistingNoAvgt12 = preexistingNoSubset.t12.mean()
            preexistingNoAvgt13 = preexistingNoSubset.t13.mean()
            preexistingNoAvgt14 = preexistingNoSubset.t14.mean()  

            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Age', 'Subcategory': '18-21', 't1': age1Avgt1, 't2': age1Avgt2, 't3': age1Avgt3, 't4': age1Avgt4, 't5': age1Avgt5,
                            't6': age1Avgt6, 't7': age1Avgt7, 't8': age1Avgt8, 't9': age1Avgt9, 't10': age1Avgt10, 't11': age1Avgt11, 't12': age1Avgt12, 't13': age1Avgt13, 't14': age1Avgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Age', 'Subcategory': '22-25', 't1': age2Avgt1, 't2': age2Avgt2, 't3': age2Avgt3, 't4': age2Avgt4, 't5': age2Avgt5,
                            't6': age2Avgt6, 't7': age2Avgt7, 't8': age2Avgt8, 't9': age2Avgt9, 't10': age2Avgt10, 't11': age2Avgt11, 't12': age2Avgt12, 't13': age2Avgt13, 't14': age2Avgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Age', 'Subcategory': '26-35', 't1': age3Avgt1, 't2': age3Avgt2, 't3': age3Avgt3, 't4': age3Avgt4, 't5': age3Avgt5,
                            't6': age3Avgt6, 't7': age3Avgt7, 't8': age3Avgt8, 't9': age3Avgt9, 't10': age3Avgt10, 't11': age3Avgt11, 't12': age3Avgt12, 't13': age3Avgt13, 't14': age3Avgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Age', 'Subcategory': '36-50', 't1': age4Avgt1, 't2': age4Avgt2, 't3': age4Avgt3, 't4': age4Avgt4, 't5': age4Avgt5,
                            't6': age4Avgt6, 't7': age4Avgt7, 't8': age4Avgt8, 't9': age4Avgt9, 't10': age4Avgt10, 't11': age4Avgt11, 't12': age4Avgt12, 't13': age4Avgt13, 't14': age4Avgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Age', 'Subcategory': '51-80', 't1': age5Avgt1, 't2': age5Avgt2, 't3': age5Avgt3, 't4': age5Avgt4, 't5': age5Avgt5,
                            't6': age5Avgt6, 't7': age5Avgt7, 't8': age5Avgt8, 't9': age5Avgt9, 't10': age5Avgt10, 't11': age5Avgt11, 't12': age5Avgt12, 't13': age5Avgt13, 't14': age5Avgt14}, ignore_index=True)

            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Male', 't1': maleAvgt1, 't2': maleAvgt2, 't3': maleAvgt3, 't4': maleAvgt4, 't5': maleAvgt5,
                            't6': maleAvgt6, 't7': maleAvgt7, 't8': maleAvgt8, 't9': maleAvgt9, 't10': maleAvgt10, 't11': maleAvgt11, 't12': maleAvgt12, 't13': maleAvgt13, 't14': maleAvgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Female', 't1': femaleAvgt1, 't2': femaleAvgt2, 't3': femaleAvgt3, 't4': femaleAvgt4, 't5': femaleAvgt5,
                            't6': femaleAvgt6, 't7': femaleAvgt7, 't8': femaleAvgt8, 't9': femaleAvgt9, 't10': femaleAvgt10, 't11': femaleAvgt11, 't12': femaleAvgt12, 't13': femaleAvgt13, 't14': femaleAvgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Other', 't1': otherAvgt1, 't2': otherAvgt2, 't3': otherAvgt3, 't4': otherAvgt4, 't5': otherAvgt5,
                            't6': otherAvgt6, 't7': otherAvgt7, 't8': otherAvgt8, 't9': otherAvgt9, 't10': otherAvgt10, 't11': otherAvgt11, 't12': otherAvgt12, 't13': otherAvgt13, 't14': otherAvgt14}, ignore_index=True)
        
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'preexisting', 'Subcategory': 'preexisting_yes', 't1': preexistingYesAvgt1, 't2': preexistingYesAvgt2, 't3': preexistingYesAvgt3, 't4': preexistingYesAvgt4, 't5': preexistingYesAvgt5,
                            't6': preexistingYesAvgt6, 't7': preexistingYesAvgt7, 't8': preexistingYesAvgt8, 't9': preexistingYesAvgt9, 't10': preexistingYesAvgt10, 't11': preexistingYesAvgt11, 't12': preexistingYesAvgt12, 't13': preexistingYesAvgt13, 't14': preexistingYesAvgt14}, ignore_index=True)
            output_vars = output_vars.append({'Country': 'World', 'Measure': msr, 'Category': 'preexisting', 'Subcategory': 'preexisting_no', 't1': preexistingNoAvgt1, 't2': preexistingNoAvgt2, 't3': preexistingNoAvgt3, 't4': preexistingNoAvgt4, 't5': preexistingNoAvgt5,
                            't6': preexistingNoAvgt6, 't7': preexistingNoAvgt7, 't8': preexistingNoAvgt8, 't9': preexistingNoAvgt9, 't10': preexistingNoAvgt10, 't11': preexistingNoAvgt11, 't12': preexistingNoAvgt12, 't13': preexistingNoAvgt13, 't14': preexistingNoAvgt14}, ignore_index=True)

            for country in countries:
                countryAgesubset1 = agesubset1[agesubset1.CurrentCountry == country]
                countryAgesubset2 = agesubset2[agesubset2.CurrentCountry == country]
                countryAgesubset3 = agesubset3[agesubset3.CurrentCountry == country]
                countryAgesubset4 = agesubset4[agesubset4.CurrentCountry == country]
                countryAgesubset5 = agesubset5[agesubset5.CurrentCountry == country]

                countryMaleSubset = maleSubset[maleSubset.CurrentCountry == country]
                countryFemaleSubset = femaleSubset[femaleSubset.CurrentCountry == country]
                countryOtherSubset = otherSubset[otherSubset.CurrentCountry == country]

                countryPreexistingYesSubset = preexistingYesSubset[preexistingYesSubset.CurrentCountry == country]
                countryPreexistingNoSubset = preexistingNoSubset[preexistingNoSubset.CurrentCountry == country]
               
                stateAge1Avgt1 = countryAgesubset1.t1.mean()
                stateAge1Avgt2 = countryAgesubset1.t2.mean()
                stateAge1Avgt3 = countryAgesubset1.t3.mean()
                stateAge1Avgt4 = countryAgesubset1.t4.mean()
                stateAge1Avgt5 = countryAgesubset1.t5.mean()
                stateAge1Avgt6 = countryAgesubset1.t6.mean()
                stateAge1Avgt7 = countryAgesubset1.t7.mean()
                stateAge1Avgt8 = countryAgesubset1.t8.mean()
                stateAge1Avgt9 = countryAgesubset1.t9.mean()
                stateAge1Avgt10 = countryAgesubset1.t10.mean()
                stateAge1Avgt11 = countryAgesubset1.t11.mean()
                stateAge1Avgt12 = countryAgesubset1.t12.mean()
                stateAge1Avgt13 = countryAgesubset1.t13.mean()
                stateAge1Avgt14 = countryAgesubset1.t14.mean()

                stateAge2Avgt1 = countryAgesubset2.t1.mean()
                stateAge2Avgt2 = countryAgesubset2.t2.mean()
                stateAge2Avgt3 = countryAgesubset2.t3.mean()
                stateAge2Avgt4 = countryAgesubset2.t4.mean()
                stateAge2Avgt5 = countryAgesubset2.t5.mean()
                stateAge2Avgt6 = countryAgesubset2.t6.mean()
                stateAge2Avgt7 = countryAgesubset2.t7.mean()
                stateAge2Avgt8 = countryAgesubset2.t8.mean()
                stateAge2Avgt9 = countryAgesubset2.t9.mean()
                stateAge2Avgt10 = countryAgesubset2.t10.mean()
                stateAge2Avgt11 = countryAgesubset2.t11.mean()
                stateAge2Avgt12 = countryAgesubset2.t12.mean()
                stateAge2Avgt13 = countryAgesubset2.t13.mean()
                stateAge2Avgt14 = countryAgesubset2.t14.mean()

                stateAge3Avgt1 = countryAgesubset3.t1.mean()
                stateAge3Avgt2 = countryAgesubset3.t2.mean()
                stateAge3Avgt3 = countryAgesubset3.t3.mean()
                stateAge3Avgt4 = countryAgesubset3.t4.mean()
                stateAge3Avgt5 = countryAgesubset3.t5.mean()
                stateAge3Avgt6 = countryAgesubset3.t6.mean()
                stateAge3Avgt7 = countryAgesubset3.t7.mean()
                stateAge3Avgt8 = countryAgesubset3.t8.mean()
                stateAge3Avgt9 = countryAgesubset3.t9.mean()
                stateAge3Avgt10 = countryAgesubset3.t10.mean()
                stateAge3Avgt11 = countryAgesubset3.t11.mean()
                stateAge3Avgt12 = countryAgesubset3.t12.mean()
                stateAge3Avgt13 = countryAgesubset3.t13.mean()
                stateAge3Avgt14 = countryAgesubset3.t14.mean()

                stateAge4Avgt1 = countryAgesubset4.t1.mean()
                stateAge4Avgt2 = countryAgesubset4.t2.mean()
                stateAge4Avgt3 = countryAgesubset4.t3.mean()
                stateAge4Avgt4 = countryAgesubset4.t4.mean()
                stateAge4Avgt5 = countryAgesubset4.t5.mean()
                stateAge4Avgt6 = countryAgesubset4.t6.mean()
                stateAge4Avgt7 = countryAgesubset4.t7.mean()
                stateAge4Avgt8 = countryAgesubset4.t8.mean()
                stateAge4Avgt9 = countryAgesubset4.t9.mean()
                stateAge4Avgt10 = countryAgesubset4.t10.mean()
                stateAge4Avgt11 = countryAgesubset4.t11.mean()
                stateAge4Avgt12 = countryAgesubset4.t12.mean()
                stateAge4Avgt13 = countryAgesubset4.t13.mean()
                stateAge4Avgt14 = countryAgesubset4.t14.mean()

                stateAge5Avgt1 = countryAgesubset5.t1.mean()
                stateAge5Avgt2 = countryAgesubset5.t2.mean()
                stateAge5Avgt3 = countryAgesubset5.t3.mean()
                stateAge5Avgt4 = countryAgesubset5.t4.mean()
                stateAge5Avgt5 = countryAgesubset5.t5.mean()
                stateAge5Avgt6 = countryAgesubset5.t6.mean()
                stateAge5Avgt7 = countryAgesubset5.t7.mean()
                stateAge5Avgt8 = countryAgesubset5.t8.mean()
                stateAge5Avgt9 = countryAgesubset5.t9.mean()
                stateAge5Avgt10 = countryAgesubset5.t10.mean()
                stateAge5Avgt11 = countryAgesubset5.t11.mean()
                stateAge5Avgt12 = countryAgesubset5.t12.mean()
                stateAge5Avgt13 = countryAgesubset5.t13.mean()
                stateAge5Avgt14 = countryAgesubset5.t14.mean()

                stateMaleAvgt1 = countryMaleSubset.t1.mean()
                stateMaleAvgt2 = countryMaleSubset.t2.mean()
                stateMaleAvgt3 = countryMaleSubset.t3.mean()
                stateMaleAvgt4 = countryMaleSubset.t4.mean()
                stateMaleAvgt5 = countryMaleSubset.t5.mean()
                stateMaleAvgt6 = countryMaleSubset.t6.mean()
                stateMaleAvgt7 = countryMaleSubset.t7.mean()
                stateMaleAvgt8 = countryMaleSubset.t8.mean()
                stateMaleAvgt9 = countryMaleSubset.t9.mean()
                stateMaleAvgt10 = countryMaleSubset.t10.mean()
                stateMaleAvgt11 = countryMaleSubset.t11.mean()
                stateMaleAvgt12 = countryMaleSubset.t12.mean()
                stateMaleAvgt13 = countryMaleSubset.t13.mean()
                stateMaleAvgt14 = countryMaleSubset.t14.mean()

                stateFemaleAvgt1 = countryFemaleSubset.t1.mean()
                stateFemaleAvgt2 = countryFemaleSubset.t2.mean()
                stateFemaleAvgt3 = countryFemaleSubset.t3.mean()
                stateFemaleAvgt4 = countryFemaleSubset.t4.mean()
                stateFemaleAvgt5 = countryFemaleSubset.t5.mean()
                stateFemaleAvgt6 = countryFemaleSubset.t6.mean()
                stateFemaleAvgt7 = countryFemaleSubset.t7.mean()
                stateFemaleAvgt8 = countryFemaleSubset.t8.mean()
                stateFemaleAvgt9 = countryFemaleSubset.t9.mean()
                stateFemaleAvgt10 = countryFemaleSubset.t10.mean()
                stateFemaleAvgt11 = countryFemaleSubset.t11.mean()
                stateFemaleAvgt12 = countryFemaleSubset.t12.mean()
                stateFemaleAvgt13 = countryFemaleSubset.t13.mean()
                stateFemaleAvgt14 = countryFemaleSubset.t14.mean()

                stateOtherAvgt1 = countryOtherSubset.t1.mean()
                stateOtherAvgt2 = countryOtherSubset.t2.mean()
                stateOtherAvgt3 = countryOtherSubset.t3.mean()
                stateOtherAvgt4 = countryOtherSubset.t4.mean()
                stateOtherAvgt5 = countryOtherSubset.t5.mean()
                stateOtherAvgt6 = countryOtherSubset.t6.mean()
                stateOtherAvgt7 = countryOtherSubset.t7.mean()
                stateOtherAvgt8 = countryOtherSubset.t8.mean()
                stateOtherAvgt9 = countryOtherSubset.t9.mean()
                stateOtherAvgt10 = countryOtherSubset.t10.mean()
                stateOtherAvgt11 = countryOtherSubset.t11.mean()
                stateOtherAvgt12 = countryOtherSubset.t12.mean()
                stateOtherAvgt13 = countryOtherSubset.t13.mean()
                stateOtherAvgt14 = countryOtherSubset.t14.mean()

                countryPreexistingYesAvgt1 = countryPreexistingYesSubset.t1.mean()
                countryPreexistingYesAvgt2 = countryPreexistingYesSubset.t2.mean()
                countryPreexistingYesAvgt3 = countryPreexistingYesSubset.t3.mean()
                countryPreexistingYesAvgt4 = countryPreexistingYesSubset.t4.mean()
                countryPreexistingYesAvgt5 = countryPreexistingYesSubset.t5.mean()
                countryPreexistingYesAvgt6 = countryPreexistingYesSubset.t6.mean()
                countryPreexistingYesAvgt7 = countryPreexistingYesSubset.t7.mean()
                countryPreexistingYesAvgt8 = countryPreexistingYesSubset.t8.mean()
                countryPreexistingYesAvgt9 = countryPreexistingYesSubset.t9.mean()
                countryPreexistingYesAvgt10 = countryPreexistingYesSubset.t10.mean()
                countryPreexistingYesAvgt11 = countryPreexistingYesSubset.t11.mean()
                countryPreexistingYesAvgt12 = countryPreexistingYesSubset.t12.mean()
                countryPreexistingYesAvgt13 = countryPreexistingYesSubset.t13.mean()
                countryPreexistingYesAvgt14 = countryPreexistingYesSubset.t14.mean()

                countryPreexistingNoAvgt1 = countryPreexistingNoSubset.t1.mean()
                countryPreexistingNoAvgt2 = countryPreexistingNoSubset.t2.mean()
                countryPreexistingNoAvgt3 = countryPreexistingNoSubset.t3.mean()
                countryPreexistingNoAvgt4 = countryPreexistingNoSubset.t4.mean()
                countryPreexistingNoAvgt5 = countryPreexistingNoSubset.t5.mean()
                countryPreexistingNoAvgt6 = countryPreexistingNoSubset.t6.mean()
                countryPreexistingNoAvgt7 = countryPreexistingNoSubset.t7.mean()
                countryPreexistingNoAvgt8 = countryPreexistingNoSubset.t8.mean()
                countryPreexistingNoAvgt9 = countryPreexistingNoSubset.t9.mean()
                countryPreexistingNoAvgt10 = countryPreexistingNoSubset.t10.mean()
                countryPreexistingNoAvgt11 = countryPreexistingNoSubset.t11.mean()
                countryPreexistingNoAvgt12 = countryPreexistingNoSubset.t12.mean()
                countryPreexistingNoAvgt13 = countryPreexistingNoSubset.t13.mean()
                countryPreexistingNoAvgt14 = countryPreexistingNoSubset.t14.mean()

                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Age', 'Subcategory': '18-21', 't1': stateAge1Avgt1, 't2': stateAge1Avgt2, 't3': stateAge1Avgt3, 't4': stateAge1Avgt4, 't5': stateAge1Avgt5,
                                't6': stateAge1Avgt6, 't7': stateAge1Avgt7, 't8': stateAge1Avgt8, 't9': stateAge1Avgt9, 't10': stateAge1Avgt10, 't11': stateAge1Avgt11, 't12': stateAge1Avgt12, 't13': stateAge1Avgt13, 't14': stateAge1Avgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Age', 'Subcategory': '22-25', 't1': stateAge2Avgt1, 't2': stateAge2Avgt2, 't3': stateAge2Avgt3, 't4': stateAge2Avgt4, 't5': stateAge2Avgt5,
                                't6': stateAge2Avgt6, 't7': stateAge2Avgt7, 't8': stateAge2Avgt8, 't9': stateAge2Avgt9, 't10': stateAge2Avgt10, 't11': stateAge2Avgt11, 't12': stateAge2Avgt12, 't13': stateAge2Avgt13, 't14': stateAge2Avgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Age', 'Subcategory': '26-35', 't1': stateAge3Avgt1, 't2': stateAge3Avgt2, 't3': stateAge3Avgt3, 't4': stateAge3Avgt4, 't5': stateAge3Avgt5,
                                't6': stateAge3Avgt6, 't7': stateAge3Avgt7, 't8': stateAge3Avgt8, 't9': stateAge3Avgt9, 't10': stateAge3Avgt10, 't11': stateAge3Avgt11, 't12': stateAge3Avgt12, 't13': stateAge3Avgt13, 't14': stateAge3Avgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Age', 'Subcategory': '36-50', 't1': stateAge4Avgt1, 't2': stateAge4Avgt2, 't3': stateAge4Avgt3, 't4': stateAge4Avgt4, 't5': stateAge4Avgt5,
                                't6': stateAge4Avgt6, 't7': stateAge4Avgt7, 't8': stateAge4Avgt8, 't9': stateAge4Avgt9, 't10': stateAge4Avgt10, 't11': stateAge4Avgt11, 't12': stateAge4Avgt12, 't13': stateAge4Avgt13, 't14': stateAge4Avgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Age', 'Subcategory': '51-80', 't1': stateAge5Avgt1, 't2': stateAge5Avgt2, 't3': stateAge5Avgt3, 't4': stateAge5Avgt4, 't5': stateAge5Avgt5,
                                't6': stateAge5Avgt6, 't7': stateAge5Avgt7, 't8': stateAge5Avgt8, 't9': stateAge5Avgt9, 't10': stateAge5Avgt10, 't11': stateAge5Avgt11, 't12': stateAge5Avgt12, 't13': stateAge5Avgt13, 't14': stateAge5Avgt14}, ignore_index=True)
               
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Male', 't1': stateMaleAvgt1, 't2': stateMaleAvgt2, 't3': stateMaleAvgt3, 't4': stateMaleAvgt4, 't5': stateMaleAvgt5,
                                't6': stateMaleAvgt6, 't7': stateMaleAvgt7, 't8': stateMaleAvgt8, 't9': stateMaleAvgt9, 't10': stateMaleAvgt10, 't11': stateMaleAvgt11, 't12': stateMaleAvgt12, 't13': stateMaleAvgt13, 't14': stateMaleAvgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Female', 't1': stateFemaleAvgt1, 't2': stateFemaleAvgt2, 't3': stateFemaleAvgt3, 't4': stateFemaleAvgt4, 't5': stateFemaleAvgt5,
                                't6': stateFemaleAvgt6, 't7': stateFemaleAvgt7, 't8': stateFemaleAvgt8, 't9': stateFemaleAvgt9, 't10': stateFemaleAvgt10, 't11': stateFemaleAvgt11, 't12': stateFemaleAvgt12, 't13': stateFemaleAvgt13, 't14': stateFemaleAvgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Sex', 'Subcategory': 'Other', 't1': stateOtherAvgt1, 't2': stateOtherAvgt2, 't3': stateOtherAvgt3, 't4': stateOtherAvgt4, 't5': stateOtherAvgt5,
                                't6': stateOtherAvgt6, 't7': stateOtherAvgt7, 't8': stateOtherAvgt8, 't9': stateOtherAvgt9, 't10': stateOtherAvgt10, 't11': stateOtherAvgt11, 't12': stateOtherAvgt12, 't13': stateOtherAvgt13, 't14': stateOtherAvgt14}, ignore_index=True)

                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Preexisting', 'Subcategory': 'preexisting_yes', 't1': countryPreexistingYesAvgt1, 't2': countryPreexistingYesAvgt2, 't3': countryPreexistingYesAvgt3, 't4': countryPreexistingYesAvgt4, 't5': countryPreexistingYesAvgt5,
                                't6': countryPreexistingYesAvgt6, 't7': countryPreexistingYesAvgt7, 't8': countryPreexistingYesAvgt8, 't9': countryPreexistingYesAvgt9, 't10': countryPreexistingYesAvgt10, 't11': countryPreexistingYesAvgt11, 't12': countryPreexistingYesAvgt12, 't13': countryPreexistingYesAvgt13, 't14': countryPreexistingYesAvgt14}, ignore_index=True)
                output_vars = output_vars.append({'Country': country, 'Measure': msr, 'Category': 'Preexisting', 'Subcategory': 'preexisting_no', 't1': countryPreexistingNoAvgt1, 't2': countryPreexistingNoAvgt2, 't3': countryPreexistingNoAvgt3, 't4': countryPreexistingNoAvgt4, 't5': countryPreexistingNoAvgt5,
                                't6': countryPreexistingNoAvgt6, 't7': countryPreexistingNoAvgt7, 't8': countryPreexistingNoAvgt8, 't9': countryPreexistingNoAvgt9, 't10': countryPreexistingNoAvgt10, 't11': countryPreexistingNoAvgt11, 't12': countryPreexistingNoAvgt12, 't13': countryPreexistingNoAvgt13, 't14': countryPreexistingNoAvgt14}, ignore_index=True)

            click.echo("processing for " + msr + " completed")
        
        output_vars = output_vars.reset_index()
        output_vars.to_csv(r'output_vars.csv', index=None, header=True)
        click.echo("output_vars.csv exported")

    elif processtype == "cclab-averages":
        # get averages for each time point for all int values
        # loaded should be the responses (probably from dashboard files, eg CCLAB-old-ints.csv)
        out = pd.read_csv(
            'CCLAB-new-responses-int-out.csv', delimiter=',', encoding='latin1', low_memory=False)
         
        allDates = out['Date'].tolist()
        allVariables = out.columns.tolist()
        del allVariables[0]

        for date in allDates:
            dateSlice = loaded[loaded.Date == date]
            for vari in allVariables:
                avg = dateSlice[vari].mean()
                out.at[date, vari] = avg

        # out = out.reset_index()
        out.to_csv(r'output.csv', index=None, header=True)
        click.echo("output.csv exported")

    elif processtype == "cclab-averages-string":
            # concatinate all strings for each timepoint
            # loaded should be the responses
            out = pd.read_csv(
                'CCLAB-new-responses-string-out.csv', index_col='Measure', delimiter=',', encoding='latin1')
                  
            # allDates = out['Date'].tolist()
            # allDates = out.index.values
            allVariables = out.index.values
            allDates = out.columns.tolist()
            # out = out.astype(str).dtypes
            click.echo(out.dtypes)
            # del allVariables[0]

            for date in allDates:
                click.echo(date)
                dateSlice = loaded[loaded.Date == date]
                for vari in allVariables:
                    # click.echo("this variable: " + vari)
                    conc = ""
                    for (idx, row) in dateSlice.iterrows():
                        if type(row.loc[vari]) is str:
                            conc = conc + str(row.loc[vari]) + " "
                    
                    out.at[vari, date] = conc

            # out = out.reset_index()
            out.to_csv(r'output.csv', header=True)
            click.echo("output.csv exported")

    elif processtype == "cclab-repayment":
        #get unique values from column
        #go through the file and for each unique value calculate weights for each expectation
        # while you are doing that, count them rows as well
        # calculate relavant weights by dividing by value 4 count
        # add all these in a smaller df
        # on export, export rows according to counts to a larger df and then export

        output_small = pd.DataFrame(
            columns=['prediction', 'count', 'count1', 'count2', 'count3', 'count4','Expectation1Weight', 'Expectation2Weight', 'Expectation3Weight'])

        
        # variables = loaded.Variable.unique()

        # for v in variables:
            # varSlice = loaded[loaded.Variable == v]
        predictedList = loaded.PredictabilityDiff.unique()
        for pred in predictedList:
            predSlice = loaded[loaded.PredictabilityDiff == pred]
            count4 = 0
            count3 = 0
            count2 = 0
            count1 = 0
            countTotal = len(predSlice)

            count1 = predSlice[predSlice.Expectation == 1].shape[0]
            count2 = predSlice[predSlice.Expectation == 2].shape[0]
            count3 = predSlice[predSlice.Expectation == 3].shape[0]
            count4 = predSlice[predSlice.Expectation == 4].shape[0]
        
            weight3 = 0
            weight2 = 0
            weight1 = 0

            if count4 == 0:
                weight3 = 4
                weight2 = 4
                weight1 = 4
            else:
                weight3 = count3/count4
                weight2 = count2/count4
                weight1 = count1/count4

            output_small = output_small.append({'prediction': pred, 'count': countTotal, 'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 
                                            'Expectation1Weight': weight1, 'Expectation2Weight': weight2,
                                                'Expectation3Weight': weight3}, ignore_index=True)
    
        output_small.to_csv(r'output_small.csv', header=True)
        click.echo("output_small.csv exported")
        
        # export to a larger file
        output_large = pd.DataFrame(
            columns=['prediction', 'Expectation', 'ExpectationType'])

        for i in range(len(output_small)):
            for j in range(output_small.at[i, "count"]):
                output_large = output_large.append({'prediction': output_small.at[i, "prediction"], 'Expectation': output_small.at[i, "Expectation1Weight"], 'ExpectationType': 'Money',
                                               }, ignore_index=True)
                output_large = output_large.append({'prediction': output_small.at[i, "prediction"], 'Expectation': output_small.at[i, "Expectation2Weight"], 'ExpectationType': 'Same',
                                                }, ignore_index=True)
                output_large = output_large.append({'prediction': output_small.at[i, "prediction"], 'Expectation': output_small.at[i, "Expectation3Weight"], 'ExpectationType': 'SameNeed',
                                               }, ignore_index=True)
        
        output_large.to_csv(r'output_large.csv', header=True)
        click.echo("output_large.csv exported")
        

    click.echo('Processing completed.')
