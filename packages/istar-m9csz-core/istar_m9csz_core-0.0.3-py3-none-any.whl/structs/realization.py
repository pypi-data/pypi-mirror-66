zones = ['A', 'B', 'C', 'D', 'E']
realization_numbers = [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 31, 32, 33
        ]
realization_strings = [
        'mean',
        'std',
        'std-'
        ]
realization_keys = [
        *realization_numbers,
        *realization_strings,
        ]

class Realization(object):
    __slots__ = [ 'zone', 'key' ]
    def __init__(self,
            zone: str,
            key: [int, str]):
        if zone not in zones:
            raise ValueError('Invalid realization zone')
        if key not in realization_keys:
            raise ValueError('Invalid realization key')
        self.zone = zone
        self.key = key

    @staticmethod
    def valid_zones():
        return zones.copy()

    @staticmethod
    def valid_realization_numbers():
        return realization_numbers.copy()


    @staticmethod
    def from_string(string: str):
        """
        Creates a realization from a string like: C27 or Dmean
        """
        zone = string[0]
        key = ''
        try:
            key = int(string[1:])
        except:
            key = string[1:]
        return Realization(zone, key)

    def into_string(self):
        return self.__str__()

    def __str__(self):
        return f'{self.zone}{self.key}'

    @property
    def file_path(self):
        from os import path
        if self.key in realization_keys:
            return path.join(self.folder_name, self.zone, 'Xarray.nc')

    @property
    def folder_name(self):
        from os import path
        if self.key == 2:
            return 'csz002_sd10'
        elif self.key in realization_numbers:
            return f'csz{self.key:03d}'
        elif self.key in realization_strings:
            return path.join('All', self.key)
        raise f'Key "{self.key}" has no associated folder name'

    @property
    def has_m9(self):
        return self.key in realization_numbers
