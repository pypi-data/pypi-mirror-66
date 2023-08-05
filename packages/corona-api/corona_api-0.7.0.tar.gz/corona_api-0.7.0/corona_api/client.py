from datetime import datetime, timezone
from .request import RequestClient
from .statistics import *
from .exceptions import BadSortParameter, BadYesterdayParameter
from .endpoints import *


class Client:
    """
    Handles interactions with the corona.lmao.ninja API
    """
    def __init__(self, api_url='https://corona.lmao.ninja'):
        self.api_url = api_url
        self.request_client = RequestClient()

    
    def _check_sort(self, sort):
        if sort not in ["cases", "deaths", "recovered", "active", "tests",
                        "critical", "deathsPerOneMillion", "testsPerOneMillion",
                        "todayCases", "todayDeaths", "casesPerOneMillion", "active"]:
            raise BadSortParameter('Invalid sort parameter.')


    def _check_yesterday(self, value):
        if not isinstance(value, bool):
            raise BadYesterdayParameter('Value for yesterday should either be True or False')

    
    def _compile_countryInfo(self, countryInfo):
        _id = countryInfo.get("_id")
        iso2 = countryInfo.get("iso2")
        iso3 = countryInfo.get("iso3")
        _lat = countryInfo.get("lat")
        _long = countryInfo.get("long")
        flag = countryInfo.get("flag")

        info = CountryInfo(
            _id,
            iso2,
            iso3,
            _lat,
            _long,
            flag
        )

        return info

    
    def _compile_country_data(self, country_stats):
        country_name = country_stats.get("country", "Null")
        total_country_cases = country_stats.get("cases", 0)
        total_country_deaths = country_stats.get("deaths", 0)
        total_country_recoveries = country_stats.get("recovered", 0)
        today_cases = country_stats.get("todayCases", 0)
        today_deaths = country_stats.get("todayDeaths", 0)
        total_critical = country_stats.get("critical", 0)
        active = country_stats.get("active", 0)
        tests = country_stats.get("tests", 0)
        cases_per_million = country_stats.get("casesPerOneMillion", 0)
        deaths_per_million = country_stats.get("deathsPerOneMillion", 0)
        tests_per_million = country_stats.get("testsPerOneMillion", 0)
        updated_epoch = country_stats.get("updated", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        countryInfo = country_stats["countryInfo"]

        info = self._compile_countryInfo(countryInfo)
        
        return CountryStatistics(
            info,
            country_name,
            total_country_cases,
            total_country_deaths,
            total_country_recoveries,
            today_cases,
            today_deaths,
            total_critical,
            active,
            tests,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            updated
        )


    def _compile_state(self, state_dict):
        state_name = state_dict.get("state")
        total_state_cases = state_dict.get("cases", 0)
        total_state_deaths = state_dict.get("deaths", 0)
        today_cases = state_dict.get("todayCases", 0)
        today_deaths = state_dict.get("todayDeaths", 0)
        active = state_dict.get("active", 0)
        tests = state_dict.get("tests", 0)
        tests_per_million = state_dict.get("testsPerOneMillion", 0)

        state_stats = StateStatistics(
        state_name,
        total_state_cases,
        total_state_deaths,
        today_cases,
        today_deaths,
        active,
        tests,
        tests_per_million
        )

        return state_stats

    
    def _generate_history(self, historical_stats, is_county=False):
        case_history = []
        death_history = []
        recovery_history = []

        if not is_county:        
            country_name = historical_stats.get("country", "Global")
            province_name = historical_stats.get("province")
            

        else:
            country_name = historical_stats.get("province")
            province_name = historical_stats.get("county")
        
        if "timeline" not in historical_stats: #if country was 'all'
            d = historical_stats
        
        else:
            d = historical_stats["timeline"]

        recovery_history = None #state counties dont provide recovered data

        for date in list(d["cases"].keys()): #pass on all historical data. let the client decide how much of it they want
            case_history.append(HistoryEntry(date, d["cases"][date]))
            death_history.append(HistoryEntry(date, d["deaths"][date]))
            if not is_county:
                recovery_history.append(HistoryEntry(date, d["recovered"][date]))

        return HistoricalStatistics(
            country_name,
            case_history,
            death_history,
            recovery_history,
            province_name
            )


    def _compile_continent(self, data):
        name = data.get('continent')
        cases = data.get("cases", 0)
        deaths = data.get("deaths", 0)
        recoveries = data.get("recovered", 0)
        today_cases = data.get("todayCases", 0)
        today_deaths = data.get("todayDeaths", 0)
        critical = data.get("critical", 0)
        updated_epoch = data.get("updated", 0)
        active = data.get("active", cases-deaths-recoveries)
        tests = data.get("tests", 0)
        cases_per_million = data.get("casesPerOneMillion", 0)
        deaths_per_million = data.get("deathsPerOneMillion", 0)
        tests_per_million = data.get("testsPerOneMillion", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return ContinentStatistics(
            name,
            cases,
            deaths,
            recoveries,
            critical,
            active,
            tests,
            today_cases,
            today_deaths,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            updated
        )    


    async def all(self, **kwargs):
        """
        Get the global stats for Coronavirus COVID-19
        """
        get_yesterday = kwargs.get('yesterday', False)

        if get_yesterday:
            self._check_yesterday(get_yesterday)
            global_endpoint = GLOBAL_YESTERDAY.format(self.api_url)

        else:
            global_endpoint = GLOBAL_DATA.format(self.api_url)

        global_data = await self.request_client.make_request(global_endpoint)

        cases = global_data.get("cases", 0)
        deaths = global_data.get("deaths", 0)
        recoveries = global_data.get("recovered", 0)
        today_cases = global_data.get("todayCases", 0)
        today_deaths = global_data.get("todayDeaths", 0)
        total_critical = global_data.get("critical", 0)
        updated_epoch = global_data.get("updated", 0)
        active = global_data.get("active", cases-deaths-recoveries)
        tests = global_data.get("tests", 0)
        cases_per_million = global_data.get("casesPerOneMillion", 0)
        deaths_per_million = global_data.get("deathsPerOneMillion", 0)
        tests_per_million = global_data.get("testsPerOneMillion", 0)
        infected_countries = global_data.get("affectedCountries")
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return GlobalStatistics(
            cases,
            deaths,
            recoveries,
            today_cases,
            today_deaths,
            total_critical,
            active,
            tests,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            infected_countries,
            updated,
            )

    
    async def get_country_data(self, country, **kwargs):
        """
        Get the data for a specific country.
        """
        get_yesterday = kwargs.get('yesterday')

        if get_yesterday:
            self._check_yesterday(get_yesterday)
            endpoint = COUNTRY_DATA_YESTERDAY.format(self.api_url, country)
        else:
            endpoint = COUNTRY_DATA.format(self.api_url, country)

        country_stats = await self.request_client.make_request(endpoint)

        return self._compile_country_data(country_stats)

    
    async def get_all_countries(self, **kwargs):
        """
        Get the data for every infected country.
        """
        get_yesterday = kwargs.get('yesterday')
        sort = kwargs.get('sort')

        if sort and get_yesterday:
            self._check_yesterday(get_yesterday)
            self._check_sort(sort)
            endpoint = ALL_COUNTRIES_YESTERDAY_SORTED.format(self.api_url, sort)

        elif sort:
            self._check_sort(sort)
            endpoint = ALL_COUNTRIES_SORTED.format(self.api_url, sort)

        elif get_yesterday:
            self._check_yesterday(get_yesterday)
            endpoint = ALL_COUNTRIES_YESTERDAY.format(self.api_url)
        
        else:
            endpoint = ALL_COUNTRIES.format(self.api_url)
            
        all_countries = await self.request_client.make_request(endpoint)

        list_of_countries = []

        for c in all_countries:
            list_of_countries.append(self._compile_country_data(c))

        return list_of_countries
    
    
    async def get_all_states(self, **kwargs):
        """
        Get the stats for all US states
        """
        get_yesterday = kwargs.get('yesterday')
        sort = kwargs.get('sort')

        if get_yesterday:
            self._check_yesterday(get_yesterday)

        if sort:
            self._check_sort(sort)

        if sort and get_yesterday:
            endpoint = ALL_STATES_YESTERDAY_SORTED.format(self.api_url, sort)

        elif sort:
            endpoint = ALL_STATES_SORTED.format(self.api_url, sort)

        elif get_yesterday:
            endpoint = ALL_STATES_YESTERDAY.format(self.api_url)
        
        else:
            endpoint = ALL_STATES.format(self.api_url)

        state_info = await self.request_client.make_request(endpoint)

        state_data = []

        for state in state_info:
            state_stats = self._compile_state(state)
            state_data.append(state_stats)

        return state_data

    
    async def get_single_state(self, state, **kwargs):
        """
        Get the stats for a specific province of a country
        """
        get_yesterday = kwargs.get('yesterday')

        if get_yesterday:
            self._check_yesterday(get_yesterday)
            endpoint = SINGLE_STATE_YESTERDAY.format(self.api_url, state)

        else:
            endpoint = SINGLE_STATE.format(self.api_url, state)

        state_info = await self.request_client.make_request(endpoint)

        compiled_state = self._compile_state(state_info)

        return compiled_state


    async def get_country_history(self, country="all", last_days='all'):
        """
        Get historical data for a specific country or globally.
        Defaults to 'all' in order to get global data. This can be overridden by the client.
        """
        endpoint = HISTORICAL_COUNTRY.format(self.api_url, country, last_days)
        historical_stats = await self.request_client.make_request(endpoint)

        return self._generate_history(historical_stats)


    async def get_province_history(self, country, province, last_days='all'):
        """
        Get the historical data for a province within a country.
        """
        endpoint = HISTORICAL_PROVINCE.format(self.api_url, country, province, last_days)
        data = await self.request_client.make_request(endpoint)

        return self._generate_history(data)


    async def get_state_county_history(self, state, county, last_days='all'):
        """
        Get the historical data for a county within a US state.
        """
        endpoint = STATE_COUNTY.format(self.api_url, state, last_days)
        data = await self.request_client.make_request(endpoint)

        matching_county = next(place for place in data if place["province"].lower() == state.lower() \
            and place["county"].lower() == county.lower())

        return self._generate_history(matching_county, True)

    
    async def get_jhu_csse_data(self):
        """
        Get data from the JHU CSSE.
        This includes province data for several countries
        """
        endpoint = JHU_CSSE.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        statistics = []

        for cp in data:
            country = cp.get("country")
            province = cp.get("province")
            confirmed_cases = cp["stats"].get("confirmed")
            deaths = cp["stats"].get("deaths")
            recoveries = cp["stats"].get("recovered")
            _lat = float(cp["coordinates"].get("latitude")) if cp["coordinates"].get("latitude") else 0.0
            _long = float(cp["coordinates"].get("longitude")) if cp["coordinates"].get("longitude") else 0.0

            updated = datetime.strptime(cp.get('updatedAt'), '%Y-%m-%d %H:%M:%S')

            jhu_statistic = JhuCsseStatistics(
                country,
                province,
                None,
                updated,
                confirmed_cases,
                deaths,
                recoveries,
                _lat,
                _long
                )
            
            statistics.append(jhu_statistic)

        return statistics


    async def get_jhu_county_data(self, state, county):
        """
        Get the data for a specific county within a US state.
        """
        endpoint = JHU_CSSE_COUNTIES.format(self.api_url, county)
        all_matching_counties = await self.request_client.make_request(endpoint)

        matching_county = next(place for place in all_matching_counties if place["province"].lower() == state.lower() \
            and place["county"].lower() == county.lower())

        country = matching_county.get("country") #will always be 'US'
        province = matching_county.get("province")
        county_name = matching_county.get("province")
        confirmed_cases = matching_county["stats"].get("confirmed")
        deaths = matching_county["stats"].get("deaths")
        recoveries = matching_county["stats"].get("recovered")
        _lat = float(matching_county["coordinates"].get("latitude")) if matching_county["coordinates"].get("latitude") else 0.0
        _long = float(matching_county["coordinates"].get("longitude")) if matching_county["coordinates"].get("longitude") else 0.0

        updated = datetime.strptime(matching_county.get('updatedAt'), '%Y-%m-%d %H:%M:%S')

        stat = JhuCsseStatistics(
                country,
                province,
                county_name,
                updated,
                confirmed_cases,
                deaths,
                recoveries,
                _lat,
                _long
                )

        return stat

    
    async def get_all_continents(self, **kwargs):
        """
        Get the statistics for world continents.
        """
        get_yesterday = kwargs.get('yesterday')
        sort = kwargs.get('sort')

        if get_yesterday:
            self._check_yesterday(get_yesterday)

        if sort:
            self._check_sort(sort)

        if sort and get_yesterday:
            endpoint = ALL_CONTINENTS_YESTERDAY_SORTED.format(self.api_url, sort)

        elif sort:
            endpoint = ALL_CONTINENTS_SORTED.format(self.api_url, sort)

        elif get_yesterday:
            endpoint = ALL_CONTINENTS_YESTERDAY.format(self.api_url)
        
        else:
            endpoint = ALL_CONTINENTS.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        continents = []

        for c in data:
            continents.append(self._compile_continent(c))

        return continents


    async def get_single_continent(self, continent, **kwargs):
        """
        Get the statistics for a single continent.
        """
        get_yesterday = kwargs.get('yesterday')

        if get_yesterday:
            self._check_yesterday(get_yesterday)
            endpoint = CONTINENT_YESTERDAY.format(self.api_url, continent)
        else:
            endpoint = CONTINENT_DATA.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        return self._compile_continent(data)

        