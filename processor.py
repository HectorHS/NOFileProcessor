import click
# import csv
import numpy as np
import pandas as pd


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
    elif processtype != 'covid19':
        loaded = pd.read_csv(input, delimiter=',', encoding='latin1')
        click.echo('file loaded')

    if processtype == 'death-tree':
        output = pd.pivot_table(loaded, values='val', columns=['cause'],
                                index=['measure', 'location', 'sex', 'age'],
                                aggfunc=lambda x: x)
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

        output = pd.DataFrame(
            columns=['Country', 'Confirmed', 'Confirmed_pc', 'Deaths', 'Deaths_pc', 'Death_rate', 'Recovered', 'Recovered_pc', 'Recovered_rate', 'Active', 'Active_pc', 'Tested', 'Tested_pc', 'Tested_rate', 'Population'])

        usDeaths, usConfirmed, usRecovered, usActive = 0, 0, 0, 0
        ausDeaths, ausConfirmed, ausRecovered, ausActive = 0, 0, 0, 0
        canDeaths, canConfirmed, canRecovered, canActive = 0, 0, 0, 0
        chnDeaths, chnConfirmed, chnRecovered, chnActive = 0, 0, 0, 0
        itDeaths, itConfirmed, itRecovered, itActive = 0, 0, 0, 0
        gerDeaths, gerConfirmed, gerRecovered, gerActive = 0, 0, 0, 0
        spnDeaths, spnConfirmed, spnRecovered, spnActive = 0, 0, 0, 0
        braDeaths, braConfirmed, braRecovered, braActive = 0, 0, 0, 0
        chlDeaths, chlConfirmed, chlRecovered, chlActive = 0, 0, 0, 0
        mexDeaths, mexConfirmed, mexRecovered, mexActive = 0, 0, 0, 0
        perDeaths, perConfirmed, perRecovered, perActive = 0, 0, 0, 0
        colDeaths, colConfirmed, colRecovered, colActive = 0, 0, 0, 0
        jpnDeaths, jpnConfirmed, jpnRecovered, jpnActive = 0, 0, 0, 0
        rusDeaths, rusConfirmed, rusRecovered, rusActive = 0, 0, 0, 0
        ukrDeaths, ukrConfirmed, ukrRecovered, ukrActive = 0, 0, 0, 0
        sweDeaths, sweConfirmed, sweRecovered, sweActive = 0, 0, 0, 0
        pakDeaths, pakConfirmed, pakRecovered, pakActive = 0, 0, 0, 0
        indDeaths, indConfirmed, indRecovered, indActive = 0, 0, 0, 0
        ukDeaths, ukConfirmed, ukRecovered, ukActive = 0, 0, 0, 0
        nldDeaths, nldConfirmed, nldRecovered, nldActive = 0, 0, 0, 0
        glDeaths, glConfirmed, glRecovered, glActive = 0, 0, 0, 0

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
                "Colombia": "Colombia - samples tested",
                "Costa Rica": "Costa Rica - people tested (incl. non-PCR)",
                "Croatia": "Croatia - people tested",
                "Cuba": "Cuba - tests performed",
                "Czechia": "Czech Republic - tests performed",
                "Denmark": "Denmark - tests performed",
                "Ecuador": "Ecuador - people tested",
                "El Salvador": "El Salvador - tests performed",
                "Estonia": "Estonia - tests performed",
                "Ethiopia": "Ethiopia - tests performed",
                "Finland": "Finland - samples tested",
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
                "Japan": "Japan - tests performed",
                "Kazakhstan": "Kazakhstan - tests performed",
                "Kenya": "Kenya - samples tested",
                "Latvia": "Latvia - tests performed",
                "Lithuania": "Lithuania - samples tested",
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
                "Peru": "Peru - people tested",
                "Philippines": "Philippines - people tested",
                "Poland": "Poland - people tested",
                "Portugal": "Portugal - samples tested",
                "Qatar": "Qatar - people tested",
                "Romania": "Romania - tests performed",
                "Russia": "Russia - tests performed",
                "Rwanda": "Rwanda - samples tested",
                "Saudi Arabia": "Saudi Arabia - tests performed",
                "Senegal": "Senegal - tests performed",
                "Serbia": "Serbia - people tested",
                "Singapore": "Singapore - people tested",
                "Slovakia": "Slovakia - tests performed",
                "Slovenia": "Slovenia - tests performed",
                "South Africa": "South Africa - people tested",
                "Korea, South": "South Korea - people tested",
                "Spain": "Spain - tests performed",
                "Sweden": "Sweden - samples tested",
                "Switzerland": "Switzerland - tests performed",
                "Taiwan": "Taiwan - tests performed",
                "Thailand": "Thailand - people tested",
                "Tunisia": "Tunisia - tests performed",
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
                    if row.entity in ["France - people tested", "Sweden - samples tested", "Democratic Republic of Congo - samples tested"]:
                        return (confirmed / row.short_term_positive_rate)
                    # Numbers for Peru do not add up, so ignore them for now
                    if row.entity == "Peru - people tested":
                        return 0
                    return row.cumulative_total
            click.echo('Testing total for ' +
                       str(testingCountryName) + ' not found')
            return 0

        def outputAppend(country, confirmed, deaths, recovered, active, tested, population):
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
                                    'Recovered_pc': recoveredPC, 'Recovered_rate': recoveredCent, 'Active': active, 'Active_pc': activePC, 'Tested': tested, 'Tested_pc': testedPC, 'Tested_rate': testedCent, 'Population': population}, ignore_index=True)

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
            elif row.Country_Region in ['Diamond Princess', 'MS Zaandam']:
                what = 'No idea what to do with this'
            # In the remainer countries, the ones that have a state are considered different countries
            # If there is no state, it's the main country. The empty value is interpreted as a float
            elif isinstance(row.Province_State, float):

                testingCountryName = getTestingCountryName(
                    row.Country_Region)

                tested = 0 if testingCountryName == "" else getTestTotal(
                    testingCountryName, row.Confirmed)

                outputAppend(row.Country_Region, row.Confirmed, row.Deaths,
                             row.Recovered, row.Active, tested, getPopulation(row.Country_Region))
            else:
                testingCountryName = getTestingCountryName(row.Province_State)

                tested = 0 if testingCountryName == "" else getTestTotal(
                    testingCountryName, row.Confirmed)
                outputAppend(row.Province_State, row.Confirmed, row.Deaths,
                             row.Recovered, row.Active, tested, getPopulation(row.Province_State))

        # There are some errors here I am fixing maually for now
        if usActive == 0:
            usActive = usConfirmed - usDeaths - usRecovered
        if canActive == 0:
            canActive = canConfirmed - canDeaths - canRecovered

        outputAppend('USA', usConfirmed, usDeaths,
                     usRecovered, usActive, getTestTotal(
                         getTestingCountryName('USA'), usConfirmed), getPopulation('USA'))
        outputAppend('Australia', ausConfirmed, ausDeaths,
                     ausRecovered, ausActive, getTestTotal(
                         getTestingCountryName("Australia"), ausConfirmed), getPopulation('Australia'))
        outputAppend('Canada', canConfirmed, canDeaths,
                     canRecovered, canActive, getTestTotal(
                         getTestingCountryName("Canada"), canConfirmed), getPopulation('Canada'))
        outputAppend('China', chnConfirmed, chnDeaths,
                     chnRecovered, chnActive, 0, getPopulation('China'))
        outputAppend('Italy', itConfirmed, itDeaths,
                     itRecovered, itActive, getTestTotal(
                         getTestingCountryName("Italy"), itConfirmed), getPopulation('Italy'))
        outputAppend('Germany', gerConfirmed, gerDeaths,
                     gerRecovered, gerActive, getTestTotal(
                         getTestingCountryName("Germany"), gerConfirmed), getPopulation('Germany'))
        outputAppend('Spain', spnConfirmed, spnDeaths,
                     spnRecovered, spnActive, getTestTotal(
                         getTestingCountryName("Spain"), spnConfirmed), getPopulation('Spain'))
        outputAppend('Brazil', braConfirmed, braDeaths,
                     braRecovered, braActive, getTestTotal(
                         getTestingCountryName("Brazil"), braConfirmed), getPopulation('Brazil'))
        outputAppend('Chile', chlConfirmed, chlDeaths,
                     chlRecovered, chlActive, getTestTotal(
                         getTestingCountryName("Chile"), chlConfirmed), getPopulation('Chile'))
        outputAppend('Mexico', mexConfirmed, mexDeaths,
                     mexRecovered, mexActive, getTestTotal(
                         getTestingCountryName("Mexico"), mexConfirmed), getPopulation('Mexico'))
        outputAppend('Peru', perConfirmed, perDeaths,
                     perRecovered, perActive, getTestTotal(
                         getTestingCountryName("Peru"), perConfirmed), getPopulation('Peru'))
        outputAppend('Colombia', colConfirmed, colDeaths,
                     colRecovered, colActive, getTestTotal(
                         getTestingCountryName("Colombia"), colConfirmed), getPopulation('Colombia'))
        outputAppend('Japan', jpnConfirmed, jpnDeaths,
                     jpnRecovered, jpnActive, getTestTotal(
                         getTestingCountryName("Japan"), jpnConfirmed), getPopulation('Japan'))
        outputAppend('Russia', rusConfirmed, rusDeaths,
                     rusRecovered, rusActive, getTestTotal(
                         getTestingCountryName("Russia"), rusConfirmed), getPopulation('Russia'))
        outputAppend('Ukraine', ukrConfirmed, ukrDeaths,
                     ukrRecovered, ukrActive, getTestTotal(
                         getTestingCountryName("Ukraine"), ukrConfirmed), getPopulation('Ukraine'))
        outputAppend('Sweden', sweConfirmed, sweDeaths,
                     sweRecovered, sweActive, getTestTotal(
                         getTestingCountryName("Sweden"), sweConfirmed), getPopulation('Sweden'))
        outputAppend('Pakistan', pakConfirmed, pakDeaths,
                     pakRecovered, pakActive, getTestTotal(
                         getTestingCountryName("Pakistan"), pakConfirmed), getPopulation('Pakistan'))
        outputAppend('India', indConfirmed, indDeaths,
                     indRecovered, indActive, getTestTotal(
                         getTestingCountryName("India"), indConfirmed), getPopulation('India'))
        outputAppend('United Kingdom', ukConfirmed, ukDeaths,
                     ukRecovered, ukActive, getTestTotal(
                         getTestingCountryName("United Kingdom"), ukConfirmed), getPopulation('United Kingdom'))
        outputAppend('Netherlands', nldConfirmed, nldDeaths,
                     nldRecovered, nldActive, getTestTotal(
                         getTestingCountryName("Netherlands"), nldConfirmed), getPopulation('Netherlands'))
        outputAppend('World', glConfirmed, glDeaths,
                     glRecovered, glActive, 0, getPopulation('World'))

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
            today.append(row.Recovered)
        for row in output.itertuples():
            today.append(row.Active)
        for row in output.itertuples():
            today.append(row.Deaths)

        for i in range(len(output)):
            today.append(output.at[i, 'Confirmed'] - older.at[i, 'Confirmed'])
        for i in range(len(output)):
            today.append(output.at[i, 'Recovered'] - older.at[i, 'Recovered'])
        for i in range(len(output)):
            today.append(output.at[i, 'Deaths'] - older.at[i, 'Deaths'])

        time = time.assign(**{input: today})
        time.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-time.csv', index=False, header=True)
        click.echo('covid-time.csv exported')

        # Update covid-lockdown.csv
        lockdown = pd.read_csv(
            '../NavigateObscurity/static/worlddata/csv/covid-lockdown.csv', delimiter=',', encoding='latin1')
        click.echo('lockdown data loaded')
        lockday = []
        lockday = lockdown.iloc[:, -1:]
        lockdown = lockdown.assign(**{input: lockday})
        lockdown.to_csv(
            r'../NavigateObscurity/worlddata/static/worlddata/csv/covid-lockdown.csv', index=False, header=True)
        click.echo('covid-lockdown.csv exported')

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
            "New Zealand"}

        years = {2015, 2016, 2017, 2018, 2019, 2020}
        weeks = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52}
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
                "New Zealand": "NZL_NP"}

            return countryCode[country]

        output = pd.DataFrame(
            columns=['Country', 'Week', 'Deaths_old', 'Deaths_2020'])

        # filter out uneeded rows
        loaded = loaded[loaded.Sex == 'b']
        loaded = loaded[loaded['Year'].isin(years)]

        for country in countries:
            for week in weeks:
                loadedFiltered = loaded[loaded.Week == week]
                loadedFiltered = loadedFiltered[loadedFiltered.CountryCode ==
                                                getCountryCode(country)]
                oldSum = 0
                latest = 0
                for row in loadedFiltered.itertuples():
                    if row.Year == 2020:
                        latest = row.DTotal
                    else:
                        oldSum += row.DTotal
                oldAverage = oldSum / 5
                output = output.append(
                    {'Country': country, 'Week': week, 'Deaths_old': oldAverage, 'Deaths_2020': latest}, ignore_index=True)

        for week in weeks:
            loadedFiltered = loaded[loaded.Week == week]
            loadedFiltered = loadedFiltered[loadedFiltered['CountryCode'].isin(
                uk)]
            oldSum = 0
            latest = 0
            i = 0
            for row in loadedFiltered.itertuples():
                if row.Year == 2020:
                    latest += row.DTotal
                    i += 1
                else:
                    oldSum += row.DTotal
            oldAverage = oldSum / 5
            if i < 3:
                latest = 0

            output = output.append({'Country': "United Kingdom", 'Week': week,
                                    'Deaths_old': oldAverage, 'Deaths_2020': latest}, ignore_index=True)
            output = output.reset_index()
            output.to_csv(r'output.csv', index=None, header=True)

    click.echo('Processing completed.')
