import logging
import os
import traceback
from tkinter import *
from tkinter.ttk import Labelframe

from src.console_gui import read_osm_full_history_config
from src.extract_historical_osm_data import get_last_available_ohsome_date, download_ohsome_data
from src.extract_tmm_data import TmmProjectDatabase


class MainDialog(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Historical data downloader')
        self.resizable(width=False, height=False)
        self.db = None
        #self.iconbitmap(os.path.join('res', 'cartong.png'))

        #######################
        # Project information #
        #######################
        row = 0
        project_label_frame = Labelframe(self, text='Project information')
        project_label_frame.grid(sticky='WE', columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

        row += 1
        self.project_id = StringVar()
        Label(project_label_frame, text='Project ID : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        e = Entry(project_label_frame, width=25, textvariable=self.project_id, validate='focusout',
                  validatecommand=self.set_project_data)
        e.grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)
        e.bind('<Return>', 'event generate %W <Tab>')

        row += 1
        self.project_name = StringVar()
        Label(project_label_frame, text='Project name : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Label(project_label_frame, textvariable=self.project_name).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        #########################
        # File name information #
        #########################
        row += 1
        file_name_label_frame = Labelframe(self, text='File name information')
        file_name_label_frame.grid(sticky='WE', columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

        row += 1
        self.iso3 = StringVar()
        Label(file_name_label_frame, text='Code ISO 3 (EX: FRA) : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Entry(file_name_label_frame, width=7, textvariable=self.iso3).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        self.localisation = StringVar()
        Label(file_name_label_frame, text='Localisation (EX: city or camp name) : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Entry(file_name_label_frame, width=7, textvariable=self.localisation).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        ###################
        # Extraction size #
        ###################
        row += 1
        extraction_size_label_frame = Labelframe(self, text='Extraction size')
        extraction_size_label_frame.grid(sticky='WE', columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

        row += 1
        self.extraction_type = StringVar(value='bbox')
        Radiobutton(extraction_size_label_frame, text='Polygon', variable=self.extraction_type, value='polygon',
                    command=self.hide_percent).grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Radiobutton(extraction_size_label_frame, text='Bounding Box', variable=self.extraction_type, value='bbox',
                    command=self.show_percent).grid(column=1, row=row, sticky=W, padx=10, pady=3)

        row += 1
        self.percent_increase_bbox = IntVar()
        self.percent_label = Label(extraction_size_label_frame,
                                   text='Surface increasing in % [0 to do not increase] : ')
        self.percent_label.grid(column=0, row=row, sticky=W, padx=10, pady=3)
        self.percent_entry = Entry(extraction_size_label_frame, width=7, textvariable=self.percent_increase_bbox)
        self.percent_entry.grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        #########
        # Dates #
        #########
        row += 1
        date_label_frame = Labelframe(self, text='Dates')
        date_label_frame.grid(sticky='WE', columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

        row += 1
        self.project_start_date = StringVar()
        Label(date_label_frame, text='Project start date : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Label(date_label_frame, textvariable=self.project_start_date).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        self.extraction_start_date = StringVar()
        Label(date_label_frame, text='Extraction start date : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Entry(date_label_frame, width=7, textvariable=self.extraction_start_date).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        self.project_end_date = StringVar()
        Label(date_label_frame, text='Project end date : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Label(date_label_frame, textvariable=self.project_end_date).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        ohsome_end_date = StringVar(value=get_last_available_ohsome_date())
        Label(date_label_frame, text='Ohsome latest available date : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Label(date_label_frame, textvariable=ohsome_end_date).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        self.extraction_end_date = StringVar()
        Label(date_label_frame, text='Extraction start date : ').grid(column=0, row=row, sticky=W, padx=10, pady=3)
        Entry(date_label_frame, width=7, textvariable=self.extraction_end_date).grid(column=1, row=row, sticky=(W, E), padx=10, pady=3)

        row += 1
        self.RunDialogButton = Button(self, text='Run', command=self.run)
        self.RunDialogButton.grid(row=row, columnspan=2, ipadx=20)

        row += 1
        self.LogBox = Text(self, height=10, width=60, state=DISABLED)
        self.LogBox.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

    def set_project_data(self):
        project_id = self.project_id.get()
        self.db = TmmProjectDatabase(project_id)
        self.project_name.set('Project #' + project_id + ' ' + self.db.get_project_name())
        self.project_start_date.set(self.db.get_creation_date())
        self.project_end_date.set(self.db.get_latest_update_date())
        return True

    def hide_percent(self):
        self.percent_label.grid_remove()
        self.percent_entry.grid_remove()

    def show_percent(self):
        self.percent_label.grid()
        self.percent_entry.grid()

    def alter_button(self, *args):
        if len(self.FilePathDisplayer.get()) > 0:
            self.RunDialogButton.config(state=NORMAL)
        else:
            self.RunDialogButton.config(state=DISABLED)

    def quit_dialog(self):
        self.destroy()

    def add_log(self, text):
        self.LogBox.config(state=NORMAL)
        self.LogBox.insert(END, text)
        self.LogBox.config(state=DISABLED)

    def run(self):
        try:
            if self.extraction_type.get() == 'polygon':
                polygons = ''
                for polygon in self.db.get_perimeter_poly()['coordinates']:
                    if polygons != '':
                        polygons += '|'
                    polygons += str(polygon).replace('[', '').replace(']', '').replace(' ', '')
                area = 'bpolys=' + polygons
            else:
                area = 'bboxes=' + self.db.get_extended_perimeter_bbox_as_string(self.percent_increase_bbox.get())
            config = read_osm_full_history_config()
            for obj in config:
                tag = obj['tag']
                tag_and_type = tag + '_' + obj['tag_type'][0] if obj['tag_type'] is not None else tag
                filename = self.iso3.get() + '_' + self.localisation.get() + '_' + tag_and_type + '_osm_' + self.extraction_start_date.get() + '_' + self.extraction_end_date.get() + '.geojson'
                output_filename = os.path.join('data', self.project_id.get(), filename)

                self.add_log(f'Extract {tag} data between {self.extraction_start_date.get()} and {self.extraction_end_date.get()}')
                download_ohsome_data(output_filename, area, self.extraction_start_date.get(), self.extraction_end_date.get(), tag, tag_type=None)
            self.LogBox.config(state=NORMAL)
            self.LogBox.delete("1.0", END)
            self.LogBox.insert(END, 'SUCCESS')
            self.LogBox.config(state=DISABLED)
        except Exception as e:
            logging.exception('Error: ' + str(e))
            self.LogBox.config(state=NORMAL)
            self.LogBox.delete("1.0", END)
            self.LogBox.insert(END, str(e) + '\n')
            self.LogBox.insert(END, ''.join(traceback.format_tb(e.__traceback__)))
            self.LogBox.config(state=DISABLED)


if __name__ == '__main__':
    logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    DialogObj = MainDialog()
    DialogObj.mainloop()
