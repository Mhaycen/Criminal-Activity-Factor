import gdelt
from datetime import date, timedelta
import os



gd2 = gdelt.gdelt(version=2)

def get_event_perday_bycountry(event_date, country_code):
    events = gd2.Search([event_date.strftime("%Y %m %d")], table = "events", coverage=True)
    return events[events.Actor1Geo_CountryCode == country_code]

def get_events(country_code,start_date, max_days = 365):
    AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
    iterate_date = start_date
    has_events = False
    for i in range(0, max_days):
        try:
            results = get_event_perday_bycountry(start_date, country_code)
            print(iterate_date)
            if not results.empty:
                results.to_csv(AIRFLOW_HOME + '/dags/data/data.csv',index = False, mode = "a", header = False)
                has_events = True
        except ValueError as err:
            print(err)
        iterate_date -= timedelta(days=1)
    if has_events:
        print("events Pulled")
    else:
        print("No events obtained.")

            
            
           