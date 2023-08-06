
from rain_api import core as m
from rain_api.core.pages import Page
import re


name = 'example'
page_ptrn = re.compile('page-([0-9]+)')
base_url = 'https://yonimdo.github.io/rain_api/example-api/page-{}.json'


# Get The Next Page or exit
def exit_function(url, page, data):
    if page.status_code == 404:
        print('Exit at: {}'.format(url))
        return False, data
    # page_number = int(page_ptrn.findall(url)[0]) + 1
    print(".", end='')
    return base_url.format(int(page_ptrn.findall(url)[0]) + 1), data


def convert_json_to_pages(data, export=False):
    pages = []
    for key, item in data['nodes'].items():
        gender = 'He' if item.get('gender', 'female') == 'female' else 'She'
        page = Page(
                meta_title='{} | {}'.format(
                    name.capitalize(),
                    item.get('name', '')),
                post_guid=item.get('guid', ''),
                post_name=item.get('name', ''),
                meta_image=item.get('picture', ''),
                post_images_links=''.join([item.get('picture', '')]),
                post_description='Company:{} Email: {}  Phone: {} </br> {}'
                .format(
                    item.get('company', 'Unknown'),
                    item.get('email', 'Unknown'),
                    item.get('phone', 'Unknown'),
                    '{} likes {}'
                    .format(gender, item.get('favoriteFruit', 'something')),
                    '{} balance is ${}'
                    .format(gender, item.get('balance', 'something')),
                ),
                post_tags=item.get('favoriteFruit', ''),
                meta_last_update=str(m.current_milli_time()),
                post_type='user'
               )
        pages.append(page)
    return pages

