import datetime
import re

from django.conf import settings

class StatisticFunctions():
    month_regex = re.compile('(\d+)/(\d+)')
    
    def set_database(self, request_dict):
        parameter = 'parameters[database]'
        if parameter in request_dict and request_dict[parameter] in settings.AVAILABLE_DATABASES:
            self.database = request_dict[parameter]
        else:
            self.database = settings.AVAILABLE_DATABASES[0]    
    
    def set_start_end_months(self, start_month_year, end_month_year):
        
        start_month, start_year = self.month_regex.match(start_month_year).groups()
        start_month = int(start_month)
        start_year = int(start_year)
        self.start_date = datetime.date(start_year, start_month, day=1)
        
        end_month, end_year = self.month_regex.match(end_month_year).groups()
        end_month = int(end_month)
        end_year = int(end_year)
        self.end_date = datetime.date(end_year, end_month, day=1) + datetime.timedelta(days=30)
        while self.end_date.month > end_month:
            self.end_date -= datetime.timedelta(days=1)      