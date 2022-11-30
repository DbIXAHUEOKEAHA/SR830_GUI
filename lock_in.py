import pandas as pd
import pyvisa as visa
import numpy as np

rm = visa.ResourceManager()

# Write command to a device and get it's output
def get(device, command):
    '''device = rm.open_resource() where this function gets all devices initiaals such as adress, baud_rate, data_bits and so on; 
    command = string Standart Commands for Programmable Instruments (SCPI)'''
    return np.round(np.random.random(1), 1) #to test the program without device it would return random numbers
    #return device.query(command)

class lock_in():

    def __init__(self, adress='GPIB0::3::INSTR'):

        #self.sr830 = rm.open_resource(adress, write_termination='\n', read_termination='\n') - device
        
        self.sr830 = 0 #for test we dont need a device

        self.modes_ch1_options = ['X', 'R', 'X noise', 'AUX in 1', 'AUX in 2'] #what can be displayed on ch1

        self.modes_ch2_options = ['Y', 'Θ', 'Y noise', 'AUX in 3', 'AUX in 4'] #what can be displayed on ch2

        self.sensitivity_options = ['2 nV/fA', '5 nV/fA', '10 nV/fA',
                                    '20 nV/fA', '50 nV/fA', '100 nV/fA',
                                    '200 nV/fA', '500 nV/fA', '1 μV/pA',
                                    '2 μV/pA', '5 μV/pA', '10 μV/pA',
                                    '20 μV/pA', '50 μV/pA', '100 μV/pA',
                                    '200 μV/pA', '500 μV/pA',
                                    '1 mV/nA', '2 mV/nA', '5 mV/nA', '10 mV/nA',
                                    '20 mV/nA', '50 mV/nA', '100 mV/nA',
                                    '200 mV/nA', '500 mV/nA', '1 V/μA']
        #all possible sensitivity for device

        self.time_constant_options = ['10 μs', '30 μs', '100 μs',
                                      '300 μs', '1 ms', '3 ms',
                                      '10 ms', '30 ms', '100 ms',
                                      '300 ms', '1 s', '3 s',
                                      '10 s', '30 s', '100 s',
                                      '300 s', '1 ks', '3 ks',
                                      '10 ks', '30 ks']
        #all possible time constant for device

        self.low_pass_filter_slope_options = ['6 dB/oct', '12 dB/oct',
                                              '18 dB/oct', '24 dB/oct']

        self.synchronous_filter_status_options = ['On', 'Off']

        self.remote_status_options = ['lock', 'Unlock']

        self.set_options = ['amplitude', 'frequency', 'phase', 
                            'AUX1_output', 'AUX2_output', 'AUX3_output', 'AUX4_output']

        self.get_options = ['x', 'y', 'r', 'Θ', 'ch1', 'ch2',
                            'AUX1_input', 'AUX2_input', 'AUX3_input', 'AUX4_input']

    def IDN(self):
        '''return lock in identification'''
        answer = get(self.sr830, '*IDN?')
        return answer

    def x(self):
        '''return Re(meaurment) of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTP?1'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTP?1'))
        if str(answer)[-4:] == 'e-00' or str(answer)[-4:] == 'e+00':
            answer = float(get(self.sr830, 'OUTP?1'))
        return answer

    def y(self):
        '''return Im(measurment) of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTP?2'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTP?2'))
        if str(answer)[-4:] == 'e-00' or str(answer)[-4:] == 'e+00':
            answer = float(get(self.sr830, 'OUTP?2'))
        return answer

    def r(self):
        '''return sqrt(Re^2 + Im^2) of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTP?3'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTP?3'))
        if str(answer)[-4:] == 'e-00' or str(answer)[-4:] == 'e+00':
            answer = float(get(self.sr830, 'OUTP?3'))
        return answer

    def Θ(self):
        '''return arctan(Im/Re) of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTP?4'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTP?4'))
        return answer

    def frequency(self):
        '''return reference frequency of lock in'''
        try:
            answer = float(get(self.sr830, 'FREQ?'))
        except ValueError:
            answer = float(get(self.sr830, 'FREQ?'))
        return answer

    def phase(self):
        '''return reference phase of lock in'''
        try:
            answer = float(get(self.sr830, 'PHAS?'))
        except ValueError:
            answer = float(get(self.sr830, 'PHAS?'))
        return answer

    def amplitude(self):
        '''return reference amplitude of lock in'''
        try:
            answer = float(get(self.sr830, 'SLVL?'))
        except ValueError:
            answer = float(get(self.sr830, 'SLVL?'))
        return answer

    def sensitivity(self):
        '''return sensitivity of lock in'''
        try:
            answer = float(get(self.sr830, 'SENS?'))
        except ValueError:
            answer = float(get(self.sr830, 'SENS?'))
        return answer

    def time_constant(self):
        '''return time constant of lock in'''
        try:
            answer = int(get(self.sr830, 'OFLT?'))
        except ValueError:
            answer = int(get(self.sr830, 'OFLT?'))
        return answer

    def low_pass_filter_slope(self):
        '''return low pass filter slope of lock in'''
        try:
            answer = int(get(self.sr830, 'OFSL?'))
        except ValueError:
            answer = int(get(self.sr830, 'OFSL?'))
        return answer

    def synchronous_filter_status(self):
        '''return synchronous filter status of lock in'''
        try:
            answer = int(get(self.sr830, 'SYNC?'))
        except ValueError:
            answer = int(get(self.sr830, 'SYNC?'))
        return answer

    def remote(self):
        '''return remote status of lock in'''
        try:
            answer = int(get(self.sr830, 'OVRM?'))
        except ValueError:
            answer = int(get(self.sr830, 'OVRM?'))
        return answer

    def ch1(self):
        '''return number shown on ch1 of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTR?1'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTR?1'))
        if str(answer)[-4:] == 'e-00' or str(answer)[-4:] == 'e+00':
            answer = float(get(self.sr830, 'OUTR?1'))
        return answer

    def ch2(self):
        '''return number shown on ch1 of lock in'''
        try:
            answer = float(get(self.sr830, 'OUTR?2'))
        except ValueError:
            answer = float(get(self.sr830, 'OUTR?2'))
        if str(answer)[-4:] == 'e-00' or str(answer)[-4:] == 'e+00':
            answer = float(get(self.sr830, 'OUTR?2'))
        return answer

    def parameter(self):
        '''return dataframe containing all measurments'''
        dataframe = pd.DataFrame({'Sensitivity': [self.sensitivity()],
                                  'Time_constant': [self.time_constant()],
                                  'Low_pass_filter_slope': [self.low_pass_filter_slope()],
                                  'Synchronous_filter_status': [self.synchronous_filter_status()],
                                  'Remote': [self.remote()],
                                  'Amplitude': [self.amplitude()],
                                  'Frequency': [self.frequency()],
                                  'Phase': [self.phase()]})
        return dataframe

    def channels(self):
        '''return dataframe containing all channels values'''
        dataframe = pd.DataFrame({'Ch1': [self.ch1()], 'Ch2': [self.ch2()]})
        return dataframe

    def AUX1_input(self):
        '''return AUX1 of lock in'''
        try:
            answer = float(get(self.sr830, 'OAUX?1'))
        except ValueError:
            answer = float(get(self.sr830, 'OAUX?1'))
        return answer

    def AUX2_input(self):
        '''return AUX2 of lock in'''
        try:
            answer = float(get(self.sr830, 'OAUX?2'))
        except ValueError:
            answer = float(get(self.sr830, 'OAUX?2'))
        return answer

    def AUX3_input(self):
        '''return AUX3 of lock in'''
        try:
            answer = float(get(self.sr830, 'OAUX?3'))
        except ValueError:
            answer = float(get(self.sr830, 'OAUX?3'))
        return answer

    def AUX4_input(self):
        '''return AUX4 of lock in'''
        try:
            answer = float(get(self.sr830, 'OAUX?4'))
        except ValueError:
            answer = float(get(self.sr830, 'OAUX?4'))
        return answer

    def set_ch1_mode(self, mode=0):
        '''set the mode on ch1'''
        line = 'DDEF1,' + str(mode) + ',0'
        self.sr830.write(line)

    def set_ch2_mode(self, mode=0):
        '''set the mode on ch2'''
        line = 'DDEF2,' + str(mode) + ',0'
        self.sr830.write(line)

    def set_frequency(self, value=30.0):
        if value < 1e-3:
            value = 1e-3
        line = 'FREQ' + str(value)
        self.sr830.write(line)

    def set_phase(self, value=0.0):
        line = 'PHAS' + str(value)
        self.sr830.write(line)

    def set_amplitude(self, value=0.5):
        if value < 4e-3:
            value = 4e-3
        line = 'SLVL' + str(value)
        self.sr830.write(line)

    def set_sensitivity(self, mode=24):
        line = 'SENS' + str(mode)
        self.sr830.write(line)

    def set_time_constant(self, mode=19):
        line = 'OFLT' + str(mode)
        self.sr830.write(line)

    def set_low_pass_filter_slope(self, mode=3):
        line = 'OFSL' + str(mode)
        self.sr830.write(line)

    def set_synchronous_filter_status(self, mode=0):
        line = 'SYNC' + str(mode)
        self.sr830.write(line)

    def set_remote(self, mode=1):
        line = 'OVRM' + str(mode)
        self.sr830.write(line)

    def set_AUX1_output(self, value=0):
        line = 'AUXV1,' + str(value)
        self.sr830.write(line)

    def set_AUX2_output(self, value=0):
        line = 'AUXV2,' + str(value)
        self.sr830.write(line)

    def set_AUX3_output(self, value=0):
        line = 'AUXV3,' + str(value)
        self.sr830.write(line)

    def set_AUX4_output(self, value=0):
        line = 'AUXV4,' + str(value)
        self.sr830.write(line)