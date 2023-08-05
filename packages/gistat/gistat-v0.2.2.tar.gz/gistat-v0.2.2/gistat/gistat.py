from selenium import webdriver
from datetime import datetime
import os


class GiStat:
    STATISTIC_URL = 'https://gismoldova.maps.arcgis.com/apps/opsdashboard/index.html#/d274da857ed345efa66e1fbc959b021b'

    def __init__(self, debug=False, firefox_path='./geckodriver', timeout=120):
        if not os.path.exists(firefox_path):
            raise Exception('Cannot find geckodriver!')

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
            'confirmed': $("div.dock-element:eq(4) text").eq(1).text(),
            'recovered': $("div.dock-element:eq(5) text").eq(1).text(),
            'suspected': $("div.dock-element:eq(6) text").eq(1).text(),
            'deaths'   : $("div.dock-element:eq(7) text").eq(0).text(),
            'monitored': $("div.dock-element:eq(8) text").eq(1).text()
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
        $("div.dock-element:eq(11) .external-html").each(function(i, el) {
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
            let elements = $("div.dock-element:eq(11) .external-html");
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

    def get_cases_by_age(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
            const regexp = /([<>0-9]+(?:\s*-\s*[0-9]+)?) (luni|ani) \s*([0-9]+)/g;
            let output = [];
            $("div.dock-element:eq(12) .amcharts-graph-column").each(function(i, el) {
                var aria = $(el).attr('aria-label');
                if (typeof aria == 'string') {
                    var parsed = [...aria.matchAll(regexp)];
                    var range = parsed[0][1].replace(' ', '');
                    var range_type = parsed[0][2];
                    var cases = parsed[0][3];
                  output.push({
                    'range': range,
                    'type': range_type,
                    'cases': cases
                  });
                }
            });
    
            return output;
        '''

        cases_by_age = self.driver.execute_script(js)

        return cases_by_age

    def get_other_cases(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
            let other_stat = {
                'men': $("div.dock-element:eq(13) .amcharts-legend-value").eq(0).text().trim(),
                'women': $("div.dock-element:eq(13) .amcharts-legend-value").eq(1).text().trim(),
                'cases_imported': $("div.dock-element:eq(15) .amcharts-pie-label tspan").eq(4).text().trim(),
                'cases_local': $("div.dock-element:eq(15) .amcharts-pie-label:eq(0) tspan").eq(1).text().trim(),
                'pregnant': $("div.dock-element:eq(17) .responsive-text-label text").eq(2).text().trim()
            };
            
            return other_stat;
        '''

        other_stat = self.driver.execute_script(js)

        return other_stat

    def get_update_time(self):
        if not self._initialized:
            raise Exception('Need to initialize (load)')

        js = '''
            return $("div.dock-element:eq(19) .external-html strong").text();
        '''

        update_time = self.driver.execute_script(js)

        return datetime.strptime(update_time, '%d/%m/%Y,%H:%M')

    def stop(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()
