import os
cur_dir = os.getcwd() 
from csv import writer
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import pandas as pd
LARGE_FONT = ('Verdana', 12)
from lock_in import lock_in
import threading

config_parameters_filename = cur_dir + '\config\parameters_' + datetime.today().strftime(
    '%H_%M_%d_%m_%Y') + '.csv' 

config_parameters = pd.DataFrame(columns=['Sensitivity', 'Time_constant',
                                 'Low_pass_filter_slope', 'Synchronous_filter_status',
                                          'Remote', 'Amplitude', 'Frequency',
                                          'Phase'])

config_parameters.to_csv(config_parameters_filename, index=False)

config_channels_filename = cur_dir + '\config\channels_' + datetime.today().strftime(
    '%H_%M_%d_%m_%Y') + '.csv' 

config_channels = pd.DataFrame(columns=['Ch1', 'Ch2'])

config_channels.to_csv(config_channels_filename, index=False)

class write_config_channels(threading.Thread):
    
    '''class that write lock in's channels values in real time in real time'''

    def __init__(self, adress='GPIB0::3::INSTR'):
        threading.Thread.__init__(self) #initialise threading
        self.adress = adress
        self.daemon = True #threading pay attention to time.sleep()
        self.start()#start thread

    def run(self): #runs in parallel beccause threading was initialised
        while True: #infinite cycle
            dataframe_channels = lock_in(adress=self.adress).channels()
            with open(config_channels_filename, 'a') as f_object:
                try:
                    writer_object = writer(f_object)
                    writer_object.writerow(*dataframe_channels.values)
                    time.sleep(0.3)

                    # Close the file object
                    f_object.close()
                except:
                    f_object.close()
                    
class write_config_parameters(threading.Thread):

    '''class that write lock in's parameters in real time in real time'''    

    def __init__(self, adress='GPIB0::3::INSTR'):
        threading.Thread.__init__(self) #initialise threading
        self.adress = adress
        self.daemon = True #threading pay attention to time.sleep()
        self.start() #start thread

    def run(self): #runs in parallel beccause threading was initialised
        while True: #infinite cycle
            dataframe_parameters = lock_in(adress=self.adress).parameter()
            if dataframe_parameters.values.all() != pd.read_csv(config_parameters_filename).tail(1).values.all():
                with open(config_parameters_filename, 'a') as f_object:
                    try:
                        # Pass this file object to csv.writer()
                        # and get a writer object
                        writer_object = writer(f_object)
    
                        # Pass the list as an argument into
                        # the writerow()
                        writer_object.writerow(*dataframe_parameters.values)
                        time.sleep(5)
    
                        # Close the file object
                        f_object.close()
                    except KeyboardInterrupt:
                        f_object.close()

class Frontend(tk.Tk):
    
    '''This is a class that creates window in general'''

    def __init__(self, window, size = '1920x1080', title = 'Lock in', *args, **kwargs):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        tk.Tk.__init__(self, *args, **kwargs) #initialising tkinter window

        tk.Tk.iconbitmap(self) #window icon is empty, may add some if needed
        tk.Tk.geometry(self, newGeometry = size) #size of window, '1920x1080' by default
        tk.Tk.wm_title(self, title) #window title 'Lock in' by default

        container = tk.Frame(self) #window object
        container.pack(side='top', fill='both', expand='True') 
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        frame = window(container, self)
        self.frames[window] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(window) #refer to show_frame function below

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #create window

