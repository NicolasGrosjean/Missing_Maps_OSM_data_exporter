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
    url = 'https://tasks.hotosm.org/api/v1/project/' + str(project_id)
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
        min_lat, min_lon, max_lat, max_lon = self.get_perimeter_bbox()
        return str(min_lat) + ', ' + str(min_lon) + ', ' + str(max_lat) + ', ' + str(max_lon)

    def export_perimeter(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.project_data['areaOfInterest'], outfile)

    def get_creation_date(self, date_format='%Y-%m-%d'):
        return datetime.datetime.strptime(self.project_data['created'], '%Y-%m-%dT%H:%M:%S.%f').strftime(date_format)
