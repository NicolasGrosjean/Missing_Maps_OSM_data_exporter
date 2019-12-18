import logging
import os

import sys

from src.extract_historical_osm_data import download_ohsome_data, get_last_available_ohsome_date

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_tmm_data import TmmProjectDatabase


def extract_perimeter(db):
    project_id = db.get_project_id()
    os.makedirs(os.path.join('data', str(project_id)), exist_ok=True)
    db.export_perimeter(os.path.join('data', str(project_id), 'perimeter.json'))
    print('Bounding box of the project : ')
    print(db.get_perimeter_bbox_as_string())


def export_historical_osm_data(db):
    project_id = db.get_project_id()
    bbox = db.get_perimeter_bbox_as_string()
    start_time = db.get_creation_date()
    end_time = get_last_available_ohsome_date()
    # TODO : Read osm_full_history_config
    tag = 'building'
    # TODO : Put nomenclature
    output_filename = os.path.join('data', str(project_id), tag + '_' + end_time + '.geojson')
    download_ohsome_data(output_filename, bbox, start_time, end_time, tag, tag_type=None)


if __name__ == '__main__':
    logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    try:
        project_id = input('Project ID : ')
        db = TmmProjectDatabase(project_id)
        extract_perimeter(db)
        # TODO Add user choice to extract or not historical osm data
        export_historical_osm_data(db)
    except Exception as e:
        logging.exception(e)
        print(f'ERROR : {e}')
