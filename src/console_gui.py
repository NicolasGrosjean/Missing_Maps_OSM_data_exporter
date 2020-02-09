import datetime
import logging
import os

import sys

from src.extract_historical_osm_data import download_ohsome_data, get_last_available_ohsome_date

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_tmm_data import TmmProjectDatabase


def extract_perimeter(db, iso3, localisation):
    project_id = db.get_project_id()
    os.makedirs(os.path.join('data', str(project_id)), exist_ok=True)
    db.export_perimeter(os.path.join('data', str(project_id),  iso3 + '_' + localisation + '_perimeter.json'))
    print('Bounding box of the project : ')
    print(db.get_perimeter_bbox_as_string())


def read_osm_full_history_config():
    config = []
    file = 'osm_full_history_config.txt'
    if not file in os.listdir():
        file = os.path.join('..', file)
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        if line.replace(' ', '').replace('\n', '') != '':
            split_line = line.split(',')
            config.append({'tag': split_line[0].replace('\n', ''),
                           'tag_type': split_line[1].replace('\n', '') if len(split_line) > 1 and split_line[1].replace('\n', '') != '' else None})
    return config


def check_date_format(date):
    splitted_date = date.split('-')
    if len(splitted_date) != 3:
        return False
    try:
        formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        if formatted_date > datetime.datetime.now():
            return False
        if int(splitted_date[0]) > 3000 or int(splitted_date[0]) < 2010:
            return False
        if int(splitted_date[1]) > 12 or int(splitted_date[1]) < 0:
            return False
    except ValueError:
        return False
    return True


def export_historical_osm_data(db, config, iso3, localisation):
    project_id = db.get_project_id()
    poly = input('Do you want download data for the exact perimeter (otherwise a bounding box) [y/N] :')
    if poly == 'y':
        polygons = ''
        for polygon in db.get_perimeter_poly()['coordinates']:
            if polygons != '':
                polygons += '|'
            polygons += str(polygon).replace('[', '').replace(']', '').replace(' ', '')
        area = 'bpolys=' + polygons
    else :
        bbox_str = db.get_perimeter_bbox_as_string()
        print(f'The bounding box of the project is {bbox_str}')
        extension_percent = input('Which percentage do you want increase the surface of the bounding box [0 to do not increase] : ')
        try:
            extension_percent = int(extension_percent)
            bbox_str = db.get_extended_perimeter_bbox_as_string(extension_percent)
            print(f'The extended bounding box is {bbox_str}')
        except Exception as e:
            print('Error when extending bounding box. Have you entered an integer like 20 for 20% ?')
        area = 'bboxes=' + bbox_str
    start_time = db.get_creation_date()
    print(f'The start time of the project is {start_time}')
    user_start_time = input(f'Start time of the data extraction [default {start_time}]: ')
    if not check_date_format(user_start_time):
        user_start_time = start_time
    latest_update = db.get_latest_update_date()
    print(f'The date of the latest update of the project is {latest_update}')
    end_time = get_last_available_ohsome_date()
    print(f'The date of the latest available data is {end_time}')
    user_end_time = input(f'End time of the data extraction [default {end_time}]: ')
    if not check_date_format(user_end_time) or \
            datetime.datetime.strptime(user_end_time, '%Y-%m-%d') > datetime.datetime.strptime(end_time, '%Y-%m-%d') or \
            datetime.datetime.strptime(user_end_time, '%Y-%m-%d') < datetime.datetime.strptime(user_start_time, '%Y-%m-%d'):
        user_end_time = end_time
    for obj in config:
        tag = obj['tag']
        tag_and_type = tag + '_' + obj['tag_type'][0] if obj['tag_type'] is not None else tag
        filename = iso3 + '_' + localisation + '_' + tag_and_type + '_osm_' + user_start_time + '_' + user_end_time + '.geojson'
        output_filename = os.path.join('data', str(project_id), filename)
        download_ohsome_data(output_filename, area, user_start_time, user_end_time, tag, tag_type=None)


if __name__ == '__main__':
    logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    try:
        project_id = input('Project ID : ')
        db = TmmProjectDatabase(project_id)
        print('Project #' + project_id + ' ' + db.get_project_name())
        iso3 = input('Code iso-3 of the country (EX: FRA) : ')
        localisation = input('Localisation of the project (EX: The city or camp name) : ')
        extract_perimeter(db, iso3, localisation)
        want_histo_data = input('Do you want extract OSM historical data [y/N] : ')
        if want_histo_data == 'y':
            config = read_osm_full_history_config()
            export_historical_osm_data(db, config, iso3, localisation)
    except Exception as e:
        logging.exception(e)
        print(f'ERROR : {e}')
