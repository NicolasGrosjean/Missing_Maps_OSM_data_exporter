import datetime
import json
import logging
import requests


def get_json_request_header():
    """
    Return the header for JSON request
    :return:
    """
    return {'Accept': 'application/json', 'Authorization': 'Token sessionTokenHere==', 'Accept-Language': 'en'}


def get_last_available_ohsome_date():
    url = 'http://api.ohsome.org/v0.9/elementsFullHistory/geometry?bboxes=0,0,0,0'\
          '&keys=landuse&properties=tags&showMetadata=false&time=2019-01-01,'
    test_time = datetime.datetime.now() - datetime.timedelta(days=30)
    status = 404
    while status == 404:
        r = requests.get(url + test_time.strftime('%Y-%m-%d'), headers=get_json_request_header())
        status = r.status_code
        test_time = test_time - datetime.timedelta(days=10)
    return test_time.strftime('%Y-%m-%d')


def download_ohsome_data(output_filename, bbox, start_time, tag, tag_type=None):
    """
    Download data for the ohsome API
    :param output_filename: The name (and path) of the file in which the downloaded result will be saved
    :param bbox: Bounding box of the download area
    :param start_time: Start time of the full history OSM (format %Y-%m-%d)
    :param tag: OSM tag on which data are filtered
    :param tag_type: OSM type 'node', 'way' or ‘relation’ OR geometry 'point', 'line' or 'polygon’; default: all 3 OSM types
    :return:
    """
    url = 'http://api.ohsome.org/v0.9/elementsFullHistory/geometry?bboxes=' + bbox +\
          '&keys=' + tag + '&properties=tags&showMetadata=false&time=' + start_time + ',' +\
          get_last_available_ohsome_date()
    if tag_type is not None:
        url += '&types=' + tag_type
    logging.info(f'Ohsome API query : {url}')
    r = requests.get(url, headers=get_json_request_header())
    with open(output_filename, 'w') as outfile:
        json.dump(r.json(), outfile)
    logging.info('Ohsome API query done')


if __name__ == '__main__':
    #TODO replace it by unit test(s)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    download_ohsome_data('ohsome_4416_landuse.geojson', '12.2318065166473,3.76756175863216,12.2694861888885,3.79394007750437', '2019-01-01', 'landuse', 'polygon')