class Lock_in_settings(tk.Frame):

    def __init__(self, parent, controller):
        '''init is the function that runs every time, when Frontend class called
        so here we should initialise all variables that we are going to use'''
        
        self.adress = 'GPIB0::3::INSTR' #adress of Lock in device

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Lock in settings', font=LARGE_FONT) #label is just a text on a window
        label.place(relx=0.485, rely=0.02) #place label in x = 0.485 * width, y = 0.02 * height

        label_time_constant = tk.Label(self, text='Time constant')
        label_time_constant.place(relx=0.02, rely=0.015) #place label in x = 0.02 * width, y = 0.15 * height

        #here we use self. before variable name, because we will use this variable later in class
        self.combo_time_constant = ttk.Combobox(self,
                                                value=lock_in(self.adress).time_constant_options)
        #combobox is entry menu with multi choise
        self.combo_time_constant.current(8)
        self.combo_time_constant.bind(
            "<<ComboboxSelected>>", self.set_time_constant) #bind a function to this combobox
        self.combo_time_constant.place(relx=0.02, rely=0.05) #place combobox in x = 0.02 * width, y = 0.05 * height 

        self.value_time_constant = tk.StringVar(value='0.0') #initialise string variable with initial value of '0.0'
        self.label_value_time_constant = tk.Label(
            self, text=(self.value_time_constant.get())) #put self.value_time_constant in label
        self.label_value_time_constant.place(relx=0.02, rely=0.085)

        label_low_pass_filter_slope = tk.Label(
            self, text='Low pass filter slope')
        label_low_pass_filter_slope.place(relx=0.02, rely=0.125)

        self.combo_low_pass_filter_slope = ttk.Combobox(self,
                                                        value=lock_in(self.adress).low_pass_filter_slope_options)
        self.combo_low_pass_filter_slope.current(1)
        self.combo_low_pass_filter_slope.bind(
            "<<ComboboxSelected>>", self.set_low_pass_filter_slope)
        self.combo_low_pass_filter_slope.place(relx=0.02, rely=0.160)

        self.value_low_pass_filter_slope = tk.StringVar(value='0.0')
        self.label_value_low_pass_filter_slope = tk.Label(
            self, text=(self.value_low_pass_filter_slope.get()))
        self.label_value_low_pass_filter_slope.place(relx=0.02, rely=0.195)

        label_synchronous_filter_status = tk.Label(
            self, text='Synchronous filter status')
        label_synchronous_filter_status.place(relx=0.02, rely=0.235)

        self.combo_synchronous_filter_status = ttk.Combobox(self,
                                                            value=lock_in(self.adress).synchronous_filter_status_options)
        self.combo_synchronous_filter_status.current(0)
        self.combo_synchronous_filter_status.bind(
            "<<ComboboxSelected>>", self.set_synchronous_filter_status)
        self.combo_synchronous_filter_status.place(relx=0.02, rely=0.270)

        self.value_synchronous_filter_status = tk.StringVar(value='0.0')
        self.label_value_synchronous_filter_status = tk.Label(
            self, text=(self.value_synchronous_filter_status.get()))
        self.label_value_synchronous_filter_status.place(relx=0.02, rely=0.305)

        label_aux_rule = tk.Label(
            self, text='AUX output voltage \n -10.5 < V < 10.5')
        label_aux_rule.place(relx=0.02, rely=0.4)

        label_aux1_voltage = tk.Label(self, text='AUX1 output')
        label_aux1_voltage.place(relx=0.02, rely=0.45)

        self.aux1_initial = tk.StringVar(value='0')

        entry_aux1_voltage = tk.Entry(self, textvariable=self.aux1_initial) #entry box with initial value of self.aux1_initial
        entry_aux1_voltage.place(relx=0.02, rely=0.485)

        label_aux2_voltage = tk.Label(self, text='AUX2 output')
        label_aux2_voltage.place(relx=0.02, rely=0.515)

        self.aux2_initial = tk.StringVar(value='0')

        entry_aux2_voltage = tk.Entry(self, textvariable=self.aux2_initial)
        entry_aux2_voltage.place(relx=0.02, rely=0.550)

        label_aux3_voltage = tk.Label(self, text='AUX3 output')
        label_aux3_voltage.place(relx=0.02, rely=0.580)

        self.aux3_initial = tk.StringVar(value='0')

        entry_aux3_voltage = tk.Entry(self, textvariable=self.aux3_initial)
        entry_aux3_voltage.place(relx=0.02, rely=0.615)

        label_aux4_voltage = tk.Label(self, text='AUX4 output')
        label_aux4_voltage.place(relx=0.02, rely=0.645)

        self.aux4_initial = tk.StringVar(value='0')

        entry_aux4_voltage = tk.Entry(self, textvariable=self.aux4_initial)
        entry_aux4_voltage.place(relx=0.02, rely=0.680)

        button_aux_voltage = tk.Button(self, text='Set AUX voltage',
                                        command=self.aux_button_clicked)
        button_aux_voltage.place(relx=0.15, rely=0.675)

        label_sensitivity = tk.Label(self, text='Sensitivity')
        label_sensitivity.place(relx=0.15, rely=0.015)

        self.combo_sensitivity = ttk.Combobox(
            self, value=lock_in(self.adress).sensitivity_options)
        self.combo_sensitivity.current(15)
        self.combo_sensitivity.bind(
            "<<ComboboxSelected>>", self.set_sensitivity)
        self.combo_sensitivity.place(relx=0.15, rely=0.05)

        self.value_sensitivity = tk.StringVar(value='0.0')
        self.label_value_sensitivity = tk.Label(
            self, text=(self.value_sensitivity.get()))
        self.label_value_sensitivity.place(relx=0.15, rely=0.085)

        label_remote = tk.Label(self, text='Display locking')
        label_remote.place(relx=0.15, rely=0.125)

        self.combo_remote = ttk.Combobox(
            self, value=lock_in(self.adress).remote_status_options)
        self.combo_remote.current(1)
        self.combo_remote.bind("<<ComboboxSelected>>", self.set_remote)
        self.combo_remote.place(relx=0.15, rely=0.160)

        self.value_remote = tk.StringVar(value='0.0')
        self.label_value_remote = tk.Label(
            self, text=(self.value_remote.get()))
        self.label_value_remote.place(relx=0.15, rely=0.195)

        self.value_ch1 = tk.StringVar(value='0.0')
        self.label_value_ch1 = tk.Label(self, text=(
            '\n' + self.value_ch1.get()), font=('Arial', 16))
        self.label_value_ch1.place(relx=0.15, rely=0.3)

        self.combo_ch1 = ttk.Combobox(self, value=lock_in(self.adress).modes_ch1_options)
        self.combo_ch1.current(0)
        self.combo_ch1.bind("<<ComboboxSelected>>", self.set_ch1_mode)
        self.combo_ch1.place(relx=0.15, rely=0.4)

        self.value_ch2 = tk.StringVar(value='0.0')
        self.label_value_ch2 = tk.Label(self, text=(
            '\n' + self.value_ch1.get()), font=('Arial', 16))
        self.label_value_ch2.place(relx=0.3, rely=0.3)

        self.combo_ch2 = ttk.Combobox(self, value=lock_in(self.adress).modes_ch2_options)
        self.combo_ch2.current(0)
        self.combo_ch2.bind("<<ComboboxSelected>>", self.set_ch2_mode)
        self.combo_ch2.place(relx=0.3, rely=0.4)

        label_amplitude = tk.Label(
            self, text='Amplitude of SIN output, V. \n 0.004 < V < 5.000')
        label_amplitude.place(relx=0.485, rely=0.315)

        self.amplitude_initial = tk.StringVar(value='0.5')

        entry_amplitude = tk.Entry(self, textvariable=self.amplitude_initial)
        entry_amplitude.place(relx=0.5, rely=0.4)

        self.value_amplitude = tk.StringVar(value='0.0')
        self.label_value_amplitude = tk.Label(
            self, text=(self.value_amplitude.get()))
        self.label_value_amplitude.place(relx=0.5, rely=0.435)

        label_frequency = tk.Label(
            self, text='Frequency, Hz. \n 0.001 < Hz < 102000')
        label_frequency.place(relx=0.65, rely=0.315)

        self.frequency_initial = tk.StringVar(value='30.0')

        entry_frequency = tk.Entry(self, textvariable=self.frequency_initial)
        entry_frequency.place(relx=0.65, rely=0.4)

        self.value_frequency = tk.StringVar(value='0.0')
        self.label_value_frequency = tk.Label(
            self, text=(self.value_frequency.get()))
        self.label_value_frequency.place(relx=0.65, rely=0.435)

        label_phase = tk.Label(
            self, text='Phase shift, deg. \n -360.00 < deg < 729.99')
        label_phase.place(relx=0.8, rely=0.315)

        self.phase_initial = tk.StringVar(value='0.0')

        entry_phase = tk.Entry(self, textvariable=self.phase_initial)
        entry_phase.place(relx=0.8, rely=0.4)

        self.value_phase = tk.StringVar(value='0.0')
        self.label_value_phase = tk.Label(self, text=(self.value_phase.get()))
        self.label_value_phase.place(relx=0.8, rely=0.435)

        button_reference = tk.Button(self, text='Set reference parameters', #button that calls command when it's pushed
                                      command=self.reference_button_clicked)
        button_reference.place(relx=0.8, rely=0.485)


        #############################################
        '''creating threads for each process'''
        thread_update_sensitivity = threading.Thread(
            target=self.update_sensitivity())
        thread_update_time_constant = threading.Thread(
            target=self.update_time_constant())
        thread_update_low_pass_filter_slope = threading.Thread(
            target=self.update_low_pass_filter_slope())
        thread_update_synchronous_filter_status = threading.Thread(
            target=self.update_synchronous_filter_status())
        thread_update_remote = threading.Thread(target=self.update_remote())
        thread_update_amplitude = threading.Thread(
            target=self.update_amplitude())
        thread_update_phase = threading.Thread(target=self.update_phase())
        thread_update_frequency = threading.Thread(
            target=self.update_frequency())
        thread_update_ch1 = threading.Thread(target=self.update_value_ch1())
        thread_update_ch2 = threading.Thread(target=self.update_value_ch2())
        #############################################

        '''start every thread'''
        thread_update_sensitivity.start()
        thread_update_time_constant.start()
        thread_update_low_pass_filter_slope.start()
        thread_update_synchronous_filter_status.start()
        thread_update_remote.start()
        thread_update_amplitude.start()
        thread_update_phase.start()
        thread_update_frequency.start()
        thread_update_ch1.start()
        thread_update_ch2.start()

        #############################################
        '''join thread into general stream of threads'''
        thread_update_sensitivity.join()
        thread_update_time_constant.join()
        thread_update_low_pass_filter_slope.join()
        thread_update_synchronous_filter_status.join()
        thread_update_remote.join()
        thread_update_amplitude.join()
        thread_update_phase.join()
        thread_update_frequency.join()
        thread_update_ch1.join()
        thread_update_ch2.join()
        #############################################

    def set_sensitivity(self, event):
        '''set sensitivity from the list in self.combo_sensitivity
        'event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_sensitivity(mode=int(self.combo_sensitivity.current()))

    def set_time_constant(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_time_constant(mode=int(self.combo_time_constant.current()))

    def set_low_pass_filter_slope(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_low_pass_filter_slope(
            mode=int(self.combo_low_pass_filter_slope.current()))

    def set_synchronous_filter_status(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_synchronous_filter_status(
            mode=int(self.combo_synchronous_filter_status.current()))

    def set_ch1_mode(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_ch1_mode(mode=int(self.combo_ch1.current()))

    def set_ch2_mode(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_ch2_mode(mode=int(self.combo_ch2.current()))

    def set_remote(self, event):
        ''''event' is passed so every time you choose an option in combobox, it calls this function immideatly'''
        lock_in(self.adress).set_remote(mode=int(self.combo_remote.current()))

    def aux_button_clicked(self): 
        '''function to run everytime button is clicked'''
        lock_in(self.adress).set_AUX1_output(value=float(self.aux1_initial.get()))
        lock_in(self.adress).set_AUX2_output(value=float(self.aux2_initial.get()))
        lock_in(self.adress).set_AUX3_output(value=float(self.aux3_initial.get()))
        lock_in(self.adress).set_AUX4_output(value=float(self.aux4_initial.get()))

    def reference_button_clicked(self):
        '''function to run everytime button is clicked'''
        lock_in(self.adress).set_frequency(value=float(self.frequency_initial.get()))
        lock_in(self.adress).set_phase(value=float(self.phase_initial.get()))
        lock_in(self.adress).set_amplitude(value=float(self.amplitude_initial.get()))

    def update_time_constant(self, interval=2987):
        '''updates label of time costant in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Time_constant'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_time_constant['text'] = str(
            lock_in(self.adress).time_constant_options[int(value)])
        self.label_value_time_constant.after(
            interval, self.update_time_constant)

    def update_sensitivity(self, interval=2989):
        '''updates label of sensitivity in a parallel thread, 
        because thread with this function was initialised before'''
        
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Sensitivity'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_sensitivity['text'] = str(
            lock_in(self.adress).sensitivity_options[int(value)])
        self.label_value_sensitivity.after(interval, self.update_sensitivity)

    def update_low_pass_filter_slope(self, interval=2991):
        '''updates label of low pass filter slope in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Low_pass_filter_slope'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_low_pass_filter_slope['text'] = str(
            lock_in(self.adress).low_pass_filter_slope_options[int(value)])
        self.label_value_low_pass_filter_slope.after(
            interval, self.update_low_pass_filter_slope)

    def update_synchronous_filter_status(self, interval=2993):
        '''updates label of synchronous filter in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Synchronous_filter_status'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_synchronous_filter_status['text'] = str(
            lock_in(self.adress).synchronous_filter_status_options[int(value)])
        self.label_value_synchronous_filter_status.after(
            interval, self.update_synchronous_filter_status)

    def update_remote(self, interval=2995):
        '''updates label of remote status in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Remote'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_remote['text'] = str(
            lock_in(self.adress).remote_status_options[int(value)])
        self.label_value_remote.after(interval, self.update_remote)

    def update_amplitude(self, interval=2997):
        '''updates label of amplitude in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Amplitude'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_amplitude['text'] = str(value)
        self.label_value_amplitude.after(interval, self.update_amplitude)

    def update_phase(self, interval=2999):
        '''updates label of phase in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)['Phase'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_phase['text'] = str(value)
        self.label_value_phase.after(interval, self.update_phase)

    def update_frequency(self, interval=3001):
        '''updates label of phase in a parallel thread, 
        because thread with this function was initialised before'''
        try:
            value = pd.read_csv(config_parameters_filename)[
                'Frequency'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_frequency['text'] = str(value)
        self.label_value_frequency.after(interval, self.update_frequency)

    def update_value_ch1(self, interval=307):
        '''updates label of ch1 in a parallel thread, 
        because thread with this function was initialised before'''
        global config_channels_filename
        
        try:
            value = pd.read_csv(config_channels_filename)['Ch1'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_ch1['text'] = '\n' + str(value)
        self.label_value_ch1.after(interval, self.update_value_ch1)

    def update_value_ch2(self, interval=311):
        '''updates label of ch2 in a parallel thread, 
        because thread with this function was initialised before'''
        global config_channels_filename

        try:
            value = pd.read_csv(config_channels_filename)['Ch2'].values[-1]
        except IndexError:
            value = 0.0
        self.label_value_ch2['text'] = '\n' + str(value)
        self.label_value_ch2.after(interval, self.update_value_ch2)
        
def main():
    write_config_parameters()
    write_config_channels()
    app = Frontend(Lock_in_settings)
    app.mainloop()
    while True:
        pass


if __name__ == '__main__':
    main()