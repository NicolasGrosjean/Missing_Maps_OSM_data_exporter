import logging
import os
from time import gmtime, strftime

import src.overpass


def extract_osm_data(expression, bbox, filename):
    """
    Extract with overpass corresponding OSM data according expression in the bounding box.
    :param expression: Expression
    :param bbox: Bounding box (Ex : '45.1416, 5.6732, 45.2270, 5.7826')
    :param filename: Filename which will be suffixed by the export date and the xml format
    """
    output_filename = filename + '_' + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.xml'
    os.makedirs('data', exist_ok=True)

    query = '('
    query += 'node[' + expression + '](' + bbox + ');'
    query += 'way[' + expression + '](' + bbox + ');'
    query += 'relation[' + expression + '](' + bbox + ');'
    query += ');(._;>;);'

    logging.info(f'Call Overpass to extract data for expression {expression}')
    api = src.overpass.API(endpoint='http://overpass-api.de/api/interpreter')
    response = api.get(query, verbosity='body', responseformat='xml')
    with open(os.path.join('data', output_filename), 'w', encoding='UTF-8') as outfile:
        outfile.write(response)
    logging.info('Data extracted from Overpass')
