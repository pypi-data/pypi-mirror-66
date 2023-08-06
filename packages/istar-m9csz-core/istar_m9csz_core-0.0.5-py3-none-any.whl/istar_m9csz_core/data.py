import xarray
from typing import List
from .structs.realization import Realization
from .structs.latlon import LatLon
from .appdata import config, data_format
import numpy as np

"""
A wrapper around an xarray object exposing easy ways to visualize a collection
of realization's data either as a map or a line.
"""

class Data(object):

    # Must be set externally, with e.g. Data.m9_path = 'a/path'
    m9_path : str = None
    m9csz_path : str = None
    z_path : str = None

    def __init__(self,
            realizations : [Realization, List[Realization]]):
        # Error if no path supplied to class
        if Data.m9_path is None\
                or Data.m9csz_path is None\
                or Data.m9csz_path is None:
            raise ValueError('Data.m9_path, Data.m9csz_path, Data.z_path must be set')
        # Always turn into list
        if not isinstance(realizations, list):
            realizations = [realizations]
        # Load Xarray data
        self.__data = self.__load_data(realizations)

    def __load_data(self, realizations: List[Realization]) -> List[str]:
        def get_paths(
                realizations : List[Realization],
                project_path : str) -> List[str] :
            """Gets path on disk for each realization"""
            from os import path
            base : str = project_path
            # return [path.join(base, r.folder_name, r.zone, 'Xarray.nc')
            return [path.join(base, r.file_path) for r in realizations]

        def get_data(
                realizations : List[Realization],
                project_path : str) -> xarray.Dataset :
            """Loads xarray data from disk"""
            realizations_xarray = xarray.DataArray(
                    [r.into_string() for r in realizations],
                    name='realization',
                    dims={'realization': realizations})
            # Build paths for each realization
            paths : List[str] = get_paths(realizations, project_path)
            # Get data
            return xarray.open_mfdataset(
                    paths,
                    coords='minimal',
                    combine='nested',
                    concat_dim=[realizations_xarray])

        m9_realizations = [r for r in realizations if r.has_m9]
        print(m9_realizations)

        # Load M9 data
        m9_data = None
        if m9_realizations:
            m9_data = get_data(m9_realizations, Data.m9_path)
        # Prepend `m9_` to m9 spectral data, so m9csz data names don't conflict
        if m9_data:
            rename_fields = ['period', 'spectra_x', 'spectra_y']
            m9_data = m9_data.rename({d : f'm9_{d}' for d in rename_fields})
        try:
            # Attempt to load M9CSZ data
            try:
                m9csz_data = get_data(realizations, Data.m9csz_path)
            except:
                raise ValueError('Error loading m9csz data')
            if m9_data:
                try:
                    return xarray.combine_by_coords(
                            [m9_data, m9csz_data],
                            join='outer')
                except: raise ValueError('Error combining m9 and m9csz data.')
            return m9csz_data

        except ValueError as e:
            # On failure, use M9 data instead of halting
            print(e)
            print('Using m9 data...')
            return m9_data

    @property
    def data(self):
        return self.__data

    def get_map(self,
            field: str,
            time: float,
            ):
        if field is None:
            raise ValueError('Must specify a map field')
        if time is None:
            time = 0.0
        data = self.__data
        try:
            time_axis = data_format['xarray']['m9csz']['fields'][field]['line_axis']
            if time_axis == 'time':
                data = data.where(data.time < data.CutOffTime)
            data = data[field].sel({ time_axis: time }, method='nearest', drop=True)
        except:
            data = data[field]
        data = np.abs(data)
        data = data.mean(dim='realization')
        data = data.squeeze()
        return data

    def get_line(self,
            field: str,
            latlon: LatLon):
        time_axis = data_format['xarray']['m9csz']['fields'][field]['line_axis']
        data = self.__data
        if time_axis == 'time':
            data = data.where(data.time < data.CutOffTime)
        data = data[field].sel(
                { 'lat': latlon.lat, 'lon': latlon.lon },
                method='nearest',
                drop=True)
        data = data.mean(dim='realization')
        data = data.squeeze()
        return data
