import logging
import struct
import numpy as np
import warnings
from typing import List, Dict, Optional

import qcodes as qc
from qcodes import VisaInstrument
from qcodes.data.data_set import DataSet
from qcodes.instrument.channel import InstrumentChannel
from qcodes.instrument.base import Instrument, Parameter
from qcodes.instrument.parameter import ArrayParameter, ParameterWithSetpoints
import qcodes.utils.validators as vals
from qcodes.utils.helpers import create_on_off_val_mapping
from qcodes.measure import Measure

log = logging.getLogger(__name__)


class LuaSweepParameter(ArrayParameter):
    """
    Parameter class to hold the data from a
    deployed Lua script sweep.
    """

    def __init__(self, name: str, instrument: Instrument) -> None:

        super().__init__(name=name,
                         shape=(1,),
                         docstring='Holds a sweep',
                         instrument=instrument)

    def prepareSweep(self, start: float, stop: float, steps: int,
                     mode: str) -> None:
        """
        Builds setpoints and labels

        Args:
            start: Starting point of the sweep
            stop: Endpoint of the sweep
            steps: No. of sweep steps
            mode: Type of sweep, either 'IV' (voltage sweep)
                or 'VI' (current sweep)
        """

        if mode not in ['IV', 'VI']:
            raise ValueError('mode must be either "VI" or "IV"')

        self.shape = (steps,)

        if mode == 'IV':
            self.unit = 'A'
            self.setpoint_names = ('Voltage',)
            self.setpoint_units = ('V',)
            self.label = 'current'
            self.name = 'iv_sweep'

        if mode == 'VI':
            self.unit = 'V'
            self.setpoint_names = ('Current',)
            self.setpoint_units = ('A',)
            self.label = 'voltage'
            self.name = 'vi_sweep'

        self.setpoints = (tuple(np.linspace(start, stop, steps)),)

        self.start = start
        self.stop = stop
        self.steps = steps
        self.mode = mode

    def get_raw(self) -> np.ndarray:

        if self._instrument is not None:
            data = self._instrument._fast_sweep(self.start,
                                                self.stop,
                                                self.steps,
                                                self.mode)
        else:
            raise RuntimeError("No instrument attached to Parameter.")

        return data


class TimeTrace(ParameterWithSetpoints):
    """
    A parameter class that holds the data corresponding to the time dependence of
    current and voltage.
    """
    def _check_time_trace(self) -> None:
        """
        A helper function that compares the integration time with measurement
        interval for accurate results.

        Raises:
            RuntimeError: If no instrument attached to Parameter.
        """
        if self.instrument is None:
            raise RuntimeError("No instrument attached to Parameter.")

        dt = self.instrument.timetrace_dt()
        nplc = self.instrument.nplc()
        linefreq = self.instrument.linefreq()
        plc = 1/linefreq
        if nplc * plc > dt:
            warnings.warn(f'Integration time of {nplc*plc*1000:.1f} ' +
                          f'ms is longer than {dt*1000:.1f} ms set ' +
                          'as measurement interval. Consider lowering ' +
                          'NPLC or increasing interval.', UserWarning, 2)

    def _set_mode(self, mode: str) -> None:
        """
        A helper function to set correct units and labels.

        Args:
            mode: User defined mode for the timetrace. It can be either
            "current" or "voltage".
        """
        if mode == 'current':
            self.unit='A'
            self.label='Current'
        if mode == 'voltage':
            self.unit='V'
            self.label='Voltage'

    def _time_trace(self) -> np.ndarray:
        """
        The function that prepares a Lua script for timetrace data acquisition.

        Raises:
            RuntimeError: If no instrument attached to Parameter.
        """

        if self.instrument is None:
            raise RuntimeError("No instrument attached to Parameter.")

        channel = self.instrument.channel
        npts = self.instrument.timetrace_npts()
        dt = self.instrument.timetrace_dt()
        mode = self.instrument.timetrace_mode()

        mode_map = {"current": "i", "voltage": "v"}

        script = ['{}.measure.count={}'.format(channel, npts),
                  'oldint={}.measure.interval'.format(channel),
                  '{}.measure.interval={}'.format(channel, dt),
                  '{}.nvbuffer1.clear()'.format(channel),
                  '{}.measure.{}({}.nvbuffer1)'.format(channel, mode_map[mode], channel),
                  '{}.measure.interval=oldint'.format(channel),
                  '{}.measure.count=1'.format(channel),
                  'format.data = format.REAL32',
                  'format.byteorder = format.LITTLEENDIAN',
                  'printbuffer(1, {}, {}.nvbuffer1.readings)'.format(npts, channel)]

        return self.instrument._execute_lua(script, npts)

    def get_raw(self) -> np.ndarray:  # pylint: disable=E0202

        if self.instrument is None:
            raise RuntimeError("No instrument attached to Parameter.")

        self._check_time_trace()
        data = self._time_trace()
        return data


