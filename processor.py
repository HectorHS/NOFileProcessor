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
<<<<<<< HEAD
                "Nepal": "Nepal - samples tested",
=======
                "Nepal": "Nepal - tests performed",
>>>>>>> f18f373d2e30c013b1e1b6832d8edcce21523e88
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
<<<<<<< HEAD
                "Poland": "Poland - tests performed",
=======
                "Poland": "Poland - people tested",
>>>>>>> f18f373d2e30c013b1e1b6832d8edcce21523e88
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
<<<<<<< HEAD
            # click.echo("got in positive rate")
=======
>>>>>>> f18f373d2e30c013b1e1b6832d8edcce21523e88
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
<<<<<<< HEAD
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
=======
            sliced = historical[historical.location == country]
            # val = 0
            meas = measure + "_" + year
            val = sliced.iloc[0][meas]
            if not(math.isnan(val)):
                return val
>>>>>>> f18f373d2e30c013b1e1b6832d8edcce21523e88
            
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

        years = {2015, 2016, 2017, 2018, 2019, 2020, 2021}
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

         # Load covid data files
        location_01 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/09-26-2020.csv'
        location_02 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/10-27-2020.csv'
        location_03 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/11-28-2020.csv'
        location_04 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/12-28-2020.csv'
        location_05 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/01-27-2021.csv'
        location_06 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/02-26-2021.csv'
        location_07 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/03-28-2021.csv'
        location_08 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/04-27-2021.csv'
        location_09 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/05-27-2021.csv'
        location_10 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/06-26-2021.csv'
        location_11 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/07-26-2021.csv'
        location_12 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/08-25-2021.csv'
        location_13 = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/10-25-2021.csv'
        loaded01 = pd.read_csv(location_01, delimiter=',', encoding='latin1')
        loaded02 = pd.read_csv(location_02, delimiter=',', encoding='latin1')
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

        click.echo('covid data loaded')

        # initialise columns
        loaded['Incident_Rate.01'] = ''
        loaded['Case-Fatality_Ratio.01'] = ''
        loaded['Incident_Rate.02'] = ''
        loaded['Case-Fatality_Ratio.02'] = ''
        loaded['Incident_Rate.03'] = ''
        loaded['Case-Fatality_Ratio.03'] = ''
        loaded['Incident_Rate.04'] = ''
        loaded['Case-Fatality_Ratio.04'] = ''
        loaded['Incident_Rate.05'] = ''
        loaded['Case-Fatality_Ratio.05'] = ''
        loaded['Incident_Rate.06'] = ''
        loaded['Case-Fatality_Ratio.06'] = ''
        loaded['Incident_Rate.07'] = ''
        loaded['Case-Fatality_Ratio.07'] = ''
        loaded['Incident_Rate.08'] = ''
        loaded['Case-Fatality_Ratio.08'] = ''
        loaded['Incident_Rate.09'] = ''
        loaded['Case-Fatality_Ratio.09'] = ''
        loaded['Incident_Rate.10'] = ''
        loaded['Case-Fatality_Ratio.10'] = ''
        loaded['Incident_Rate.11'] = ''
        loaded['Case-Fatality_Ratio.11'] = ''
        loaded['Incident_Rate.12'] = ''
        loaded['Case-Fatality_Ratio.12'] = ''
        loaded['Incident_Rate.13'] = ''
        loaded['Case-Fatality_Ratio.13'] = ''

        for i in range(len(loaded)):
            for row in loaded01.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.01'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.01'] = row.Mortality_Rate
                    break
            for row in loaded02.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.02'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.02'] = row.Mortality_Rate
                    break
            for row in loaded03.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.03'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Case_Fatality_Ratio
                    break
            for row in loaded04.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.04'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Case_Fatality_Ratio
                    break
            for row in loaded05.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.05'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Case_Fatality_Ratio
                    break
            for row in loaded06.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.06'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Case_Fatality_Ratio
                    break
            for row in loaded07.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.07'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Case_Fatality_Ratio
                    break
            for row in loaded08.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.08'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.08'] = row.Case_Fatality_Ratio
                    break
            for row in loaded09.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.09'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.09'] = row.Case_Fatality_Ratio
                    break
            for row in loaded10.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.10'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.10'] = row.Case_Fatality_Ratio
                    break
            for row in loaded11.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.11'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.11'] = row.Case_Fatality_Ratio
                    break
            for row in loaded12.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.12'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.12'] = row.Case_Fatality_Ratio
                    break
            for row in loaded13.itertuples():
                if loaded.at[i, 'State_full'] == row.Province_State:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incident_Rate.13'] = row.Incident_Rate
                        loaded.at[i, 'Case-Fatality_Ratio.13'] = row.Case_Fatality_Ratio
                    break


        loaded = loaded.reset_index()
        loaded.to_csv(r'output.csv', index=None, header=True)
        
        click.echo('output file exported')
    elif processtype == 'cclab-covid-time':

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
        for row in newData.itertuples():
            today.append(row.confirmed)
        for row in newData.itertuples():
            today.append(row.deaths)

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

        measures = ["Age", "PerceptionRisk", "PFIaffectNeigh", "PFINeigh1", "PFINeigh6", "PFIcountry1", 
        "PFIcountry6", "WillingnessNeigh", "NBTneigh", "WillingnessCountry", "NBTcountry"]

        # get states
        states = loaded.State_full.unique()

        output = pd.DataFrame(
            columns=['State', 'Measure', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12'])

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
                
                output = output.append({'State': state, 'Measure': msr, 't1': avg1, 't2': avg2, 't3': avg3, 't4': avg4, 't5': avg5,
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

            output = output.append({'State': "All", 'Measure': msr, 't1': tot_avg1, 't2': tot_avg2, 't3': tot_avg3, 't4': tot_avg4, 't5': tot_avg5,
                                    't6': tot_avg6, 't7': tot_avg7, 't8': tot_avg8, 't9': tot_avg9, 't10': tot_avg10, 't11': tot_avg11, 't12': tot_avg12}, ignore_index=True)
            click.echo("processing for " + msr + " completed")
        
        # sex & covid
        sex_total_all = 0
        sex_count_all = 0
        covid_total_all = 0
        covid_count_all = 0
        for state in states: 
            sex_total = 0
            sex_count = 0
            covid_total = 0

            for i in range(len(loaded)):
                sex = float(loaded.at[i, "Sex"])
                covid = float(loaded.at[i, "InfectedCovidLatest"])
                
                if state == loaded.at[i, "State_full"] and math.isnan(sex) == False and loaded.at[i, "Date"] == "09/26/2020":
                        if sex == 2:
                            sex_total += 1
                        sex_count += 1
                
                if state == loaded.at[i, "State_full"] and math.isnan(covid) == False and loaded.at[i, "Date"] == "09/26/2020":
                        if covid == 3:
                            covid_total += 1
            
            sex_per = sex_total/sex_count
            output = output.append({'State': state, 'Measure': "Sex", 't1': sex_per, 't2': '', 't3': '', 't4': '', 't5': '',
                                't6': '', 't7': '', 't8': '', 't9': '', 't10': '', 't11': '', 't12': ''}, ignore_index=True)
            output = output.append({'State': state, 'Measure': "InfectedCovidLatest", 't1': covid_total, 't2': '', 't3': '', 't4': '', 't5': '',
                                't6': '', 't7': '', 't8': '', 't9': '', 't10': '', 't11': '', 't12': ''}, ignore_index=True)
            sex_total_all += sex_total
            sex_count_all += sex_count
            covid_total_all += covid_total

            sex_per_all = sex_total_all/sex_count_all
        
        output = output.append({'State': "All", 'Measure': "Sex", 't1': sex_per_all, 't2': '', 't3': '', 't4': '', 't5': '',
                                't6': '', 't7': '', 't8': '', 't9': '', 't10': '', 't11': '', 't12': ''}, ignore_index=True)
        output = output.append({'State': "All", 'Measure': "InfectedCovidLatest", 't1': covid_total_all, 't2': '', 't3': '', 't4': '', 't5': '',
                                't6': '', 't7': '', 't8': '', 't9': '', 't10': '', 't11': '', 't12': ''}, ignore_index=True)
        
        output = output.reset_index()
        output.to_csv(r'output.csv', index=None, header=True)

    click.echo('Processing completed.')
