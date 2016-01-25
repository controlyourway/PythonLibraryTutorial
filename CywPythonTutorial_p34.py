#!/usr/bin/python

import ControlYourWay_v1_p34
import tkinter
from tkinter import messagebox

class GuiControls():
    def __init__(self):
        gui = tkinter.Tk()
        pad_x = 5
        pad_y = 3
        self.gui = gui
        self.cyw = None
        self.data_received = ''
        self.debug_messages = ''
        self.packet_id = 0
        self.gui_row_number = 0

        gui.title('Control Your Way Tutorial')

        # user name, network password, set network names and start button (column 1)
        tkinter.Label(gui, text='User name:').grid(row=self.get_row_num(False), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_user_name = tkinter.Entry(gui, width=25)
        self.entry_user_name.insert(0, 'your_email@address.com')
        self.entry_user_name.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        tkinter.Label(gui, text='Network password:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_network_password = tkinter.Entry(gui, width=25)
        self.entry_network_password.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        self.entry_network_password.insert(0, 'network_password')
        tkinter.Label(gui, text='Network names:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_network_names = tkinter.Text(gui, wrap=tkinter.WORD, undo=True, height=5, width=15)
        self.text_network_names.grid(row=self.get_row_num(True), column=0, columnspan=1, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_network_names = tkinter.Scrollbar(gui, command=self.text_network_names.yview)
        self.scroll_network_names.grid(row=self.get_row_num(False), column=0, sticky='nsew')
        self.text_network_names['yscrollcommand'] = self.scroll_network_names.set
        self.text_network_names.insert(tkinter.INSERT, 'network 1')
        self.button_set_network_names = tkinter.Button(gui, text='Set network names', width=16, command=self.click_button_set_network_names)
        self.button_set_network_names.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.button_start = tkinter.Button(gui, text='Start', width=12, command=self.click_button_start)
        self.button_start.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')

        # send data controls
        tkinter.Label(gui, text='Text to send:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_send_data = tkinter.Entry(gui, width=56)
        self.entry_send_data.grid(row=self.get_row_num(True), column=0, columnspan=2, padx=pad_x, pady=pad_y, sticky='W')
        self.entry_send_data.insert(0, 'test message')
        self.button_send = tkinter.Button(gui, text='Send', width=12, command=self.click_send_data)
        self.button_send.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.button_send_discovery = tkinter.Button(gui, text='Send discovery', width=12, command=self.click_send_discovery)
        self.button_send_discovery.grid(row=self.get_row_num(False), column=1, padx=pad_x, pady=pad_y, sticky='W')

        # received data
        tkinter.Label(gui, text='Text received:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_rec_data = tkinter.Text(gui, wrap=tkinter.WORD, undo=True, height=5, width=40)
        self.text_rec_data.grid(row=self.get_row_num(True), column=0, columnspan=3, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_rec_data = tkinter.Scrollbar(gui, command=self.text_rec_data.yview)
        self.scroll_rec_data.grid(row=self.get_row_num(False), column=3, sticky='nsew')
        self.text_rec_data['yscrollcommand'] = self.scroll_rec_data.set
        self.button_clear_rec_data = tkinter.Button(gui, text='Clear', width=12, command=self.click_clear_rec_data)
        self.button_clear_rec_data.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        
        # debug messages
        tkinter.Label(gui, text='Debug messages:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_debug_messages = tkinter.Text(gui, wrap=tkinter.WORD, undo=True, height=5, width=40)
        self.text_debug_messages.grid(row=self.get_row_num(True), column=0, columnspan=3, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_debug_messages = tkinter.Scrollbar(gui, command=self.text_debug_messages.yview)
        self.scroll_debug_messages.grid(row=self.get_row_num(False), column=3, sticky='nsew')
        self.text_debug_messages['yscrollcommand'] = self.scroll_debug_messages.set
        self.button_clear_debug_messages = tkinter.Button(gui, text='Clear', width=12, command=self.click_clear_debug_messages)
        self.button_clear_debug_messages.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')

        # set callback for when the window closes. This will terminate the Control Your Way service and
        # stop all the threads
        self.gui.protocol("WM_DELETE_WINDOW", self.form_closing)

        gui.mainloop()

    def get_row_num(self, new_row):
        if new_row:
            self.gui_row_number += 1
        return  self.gui_row_number

    def add_debug_message(self, message):
        self.debug_messages += message + '\n'
        self.text_debug_messages.insert(tkinter.END, message + '\n')
        self.text_debug_messages.see(tkinter.END)

    def data_received_callback(self, data, data_type, from_who):
        if self.cyw.get_discoverable() and data_type == 'Discovery Response':
            # valid discovery response received
            self.add_debug_message('Device Discovered: ' + data + ', ID: ' + str(from_who))
        else:
            message = data + ', ' + data_type + ', ' + str(from_who)
            self.text_rec_data.insert(tkinter.END, message + '\n')
            self.text_rec_data.see(tkinter.END)

    def connection_status_callback(self, connected):
        if connected:  # connection was successful
            self.add_debug_message('Connection successful')
        else:
            # there was an error
            self.add_debug_message('Connection failed')


    def click_button_set_network_names(self):
        if self.cyw is not None:
            network_names = self.text_network_names.get("1.0", tkinter.END).split('\n')
            self.cyw.set_network_names(network_names)

    def click_send_discovery(self):
        if self.cyw is not None:
            self.cyw.send_discovery()

    def click_button_start(self):
        if self.cyw is None:
            user_name = self.entry_user_name.get()
            network_password = self.entry_network_password.get()
            network_names = self.text_network_names.get("1.0", tkinter.END).split('\n')
            input_error = False
            if user_name is '':
                messagebox.showerror('User name error', 'Please enter a valid user name')
                input_error = True
            if network_password is '':
                messagebox.showerror('Network password error', 'Please enter a valid network password')
                input_error = True
            if not input_error:
                # start cyw service
                self.cyw = ControlYourWay_v1_p34.CywInterface()
                self.cyw.set_user_name(user_name)
                self.cyw.set_network_password(network_password)
                self.cyw.set_network_names(network_names)
                self.cyw.set_connection_status_callback(self.connection_status_callback)
                self.cyw.set_data_received_callback(self.data_received_callback)
                self.cyw.name = 'Cyw Python Tutorial'
                self.cyw.start()
            self.button_start['text'] = 'Stop'
        else:
            self.cyw.close_connection()
            self.button_start['text'] = 'Start'
            self.cyw = None

    def click_send_data(self):
        if self.cyw is not None:
            send_data = ControlYourWay_v1_p34.CreateSendData()
            send_data.data = self.entry_send_data.get()
            send_data.data_type = 'data'
            if self.cyw.connected:
                self.cyw.send_data(send_data)
        else:
            messagebox.showerror('Please start service', 'The service needs to be started before this action can be performed')

    def click_clear_rec_data(self):
        self.text_rec_data.delete(1.0, tkinter.END)

    def click_clear_debug_messages(self):
        self.text_debug_messages.delete(1.0, tkinter.END)

    def form_closing(self):
        if self.cyw is not None:
            self.cyw.close_connection(True)
        self.cyw = None
        self.gui.destroy()


if __name__ == "__main__":
    # cyw = CywInterface()
    gui_controls = GuiControls()
