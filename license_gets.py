'''license_gets.py
    Menkyo Get's like Gui app
'''

import tkinter as tk
from tkinter import ttk

import urllib.parse
import webbrowser

from denpa_basic import DenpaSearch
import ja_call


class Application(tk.Frame):
    '''Application - class to define GUI widgets

        tkinter widgets will be defined in Application.__init__

        Args:
            master
        Returns:
            None
    '''

    def __init__(self, master):
        super().__init__(master)
        # self.grid()

        self.record_matched = False
        self.address = ''

        INITIAL_MSG = '総務省による免許状情報の交信には、\nタイムラグがあります。\n' +\
            '相手方の免許の有効期限が少し過ぎていても、\n再免許済みの可能性がありますのでご注意を!'

        frame1 = tk.Frame(master)

        label1 = tk.Label(frame1,
                          # width=10,
                          height=1,
                          text='Call',
                          # bg='white',
                          border=1,
                          # font=('', 12, 'bold'),
                          # justify=tk.CENTER,
                          padx=5,
                          pady=5,
                          # relief='ridge',
                          # textvariable=some_StringVar,
                          )
        
        label1.grid(row=0, column=0)

        self.entry1 = tk.Entry(frame1,
                               background='white', foreground='black',
                               width=10,
                               # font=('',10,'bold'),
                               justify=tk.CENTER,
                               relief='ridge',
                               # textvariable='JS2IIU',
                               # border=1,
                               )
        self.entry1.grid(row=0, column=1)
        label1.bind('<Button-1>', self.click_call)
        self.entry1.bind('<KeyRelease>', self.entry_key_release)
        entry1_tooltip = Tooltip(self.entry1, 'コールサインを入力してEnterキーを押してください')

        qth_button = tk.Button(frame1,
                               text='QTH',
                               command=self.qth_command)
        qth_button.grid(row=0, column=2)
        qth_button_tooltip = Tooltip(qth_button, 'QTHと免許状情報を検索して表示します')

        from_button = tk.Button(frame1,
                                text='From')
        from_button.grid(row=0, column=3)

        to_button = tk.Button(frame1,
                              text='To')
        to_button.grid(row=0, column=4)

        qrz_button = tk.Button(frame1,
                               text='QRZ',
                               command=self.qrz_command)
        qrz_button.grid(row=0, column=5)
        qrz_button_tooltip = Tooltip(qrz_button, 'QRZ.comでコールサインを検索します')

        map_button = tk.Button(frame1,
                               text='Map',
                               command=self.map_command)
        map_button.grid(row=0, column=6)
        map_button_tooltip = Tooltip(map_button, 'Google MapsでQTHの地図を表示します')

        frame1.grid(pady=10)

        # 検索結果表示用ラベル
        self.out_label = tk.Label(master,
                                  text=INITIAL_MSG,
                                  width=45, height=12,
                                  font=('', 15),
                                  # bg='lightgreen',
                                  pady=20,
                                  border=1,
                                  wraplength=380,
                                  justify=tk.LEFT,
                                  )
        self.out_label.grid()

        extbtn = tk.Button(master,
                           text='Exit',
                           # foreground='black'
                           # background='white',
                           # font=('', 12, 'bold'),
                           # borderwidth=1,
                           height=1,
                           width=6,
                           justify=tk.CENTER,
                           # padx=5, pady=5,
                           # textvariable=some_StringVar,
                           command=quit
                           )
        extbtn.grid()

    def qth_command(self):
        ''' QTH button action to get station information from soumu-DB '''
        self.record_matched = False

        callsign = self.entry1.get()
        callsign = callsign.upper()

        if len(callsign) > 4:

            out_text = ''

            if ja_call.is_ja_call(callsign):
                info_dict = DenpaSearch.get_station_detail_by_callsign(callsign)

                num = int(info_dict['musenInformation']['totalCount'])
                last_update = info_dict['musenInformation']['lastUpdateDate']

                out_text = out_text + f'*データ更新日： {last_update}\n'
            else:
                num = 0

            if num != 0:
                self.record_matched = True
                for _ in range(num):
                    self.address = info_dict['musen'][_]['listInfo']['tdfkCd']
                    station_name = info_dict['musen'][_]['listInfo']['name']
                    baseaddress = \
                        info_dict['musen'][_]['detailInfo']['radioEuipmentLocation']
                    license_date = info_dict['musen'][_]['detailInfo']['licenseDate']
                    valid_terms = info_dict['musen'][_]['detailInfo']['validTerms']
                    movement_area = info_dict['musen'][_]['detailInfo']['movementArea']
                    radio_spec = info_dict['musen'][_]['detailInfo']['radioSpec1']

                    out_text = out_text +\
                        f'[{_}/{num}]{station_name}\n{baseaddress}\n' +\
                        f'{license_date}から {valid_terms}\n' +\
                        f'{movement_area}\n{radio_spec}\n'

                out_text = f'設置場所=  {self.address}\n' + out_text
            else:
                self.record_matched = False
                out_text = out_text + '結果なし\n'

            self.out_label['text'] = out_text

    def qrz_command(self):
        ''' try to open QRZ.com '''
        callsign = self.entry1.get()
        callsign = callsign.upper()

        if callsign:
            qrz_url = f'https://www.qrz.com/db/{callsign}'
            webbrowser.open(url=qrz_url, new=0)
            self.out_label['text'] = f'QRZ.com, {callsign}のページを開きます。'

    def map_command(self):
        ''' try to open Google Map '''
        if self.record_matched:
            address_quoted = urllib.parse.quote(self.address)
            qrz_url = f'https://www.google.com/maps/place/{address_quoted}'
            webbrowser.open(url=qrz_url, new=0)
            self.out_label['text'] = f'Google Mapsで, {self.address}のページを開きます。'
        else:
            self.out_label['text'] = 'コールサインを入力してQTHボタンを押してください。'

    def click_call(self, event):
        ''' clear callsign '''
        # print('delete')
        self.entry1.delete(0, tk.END)

    def entry_key_release(self, event):
        ''' Keyrelease event handler on Entry1 '''
        # print(event.keycode, event.keysym, repr(event.keysym), type(event.keysym))
        if event.keysym == 'Return':
            self.qth_command()


class Tooltip:
    ''' ToolTip class'''
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 30

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(self.tooltip,
                          text=self.text,
                          background="#ffffe0", relief="solid",
                          borderwidth=1, anchor=tk.CENTER)
        label.pack(ipadx=3, ipady=3)

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def main():
    '''example to call Application class'''

    root = tk.Tk()

    root.geometry('500x380')
    root.title('License Get')
    root.grid_anchor(tk.CENTER)

    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
