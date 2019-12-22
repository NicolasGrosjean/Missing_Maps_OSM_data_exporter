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
                           'tag_type': split_line[1].replace('\n', '') if len(split_line) > 1 else None})
    return config


def export_historical_osm_data(db, config, iso3, localisation):
    project_id = db.get_project_id()
    bbox = db.get_perimeter_bbox_as_string()
    start_time = db.get_creation_date()
    end_time = get_last_available_ohsome_date()
    for obj in config:
        tag = obj['tag']
        tag_and_type = tag + '_' + obj['tag_type'][0] if obj['tag_type'] is not None else tag
        filename = iso3 + '_' + localisation + '_' + tag_and_type + '_osm_' + start_time + '_' + end_time + '.geojson'
        output_filename = os.path.join('data', str(project_id), filename)
        download_ohsome_data(output_filename, bbox, start_time, end_time, tag, tag_type=None)


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
