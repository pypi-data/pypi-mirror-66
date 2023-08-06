"""
LatLon holds a latitude and longitude location and provides several helper
functions.
"""

class LatLon(object):
    __slots__ = [ 'lat', 'lon' ]
    def __init__(self, lat: float, lon: float):
        self.lat : float = lat
        self.lon : float = lon
        # if not utils.latlon_in_zone(self, 'B') and not utils.latlon_in_zone(self, 'D'):
        #     raise ValueError(f'{self} outside of project boundary')

    def __eq__(self, other: any):
        if isinstance(other, LatLon):
            return self.lat == other.lat and self.lon == other.lon
        return False

    def __repr__(self):
        return f'LatLon({self.lat}, {self.lon})'

    def __str__(self):
        return f'{self.lat:.2f}:{self.lon:.2f}'


    def to_tuple(self):
        return (self.lat, self.lon)


    # TODO is this used?
    def to_dims(self):
        return {
                'lat': self.lat,
                'lon': self.lon,
                }


    def get_label(self):
        return f'({self.lat:.2f}, {self.lon:.2f})'

    @staticmethod
    def from_string(string: str):
        import re
        # [lat, lon] = string.split(',')
        [lat, lon] = re.split(r'[:,_]', string)
        lat = float(lat)
        lon = -float(lon)
        return LatLon(lat, lon)

    @staticmethod
    def Portland():
        # return LatLon(45.5155, -122.668)
        return LatLon(45.5051, -122.6750)