class TimeAxis(Parameter):
    """
    A simple :class:`.Parameter` that holds all the times (relative to the
    measurement start) at which the points of the time trace were acquired.
    """
    def get_raw(self) -> np.ndarray:  # pylint: disable=E0202

        if self.instrument is None:
            raise RuntimeError("No instrument attached to Parameter.")

        npts = self.instrument.timetrace_npts()
        dt = self.instrument.timetrace_dt()
        return np.linspace(0, dt*npts, npts, endpoint=False)


class KeithleyChannel(InstrumentChannel):
    """
    Class to hold the two Keithley channels, i.e.
    SMUA and SMUB.
    """

    def __init__(self, parent: Instrument, name: str, channel: str) -> None:
        """
        Args:
            parent: The Instrument instance to which the channel is
                to be attached.
            name: The 'colloquial' name of the channel
            channel: The name used by the Keithley, i.e. either
                'smua' or 'smub'
        """

        if channel not in ['smua', 'smub']:
            raise ValueError('channel must be either "smub" or "smua"')

        super().__init__(parent, name)
        self.model = self._parent.model
        self._extra_visa_timeout = 5000
        self._measurement_duration_factor = 2 # Ensures that we are always above
                                              # the expected time.
        vranges = self._parent._vranges
        iranges = self._parent._iranges
        vlimit_minmax = self.parent._vlimit_minmax
        ilimit_minmax = self.parent._ilimit_minmax

        self.add_parameter('volt',
                           get_cmd=f'{channel}.measure.v()',
                           get_parser=float,
                           set_cmd=f'{channel}.source.levelv={{:.12f}}',
                           label='Voltage',
                           unit='V')

        self.add_parameter('curr',
                           get_cmd=f'{channel}.measure.i()',
                           get_parser=float,
                           set_cmd=f'{channel}.source.leveli={{:.12f}}',
                           label='Current',
                           unit='A')

        self.add_parameter('res',
                           get_cmd=f'{channel}.measure.r()',
                           get_parser=float,
                           set_cmd=False,
                           label='Resistance',
                           unit='Ohm')

        self.add_parameter('mode',
                           get_cmd=f'{channel}.source.func',
                           get_parser=float,
                           set_cmd=f'{channel}.source.func={{:d}}',
                           val_mapping={'current': 0, 'voltage': 1},
                           docstring='Selects the output source type. '
                                     'Can be either voltage or current.')

        self.add_parameter('output',
                           get_cmd=f'{channel}.source.output',
                           get_parser=float,
                           set_cmd=f'{channel}.source.output={{:d}}',
                           val_mapping=create_on_off_val_mapping(on_val=1,
                                                                 off_val=0))

        self.add_parameter('linefreq',
                           label='Line frequency',
                           get_cmd='localnode.linefreq',
                           get_parser=float,
                           set_cmd=False,
                           unit='Hz')

        self.add_parameter('nplc',
                           label='Number of power line cycles',
                           set_cmd=f'{channel}.measure.nplc={{}}',
                           get_cmd=f'{channel}.measure.nplc',
                           get_parser=float,
                           docstring='Number of power line cycles, used '
                                     'to perform measurements',
                           vals=vals.Numbers(0.001, 25))
        # volt range
        # needs get after set (WilliamHPNielsen): why?
        self.add_parameter('sourcerange_v',
                           label='voltage source range',
                           get_cmd=f'{channel}.source.rangev',
                           get_parser=float,
                           set_cmd=self._set_sourcerange_v,
                           unit='V',
                           docstring='The range used when sourcing voltage '
                                     'This affects the range and the precision '
                                     'of the source.',
                           vals=vals.Enum(*vranges[self.model]))

        self.add_parameter('source_autorange_v_enabled',
                           label='voltage source autorange',
                           get_cmd=f'{channel}.source.autorangev',
                           get_parser=float,
                           set_cmd=f'{channel}.source.autorangev={{}}',
                           docstring='Set autorange on/off for source voltage.',
                           val_mapping=create_on_off_val_mapping(on_val=1,
                                                                 off_val=0))

        self.add_parameter('measurerange_v',
                           label='voltage measure range',
                           get_cmd=f'{channel}.measure.rangev',
                           get_parser=float,
                           set_cmd=self._set_measurerange_v,
                           unit='V',
                           docstring='The range to perform voltage '
                                     'measurements in. This affects the range '
                                     'and the precision of the measurement. '
                                     'Note that if you both measure and '
                                     'source current this will have no effect, '
                                     'set `sourcerange_v` instead',
                           vals=vals.Enum(*vranges[self.model]))

        self.add_parameter('measure_autorange_v_enabled',
                           label='voltage measure autorange',
                           get_cmd=f'{channel}.measure.autorangev',
                           get_parser=float,
                           set_cmd=f'{channel}.measure.autorangev={{}}',
                           docstring='Set autorange on/off for measure voltage.',
                           val_mapping=create_on_off_val_mapping(on_val=1,
                                                                 off_val=0))
        # current range
        # needs get after set
        self.add_parameter('sourcerange_i',
                           label='current source range',
                           get_cmd=f'{channel}.source.rangei',
                           get_parser=float,
                           set_cmd=self._set_sourcerange_i,
                           unit='A',
                           docstring='The range used when sourcing current '
                                     'This affects the range and the '
                                     'precision of the source.',
                           vals=vals.Enum(*iranges[self.model]))

        self.add_parameter('source_autorange_i_enabled',
                            label='current source autorange',
                            get_cmd=f'{channel}.source.autorangei',
                            get_parser=float,
                            set_cmd=f'{channel}.source.autorangei={{}}',
                            docstring='Set autorange on/off for source current.',
                            val_mapping=create_on_off_val_mapping(on_val=1,
                                                                 off_val=0))

        self.add_parameter('measurerange_i',
                           label='current measure range',
                           get_cmd=f'{channel}.measure.rangei',
                           get_parser=float,
                           set_cmd=self._set_measurerange_i,
                           unit='A',
                           docstring='The range to perform current '
                                     'measurements in. This affects the range '
                                     'and the precision of the measurement. '
                                     'Note that if you both measure and source '
                                     'current this will have no effect, set '
                                     '`sourcerange_i` instead',
                           vals=vals.Enum(*iranges[self.model]))

        self.add_parameter('measure_autorange_i_enabled',
                           label='current autorange',
                           get_cmd=f'{channel}.measure.autorangei',
                           get_parser=float,
                           set_cmd=f'{channel}.measure.autorangei={{}}',
                           docstring='Set autorange on/off for measure current.',
                           val_mapping=create_on_off_val_mapping(on_val=1,
                                                                 off_val=0))
        # Compliance limit
        self.add_parameter('limitv',
                           get_cmd=f'{channel}.source.limitv',
                           get_parser=float,
                           set_cmd=f'{channel}.source.limitv={{}}',
                           docstring='Voltage limit e.g. the maximum voltage '
                                     'allowed in current mode. If exceeded '
                                     'the current will be clipped.',
                           vals=vals.Numbers(vlimit_minmax[self.model][0],
                                             vlimit_minmax[self.model][1]),
                           unit='V')
        # Compliance limit
        self.add_parameter('limiti',
                           get_cmd=f'{channel}.source.limiti',
                           get_parser=float,
                           set_cmd=f'{channel}.source.limiti={{}}',
                           docstring='Current limit e.g. the maximum current '
                                     'allowed in voltage mode. If exceeded '
                                     'the voltage will be clipped.',
                           vals=vals.Numbers(ilimit_minmax[self.model][0],
                                             ilimit_minmax[self.model][1]),
                           unit='A')

        self.add_parameter('fastsweep',
                           parameter_class=LuaSweepParameter)

        self.add_parameter('timetrace_npts',
                           initial_value=500,
                           label='Number of points',
                           get_cmd=None,
                           set_cmd=None)

        self.add_parameter('timetrace_dt',
                           initial_value=1e-3,
                           label='Time resolution',
                           unit='s',
                           get_cmd=None,
                           set_cmd=None)

        self.add_parameter(name='time_axis',
                           label='Time',
                           unit='s',
                           snapshot_value=False,
                           vals=vals.Arrays(shape=(self.timetrace_npts,)),
                           parameter_class=TimeAxis)

        self.add_parameter('timetrace',
                           vals=vals.Arrays(shape=(self.timetrace_npts,)),
                           setpoints=(self.time_axis,),
                           parameter_class=TimeTrace)

        self.add_parameter('timetrace_mode',
                           initial_value='current',
                           get_cmd=None,
                           set_cmd=self.timetrace._set_mode,
                           vals=vals.Enum('current', 'voltage'))

        self.channel = channel

    def reset(self) -> None:
        """
        Reset instrument to factory defaults.
        This resets only the relevant channel.
        """
        self.write('{}.reset()'.format(self.channel))
        # remember to update all the metadata
        log.debug('Reset channel {}.'.format(self.channel) +
                  'Updating settings...')
        self.snapshot(update=True)

    def doFastSweep(self, start: float, stop: float,
                    steps: int, mode: str) -> DataSet:
        """
        Perform a fast sweep using a deployed lua script and
        return a QCoDeS DataSet with the sweep.

        Args:
            start: starting sweep value (V or A)
            stop: end sweep value (V or A)
            steps: number of steps
            mode: What kind of sweep to make.
                'IV' (I versus V) or 'VI' (V versus I)
        """
        # prepare setpoints, units, name
        self.fastsweep.prepareSweep(start, stop, steps, mode)

        data = Measure(self.fastsweep).run()

        return data

    def _fast_sweep(self, start: float, stop: float, steps: int,
                    mode: str='IV') -> np.ndarray:
        """
        Perform a fast sweep using a deployed Lua script.
        This is the engine that forms the script, uploads it,
        runs it, collects the data, and casts the data correctly.

        Args:
            start: starting voltage
            stop: end voltage
            steps: number of steps
            mode: What kind of sweep to make.
                'IV' (I versus V) or 'VI' (V versus I)
        """

        channel = self.channel

        # an extra visa query, a necessary precaution
        # to avoid timing out when waiting for long
        # measurements
        nplc = self.nplc()

        dV = (stop-start)/(steps-1)

        if mode == 'IV':
            meas = 'i'
            sour = 'v'
            func = '1'

        if mode == 'VI':
            meas = 'v'
            sour = 'i'
            func = '0'

        script = ['{}.measure.nplc = {:.12f}'.format(channel, nplc),
                  '{}.source.output = 1'.format(channel),
                  'startX = {:.12f}'.format(start),
                  'dX = {:.12f}'.format(dV),
                  '{}.source.output = 1'.format(channel),
                  '{}.source.func = {}'.format(channel, func),
                  '{}.measure.count = 1'.format(channel),
                  '{}.nvbuffer1.clear()'.format(channel),
                  '{}.nvbuffer1.appendmode = 1'.format(channel),
                  'for index = 1, {} do'.format(steps),
                  '  target = startX + (index-1)*dX',
                  '  {}.source.level{} = target'.format(channel, sour),
                  '  {}.measure.{}({}.nvbuffer1)'.format(channel, meas,
                                                         channel),
                  'end',
                  'format.data = format.REAL32',
                  'format.byteorder = format.LITTLEENDIAN',
                  'printbuffer(1, {}, {}.nvbuffer1.readings)'.format(steps,
                                                                     channel)]

        return self._execute_lua(script, steps)

    def _execute_lua(self, _script: List[str], steps: int) -> np.ndarray:
        """
        This is the function that sends the Lua script to be executed and
        returns the corresponding data from the buffer.

        Args:
            _script: The Lua script to be executed.
            steps: Number of points.
        """
        nplc = self.nplc()
        linefreq = self.linefreq()
        _time_trace_extra_visa_timeout = self._extra_visa_timeout
        _factor = self._measurement_duration_factor
        estimated_measurement_duration = _factor*1000*steps*nplc/linefreq
        new_visa_timeout = (estimated_measurement_duration
                          + _time_trace_extra_visa_timeout)

        self.write(self.root_instrument._scriptwrapper(program=_script, debug=True))

        # now poll all the data
        # The problem is that a '\n' character might by chance be present in
        # the data
        fullsize = 4*steps + 3
        received = 0
        data = b''
        # we must wait for the script to execute
        with self.root_instrument.timeout.set_to(new_visa_timeout):
            while received < fullsize:
                data_temp = self.root_instrument.visa_handle.read_raw()
                received += len(data_temp)
                data += data_temp

        # From the manual p. 7-94, we know that a b'#0' is prepended
        # to the data and a b'\n' is appended
        data = data[2:-1]
        outdata = np.array(list(struct.iter_unpack('<f', data)))
        outdata = np.reshape(outdata, len(outdata))
        return outdata

    def _set_sourcerange_v(self, val: float) -> None:
        channel = self.channel
        self.source_autorange_v_enabled(False)
        self.write(f'{channel}.source.rangev={val}')

    def _set_measurerange_v(self, val: float) -> None:
        channel = self.channel
        self.measure_autorange_v_enabled(False)
        self.write(f'{channel}.measure.rangev={val}')

    def _set_sourcerange_i(self, val: float) -> None:
        channel = self.channel
        self.source_autorange_i_enabled(False)
        self.write(f'{channel}.source.rangei={val}')

    def _set_measurerange_i(self, val: float) -> None:
        channel = self.channel
        self.measure_autorange_i_enabled(False)
        self.write(f'{channel}.measure.rangei={val}')


