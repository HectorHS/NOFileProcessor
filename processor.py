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
    elif processtype not in ['covid19', 'cclab-covid']:
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
        day = input[:2]
        month = input[3:5]
        year = input[6:10]

        loaded_location = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' + \
            month + '-' + day + '-' + year + '.csv'

        loaded = pd.read_csv(loaded_location, delimiter=',', encoding='latin1')

        population = pd.read_csv(
            'resources/population.csv', delimiter=',', encoding='latin1')
        click.echo('population data loaded')
        testing = pd.read_csv(
            '../owid-covid-data/public/data/testing/covid-testing-latest-data-source-details.csv', delimiter=',', encoding='latin1')
        testing.columns = [c.strip().lower().replace(' ', '_')
                           for c in testing.columns]
        testing.columns = [c.strip().lower().replace('-', '_')
                           for c in testing.columns]
        click.echo('testing data loaded')
        vaccinations = pd.read_csv(
            '../owid-covid-data/public/data/vaccinations/vaccinations.csv', delimiter=',', encoding='latin1')
        click.echo('vaccination data loaded')

        output = pd.DataFrame(
            columns=['Country', 'Confirmed', 'Confirmed_pc', 'Deaths', 'Deaths_pc', 'Death_rate', 'Recovered', 'Recovered_pc', 'Recovered_rate', 'Active', 'Active_pc', 'Tested', 'Tested_pc', 'Tested_rate', 'Fully_vaccinated_pc', 'Population'])

        usDeaths, usConfirmed, usRecovered, usActive, usTest = 0, 0, 0, 0, 0
        ausDeaths, ausConfirmed, ausRecovered, ausActive, ausTest = 0, 0, 0, 0, 0
        canDeaths, canConfirmed, canRecovered, canActive, canTest = 0, 0, 0, 0, 0
        chnDeaths, chnConfirmed, chnRecovered, chnActive, chnTest = 0, 0, 0, 0, 0
        itDeaths, itConfirmed, itRecovered, itActive, itTest = 0, 0, 0, 0, 0
        gerDeaths, gerConfirmed, gerRecovered, gerActive, gerTest = 0, 0, 0, 0, 0
        spnDeaths, spnConfirmed, spnRecovered, spnActive, spnTest = 0, 0, 0, 0, 0
        braDeaths, braConfirmed, braRecovered, braActive, braTest = 0, 0, 0, 0, 0
        chlDeaths, chlConfirmed, chlRecovered, chlActive, chlTest = 0, 0, 0, 0, 0
        mexDeaths, mexConfirmed, mexRecovered, mexActive, mexTest = 0, 0, 0, 0, 0
        perDeaths, perConfirmed, perRecovered, perActive, perTest = 0, 0, 0, 0, 0
        colDeaths, colConfirmed, colRecovered, colActive, colTest = 0, 0, 0, 0, 0
        jpnDeaths, jpnConfirmed, jpnRecovered, jpnActive, jpnTest = 0, 0, 0, 0, 0
        rusDeaths, rusConfirmed, rusRecovered, rusActive, rusTest = 0, 0, 0, 0, 0
        ukrDeaths, ukrConfirmed, ukrRecovered, ukrActive, ukrTest = 0, 0, 0, 0, 0
        sweDeaths, sweConfirmed, sweRecovered, sweActive, sweTest = 0, 0, 0, 0, 0
        pakDeaths, pakConfirmed, pakRecovered, pakActive, pakTest = 0, 0, 0, 0, 0
        indDeaths, indConfirmed, indRecovered, indActive, indTest = 0, 0, 0, 0, 0
        ukDeaths, ukConfirmed, ukRecovered, ukActive, ukTest = 0, 0, 0, 0, 0
        nldDeaths, nldConfirmed, nldRecovered, nldActive, nldTest = 0, 0, 0, 0, 0
        belDeaths, belConfirmed, belRecovered, belActive, belTest = 0, 0, 0, 0, 0
        malDeaths, malConfirmed, malRecovered, malActive, malTest = 0, 0, 0, 0, 0
        glDeaths, glConfirmed, glRecovered, glActive, glTest = 0, 0, 0, 0, 0

        def getPopulation(country):
            nonlocal population
            for row in population.itertuples():
                if row.Country == country:
                    return row.Population
            click.echo('population for ' + str(country) + ' not found')
            return 0

        def getTestingCountryName(country):
            countryName = {
                "Argentina": "Argentina - tests performed",
                "Australia": "Australia - tests performed",
                "Austria": "Austria - tests performed",
                "Bahrain": "Bahrain - units unclear",
                "Bangladesh": "Bangladesh - tests performed",
                "Belarus": "Belarus - tests performed",
                "Belgium": "Belgium - tests performed",
                "Bolivia": "Bolivia - tests performed",
                "Brazil": "Brazil - tests performed",
                "Bulgaria": "Bulgaria - tests performed",
                "Canada": "Canada - people tested",
                "Chile": "Chile - tests performed",
                "Colombia": "Colombia - tests performed",
                "Costa Rica": "Costa Rica - people tested",
                "Croatia": "Croatia - people tested",
                "Cuba": "Cuba - tests performed",
                "Czechia": "Czechia - tests performed",
                "Denmark": "Denmark - tests performed",
                "Ecuador": "Ecuador - people tested",
                "El Salvador": "El Salvador - tests performed",
                "Estonia": "Estonia - tests performed",
                "Ethiopia": "Ethiopia - tests performed",
                "Finland": "Finland - tests performed",
                "France": "France - people tested",
                "Germany": "Germany - tests performed",
                "Ghana": "Ghana - samples tested",
                "Greece": "Greece - samples tested",
                "Hong Kong": "Hong Kong - tests performed",
                "Hungary": "Hungary - tests performed",
                "Iceland": "Iceland - tests performed",
                "India": "India - samples tested",
                "Indonesia": "Indonesia - people tested",
                "Iran": "Iran - tests performed",
                "Ireland": "Ireland - tests performed",
                "Israel": "Israel - tests performed",
                "Italy": "Italy - people tested",
                "Japan": "Japan - people tested",
                "Kazakhstan": "Kazakhstan - tests performed",
                "Kenya": "Kenya - samples tested",
                "Latvia": "Latvia - tests performed",
                "Lithuania": "Lithuania - tests performed",
                "Luxembourg": "Luxembourg - tests performed",
                "Malaysia": "Malaysia - people tested",
                "Mexico": "Mexico - people tested",
                "Maldives": "Maldives - samples tested",
                "Morocco": "Morocco - people tested",
                "Burma": "Myanmar - samples tested",
                "Nepal": "Nepal - tests performed",
                "Netherlands": "Netherlands - people tested",
                "New Zealand": "New Zealand - tests performed",
                "Nigeria": "Nigeria - samples tested",
                "Norway": "Norway - people tested",
                "Pakistan": "Pakistan - tests performed",
                "Panama": "Panama - tests performed",
                "Paraguay": "Paraguay - tests performed",
                "Peru": "Peru - tests performed",
                "Philippines": "Philippines - people tested",
                "Poland": "Poland - people tested",
                "Portugal": "Portugal - tests performed",
                "Qatar": "Qatar - people tested",
                "Romania": "Romania - tests performed",
                "Russia": "Russia - tests performed",
                "Rwanda": "Rwanda - samples tested",
                "Saudi Arabia": "Saudi Arabia - tests performed",
                "Senegal": "Senegal - tests performed",
                "Serbia": "Serbia - people tested",
                "Singapore": "Singapore - samples tested",
                "Slovakia": "Slovakia - tests performed",
                "Slovenia": "Slovenia - tests performed",
                "South Africa": "South Africa - people tested",
                "Korea, South": "South Korea - people tested",
                "Spain": "Spain - tests performed",
                "Sweden": "Sweden - tests performed",
                "Switzerland": "Switzerland - tests performed",
                "Taiwan": "Taiwan - tests performed",
                "Thailand": "Thailand - tests performed",
                "Tunisia": "Tunisia - people tested",
                "Turkey": "Turkey - tests performed",
                "Uganda": "Uganda - samples tested",
                "Ukraine": "Ukraine - tests performed",
                "United Kingdom": "United Kingdom - tests performed",
                "USA": "United States - tests performed",
                "Uruguay": "Uruguay - tests performed",
                "Vietnam": "Vietnam - samples tested",
                "Zimbabwe": "Zimbabwe - tests performed"
            }

            name = countryName[country] if country in countryName else ""
            return name

        def getTestTotal(testingCountryName, confirmed):
            nonlocal testing
            for row in testing.itertuples():
                if row.entity == testingCountryName:
                    # France, DRC and Sweden are missing testing totals, so this is a workaround
                    if row.entity in ["France - people tested", "Sweden - tests performed", "Democratic Republic of Congo - samples tested"]:
                        return (confirmed / row.short_term_positive_rate)
                    # Numbers for Peru do not add up, so ignore them for now
                    if row.entity == "Peru - people tested":
                        return 0
                    return row.cumulative_total
            click.echo('Testing total for ' +
                       str(testingCountryName) + ' not found')
            return 0

        def getVaccination(country):
            nonlocal vaccinations
            value = 0

            if country == "Korea, South":
                country = "South Korea"
            elif country == "Taiwan*":
                country = "Taiwan"
            elif country == "Burma":
                country = "Myanmar"
            elif country == "Cabo Verde":
                country = "Cape Verde"
            elif country == "Congo (Brazzaville)":
                country = "Congo"
            elif country == "West Bank and Gaza":
                country = "Palestine"
            elif country == "Timor-Leste":
                country = "Timor"

            # filter out uneeded rows
            subset = vaccinations[vaccinations.location == country]
            if len(subset.index) > 0:
                lastRow = subset.tail(1)
                if not(math.isnan(lastRow.people_fully_vaccinated_per_hundred)):
                    value = lastRow.iloc[0]['people_fully_vaccinated_per_hundred']
            else:
                click.echo("No vaccination rows found for " + country)

            return value

        def outputAppend(country, confirmed, deaths, recovered, active, tested, vaccinated, population):
            nonlocal output
            confirmedPC, deathsPC, deathCent, recoveredPC, recoveredCent, activePC, testedPC, testedCent = 0, 0, 0, 0, 0, 0, 0, 0
            if confirmed > 0:
                confirmedPC = confirmed / (population/1000000)

            if deaths > 0:
                deathsPC = deaths / (population/1000000)
                deathCent = (deaths / confirmed) * 100

            if recovered > 0:
                recoveredPC = recovered / (population/1000000)
                recoveredCent = (recovered / confirmed) * 100

            if active > 0:
                activePC = active / (population/1000000)

            if tested > 0:
                testedPC = tested / (population/1000000)
                testedCent = (confirmed / tested) * 100

            output = output.append({'Country': country, 'Confirmed': confirmed, 'Confirmed_pc': confirmedPC, 'Deaths': deaths, 'Deaths_pc': deathsPC, 'Death_rate': deathCent, 'Recovered': recovered,
                                    'Recovered_pc': recoveredPC, 'Recovered_rate': recoveredCent, 'Active': active, 'Active_pc': activePC, 'Tested': tested, 'Tested_pc': testedPC, 'Tested_rate': testedCent, 'Fully_vaccinated_pc': vaccinated, 'Population': population}, ignore_index=True)

        for row in loaded.itertuples():
            # counters for global values
            glDeaths += row.Deaths
            glConfirmed += row.Confirmed
            glRecovered += row.Recovered
            if row.Active > 0:
                glActive += row.Active

            # These countries are split up in regions, so add them up
            if row.Country_Region == 'US':
                usDeaths += row.Deaths
                usConfirmed += row.Confirmed
                usRecovered += row.Recovered
                if row.Active > 0:
                    usActive += row.Active
            elif row.Country_Region == 'Australia':
                ausDeaths += row.Deaths
                ausConfirmed += row.Confirmed
                ausRecovered += row.Recovered
                if row.Active > 0:
                    ausActive += row.Active
            elif row.Country_Region == 'Canada':
                canDeaths += row.Deaths
                canConfirmed += row.Confirmed
                canRecovered += row.Recovered
                if row.Active > 0:
                    canActive += row.Active
            elif row.Country_Region == 'China':
                chnDeaths += row.Deaths
                chnConfirmed += row.Confirmed
                chnRecovered += row.Recovered
                if row.Active > 0:
                    chnActive += row.Active
            elif row.Country_Region == 'Italy':
                itDeaths += row.Deaths
                itConfirmed += row.Confirmed
                itRecovered += row.Recovered
                if row.Active > 0:
                    itActive += row.Active
            elif row.Country_Region == 'Germany':
                gerDeaths += row.Deaths
                gerConfirmed += row.Confirmed
                gerRecovered += row.Recovered
                if row.Active > 0:
                    gerActive += row.Active
            elif row.Country_Region == 'Spain':
                spnDeaths += row.Deaths
                spnConfirmed += row.Confirmed
                spnRecovered += row.Recovered
                if row.Active > 0:
                    spnActive += row.Active
            elif row.Country_Region == 'Brazil':
                braDeaths += row.Deaths
                braConfirmed += row.Confirmed
                braRecovered += row.Recovered
                if row.Active > 0:
                    braActive += row.Active
            elif row.Country_Region == 'Chile':
                chlDeaths += row.Deaths
                chlConfirmed += row.Confirmed
                chlRecovered += row.Recovered
                if row.Active > 0:
                    chlActive += row.Active
            elif row.Country_Region == 'Mexico':
                mexDeaths += row.Deaths
                mexConfirmed += row.Confirmed
                mexRecovered += row.Recovered
                if row.Active > 0:
                    mexActive += row.Active
            elif row.Country_Region == 'Peru':
                perDeaths += row.Deaths
                perConfirmed += row.Confirmed
                perRecovered += row.Recovered
                if row.Active > 0:
                    perActive += row.Active
            elif row.Country_Region == 'Colombia':
                colDeaths += row.Deaths
                colConfirmed += row.Confirmed
                colRecovered += row.Recovered
                if row.Active > 0:
                    colActive += row.Active
            elif row.Country_Region == 'Japan':
                jpnDeaths += row.Deaths
                jpnConfirmed += row.Confirmed
                jpnRecovered += row.Recovered
                if row.Active > 0:
                    jpnActive += row.Active
            elif row.Country_Region == 'Russia':
                rusDeaths += row.Deaths
                rusConfirmed += row.Confirmed
                rusRecovered += row.Recovered
                if row.Active > 0:
                    rusActive += row.Active
            elif row.Country_Region == 'Ukraine':
                ukrDeaths += row.Deaths
                ukrConfirmed += row.Confirmed
                ukrRecovered += row.Recovered
                if row.Active > 0:
                    ukrActive += row.Active
            elif row.Country_Region == 'Sweden':
                sweDeaths += row.Deaths
                sweConfirmed += row.Confirmed
                sweRecovered += row.Recovered
                if row.Active > 0:
                    sweActive += row.Active
            elif row.Country_Region == 'Pakistan':
                pakDeaths += row.Deaths
                pakConfirmed += row.Confirmed
                pakRecovered += row.Recovered
                if row.Active > 0:
                    pakActive += row.Active
            elif row.Country_Region == 'India':
                indDeaths += row.Deaths
                indConfirmed += row.Confirmed
                indRecovered += row.Recovered
                if row.Active > 0:
                    indActive += row.Active
            elif row.Country_Region == 'Belgium':
                belDeaths += row.Deaths
                belConfirmed += row.Confirmed
                belRecovered += row.Recovered
                if row.Active > 0:
                    belActive += row.Active
            elif row.Country_Region == 'Malaysia':
                malDeaths += row.Deaths
                malConfirmed += row.Confirmed
                malRecovered += row.Recovered
                if row.Active > 0:
                    malActive += row.Active
            elif row.Country_Region == 'United Kingdom' and row.Province_State in ['England', 'Scotland', 'Northern Ireland', 'Unknown', 'Wales']:
                ukDeaths += row.Deaths
                ukConfirmed += row.Confirmed
                ukRecovered += row.Recovered
                if row.Active > 0:
                    ukActive += row.Active
            elif row.Country_Region == 'Netherlands' and row.Province_State in ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant', 'Noord-Holland', 'Overijssel', 'Unknown', 'Utrecht', 'Zeeland', 'Zuid-Holland']:
                nldDeaths += row.Deaths
                nldConfirmed += row.Confirmed
                nldRecovered += row.Recovered
                if row.Active > 0:
                    nldActive += row.Active
            elif row.Country_Region in ['Diamond Princess', 'MS Zaandam', 'Summer Olympics 2020']:
                what = 'No idea what to do with this'
            # In the remainer countries, the ones that have a state are considered different countries
            # If there is no state, it's the main country. The empty value is interpreted as a float
            elif isinstance(row.Province_State, float):

                testingCountryName = getTestingCountryName(
                    row.Country_Region)

                tested = 0 if testingCountryName == "" else getTestTotal(
                    testingCountryName, row.Confirmed)

                if tested > 0:
                    glTest += tested

                if not isinstance(row.Country_Region, float):
                    outputAppend(row.Country_Region, row.Confirmed, row.Deaths,
                                 row.Recovered, row.Active, tested, getVaccination(row.Country_Region), getPopulation(row.Country_Region))
            else:
                testingCountryName = getTestingCountryName(row.Province_State)

                tested = 0 if testingCountryName == "" else getTestTotal(
                    testingCountryName, row.Confirmed)
                glTest += tested
                outputAppend(row.Province_State, row.Confirmed, row.Deaths,
                             row.Recovered, row.Active, tested, getVaccination(row.Country_Region), getPopulation(row.Province_State))

        # There are some errors here I am fixing maually for now
        if usActive == 0:
            usActive = usConfirmed - usDeaths - usRecovered
        if canActive == 0:
            canActive = canConfirmed - canDeaths - canRecovered
        # get test values and add to global
        usTest = getTestTotal(getTestingCountryName('USA'), usConfirmed)
        ausTest = getTestTotal(
            getTestingCountryName('Australia'), ausConfirmed)
        canTest = getTestTotal(getTestingCountryName('Canada'), canConfirmed)
        itTest = getTestTotal(getTestingCountryName('Italy'), itConfirmed)
        gerTest = getTestTotal(getTestingCountryName('Germany'), gerConfirmed)
        spnTest = getTestTotal(getTestingCountryName('Spain'), spnConfirmed)
        braTest = getTestTotal(getTestingCountryName('Brazil'), braConfirmed)
        chlTest = getTestTotal(getTestingCountryName('Chile'), chlConfirmed)
        mexTest = getTestTotal(getTestingCountryName('Mexico'), mexConfirmed)
        perTest = getTestTotal(getTestingCountryName('Peru'), perConfirmed)
        colTest = getTestTotal(getTestingCountryName('Colombia'), colConfirmed)
        jpnTest = getTestTotal(getTestingCountryName('Japan'), jpnConfirmed)
        rusTest = getTestTotal(getTestingCountryName('Russia'), rusConfirmed)
        ukrTest = getTestTotal(getTestingCountryName('Ukraine'), ukrConfirmed)
        sweTest = getTestTotal(getTestingCountryName('Sweden'), sweConfirmed)
        pakTest = getTestTotal(getTestingCountryName('Pakistan'), pakConfirmed)
        indTest = getTestTotal(getTestingCountryName('India'), indConfirmed)
        belTest = getTestTotal(getTestingCountryName('Belgium'), belConfirmed)
        malTest = getTestTotal(getTestingCountryName('Malaysia'), malConfirmed)
        ukTest = getTestTotal(getTestingCountryName(
            'United Kingdom'), ukConfirmed)
        nldTest = getTestTotal(getTestingCountryName(
            'Netherlands'), nldConfirmed)

        glTest = glTest + usTest + ausTest + canTest + itTest + gerTest + spnTest + braTest + chlTest + mexTest + perTest + colTest + jpnTest + rusTest + ukrTest + sweTest + \
            pakTest + indTest + belTest + ukTest + nldTest

        outputAppend('USA', usConfirmed, usDeaths,
                     usRecovered, usActive, usTest, getVaccination('United States'), getPopulation('USA'))
        outputAppend('Australia', ausConfirmed, ausDeaths,
                     ausRecovered, ausActive, ausTest, getVaccination('Australia'), getPopulation('Australia'))
        outputAppend('Canada', canConfirmed, canDeaths,
                     canRecovered, canActive, canTest, getVaccination('Canada'), getPopulation('Canada'))
        outputAppend('China', chnConfirmed, chnDeaths,
                     chnRecovered, chnActive, 0, getVaccination('China'), getPopulation('China'))
        outputAppend('Italy', itConfirmed, itDeaths,
                     itRecovered, itActive, itTest, getVaccination('Italy'), getPopulation('Italy'))
        outputAppend('Germany', gerConfirmed, gerDeaths,
                     gerRecovered, gerActive, gerTest, getVaccination('Germany'), getPopulation('Germany'))
        outputAppend('Spain', spnConfirmed, spnDeaths,
                     spnRecovered, spnActive, spnTest, getVaccination('Spain'), getPopulation('Spain'))
        outputAppend('Brazil', braConfirmed, braDeaths,
                     braRecovered, braActive, braTest, getVaccination('Brazil'), getPopulation('Brazil'))
        outputAppend('Chile', chlConfirmed, chlDeaths,
                     chlRecovered, chlActive, chlTest, getVaccination('Chile'), getPopulation('Chile'))
        outputAppend('Mexico', mexConfirmed, mexDeaths,
                     mexRecovered, mexActive, mexTest, getVaccination('Mexico'), getPopulation('Mexico'))
        outputAppend('Peru', perConfirmed, perDeaths,
                     perRecovered, perActive, perTest, getVaccination('Peru'), getPopulation('Peru'))
        outputAppend('Colombia', colConfirmed, colDeaths,
                     colRecovered, colActive, colTest, getVaccination('Colombia'), getPopulation('Colombia'))
        outputAppend('Japan', jpnConfirmed, jpnDeaths,
                     jpnRecovered, jpnActive, jpnTest, getVaccination('Japan'), getPopulation('Japan'))
        outputAppend('Russia', rusConfirmed, rusDeaths,
                     rusRecovered, rusActive, rusTest, getVaccination('Russia'), getPopulation('Russia'))
        outputAppend('Ukraine', ukrConfirmed, ukrDeaths,
                     ukrRecovered, ukrActive, ukrTest, getVaccination('Ukraine'), getPopulation('Ukraine'))
        outputAppend('Sweden', sweConfirmed, sweDeaths,
                     sweRecovered, sweActive, sweTest, getVaccination('Sweden'), getPopulation('Sweden'))
        outputAppend('Pakistan', pakConfirmed, pakDeaths,
                     pakRecovered, pakActive, pakTest, getVaccination('Pakistan'), getPopulation('Pakistan'))
        outputAppend('India', indConfirmed, indDeaths,
                     indRecovered, indActive, indTest, getVaccination('India'), getPopulation('India'))
        outputAppend('Belgium', belConfirmed, belDeaths,
                     belRecovered, belActive, belTest, getVaccination('Belgium'), getPopulation('Belgium'))
        outputAppend('Malaysia', malConfirmed, malDeaths,
                     malRecovered, malActive, malTest, getVaccination('Malaysia'), getPopulation('Malaysia'))
        outputAppend('United Kingdom', ukConfirmed, ukDeaths,
                     ukRecovered, ukActive, ukTest, getVaccination('United Kingdom'), getPopulation('United Kingdom'))
        outputAppend('Netherlands', nldConfirmed, nldDeaths,
                     nldRecovered, nldActive, nldTest, getVaccination('Netherlands'), getPopulation('Netherlands'))
        outputAppend('World', glConfirmed, glDeaths,
                     glRecovered, glActive, glTest, getVaccination('World'), getPopulation('World'))

        # Sort by country, but because sorting in python with mixed cases is messy, do all this
        output['country_lower'] = output['Country'].str.lower()
        output = output.sort_values(by=['country_lower'])
        output.drop('country_lower', axis=1, inplace=True)

        output = output.reset_index()
        output.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-map.csv', index=None, header=True)
        click.echo('covid-map.csv exported')

        # Update covid-time.csv
        time = pd.read_csv(
            '../NavigateObscurity/static/worlddata/csv/covid-time.csv', delimiter=',', encoding='latin1')
        click.echo('time series data loaded')

        older = pd.read_csv(
            '../NavigateObscurity/static/worlddata/csv/covid-map.csv', delimiter=',', encoding='latin1')
        click.echo('older data loaded')

        today = []
        for row in output.itertuples():
            today.append(row.Confirmed)
        for row in output.itertuples():
            today.append(row.Deaths)

        for i in range(len(output)):
            today.append(output.at[i, 'Confirmed'] - older.at[i, 'Confirmed'])
        for i in range(len(output)):
            today.append(output.at[i, 'Deaths'] - older.at[i, 'Deaths'])

        time = time.assign(**{input: today})
        time.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-time.csv', index=False, header=True)
        click.echo('covid-time.csv exported')

        # Update covid-lockdown.csv
        # lockdown = pd.read_csv(
        #     '../NavigateObscurity/static/worlddata/csv/covid-lockdown.csv', delimiter=',', encoding='latin1')
        # click.echo('lockdown data loaded')
        # lockday = []
        # lockday = lockdown.iloc[:, -1:]
        # lockdown = lockdown.assign(**{input: lockday})
        # lockdown.to_csv(
        #     r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-lockdown.csv', index=False, header=True)
        # click.echo('covid-lockdown.csv exported')

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
            columns=['Country', 'Week', 'Deaths_old', 'Deaths_2020', 'Deaths_2021'])

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
                for row in loadedFiltered.itertuples():
                    if row.Year == 2020:
                        sum20 = row.DTotal
                    elif row.Year == 2021:
                        sum21 = row.DTotal
                    else:
                        oldSum += row.DTotal
                if week == 53 and country != "Australia":
                    oldAverage = oldSum
                elif country in ['Greece', 'Germany']:
                    oldAverage = oldSum / 4
                else:
                    oldAverage = oldSum / 5

                output = output.append(
                    {'Country': country, 'Week': week, 'Deaths_old': oldAverage, 'Deaths_2020': sum20, 'Deaths_2021': sum21}, ignore_index=True)

        for week in weeks:
            loadedFiltered = loaded[loaded.Week == week]
            loadedFiltered = loadedFiltered[loadedFiltered['CountryCode'].isin(
                uk)]
            oldSum = 0
            sum20 = 0
            sum21 = 0
            i = 0
            j = 0
            for row in loadedFiltered.itertuples():
                if row.Year == 2020:
                    sum20 += row.DTotal
                    i += 1
                elif row.Year == 2021:
                    sum21 += row.DTotal
                    j += 1
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

            output = output.append({'Country': "United Kingdom", 'Week': week,
                                    'Deaths_old': oldAverage, 'Deaths_2020': sum20, 'Deaths_2021': sum21}, ignore_index=True)
        output = output.reset_index()
        output.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-excess-deaths.csv', index=None, header=True)

    elif processtype == 'cclab-covid':

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
        loaded['Incidence_Rate.14'] = ''

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

        def getPopulation(country, state, admin):
            nonlocal population
            click.echo(str(country) +
                       str(state) + str(admin))
            for row in population.itertuples():
                if row.Country_Region == country and row.Province_State == state and row.Admin2 == admin:
                    return int(row.Population)
            for row in population.itertuples():
                if row.Country_Region == country and row.Province_State == state:
                    return int(row.Population)
            for row in population.itertuples():
                if row.Country_Region == country:
                    return int(row.Population)
            click.echo('population for ' + str(country) +
                       str(state) + str(admin) + ' not found')
            return 0

        # Populate columns. one loop for each time point
        for i in range(len(loaded)):
            pop = getPopulation(loaded.at[i, 'CurrentCountry'],
                                loaded.at[i, 'CovidArea'], loaded.at[i, 'CovidAreaSmaller'])

            for row in loaded03.itertuples():

                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    click.echo(row.Confirmed)
                    click.echo(pop)
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
                        loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
                            row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
                        row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.03'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.03'] = row.Deaths / \
                        row.Confirmed*100
                    break

            for row in loaded04.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
                        loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
                            row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
                        row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.04'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.04'] = row.Deaths / \
                        row.Confirmed*100
                    break

            for row in loaded05.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
                        loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
                            row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
                        row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.05'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.05'] = row.Deaths / \
                        row.Confirmed*100
                    break

            for row in loaded06.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
                        loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
                            row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
                        row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.06'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.06'] = row.Deaths / \
                        row.Confirmed*100
                    break

            for row in loaded07.itertuples():
                if loaded.at[i, 'CurrentCountry'] == 'US' and loaded.at[i, 'CovidArea'] == row.Province_State and loaded.at[i, 'CovidAreaSmaller'] == row.Admin2:
                    if (row.Confirmed > 0):
                        loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
                        loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
                            row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] != 'US' and loaded.at[i, 'CurrentCountry'] == row.Country_Region and loaded.at[i, 'CovidArea'] == row.Province_State:
                    loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
                        row.Confirmed*100
                    break
                elif loaded.at[i, 'CurrentCountry'] == row.Combined_Key:
                    loaded.at[i, 'Incidence_Rate.07'] = row.Confirmed/pop*100000
                    loaded.at[i, 'Case-Fatality_Ratio.07'] = row.Deaths / \
                        row.Confirmed*100
                    break

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
            if (i == 100):
                # loaded = loaded.reset_index()
                loaded.to_csv(r'output2.csv', index=None, header=True)
                click.echo('sample exported')
            if (i == 500):
                # loaded = loaded.reset_index()
                loaded.to_csv(r'output3.csv', index=None, header=True)
                click.echo('sample exported')

        loaded = loaded.reset_index()
        loaded.to_csv(r'output.csv', index=None, header=True)

    click.echo('Processing completed.')
