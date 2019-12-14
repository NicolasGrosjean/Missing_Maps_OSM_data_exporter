import json
import os

import requests


def get_json_request_header():
    """
    Return the header for JSON request
    :return:
    """
    return {'Accept': 'application/json', 'Authorization': 'Token sessionTokenHere==', 'Accept-Language': 'en'}


def download_project_aoi(project_id):
    """
    Download the project data of the HOT tasking manager project id
    :param project_id:
    :return:
    """
    url = 'https://tasks.hotosm.org/api/v1/project/' + str(project_id) + '/aoi'
    r = requests.get(url, headers=get_json_request_header())
    return r.json()


class TmmProjectDatabase:
    """
    The Database class manage the loading of the data and if necessary the downloading and the storage
    """
    def __init__(self, project_id):
        os.makedirs(os.path.join('data', 'tmm'), exist_ok=True)
        self.data_file_path = os.path.join('data', 'tmm', str(project_id) + '.json')
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path) as f:
                self.project_aoi = json.load(f)
        else:
            self.project_aoi = download_project_aoi(project_id)
            with open(self.data_file_path, 'w') as outfile:
                json.dump(self.project_aoi, outfile)

    def get_perimeter_bbox(self):
        coordinates = self.project_aoi['coordinates']
        while len(coordinates) == 1:
            coordinates = coordinates[0]
        min_lat = 180
        min_lon = 180
        max_lat = -180
        max_lon = -180
        for point in coordinates:
            if point[0] < min_lat:
                min_lat = point[0]
            if point[0] > max_lat:
                max_lat = point[0]
            if point[1] < min_lon:
                min_lon = point[1]
            if point[1] > max_lon:
                max_lon = point[1]
        return min_lat, min_lon, max_lat, max_lon

    def export_perimeter(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.project_aoi, outfile)
