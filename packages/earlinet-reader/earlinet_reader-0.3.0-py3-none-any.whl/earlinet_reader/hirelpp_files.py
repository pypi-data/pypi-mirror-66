import datetime
import logging
import netCDF4 as netcdf
import numpy as np
import os
import pytz

logger = logging.getLogger(__name__)


class HiRElPPFile:
    elastic_flag = 15

    def __init__(self, file_path, read_now=True):
        self.file_path = file_path

        if read_now:
            self.read_file()

    def read_file(self):
        """ Read required data from the NetCDF file."""
        with netcdf.Dataset(self.file_path) as f:
            self._import_metadata(f)
            self._import_data(f)

    def _import_data(self, f):
        """ Read data from an open file.

        Parameters
        ----------
        f : netcdf.Dataset object
           An open netcdf dataset.
        """
        self.attenuated_backscatter = f.variables['attenuated_backscatter'][:]
        self.attenuated_backscatter_error = f.variables['attenuated_backscatter_statistical_error'][:]
        self.attenuated_backscatter_scatterers = f.variables['attenuated_backscatter_scatterers'][:]
        self.attenuated_backscatter_range = f.variables['attenuated_backscatter_range'][:]
        self.attenuated_backscatter_detection_wavelength = f.variables[
                                                               'attenuated_backscatter_detection_wavelength'][:]
        self.attenuated_backscatter_emission_wavelength = f.variables[
                                                              'attenuated_backscatter_emission_wavelength'][:]
        try:
            calibration = f.variables['attenuated_backscatter_calibration'][:]
        except:
            calibration = None
        self.signal_calibration = calibration

        try:
            calibration_error = f.variables['attenuated_backscatter_calibration_statistical_error'][:]
        except:
            calibration_error = None
        self.signal_calibration_statistica_error = calibration_error

        self.laser_pointing_angle = f.variables['laser_pointing_angle'][:]
        self.laser_pointing_angle_of_profile = f.variables['laser_pointing_angle_of_profiles'][:]
        self.accumulated_shots = f.variables['shots'][:]

        try:
            self.vldr = f.variables['volume_linear_depolarization_ratio'][:]
            self.has_depolarization = True
        except:
            self.has_depolarization = False

        if self.has_depolarization:
            self.vldr_channel_names = f.variables['volume_linear_depolarization_ratio_channel_name'][:]
            self.vldr_wavelength = f.variables['volume_linear_depolarization_ratio_wavelength'][:]
            self.vldr_range = f.variables['volume_linear_depolarization_ratio_range'][:]
            self.vldr_scatterers = f.variables['volume_linear_depolarization_ratio_scatterers'][:]
            self.vldr_error = f.variables['volume_linear_depolarization_ratio_statistical_error'][:]

        self.background = f.variables['atmospheric_background'][:]
        self.background_max = f.variables['atmospheric_background_max'][:]
        self.background_min = f.variables['atmospheric_background_min'][:]
        self.background_stdev = f.variables['atmospheric_background_stdev'][:]
        self.background_sterr = f.variables['atmospheric_background_sterr'][:]

    def _import_metadata(self, f):
        """ Read metadata from an open file.

        Parameters
        ----------
        f : netcdf.Dataset object
           An open netcdf dataset.
        """
        self.time = f.variables['time'][:]
        self.time_bounds = f.variables['time_bounds'][:]
        self.z = f.variables['altitude'][0, :]
        self.station_altitude = f.variables['station_altitude'][:]
        self.longitude = f.variables['longitude'][:]
        self.latitude = f.variables['latitude'][:]
        self.measurement_ID = f.measurement_ID
        self.hoi_system_ID = f.hoi_system_ID
        self.measurement_start_datetime_str = f.measurement_start_datetime
        self.measurement_stop_datetime_str = f.measurement_stop_datetime
        self.start_time = datetime.datetime.strptime(f.measurement_start_datetime, '%Y-%m-%dT%H:%M:%SZ')
        self.stop_time = datetime.datetime.strptime(f.measurement_stop_datetime, '%Y-%m-%dT%H:%M:%SZ')
        self.institution = f.institution
        self.system = f.system
        self.station_id = f.station_ID

        self.pi = getattr(f, 'PI', '')
        self.pi_affiliation = getattr(f, 'PI_affiliation', '')
        self.pi_affiliation_acronym = getattr(f, 'PI_affiliation_acronym', '')
        self.pi_address = getattr(f, 'PI_address', '')
        self.pi_phone = getattr(f, 'PI_phone', '')
        self.pi_email = getattr(f, 'PI_email', '')

        self.do = getattr(f, 'Data_Originator', '')
        self.do_affiliation = getattr(f, 'Data_Originator_affiliation', '')
        self.do_affiliation_acronym = getattr(f, 'Data_Originator_affiliation_acronym', "")
        self.do_address = getattr(f, 'Data_Originator_address', '')
        self.do_phone = getattr(f, 'Data_Originator_phone', '')
        self.dp_email = getattr(f, 'Data_Originator_email', '')

        self.comments = f.comment

        self.source = f.source
        self.title = f.title
        self.references = f.references
        self.processor_version = f.processor_version
        self.processor_name = f.processor_name

        try:
            self.location = f.location
        except Exception as e:
            self.location = ''

        self.channel_names = f.variables['attenuated_backscatter_channel_name'][:]

        self.number_of_profiles = len(self.time)

        self.dts = np.diff(self.time)  # Should be self.time_bounds[:, 1] - self.time_bounds[:, 0]
        self.dzs = np.diff(self.z)

        if len(set(self.dzs)) > 1:
            logger.warning('More than one range resolutions found: %s. Using first value.' % set(self.dzs))

        self.dz = self.dzs[0]

        if len(set(self.dts)) > 1:
            logger.warning('More than one time resolutions found: %s. Using largest value.' % set(self.dts))

        self.dt = np.max(self.dts)

        self.t = [datetime.datetime.fromtimestamp(t, pytz.UTC) for t in self.time]
        self.t_start = [datetime.datetime.fromtimestamp(t, pytz.UTC) for t in self.time_bounds[:, 0]]
        self.t_stop = [datetime.datetime.fromtimestamp(t, pytz.UTC) for t in self.time_bounds[:, 1]]

    def read_metadata(self):
        """ Read only metadata from Hirelpp file."""
        with netcdf.Dataset(self.file_path) as f:
            self._import_metadata(f)

    def get_elastic_idxs(self):
        """ Return the indices of elastic channels. """
        idxs = np.where(self.attenuated_backscatter_scatterers == self.elastic_flag)[0]
        return idxs

    def get_wavelength_idxs(self, wavelength, tolerance=5):
        """
        Return the indices of channels detecting the specific wavelength.

        Parameters
        ----------
        wavelength : float
           The channel detection wavelength (nm)
        tolerance : float
           The accepted tolerance for wavelegnth (nm)
        """
        min_wavelength = wavelength - tolerance
        max_wavelegnth = wavelength + tolerance

        idxs = np.where((self.attenuated_backscatter_detection_wavelength > min_wavelength) &
                        (self.attenuated_backscatter_detection_wavelength < max_wavelegnth))[0]

        return idxs

    def convert_to_geoms(self, output_dir, location, affiliation=None):
        """ Convert the input file to something looking like GEOMS format.

        The aim is to demonstrate the possiblities and limitation of GEOMS format,
        not to make a full GEOMS-compatible format.

        Parameters
        ----------
        output_dir : str
           Directory of output file. Filename is creates automatically.
        location : str
           Location name, to be used in filename (e.g. bucharest).
        """
        # Affiliation should be something like "inoe", to be used in the filename
        if affiliation is None:
            if self.pi_affiliation_acronym:
                affiliation = self.pi_affiliation_acronym
            else:
                affiliation = self.station_id

        if len(self.laser_pointing_angle) != 1:
            raise ValueError("GEOMS converter does not currently support more than one pointing angles per profile.")

        time_size = len(self.time)
        altitude_size = len(self.z)
        backscatter_size = len(self.channel_names)

        if self.has_depolarization:
            depolarization_size = len(self.vldr_channel_names)
        else:
            depolarization_size = 0

        start_time = self.start_time.strftime('%Y%m%dT%H%M%SZ')
        stop_time = self.stop_time.strftime('%Y%m%dT%H%M%SZ')
        # What is the dataname identifier
        output_filename = 'groundbased_lidar.aerosol_{0}001_{1}_{2}_{3}.nc'.format(affiliation.lower(),
                                                                                   location.lower(),
                                                                                   start_time.lower(),
                                                                                   stop_time.lower())
        output_path = os.path.join(output_dir, output_filename)

        self.initialize_geoms_file(
            output_path, time_size, altitude_size, backscatter_size, depolarization_size,
            start_time, stop_time)

        self.fill_geoms_file(output_path)

    def fill_geoms_file(self, output_path, min_idx=None, max_idx=None, min_output_idx=None, max_output_idx=None):
        """ Copy hirelpp data to an initialized geoms file. """

        with netcdf.Dataset(output_path, 'a') as geoms_file:

            # geoms_file = netcdf.Dataset(output_path, 'a')

            vars = geoms_file.variables  # Shorthand
            altitude = vars['ALTITUDE']
            altitude_inst = vars['ALTITUDE.INSTRUMENT']
            atmospheric_background = vars['BACKGROUND.ATMOSPHERIC']
            atmospheric_background_max = vars['BACKGROUND.ATMOSPHERIC_MAXIMUM']
            atmospheric_background_min = vars['BACKGROUND.ATMOSPHERIC_MINIMUM']
            atmospheric_background_stdev = vars['BACKGROUND.ATMOSPHERIC_STANDARD.DEVIATION']
            atmospheric_background_sterr = vars['BACKGROUND.ATMOSPHERIC_STANDARD.ERROR']
            backscatter = vars['BACKSCATTER.COEFFICIENT.ATTENUATED']
            backscatter_calibration = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT']
            backscatter_calibration_error = vars[
                'BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT_UNCERTAINTY.RANDOM']
            backscatter_channel = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME']
            backscatter_detection_wl = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_DETECTION.WAVELENGTH']
            backscatter_emission_wl = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_EMISSION.WAVELENGTH']
            backscatter_error = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_UNCERTAINTY.RANDOM']
            backscatter_range_type = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_RANGE.TYPE']
            backscatter_scatterers = vars['BACKSCATTER.COEFFICIENT.ATTENUATED_SCATTERERS']
            datetime_start = vars['DATETIME.START']
            datetime_stop = vars['DATETIME.STOP']
            datetime_var = vars['DATETIME']
            latitude = vars['LATITUDE.INSTRUMENT']
            longitude = vars['LONGITUDE.INSTRUMENT']
            viewing_angle = vars['ANGLE.VIEW_ZENITH']

            if self.has_depolarization:
                depol_channel = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME']
                vldr = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO']
                vldr_error = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO_UNCERTAINTY.RANDOM']
                vldr_range_type = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO_RANGE.TYPE']
                vldr_scatterers = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO_SCATTERERS']
                vldr_wl = vars['VOLUME.LINEAR.DEPOLARIZATION.RATIO_EMISSION.WAVELENGTH']

            # Assign values
            altitude[:] = self.z
            datetime_var[min_output_idx:max_output_idx] = self.epoch_to_mjd2k(np.mean(self.time_bounds, axis=1))[
                                                          min_idx:max_idx]
            datetime_start[min_output_idx:max_output_idx] = self.epoch_to_mjd2k(self.time_bounds[:, 0])[min_idx:max_idx]
            datetime_stop[min_output_idx:max_output_idx] = self.epoch_to_mjd2k(self.time_bounds[:, 1])[min_idx:max_idx]
            backscatter_channel[:] = self.channel_names
            latitude[:] = self.latitude
            longitude[:] = self.longitude
            altitude_inst[:] = self.station_altitude
            viewing_angle[:] = self.laser_pointing_angle[0]
            backscatter_emission_wl[:] = self.attenuated_backscatter_emission_wavelength
            backscatter_detection_wl[:] = self.attenuated_backscatter_detection_wavelength
            backscatter_range_type[:] = self.attenuated_backscatter_range
            backscatter_scatterers[:] = self.attenuated_backscatter_scatterers
            backscatter[min_output_idx:max_output_idx, :, :] = np.transpose(self.attenuated_backscatter, (1, 2, 0))[
                                                               min_idx:max_idx, :, :]
            backscatter_error[min_output_idx:max_output_idx, :, :] = np.transpose(self.attenuated_backscatter_error,
                                                                                  (1, 2, 0))[min_idx:max_idx, :, :]
            backscatter_calibration[min_output_idx:max_output_idx, :] = np.transpose(self.signal_calibration, (1, 0))[
                                                                        min_idx:max_idx, :]
            backscatter_calibration_error[min_output_idx:max_output_idx, :, ] = np.transpose(
                self.signal_calibration_statistica_error, (1, 0))[min_idx:max_idx, :]

            if self.has_depolarization:
                depol_channel[:] = self.vldr_channel_names
                vldr_wl[:] = self.vldr_wavelength
                vldr_range_type[:] = self.vldr_range
                vldr_scatterers[:] = self.vldr_scatterers
                vldr[min_output_idx:max_output_idx, :, :] = np.transpose(self.vldr, (1, 2, 0))[min_idx:max_idx, :, :]
                vldr_error[min_output_idx:max_output_idx, :, :] = np.transpose(self.vldr_error, (1, 2, 0))[
                                                                  min_idx:max_idx, :, :]

            atmospheric_background[min_output_idx:max_output_idx, :] = np.transpose(self.background, (1, 0))[
                                                                       min_idx:max_idx, :]
            atmospheric_background_stdev[min_output_idx:max_output_idx, :] = np.transpose(self.background_stdev,
                                                                                          (1, 0))[min_idx:max_idx, :]
            atmospheric_background_sterr[min_output_idx:max_output_idx, :] = np.transpose(self.background_sterr,
                                                                                          (1, 0))[min_idx:max_idx, :]
            atmospheric_background_min[min_output_idx:max_output_idx, :] = np.transpose(self.background_min, (1, 0))[
                                                                           min_idx:max_idx, :]
            atmospheric_background_max[min_output_idx:max_output_idx, :] = np.transpose(self.background_max, (1, 0))[
                                                                           min_idx:max_idx, :]

            # geoms_file.close()

    def initialize_geoms_file(self, output_path, time_size, altitude_size, backscatter_size,
                              depolarization_size, start_time, stop_time):
        """ Initialize variables in an open GEOMS file.

        Parameters
        ----------
        output_path : str
           Output path
        time_size : int
           Length of the time axis
        altitude_size : int
           Length of the altitude axis
        backscatter_size : int or None
           The number of backscatter channels in the file.
        depolarization_size : int
           The number of depolarization channels in the file.
        start_time : str
           String representing the star time (format: YYYYMMDDTHHMMSSZ)
        stop_time : str
           String representing the stop time (format: YYYYMMDDTHHMMSSZ)
        """
        output_filename = os.path.basename(output_path)

        # TODO: Add data submitter name, affiliation (? Submitter to SCC, or further database?)
        # TODO: Setup a unique *numeric* instrument ID. Maybe HOI system ID is OK. Note: In this sense, GEOMS goes beyond a data format and damands a specific insfrastucture managment.
        # TODO: Acronym of stations (separate from full name)
        # TODO: Have a unique numeric ID to identify the DATA_FILE_VERSION (e.g. 001=nrt data, 002=analyzed with ECMWF).

        with netcdf.Dataset(output_path, 'w') as geoms_file:

            geoms_file.DATA_DESCRIPTION = self.title
            geoms_file.DATA_DISCIPLINE = 'ATMOSPHERIC.PHYSICS;REMOTE.SENSING;GROUNDBASED'
            geoms_file.DATA_GROUP = 'EXPERIMENTAL;PROFILE.STATIONARY'
            geoms_file.DATA_LOCATION = self.location.replace(', ', '.').replace(',', '.').replace(' ',
                                                                                                  '.')  # TODO: This should be chosen from a fixed list!!! https://avdc.gsfc.nasa.gov/index.php?site=2024100160&GEOMS=DATA_LOCATION
            geoms_file.DATA_SOURCE = 'LIDAR.AEROSOL_EARLINET{0}'.format(
                self.hoi_system_ID)  # TODO: Add acronym after the underscore
            geoms_file.DATA_START_DATE = start_time
            geoms_file.DATA_STOP_DATE = stop_time
            geoms_file.DATA_FILE_VERSION = '001'  # TODO: Choose this dynamically
            geoms_file.DATA_MODIFICATION = 'Version 001, Automatic NRT HiRELPP processing.'
            geoms_file.DATA_RULES_OF_USE = 'Refer to EARLINET data policy, https://earlinet.org/index.php?id=127'
            geoms_file.DATA_QUALITY = 'Data following EARLINET QA procedures. Processed with the SCC: {0}'.format(
                self.references)
            geoms_file.DATA_PROCESSOR = '{0}v{1}'.format(self.processor_name, self.processor_version)
            geoms_file.FILE_NAME = output_filename
            geoms_file.FILE_GENERATION_DATE = datetime.datetime.utcnow().isoformat()
            geoms_file.FILE_ACCESS = 'DIVA'  # TODO: Add FILE_ACCESS to allowed project
            geoms_file.FILE_META_VERSION = '00R000;CUSTOM'  # TODO: How is metadata version defined?
            geoms_file.FILE_DOI = ' '

            geoms_file.PI_NAME = self.pi
            geoms_file.PI_AFFILIATION = self.pi_affiliation
            geoms_file.PI_ADDRESS = self.pi_address
            geoms_file.PI_EMAIL = self.pi_email

            geoms_file.DO_NAME = self.do
            geoms_file.DO_AFFILIATION = self.do_affiliation
            geoms_file.DO_ADDRESS = self.do_address
            geoms_file.DO_EMAIL = self.dp_email

            # Dimensions
            geoms_file.createDimension('DATETIME', time_size)
            geoms_file.createDimension('ALTITUDE', altitude_size)
            geoms_file.createDimension('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME', backscatter_size)
            if self.has_depolarization:
                geoms_file.createDimension('VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME', depolarization_size)

            # Variables
            altitude = geoms_file.createVariable('ALTITUDE', 'f4', dimensions=('ALTITUDE',), )
            altitude.VAR_NAME = 'ALTITUDE'
            altitude.VAR_DESCRIPTION = "altitude above sea level"
            altitude.VAR_SIZE = '{0}'.format(altitude_size)
            altitude.VAR_DEPEND = 'ALTITUDE'
            altitude.VAR_DATA_TYPE = 'REAL'
            altitude.VAR_UNITS = 'm'
            altitude.VAR_SI_CONVERSION = '0;1;m'
            altitude.VAR_VALID_MIN = -413.0  # Minimum altitude on earth
            altitude.VAR_VALID_MAX = 120000.0  # Very high (used in an NDACC file)
            altitude.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            datetime_var = geoms_file.createVariable('DATETIME', 'f8', dimensions=('DATETIME',), )
            datetime_var.VAR_NAME = 'DATETIME'
            datetime_var.VAR_DESCRIPTION = "average time of lidar profile"
            datetime_var.VAR_SIZE = '{0}'.format(time_size)
            datetime_var.VAR_DEPEND = 'DATETIME'
            datetime_var.VAR_DATA_TYPE = 'DOUBLE'
            datetime_var.VAR_UNITS = 'MJD2K'
            datetime_var.VAR_SI_CONVERSION = "0.0;86400.0;s"
            datetime_var.VAR_VALID_MIN = -36600.0  # Used in an NDACC file
            datetime_var.VAR_VALID_MAX = 36600.0  # Used in an NDACC file
            datetime_var.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            datetime_start = geoms_file.createVariable('DATETIME.START', 'f8', dimensions=('DATETIME',), )
            datetime_start.VAR_NAME = 'DATETIME.START'
            datetime_start.VAR_DESCRIPTION = "start time of lidar profile"
            datetime_start.VAR_SIZE = '{0}'.format(time_size)
            datetime_start.VAR_DEPEND = 'DATETIME'
            datetime_start.VAR_DATA_TYPE = 'DOUBLE'
            datetime_start.VAR_UNITS = 'MJD2K'
            datetime_start.VAR_SI_CONVERSION = "0.0;86400.0;s"
            datetime_start.VAR_VALID_MIN = -36600.0  # Used in an NDACC file
            datetime_start.VAR_VALID_MAX = 36600.0  # Used in an NDACC file
            datetime_start.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            datetime_stop = geoms_file.createVariable('DATETIME.STOP', 'f8', dimensions=('DATETIME',), )
            datetime_stop.VAR_NAME = 'DATETIME.STOP'
            datetime_stop.VAR_DESCRIPTION = "stop time of lidar profile"
            datetime_stop.VAR_SIZE = '{0}'.format(time_size)
            datetime_stop.VAR_DEPEND = 'DATETIME'
            datetime_stop.VAR_DATA_TYPE = 'DOUBLE'
            datetime_stop.VAR_UNITS = 'MJD2K'
            datetime_stop.VAR_SI_CONVERSION = "0.0;86400.0;s"
            datetime_stop.VAR_VALID_MIN = -36600.0  # Used in an NDACC file
            datetime_stop.VAR_VALID_MAX = 36600.0  # Used in an NDACC file
            datetime_stop.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            backscatter_channel = geoms_file.createVariable('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME', str,
                                                            dimensions=(
                                                                'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_channel.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_channel.VAR_DESCRIPTION = "channel name according to SCC"
            backscatter_channel.VAR_SIZE = '{0}'.format(backscatter_size)
            backscatter_channel.VAR_DEPEND = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_channel.VAR_DATA_TYPE = 'STRING'
            backscatter_channel.VAR_UNITS = ''
            backscatter_channel.VAR_SI_CONVERSION = ""
            backscatter_channel.VAR_VALID_MIN = ""
            backscatter_channel.VAR_VALID_MAX = ""
            backscatter_channel.VAR_FILL_VALUE = ""

            if self.has_depolarization:
                depol_channel = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME', str,
                    dimensions=('VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                depol_channel.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                depol_channel.VAR_DESCRIPTION = "channel name according to SCC"
                depol_channel.VAR_SIZE = '{0}'.format(depolarization_size)
                depol_channel.VAR_DEPEND = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                depol_channel.VAR_DATA_TYPE = 'STRING'
                depol_channel.VAR_UNITS = ''
                depol_channel.VAR_SI_CONVERSION = ""
                depol_channel.VAR_VALID_MIN = ""
                depol_channel.VAR_VALID_MAX = ""
                depol_channel.VAR_FILL_VALUE = ""

            # Lat, lon following an NDACC file
            latitude = geoms_file.createVariable('LATITUDE.INSTRUMENT', 'f4', dimensions=(), )
            latitude.VAR_NAME = 'LATITUDE.INSTRUMENT'
            latitude.VAR_DESCRIPTION = "instrument latitude (deg.)"
            latitude.VAR_SIZE = '1'
            latitude.VAR_DEPEND = 'CONSTANT'
            latitude.VAR_DATA_TYPE = 'REAL'
            latitude.VAR_UNITS = 'deg'
            latitude.VAR_SI_CONVERSION = "0.0;1.74533E-2;rad"
            latitude.VAR_VALID_MIN = "-90"
            latitude.VAR_VALID_MAX = "90"
            latitude.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            longitude = geoms_file.createVariable('LONGITUDE.INSTRUMENT', 'f4')
            longitude.VAR_NAME = 'LONGITUDE.INSTRUMENT'
            longitude.VAR_DESCRIPTION = "instrument longitude (deg.)"
            longitude.VAR_SIZE = '1'
            longitude.VAR_DEPEND = 'CONSTANT'
            longitude.VAR_DATA_TYPE = 'REAL'
            longitude.VAR_UNITS = 'deg'
            longitude.VAR_SI_CONVERSION = "0.0;1.74533E-2;rad"
            longitude.VAR_VALID_MIN = "-180"
            longitude.VAR_VALID_MAX = "180"
            longitude.VAR_FILL_VALUE = netcdf.default_fillvals['f4']
            altitude_inst = geoms_file.createVariable('ALTITUDE.INSTRUMENT', 'f4')
            altitude_inst.VAR_NAME = 'ALTITUDE.INSTRUMENT'
            altitude_inst.VAR_DESCRIPTION = "instrument altitude (m)"
            altitude_inst.VAR_SIZE = '1'
            altitude_inst.VAR_DEPEND = 'CONSTANT'
            altitude_inst.VAR_DATA_TYPE = 'REAL'
            altitude_inst.VAR_UNITS = 'm'
            altitude_inst.VAR_SI_CONVERSION = "0.0;1.0;m"
            altitude_inst.VAR_VALID_MIN = -413.0  # Minimum altitude on earth
            altitude_inst.VAR_VALID_MAX = 8850.0  # Everest
            altitude_inst.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            viewing_angle = geoms_file.createVariable('ANGLE.VIEW_ZENITH',
                                                      'f4')  # Name following UV-VIS DOAS measurement
            viewing_angle.VAR_NAME = 'ANGLE.VIEW_ZENITH'
            viewing_angle.VAR_DESCRIPTION = "the zenith viewing direction of the instrument"
            viewing_angle.VAR_SIZE = '1'
            viewing_angle.VAR_DEPEND = 'CONSTANT'
            viewing_angle.VAR_DATA_TYPE = 'REAL'
            viewing_angle.VAR_UNITS = 'deg'
            viewing_angle.VAR_SI_CONVERSION = "0.0;1.74533E-2;rad"
            viewing_angle.VAR_VALID_MIN = "0"
            viewing_angle.VAR_VALID_MAX = "180"
            viewing_angle.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            backscatter_emission_wl = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_EMISSION.WAVELENGTH', 'f4',
                dimensions=('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_emission_wl.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_EMISSION_WAVELENGTH'
            backscatter_emission_wl.VAR_DESCRIPTION = "emission wavelength"
            backscatter_emission_wl.VAR_SIZE = '{0}'.format(backscatter_size)
            backscatter_emission_wl.VAR_DEPEND = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_emission_wl.VAR_DATA_TYPE = 'REAL'
            backscatter_emission_wl.VAR_UNITS = 'nm'
            backscatter_emission_wl.VAR_SI_CONVERSION = "0;1e-9;m"
            backscatter_emission_wl.VAR_VALID_MIN = "100"
            backscatter_emission_wl.VAR_VALID_MAX = "10000"
            backscatter_emission_wl.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            backscatter_detection_wl = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_DETECTION.WAVELENGTH', 'f4',
                dimensions=('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_detection_wl.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_DETECTION.WAVELENGTH'
            backscatter_detection_wl.VAR_DESCRIPTION = "detection wavelength"
            backscatter_detection_wl.VAR_SIZE = '{0}'.format(backscatter_size)
            backscatter_detection_wl.VAR_DEPEND = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_detection_wl.VAR_DATA_TYPE = 'REAL'
            backscatter_detection_wl.VAR_UNITS = 'nm'
            backscatter_detection_wl.VAR_SI_CONVERSION = "0;1e-9;m"
            backscatter_detection_wl.VAR_VALID_MIN = "100"
            backscatter_detection_wl.VAR_VALID_MAX = "10000"
            backscatter_detection_wl.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

            backscatter_range_type = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_RANGE.TYPE', 'i4',
                dimensions=('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_range_type.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_RANGE.TYPE'
            backscatter_range_type.VAR_DESCRIPTION = "bitmask describing the sounding ranges included in the product."
            backscatter_range_type.VAR_SIZE = '{0}'.format(backscatter_size)
            backscatter_range_type.VAR_DEPEND = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_range_type.VAR_DATA_TYPE = 'INTEGER'
            backscatter_range_type.VAR_UNITS = '1:ultra-near-range 2:near-range 4:far-range'  # TODO: What is the meaning of 0? No range defined?
            backscatter_range_type.VAR_SI_CONVERSION = ''
            backscatter_range_type.VAR_VALID_MIN = "0"
            backscatter_range_type.VAR_VALID_MAX = "7"
            backscatter_range_type.VAR_FILL_VALUE = -127

            backscatter_scatterers = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_SCATTERERS', 'i4',
                dimensions=('BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_scatterers.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_SCATTERERS'
            backscatter_scatterers.VAR_DESCRIPTION = "bitmask describing the scatterers responsible for the signal"
            backscatter_scatterers.VAR_SIZE = '{0}'.format(backscatter_size)
            backscatter_scatterers.VAR_DEPEND = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_scatterers.VAR_DATA_TYPE = 'INTEGER'
            backscatter_scatterers.VAR_UNITS = '1: particle 2: nitrogen 4:oxygen 8:water-vapour'  # What is the meaning of zero
            backscatter_scatterers.VAR_SI_CONVERSION = "0;1;m"
            backscatter_scatterers.VAR_VALID_MIN = "0"
            backscatter_scatterers.VAR_VALID_MAX = "15"
            backscatter_scatterers.VAR_FILL_VALUE = -127

            backscatter = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED', 'f8',
                dimensions=('DATETIME', 'ALTITUDE', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED'
            backscatter.VAR_DESCRIPTION = "attenuated backscatter coefficient"
            backscatter.VAR_SIZE = '{0};{1};{2}'.format(time_size,
                                                        altitude_size,
                                                        backscatter_size,
                                                        )
            backscatter.VAR_DEPEND = 'DATETIME;ALTITUDE;BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter.VAR_DATA_TYPE = 'DOUBLE'
            backscatter.VAR_UNITS = 'm-1sr-1'
            backscatter.VAR_SI_CONVERSION = "0;1;m-1sr-1"
            backscatter.VAR_VALID_MIN = ""  # TODO: How to fill valid min and max values
            backscatter.VAR_VALID_MAX = ""  # TODO: How to fill valid min and max values
            backscatter.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            backscatter_error = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_UNCERTAINTY.RANDOM', 'f8',
                dimensions=('DATETIME', 'ALTITUDE', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_error.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_UNCERTAINTY.RANDOM'
            backscatter_error.VAR_DESCRIPTION = "statistical error of attenuated backscatter coefficient"
            backscatter_error.VAR_SIZE = '{0};{1};{2}'.format(time_size,
                                                              altitude_size,
                                                              backscatter_size,
                                                              )
            backscatter_error.VAR_DEPEND = 'DATETIME;ALTITUDE;BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_error.VAR_DATA_TYPE = 'DOUBLE'
            backscatter_error.VAR_UNITS = 'm-1sr-1'
            backscatter_error.VAR_SI_CONVERSION = "0;1;m-1sr-1"
            backscatter_error.VAR_VALID_MIN = "0"
            backscatter_error.VAR_VALID_MAX = ""  # TODO: How to fill max values
            backscatter_error.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            backscatter_calibration = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_calibration.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT'
            backscatter_calibration.VAR_DESCRIPTION = "constant used to calibrate the attenuated backscatter coefficient"
            backscatter_calibration.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                backscatter_size,
                                                                )
            backscatter_calibration.VAR_DEPEND = 'DATETIME;BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_calibration.VAR_DATA_TYPE = 'DOUBLE'
            backscatter_calibration.VAR_UNITS = ''
            backscatter_calibration.VAR_SI_CONVERSION = "0;1;m-1sr-1"
            backscatter_calibration.VAR_VALID_MIN = "0"
            backscatter_calibration.VAR_VALID_MAX = ""  # TODO: How to fill valid max values
            backscatter_calibration.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            backscatter_calibration_error = geoms_file.createVariable(
                'BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT_UNCERTAINTY.RANDOM', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            backscatter_calibration_error.VAR_NAME = 'BACKSCATTER.COEFFICIENT.ATTENUATED_CALIBRATION.COEFFICIENT_UNCERTAINTY.RANDOM'
            backscatter_calibration_error.VAR_DESCRIPTION = "statistical error of attenuated backscatter calibration"
            backscatter_calibration_error.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                      backscatter_size,
                                                                      )
            backscatter_calibration_error.VAR_DEPEND = 'DATETIME;BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            backscatter_calibration_error.VAR_DATA_TYPE = 'DOUBLE'
            backscatter_calibration_error.VAR_UNITS = ''
            backscatter_calibration_error.VAR_SI_CONVERSION = "0;1;m-1sr-1"
            backscatter_calibration_error.VAR_VALID_MIN = "0"
            backscatter_calibration_error.VAR_VALID_MAX = ""  # TODO: How to fill valid max values
            backscatter_calibration_error.VAR_FILL_VALUE = netcdf.default_fillvals['f8']
            if self.has_depolarization:
                vldr_wl = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO_EMISSION.WAVELENGTH', 'f4',
                    dimensions=('VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                vldr_wl.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_EMISSION_WAVELENGTH'
                vldr_wl.VAR_DESCRIPTION = "wavelength at which the volume linear depolarization ratio is calculated"
                vldr_wl.VAR_SIZE = '{0}'.format(depolarization_size)
                vldr_wl.VAR_DEPEND = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                vldr_wl.VAR_DATA_TYPE = 'REAL'
                vldr_wl.VAR_UNITS = 'nm'
                vldr_wl.VAR_SI_CONVERSION = "0;1e-9;m"
                vldr_wl.VAR_VALID_MIN = "100"
                vldr_wl.VAR_VALID_MAX = "10000"
                vldr_wl.VAR_FILL_VALUE = netcdf.default_fillvals['f4']

                vldr_range_type = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO_RANGE.TYPE', 'i4',
                    dimensions=('VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                vldr_range_type.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_RANGE.TYPE'
                vldr_range_type.VAR_DESCRIPTION = "bitmask describing the sounding ranges included in the product."
                vldr_range_type.VAR_SIZE = '{0}'.format(depolarization_size)
                vldr_range_type.VAR_DEPEND = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                vldr_range_type.VAR_DATA_TYPE = 'INTEGER'
                vldr_range_type.VAR_UNITS = '1:ultra-near-range 2:near-range 3:far-range'  # TODO: What is the meaning of 0? No range defined?
                vldr_range_type.VAR_SI_CONVERSION = ''
                vldr_range_type.VAR_VALID_MIN = "0"
                vldr_range_type.VAR_VALID_MAX = "7"
                vldr_range_type.VAR_FILL_VALUE = -127

                vldr_scatterers = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO_SCATTERERS', 'i4',
                    dimensions=('VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                vldr_scatterers.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_SCATTERERS'
                vldr_scatterers.VAR_DESCRIPTION = "bitmask describing the scatterers responsible for the signal"
                vldr_scatterers.VAR_SIZE = '{0}'.format(depolarization_size)
                vldr_scatterers.VAR_DEPEND = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                vldr_scatterers.VAR_DATA_TYPE = 'INTEGER'
                vldr_scatterers.VAR_UNITS = '1: particle 2: nitrogen 4:oxygen 8:water-vapour'  # What is the meaning of zero
                vldr_scatterers.VAR_SI_CONVERSION = "0;1;m"
                vldr_scatterers.VAR_VALID_MIN = "0"
                vldr_scatterers.VAR_VALID_MAX = "15"
                vldr_scatterers.VAR_FILL_VALUE = -127

                vldr = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO', 'f8',
                    dimensions=('DATETIME', 'ALTITUDE', 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                vldr.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO'
                vldr.VAR_DESCRIPTION = "volume linear depolarization ratio"
                vldr.VAR_SIZE = '{0};{1};{2}'.format(time_size,
                                                     altitude_size,
                                                     depolarization_size,
                                                     )
                vldr.VAR_DEPEND = 'DATETIME;ALTITUDE;VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                vldr.VAR_DATA_TYPE = 'DOUBLE'
                vldr.VAR_UNITS = ''
                vldr.VAR_SI_CONVERSION = ""
                vldr.VAR_VALID_MIN = "0"
                vldr.VAR_VALID_MAX = "1"
                vldr.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

                vldr_error = geoms_file.createVariable(
                    'VOLUME.LINEAR.DEPOLARIZATION.RATIO_UNCERTAINTY.RANDOM', 'f8',
                    dimensions=('DATETIME', 'ALTITUDE', 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME',), )
                vldr_error.VAR_NAME = 'VOLUME.LINEAR.DEPOLARIZATION.RATIO_UNCERTAINTY.RANDOM'
                vldr_error.VAR_DESCRIPTION = "statistical error of volume linear depolarization ratio"
                vldr_error.VAR_SIZE = '{0};{1};{2}'.format(time_size,
                                                           altitude_size,
                                                           depolarization_size,
                                                           )
                vldr_error.VAR_DEPEND = 'DATETIME;ALTITUDE;VOLUME.LINEAR.DEPOLARIZATION.RATIO_CHANNEL.NAME'
                vldr_error.VAR_DATA_TYPE = 'DOUBLE'
                vldr_error.VAR_UNITS = ''
                vldr_error.VAR_SI_CONVERSION = ""
                vldr_error.VAR_VALID_MIN = "0"
                vldr_error.VAR_VALID_MAX = ""  # TODO: How to fill max values
                vldr_error.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            # Background
            atmospheric_background = geoms_file.createVariable(
                'BACKGROUND.ATMOSPHERIC', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            atmospheric_background.VAR_NAME = 'BACKGROUND.ATMOSPHERIC'
            atmospheric_background.VAR_DESCRIPTION = "mean atmospheric background calculated from lidar signal"
            atmospheric_background.VAR_SIZE = '{0};{1}'.format(time_size,
                                                               backscatter_size,
                                                               )
            atmospheric_background.VAR_DEPEND = 'DATETIME; BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            atmospheric_background.VAR_DATA_TYPE = 'DOUBLE'
            atmospheric_background.VAR_UNITS = 'm-3 sr-1'
            atmospheric_background.VAR_SI_CONVERSION = "0;1;m-3 sr-1"
            atmospheric_background.VAR_VALID_MIN = ""
            atmospheric_background.VAR_VALID_MAX = ""
            atmospheric_background.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            atmospheric_background_stdev = geoms_file.createVariable(
                'BACKGROUND.ATMOSPHERIC_STANDARD.DEVIATION', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            atmospheric_background_stdev.VAR_NAME = 'BACKGROUND.ATMOSPHERIC_STANDARD.DEVIATION'
            atmospheric_background_stdev.VAR_DESCRIPTION = "standard deviation of atmospheric background calculated from lidar signal"
            atmospheric_background_stdev.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                     backscatter_size,
                                                                     )
            atmospheric_background_stdev.VAR_DEPEND = 'DATETIME; BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            atmospheric_background_stdev.VAR_DATA_TYPE = 'DOUBLE'
            atmospheric_background_stdev.VAR_UNITS = 'm-3 sr-1'
            atmospheric_background_stdev.VAR_SI_CONVERSION = "0;1;m-3 sr-1"
            atmospheric_background_stdev.VAR_VALID_MIN = ""
            atmospheric_background_stdev.VAR_VALID_MAX = ""
            atmospheric_background_stdev.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            atmospheric_background_sterr = geoms_file.createVariable(
                'BACKGROUND.ATMOSPHERIC_STANDARD.ERROR', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            atmospheric_background_sterr.VAR_NAME = 'BACKGROUND.ATMOSPHERIC_STANDARD.ERROR'
            atmospheric_background_sterr.VAR_DESCRIPTION = "standard error of atmospheric background calculated from lidar signal"
            atmospheric_background_sterr.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                     backscatter_size,
                                                                     )
            atmospheric_background_sterr.VAR_DEPEND = 'DATETIME; BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            atmospheric_background_sterr.VAR_DATA_TYPE = 'DOUBLE'
            atmospheric_background_sterr.VAR_UNITS = 'm-3 sr-1'
            atmospheric_background_sterr.VAR_SI_CONVERSION = "0;1;m-3 sr-1"
            atmospheric_background_sterr.VAR_VALID_MIN = ""
            atmospheric_background_sterr.VAR_VALID_MAX = ""
            atmospheric_background_sterr.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            atmospheric_background_min = geoms_file.createVariable(
                'BACKGROUND.ATMOSPHERIC_MINIMUM', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            atmospheric_background_min.VAR_NAME = 'BACKGROUND.ATMOSPHERIC_MINIMUM'
            atmospheric_background_min.VAR_DESCRIPTION = "minimum atmospheric background calculated from lidar signal"
            atmospheric_background_min.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                   backscatter_size,
                                                                   )
            atmospheric_background_min.VAR_DEPEND = 'DATETIME; BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            atmospheric_background_min.VAR_DATA_TYPE = 'DOUBLE'
            atmospheric_background_min.VAR_UNITS = 'm-3 sr-1'
            atmospheric_background_min.VAR_SI_CONVERSION = "0;1;m-3 sr-1"
            atmospheric_background_min.VAR_VALID_MIN = ""
            atmospheric_background_min.VAR_VALID_MAX = ""
            atmospheric_background_min.VAR_FILL_VALUE = netcdf.default_fillvals['f8']

            atmospheric_background_max = geoms_file.createVariable(
                'BACKGROUND.ATMOSPHERIC_MAXIMUM', 'f8',
                dimensions=('DATETIME', 'BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME',), )
            atmospheric_background_max.VAR_NAME = 'ATMOSPHERIC_MAXIMUM.ATMOSPHERIC'
            atmospheric_background_max.VAR_DESCRIPTION = "maximum atmospheric background calculated from lidar signal"
            atmospheric_background_max.VAR_SIZE = '{0};{1}'.format(time_size,
                                                                   backscatter_size,
                                                                   )
            atmospheric_background_max.VAR_DEPEND = 'DATETIME; BACKSCATTER.COEFFICIENT.ATTENUATED_CHANNEL.NAME'
            atmospheric_background_max.VAR_DATA_TYPE = 'DOUBLE'
            atmospheric_background_max.VAR_UNITS = 'm-3 sr-1'
            atmospheric_background_max.VAR_SI_CONVERSION = "0;1;m-3 sr-1"
            atmospheric_background_max.VAR_VALID_MIN = ""
            atmospheric_background_max.VAR_VALID_MAX = ""
            atmospheric_background_max.VAR_FILL_VALUE = netcdf.default_fillvals['f8']
            # Fill the variable property
            geoms_file.DATA_VARIABLES = ';'.join(geoms_file.variables.keys())

        return geoms_file

    @classmethod
    def datetime_to_mjd2k(cls, date):
        """ Convert datetime object to modified julian date 2000.

        According to GEOMS documentation:
           The Modified Julian Date, MJD2K, used throughout this document is defined as follows:
           MJD2K is 0.000000 on January 1, 2000 at 00:00:00 UTC

        Parameters
        ----------
        date : datetime object
           A datetime object.

        Returns
        -------
        mjd : float
           The modified julian date.
        """
        base_date = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        dt = date - base_date

        mjd = dt.days + dt.seconds / 86400.
        return mjd

    @classmethod
    def epoch_to_mjd2k(cls, seconds_since_epoch):
        """ Convert seconds since 1970 to days since 2000.

        Parameters
        ----------
        seconds_since_epoch : float
           Seconds since 1970-01-01T00:00:00Z

        Returns
        -------
        mjd : float
           The modified julian date.
        """
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        mjd_base = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        offset_seconds = (mjd_base - epoch).days * 86400.

        mjd = (seconds_since_epoch - offset_seconds) / 86400.
        return mjd


class HiRElPPArchive(object):

    def __init__(self, file_list):
        """ Handle a dataset of HiRElPP files. The aim is to merge serveral hirelpp files
        to daily GEOMS files.

        Parameters
        ----------
        file_list : list
           A list of full paths for the HiRElPP files.
        """
        self.file_list = sorted(file_list)

        # Read metadata from all files
        self.files = []
        for file_path in self.file_list:
            h = HiRElPPFile(file_path, read_now=False)
            h.read_metadata()
            self.files.append(h)

        self.start_dates = [h.start_time.date() for h in self.files]
        self.stop_dates = [h.stop_time.date() for h in self.files]
        self.available_dates = sorted(list(set(self.start_dates + self.stop_dates)))

    def convert_date_to_geoms(self, date, output_dir, affiliation, location):
        """ Convert all data for a specific date to a daily geoms file.

        Parameters
        ----------
        date : date object
           The date to convert.
        output_dir : str
           Directory of output file. Filename is creates automatically.
        affiliation : str
           Initials of institute, to be used in filename (e.g. inoe).
        location : str
           Location name, to be used in filename (e.g. bucharest)."""

        if date not in self.available_dates:
            raise ValueError('Date {0} not in available dates.'.format(date))

        start_idxs = [n for n, d in enumerate(self.start_dates) if d == date]
        stop_idxs = [n for n, d in enumerate(self.stop_dates) if d == date]
        idxs = list(set(start_idxs + stop_idxs))

        files = [self.files[c] for c in idxs]
        files.sort(key=lambda x: x.start_time)

        epoch = datetime.date(1970, 1, 1)
        date_timestamp = (date - epoch).total_seconds()
        next_date_timestamp = date_timestamp + 86400

        file_metadata = []

        last_output_idx = 0
        for h in files:
            valid_idxs = \
            np.where(((h.time_bounds[:, 0] >= date_timestamp) & (h.time_bounds[:, 0] < next_date_timestamp)))[0]

            if len(valid_idxs) > 0:
                number_of_profiles = len(valid_idxs)
                start_output_idx = last_output_idx
                last_output_idx = start_output_idx + number_of_profiles
                file_min_idx = valid_idxs[
                    0]  # Here I assume that selected profiles are ordered and consecutive. This should always be true
                file_max_idx = valid_idxs[-1]

                metadata = {'file': h,
                            'valid_idxs': valid_idxs,
                            'min_idx': file_min_idx,
                            'max_idx': file_max_idx + 1,
                            'output_min_idx': start_output_idx,
                            'output_max_idx': last_output_idx,
                            'start_time': h.t_start[file_min_idx],
                            'stop_time': h.t_stop[file_max_idx], }

                file_metadata.append(metadata)

        start_time = file_metadata[0]['start_time']
        stop_time = file_metadata[-1]['stop_time']

        start_time_str = start_time.strftime('%Y%m%dT%H%M%SZ')
        stop_time_str = stop_time.strftime('%Y%m%dT%H%M%SZ')

        output_filename = 'groundbased_lidar.aerosol_{0}001_{1}_{2}_{3}.nc'.format(affiliation.lower(),
                                                                                   location.lower(),
                                                                                   start_time_str.lower(),
                                                                                   stop_time_str.lower())

        output_path = os.path.join(output_dir, output_filename)

        first_file = file_metadata[0]['file']
        first_file.read_file()

        altitude_size = len(first_file.z)
        backscatter_size = len(first_file.channel_names)

        if first_file.has_depolarization:
            depolarization_size = len(first_file.vldr_channel_names)
        else:
            depolarization_size = 0

        first_file.initialize_geoms_file(output_path, last_output_idx, altitude_size, backscatter_size,
                                         depolarization_size, start_time_str, stop_time_str)
        min_idx = file_metadata[0]['min_idx']
        max_idx = file_metadata[0]['max_idx']
        output_min_idx = file_metadata[0]['output_min_idx']
        output_max_idx = file_metadata[0]['output_max_idx']

        logger.debug('Filling with data from the first file.')
        first_file.fill_geoms_file(output_path, min_idx, max_idx, output_min_idx, output_max_idx)

        for metadata in file_metadata[1:]:
            f = metadata['file']

            logger.debug('Filling with data from {}.'.format(f.file_path))

            min_idx = metadata['min_idx']
            max_idx = metadata['max_idx']
            output_min_idx = metadata['output_min_idx']
            output_max_idx = metadata['output_max_idx']

            f.read_file()
            f.fill_geoms_file(output_path, min_idx, max_idx, output_min_idx, output_max_idx)

        return output_filename
