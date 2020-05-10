import datetime
import json
import logging
import os

import requests


def get_json_request_header():
    """
    Return the header for JSON request
    :return:
    """
    return {'Accept': 'application/json', 'Authorization': 'Token sessionTokenHere==', 'Accept-Language': 'en'}


def download_project_data(project_id):
    """
    Download the project data of the HOT tasking manager project id
    :param project_id:
    :return:
    """
    url = 'https://tasking-manager-tm4-production-api.hotosm.org/api/v2/projects/' + str(project_id)
    r = requests.get(url, headers=get_json_request_header())
    print(f'Tasking Manager data for project {project_id} downloaded')
    logging.info(f'Tasking Manager data for {project_id} downloaded')
    return r.json()


class TmmProjectDatabase:
    """
    The Database class manage the loading of the data and if necessary the downloading and the storage
    """
    def __init__(self, project_id):
        self.project_id = project_id
        os.makedirs(os.path.join('data', 'tmm'), exist_ok=True)
        self.data_file_path = os.path.join('data', 'tmm', str(project_id) + '.json')
        if os.path.exists(self.data_file_path):
            logging.info(f'Tasking Manager data for {project_id} already downloaded')
            with open(self.data_file_path) as f:
                self.project_data = json.load(f)
        else:
            self.project_data = download_project_data(project_id)
            with open(self.data_file_path, 'w') as outfile:
                json.dump(self.project_data, outfile)
            logging.info(f'Tasking Manager data for {project_id} stored in {self.data_file_path}')

    def get_project_id(self):
        return self.project_id

    def get_project_name(self):
        return self.project_data['projectInfo']['name']

    def get_perimeter_bbox(self):
        return self.project_data['aoiBBOX'][0], self.project_data['aoiBBOX'][1], self.project_data['aoiBBOX'][2], self.project_data['aoiBBOX'][3]

    def get_perimeter_bbox_as_string(self):
        return bounding_box_to_str(self.get_perimeter_bbox())

    def get_extended_perimeter_bbox_as_string(self, extension_percent):
        return bounding_box_to_str(extend_bounding_box(self.get_perimeter_bbox(), extension_percent))

    def get_perimeter_poly(self):
        return self.project_data['areaOfInterest']

    def export_perimeter(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.project_data['areaOfInterest'], outfile)

    def get_creation_date(self, date_format='%Y-%m-%d'):
        try:
            creation_datetime = datetime.datetime.strptime(self.project_data['created'], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            creation_datetime = datetime.datetime.strptime(self.project_data['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return creation_datetime.strftime(date_format)

    def get_latest_update_date(self, date_format='%Y-%m-%d'):
        #TODO Improve it by putting the latest validation date
        try:
            latest_update_datetime = datetime.datetime.strptime(self.project_data['lastUpdated'], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            latest_update_datetime = datetime.datetime.strptime(self.project_data['lastUpdated'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return latest_update_datetime.strftime(date_format)


def bounding_box_to_str(bbox):
    min_lat, min_lon, max_lat, max_lon = bbox
    return str(min_lat) + ', ' + str(min_lon) + ', ' + str(max_lat) + ', ' + str(max_lon)


def extend_bounding_box(bbox, extension_percent):
    import math
    min_lat, min_lon, max_lat, max_lon = bbox
    factor = math.sqrt(1 + extension_percent/100)
    min_lat -= (factor - 1) * (max_lat - min_lat) / 2
    min_lon -= (factor - 1) * (max_lon - min_lon) / 2
    max_lat += (factor - 1) * (max_lat - min_lat) / 2
    max_lon += (factor - 1) * (max_lon - min_lon) / 2
    return min_lat, min_lon, max_lat, max_lon
