import logging
import os

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_tmm_data import TmmProjectDatabase


def extract_perimeter():
    project_id = input('Project ID : ')
    db = TmmProjectDatabase(project_id)
    os.makedirs(os.path.join('data', str(project_id)), exist_ok=True)
    db.export_perimeter(os.path.join('data', str(project_id), 'perimeter.json'))
    print('Bounding box of the project : ')
    db.print_perimeter_bbox()


if __name__ == '__main__':
    logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    try:
        extract_perimeter()
    except Exception as e:
        logging.exception(e)
        print(f'ERROR : {e}')
