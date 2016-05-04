import json
import requests

class DockerhubClient():
    default_image = "tusoftwarestudio/dreamsuite"

    def __init__(self):
        self.base_url = "https://registry.hub.docker.com/v1/repositories/"


    def list_tags(self, image=default_image):
        request = requests.get(self.base_url + image + '/tags')
        tags_list = json.loads(request.content)
        return [tag['name'] for tag in tags_list]


    def check_if_tag_exists(self, tag, image=default_image):
        tags = self.list_tags(image)
        return tag in tags