class Keithley_2600(VisaInstrument):
    """
    This is the qcodes driver for the Keithley_2600 Source-Meter series,
    tested with Keithley_2614B

    """
    def __init__(self, name: str, address: str, **kwargs) -> None:
        """
        Args:
            name: Name to use internally in QCoDeS
            address: VISA resource address
        """
        super().__init__(name, address, terminator='\n', **kwargs)

        model = self.ask('localnode.model')

        knownmodels = ['2601B', '2602A', '2602B', '2604B', '2611B', '2612B',
                       '2614B', '2635B', '2636B']
        if model not in knownmodels:
            kmstring = ('{}, '*(len(knownmodels)-1)).format(*knownmodels[:-1])
            kmstring += 'and {}.'.format(knownmodels[-1])
            raise ValueError('Unknown model. Known model are: ' +
                             kmstring)

        self.model = model

        self._vranges = {'2601B': [0.1, 1, 6, 40],
                         '2602A': [0.1, 1, 6, 40],
                         '2602B': [0.1, 1, 6, 40],
                         '2604B': [0.1, 1, 6, 40],
                         '2611B': [0.2, 2, 20, 200],
                         '2612B': [0.2, 2, 20, 200],
                         '2614B': [0.2, 2, 20, 200],
                         '2635B': [0.2, 2, 20, 200],
                         '2636B': [0.2, 2, 20, 200]}

        # TODO: In pulsed mode, models 2611B, 2612B, and 2614B
        # actually allow up to 10 A.
        self._iranges = {'2601B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 3],
                         '2602A': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 3],
                         '2602B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 3],
                         '2604B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 3],
                         '2611B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 1.5],
                         '2612B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 1.5],
                         '2614B': [100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 0.01, 0.1, 1, 1.5],
                         '2634B': [1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 10e-6, 100e-3, 1, 1.5],
                         '2635B': [1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 10e-6, 100e-3, 1, 1.5],
                         '2636B': [1e-9, 10e-9, 100e-9, 1e-6, 10e-6, 100e-6,
                                   1e-3, 10e-6, 100e-3, 1, 1.5]}

        self._vlimit_minmax = {'2601B': [10e-3, 40],
                               '2602A': [10e-3, 40],
                               '2602B': [10e-3, 40],
                               '2604B': [10e-3, 40],
                               '2611B': [20e-3, 200],
                               '2612B': [20e-3, 200],
                               '2614B': [20e-3, 200],
                               '2634B': [20e-3, 200],
                               '2635B': [20e-3, 200],
                               '2636B': [20e-3, 200],}

        self._ilimit_minmax = {'2601B': [10e-9, 3],
                               '2602A': [10e-9, 3],
                               '2602B': [10e-9, 3],
                               '2604B': [10e-9, 3],
                               '2611B': [10e-9, 3],
                               '2612B': [10e-9, 3],
                               '2614B': [10e-9, 3],
                               '2634B': [100e-12, 1.5],
                               '2635B': [100e-12, 1.5],
                               '2636B': [100e-12, 1.5],}
        # Add the channel to the instrument
        self.channels: List[KeithleyChannel] = []
        for ch in ['a', 'b']:
            ch_name = 'smu{}'.format(ch)
            channel = KeithleyChannel(self, ch_name, ch_name)
            self.add_submodule(ch_name, channel)
            self.channels.append(channel)

        # display
        self.add_parameter('display_settext',
                           set_cmd=self._display_settext,
                           vals=vals.Strings())

        self.connect_message()

    def _display_settext(self, text: str) -> None:
        self.visa_handle.write('display.settext("{}")'.format(text))

    def get_idn(self) -> Dict[str, Optional[str]]:
        IDNstr = self.ask_raw('*IDN?')
        vendor, model, serial, firmware = map(str.strip, IDNstr.split(','))
        model = model[6:]

        IDN: Dict[str, Optional[str]] = {'vendor': vendor, 'model': model,
                                         'serial': serial, 'firmware': firmware}
        return IDN

    def display_clear(self) -> None:
        """
        This function clears the display, but also leaves it in user mode
        """
        self.visa_handle.write('display.clear()')

    def display_normal(self) -> None:
        """
        Set the display to the default mode
        """
        self.visa_handle.write('display.screen = display.SMUA_SMUB')

    def exit_key(self) -> None:
        """
        Get back the normal screen after an error:
        send an EXIT key press event
        """
        self.visa_handle.write('display.sendkey(75)')

    def reset(self) -> None:
        """
        Reset instrument to factory defaults.
        This resets both channels.
        """
        self.write('reset()')
        # remember to update all the metadata
        log.debug('Reset instrument. Re-querying settings...')
        self.snapshot(update=True)

    def ask(self, cmd: str) -> str:
        """
        Override of normal ask. This is important, since queries to the
        instrument must be wrapped in 'print()'
        """
        return super().ask('print({:s})'.format(cmd))

    @staticmethod
    def _scriptwrapper(program: List[str], debug: bool=False) -> str:
        """
        wraps a program so that the output can be put into
        visa_handle.write and run.
        The script will run immediately as an anonymous script.

        Args:
            program: A list of program instructions. One line per
            list item, e.g. ['for ii = 1, 10 do', 'print(ii)', 'end' ]
        """
        mainprog = '\r\n'.join(program) + '\r\n'
        wrapped = 'loadandrunscript\r\n{}endscript\n'.format(mainprog)
        if debug:
            log.debug('Wrapped the following script:')
            log.debug(wrapped)
        return wrapped
