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


def download_ohsome_data(output_filename, area, start_time, end_time, tag, tag_type=None):
    """
    Download data for the ohsome API
    :param output_filename: The name (and path) of the file in which the downloaded result will be saved
    :param area: Download area
    :param start_time: Start time of the full history OSM (format %Y-%m-%d)
    :param end_time: End time of the full history OSM (format %Y-%m-%d)
    :param tag: OSM tag on which data are filtered
    :param tag_type: OSM type 'node', 'way' or ‘relation’ OR geometry 'point', 'line' or 'polygon’; default: all 3 OSM types
    :return:
    """
    url = 'http://api.ohsome.org/v0.9/elementsFullHistory/geometry?' + area +\
          '&keys=' + tag + '&properties=tags&showMetadata=false&time=' + start_time + ',' + end_time
    if tag_type is not None:
        url += '&types=' + tag_type
    logging.info(f'Ohsome API query : {url}')
    print(f'Extract {tag} data between {start_time} and {end_time}')
    r = requests.get(url, headers=get_json_request_header())
    with open(output_filename, 'w') as outfile:
        json.dump(r.json(), outfile)
    logging.info('Ohsome API query done')


if __name__ == '__main__':
    #TODO replace it by unit test(s)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    #download_ohsome_data('ohsome_4416_landuse.geojson', 'bboxes=12.2318065166473,3.76756175863216,12.2694861888885,3.79394007750437', '2019-01-01', '2019-10-31', 'landuse', 'polygon')
    #poly = '-1.62814136470792,12.2784694870073,-1.63989587306597,12.2834707118329,-1.64880483030894,12.2958465179707,-1.66373937010386,12.3194650066627,-1.63251443385699,12.3336065182876,-1.60014888822654,12.3407795046204,-1.59506409048655,12.3305577758608,-1.58803737341979,12.3269793559982,-1.58506481527903,12.3255165297506,-1.5917697932806,12.3175271721334,-1.60379748905563,12.308644626348,-1.60957295561695,12.293538334863,-1.6198397811737,12.2798651069825,-1.62814136470792,12.2784694870073'
    poly='-1.54031754612941,12.28019064899,-1.52987838863938,12.27988663163,-1.53038265466939,12.27582954918,-1.54043008834941,12.27744420216,-1.54031754612941,12.28019064899|-1.59952077058669,12.3117523772958,-1.59176979328011,12.3175271721334,-1.58758885952442,12.3225232060329,-1.58596415148374,12.3169108440359,-1.59386028752265,12.3127283112115,-1.59952077058669,12.3117523772958'
    download_ohsome_data('ohsome_4416_landuse.geojson', 'bpolys=' + poly, '2019-01-01', '2019-10-31', 'landuse', 'polygon')
