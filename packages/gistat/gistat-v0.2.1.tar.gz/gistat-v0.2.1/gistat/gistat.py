from selenium import webdriver
import os


class GiStat:
    STATISTIC_URL = 'https://gismoldova.maps.arcgis.com/apps/opsdashboard/index.html#/d274da857ed345efa66e1fbc959b021b'

    def __init__(self, debug=False, firefox_path='./geckodriver', timeout=120):
        if not debug:
            # Hide Browser
            os.environ['MOZ_HEADLESS'] = '1'

        self.driver = webdriver.Firefox(executable_path=firefox_path)
        self.driver.set_script_timeout(timeout)
        self._initialized = False

    def load(self):
        self.driver.get(self.STATISTIC_URL)
        self._initialized = True

    def get_general_stat(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
        let mainStatistics = {
            'confirmed': $("div.dock-element:eq(3) text").eq(1).text(),
            'recovered': $("div.dock-element:eq(4) text").eq(1).text(),
            'suspected': $("div.dock-element:eq(5) text").eq(1).text(),
            'deaths'   : $("div.dock-element:eq(6) text").eq(0).text(),
            'monitored': $("div.dock-element:eq(7) text").eq(1).text()
        };
        
        return mainStatistics;
        '''

        main_statistics = self.driver.execute_script(js)

        return main_statistics

    def get_cases_by_country(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
        let country = [];
        $("div.dock-element:eq(10) .external-html").each(function(i, el) {
            country.push({'country': $(el).find('span').eq(0).text().trim(), 'cases': $(el).find('span').eq(4).text().trim()})
        });

        return country;
        '''

        cases_by_country = self.driver.execute_script(js)

        return cases_by_country

    def get_full_cases_by_country(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
            let elements = $("div.dock-element:eq(10) .external-html");
            let totalElements = elements.length;
            let n = 0;
            
            let details = [];
            
            // First Click
            elements.eq(n).click();
            
            const myLoop = async _ => {
                while(n < totalElements) {
                    let cityName = elements.eq(n).find('span').eq(0).text().trim();
                    let countryDetailsName = $(".ember-view div span.esriDateValue").parent().text();
            
                    if (countryDetailsName !== '' && countryDetailsName.indexOf(cityName) !== -1) {
                        let displayInfo = $(".feature-description.ember-view span.esriNumericValue");
            
                        let confirmedCases = displayInfo.eq(0).text();
                        let deaths = displayInfo.eq(1).text();
                        let recoveredCases = displayInfo.eq(2).text();
                        let monitoredCases = displayInfo.eq(3).text();
            
                        details.push({
                            'city': cityName,
                            'confirmed': confirmedCases,
                            'deaths': deaths,
                            'recovered': recoveredCases,
                            'monitored': monitoredCases
                        });
            
                        console.log(confirmedCases, deaths, recoveredCases, monitoredCases);
            
                        // Go Next
                        n++;
                        elements.eq(n).click();
                    }
            
                    await delay(100);
                }
            }
            
            const delay = ms => new Promise(res => setTimeout(res, ms));
            let done = arguments[0];
            myLoop().then(() => {
                done(details);
            });
        '''

        cases_by_country = self.driver.execute_async_script(js)

        return cases_by_country

    def stop(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()
