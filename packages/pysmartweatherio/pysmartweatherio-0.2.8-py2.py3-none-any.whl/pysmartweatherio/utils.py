import sys
import datetime


class UnicodeMixin(object):

    """Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3."""

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')


class PropertyUnavailable(AttributeError):
    pass

class Conversion:

    """
    Conversion Class to convert between different units.
    WeatherFlow always delivers values in the following formats:
    Temperature: C
    Wind Speed: m/s
    Wind Direction: Degrees
    Pressure: mb
    Distance: km
    """

    def temperature(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value F
            return round((value*9/5)+32,1)
        else:
            # Return value C
            return round(value,1)

    def volume(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in
            return round(value * 0.0393700787,2)
        else:
            # Return value mm
            return round(value,1)

    def rate(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in
            return float(value * 60 * 0.0393700787)
        else:
            # Return value mm
            return float(value * 60)

    def pressure(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value inHg
            return round(value * 0.0295299801647,3)
        else:
            # Return value mb
            return round(value,1)

    def speed(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi/h
            return round(value*2.2369362921,1)
        else:
            # Return value in m/s
            return round(value,1)

    def distance(self, value, unit):
        if unit.lower() == 'imperial':
            # Return value in mi
            return round(value*0.621371192,1)
        else:
            # Return value in m/s
            return round(value,0)

    def wind_direction(self, bearing):
        direction_array = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
        direction = direction_array[int((bearing + 11.25) / 22.5)]
        return direction

    def epoch_to_datetime(self, value):
        """Converts EPOC time to Date Time String."""
        timestring = datetime.datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
        return timestring

