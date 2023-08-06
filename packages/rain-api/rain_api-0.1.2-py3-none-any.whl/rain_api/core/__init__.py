import json
import threading
import time
import requests
import io
import os
from PIL import Image
from . import config
import uuid
from . import templates
from .pages import Page, CREATE_STRING, savemany, save as saveline
import requests as r


def create_api_folder(name, link):
    makedir('apis/{}'.format(name))
    makedir('apis/{}/chunks'.format(name))
    makedir('apis/{}/html'.format(name))
    with open('apis/{}/__init__.py'.format(name), 'w', encoding='utf8') as f:
        f.write('')
    with open('apis/{}/run.py'.format(name), 'w', encoding='utf8') as f:
        f.write(templates.run.format(name, link, '{}'))
    with open('apis/{}/template.html'.format(name), 'w', encoding='utf8') as f:
        f.write(templates.example_html)
    with open('apis/{}/html/styles.css'.format(name),
              'w',
              encoding='utf8') as f:
        f.write(templates.example_css)


def current_milli_time():
    return lambda: int(round(time.time() * 1000))


url = 'https://source.unsplash.com/609x406/?{}'

BASE_DIR = config.BASE_DIR
MEMOREY_ERROR_ACCURED = False
TIMEOUT_ERROR = False
_doc = ['']


def doc(message, logit=True, cmd=True, end='\n'):
    if logit:
        if end == '\n':
            _doc.append(message)
        else:
            _doc[-1] = _doc[-1] + message
    if cmd:
        print(message, end=end)


def get_them(url, data, exit_function, list_prefix=config.LIST_PREFIX,
             item_id_prefix=config.ITEM_ID_PREFIX):
    try:
        if url:
            page = r.get(url)
            if not page.ok:
                return url, data
            # page = page.json()
            for item in page.json()[list_prefix]:
                data[config.NODES_PREFIX][item[item_id_prefix]] = item
        next_url, cache_data = exit_function(url, page, data)
        count = len(data[config.NODES_PREFIX].items())
        if count >= config.JSON_FILE_MAX_ITEM_COUNT:
            raise MemoryError
        return next_url, cache_data
    except TimeoutError:
        global TIMEOUT_ERROR
        TIMEOUT_ERROR = True
    except MemoryError:
        global MEMOREY_ERROR_ACCURED
        MEMOREY_ERROR_ACCURED = True
        return url, data


def get_chunks_file(name, ends="json"):
    return os.path.join(BASE_DIR, name,
                        config.JSON_CHUNKS_FOLDER if ends == 'json' else ends,
                        '{}.{}.{}'.format(name, uuid.uuid1(), ends))


def get_available_apis_file(name):
    return os.listdir(os.path.join(BASE_DIR, name, config.JSON_CHUNKS_FOLDER))


def get_json_file_chunked(name, uid):
    return os.path.join(BASE_DIR,
                        name,
                        config.JSON_CHUNKS_FOLDER,
                        '{}.{}.json'.format(name, uid))


def get_file(name, end='json'):
    return os.path.join(BASE_DIR, name, '{}.{}'.format(name, end))


def get_url_file(name):
    return os.path.join(BASE_DIR, name, 'url')


def empty_item():
    item = {}
    item[config.NODES_PREFIX] = {}
    item[config.EDGES_PREFIX] = []
    return item


def start(name):
    doc('Started at: {}'.format(name))
    url = __import__(
        'apis.{}.run'.format(name), globals(),
        locals(),
        ['base_url'],
        0).base_url
    data = get_file_items(os.path.join(BASE_DIR, name, '{}.json'.format(name)))

    if file_exist(get_url_file(name)):
        with open(get_url_file(name), 'r', encoding='utf8') as f:
            url = f.read()
    else:
        url = url.format('1')
    return url, data


def finish(name):
    doc('Exit: {}'.format(name))
    with open(os.path.join(BASE_DIR,
                           name,
                           'readable.md'),
              'w',
              encoding='utf8') as f:
        f.write(json.dumps(_doc))


def makedir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def file_exist(name):
    return os.path.isfile(name)


def get_file_items(filename, mode='r', is_json=True):
    if file_exist(filename):
        with open(filename, 'r', encoding='utf') as f:
            return json.loads(f.read()) if is_json else f.read()
    else:
        return empty_item() if is_json else None


def get_items_from_chunks(name, names):
    doc('Getting items from chunk')
    items = empty_item()
    count = len(items[config.NODES_PREFIX].keys())

    while len(names) != 0:
        items[config.NODES_PREFIX].update(get_file_items(os.path.join(
            BASE_DIR,
            name,
            config.JSON_CHUNKS_FOLDER,
            names.pop()))[config.NODES_PREFIX])
        doc(".", end='')
        count = len(items[config.NODES_PREFIX].keys())
        if count > config.SQL_FILE_MAX_ITEM_COUNT:
            break
    doc("Count:{}".format(count))
    return items


def export_page(name, page: Page, categories, template):
    makedir(os.path.join(BASE_DIR, name,
                         config.HTML_OUTPUT_FOLDER, page.post_type))
    obj = {'script': '''
        var item = {};
        var categories = {};
        '''.format(json.dumps(page.__dict__), json.dumps(categories))}
    obj.update(page.__dict__)
    page_template = str(template).format(**obj)

    with open(os.path.join(BASE_DIR, name, config.HTML_OUTPUT_FOLDER,
                           page.post_type,
                           "{}.html".format(page.post_guid)),
              'w',
              encoding='utf8') as f:
        f.write(page_template)


def export_pages(name, pages, categories):
    template = 'No template'
    with open(os.path.join(BASE_DIR, name,
                           'template.html'), 'r', encoding='utf8') as f:
        template = f.read()
    # export_page(name, pages[0], categories, template)
    [threading.Thread(target=export_page,
                      args=(name, page, categories, template))
     .start() for page in pages]


def create_html_website(name, map_function):
    url, data = start(name)
    keywords = {}
    # cat_ptrn = '''
    # <li class="">
    #     <a href="index.html?s={tag_search}" class="label">
    #         <i class="thumbnail">{tag_count}</i>
    #         {tag_search}
    #     </a>
    # </li>'''

    def insert(key, value):
        keywords[key] = value
    try:
        doc('Extracting keywords for {}. Please stand by'.format(name))
        [insert(item, keywords.get(item, 0)+1)
         for result in Page().get_keywords()
         for item in result['meta_keywords'].split(',')]
        categories = [{'tag_search': key, 'tag_count': '{}'.format(str(
            keyword/1000).split('.')[0])}
            for key, keyword in keywords.items() if keyword > 10000]
        doc('Mapping {} items'.format(
            len(data[config.NODES_PREFIX].keys())))
        pages = map_function(data)
        count = len(data)
        save_to_html(name, pages, categories)

        names = os.listdir(os.path.join(
            BASE_DIR, name, config.JSON_CHUNKS_FOLDER))
        doc('Extracting {} jsons to html files '.format(name))
        count = len(names)
        while count != 0:
            items = get_items_from_chunks(name, names)
            doc('Mapping {} items'.format(
                len(items[config.NODES_PREFIX].keys())))
            pages = map_function(items)
            count = len(names)
            if count != 0:
                doc('Memory Error: saving {} pages in sql chunks'.format(
                    len(pages)))
            save_to_html(name, pages, categories)
            doc('Saved!')
        finish(name)
    except KeyboardInterrupt:
        doc('Keyboard Interruped, exiting')
    finally:
        finish(name)


def import_files_to_db(name, map_function):
    url, data = start(name)
    try:
        doc('Mapping {} items'.format(
            len(data[config.NODES_PREFIX].keys())))
        pages = map_function(data)
        count = len(data)
        if count != 0:
            doc('Memory Error: saving {} pages in sql chunks'.format(
                len(pages)))
        save_sql(name, pages)
        names = os.listdir(os.path.join(
            BASE_DIR, name, config.JSON_CHUNKS_FOLDER))
        count = len(names)
        doc('Importing {} files from `{}` chunks folder'.format(
            count, name))
        while count != 0:
            items = get_items_from_chunks(name, names)
            doc('Mapping {} items'.format(
                len(items[config.NODES_PREFIX].keys())))
            pages = map_function(items)
            count = len(names)
            if count != 0:
                doc('Memory Error: saving {} pages in sql chunks'.format(
                    len(pages)))
            save_sql(name, pages)
            doc('Saved!')
    except KeyboardInterrupt:
        doc('Keyboard Interruped, exiting')
    finally:
        finish(name)


def convert_to_sql_file(name, map_function, remove_jsons=False):
    start(name)
    doc('Converting `{}` json to pages'.format(name))
    names = os.listdir(os.path.join(BASE_DIR, name, config.JSON_CHUNKS_FOLDER))
    names.append('{}.json'.format(name))
    count = len(names)
    while count != 0:
        items = get_items_from_chunks(name, names)
        doc('Mapping {} items'.format(len(items[config.NODES_PREFIX].keys())))
        pages = map_function(items)
        count = len(names)
        if count != 0:
            doc('Memory Error: saving {} pages in sql chunks'.format(
                len(pages)))
        save_sql_files(name, pages, chunk=count != 0)
    finish(name)


def save_to_csv(name, items):
    keys = items.keys()
    headers = []
    for key in keys:
        val = items[key]
        headers = headers + list(val.keys())
    headers = set(headers)
    lines = []
    lines.append(','.join(headers))
    for key in keys:
        line = []
        for header in headers:
            line.append(items[key].get(header, ''))
        lines.append(r"'{}'".format(r"','".join(line)))
    with open(os.path.join(BASE_DIR, name, "{}.csv".format(name)),
              'w',
              encoding='utf8') as f:
        f.write("\n".join(lines))


def save_sql_files(name, pages, chunk=False):
    # Save items
    makedir(os.path.join(BASE_DIR, name, config.SQL_CHUNKS_FOLDER))
    res = CREATE_STRING.format(name, config.DATABASE['db'], name)
    res = res + \
        ('\n').join([page.get_insert_string(
            config.DATABASE['db'], name, False) for page in pages])
    if chunk:
        filename = get_chunks_file(name, config.SQL_CHUNKS_FOLDER)
        doc('Saved To: {}'.format(filename))
        with open(filename, 'w', encoding='utf8') as f:
            f.write(res)
    else:
        with open(get_file(name, config.SQL_CHUNKS_FOLDER),
                  'w',
                  encoding='utf8') as f:
            f.write(res)


def save_to_html(name, pages, categories):
    # Save items
    export_pages(name, pages, categories)
    doc('Saved ({}) {} html pages'.format(len(pages), name))


def save_sql(name, pages):
    # Save items
    table = CREATE_STRING.format(name, config.DATABASE['db'], name)
    items = [page.get_insert_string(
        config.DATABASE['db'], name, True) for page in pages]
    if len(pages) == 0:
        print("0 Pages")
    sql_sample = items[0][0]
    saveline(table)
    items = [values for sql, values in items]
    savemany(sql_sample, items)
    doc('Saved ({}) {} pages to db'.format(len(pages), name))


def save(name, url, data, chunk=False):
    # Save url
    if url:
        doc('Stoped at: {}'.format(url))
        with open(get_url_file(name), 'w', encoding='utf8') as f:
            f.write(url)
    # Save items
    if chunk:
        filename = get_chunks_file(name)
        doc('Saved To: {}'.format(filename))
        with open(filename, 'w', encoding='utf8') as f:
            f.write(json.dumps(data))
    else:
        with open(get_file(name), 'w', encoding='utf8') as f:
            f.write(json.dumps(data))


def download_list(name, exit_function, list_prefix="data",
                  item_id_prefix="ocpc"):
    try:
        while True:
            get_list(name, exit_function, list_prefix, item_id_prefix)
            doc("Wating {} sec. read man".format(config.timeout))
            time.sleep(config.timeout)
    except KeyboardInterrupt:
        pass
    finish(name)


def get_list(name, exit_function, list_prefix, item_id_prefix):
    url, data = start(name)
    doc('Getting url: {}'.format(url))
    global MEMOREY_ERROR_ACCURED
    global TIMEOUT_ERROR
    try:
        delta_url = ''
        delta_count = config.DELTA_COUNT
        while url and (not MEMOREY_ERROR_ACCURED or TIMEOUT_ERROR):
            url, data = get_them(url, data, exit_function,
                                 list_prefix, item_id_prefix)
            if delta_url == url:
                delta_count = delta_count - 1
            else:
                delta_url = url
                delta_count = config.DELTA_COUNT
            print('.', end='')
            if delta_count == 0:
                raise KeyboardInterrupt
        if MEMOREY_ERROR_ACCURED:
            doc('Memory Error: saving data in chunks please read man')
        if TIMEOUT_ERROR:
            doc('Timeout Error Please change in config\n\t' + url)
        save(name, url, data, MEMOREY_ERROR_ACCURED)
        MEMOREY_ERROR_ACCURED = False
        TIMEOUT_ERROR = False
    except KeyboardInterrupt:
        doc('User Quit. Saving latest url \n\t' + url)
        raise KeyboardInterrupt
    finally:
        save(name, url, data)


def persist_image(name: str, image_name, url: str):
    try:
        image_content = requests.get(url).content
        doc("Downloaded {}".format(image_name))

    except Exception as e:
        doc("ERROR - Could not download {} - {}".format(url, e))

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(
            BASE_DIR, 'images', name, '{}.jpg'.format(image_name))
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        doc("SUCCESS - saved {} - as {}".format(url, file_path))
    except Exception as e:
        doc("ERROR - Could not save {} - {}".format(url, e))


def get_image(image_name, name, url):
    threading.Thread(target=persist_image, args=(
        name, image_name, url)).start()


def get_as_list(name):
    graph = {}
    with open(os.path.join(BASE_DIR, name, '{}.json'.format(name)),
              'r',
              encoding='utf8') as f:
        graph = json.loads(f.read())
        graph = graph[config.NODES_PREFIX]
        graph = graph.values()
        pass

    with open(os.path.join(BASE_DIR, 'output', '{}-list.json'.format(name)),
              'w',
              encoding='utf8') as f:
        f.write(json.dumps(list(graph)))


# def get_iamges(name, item_url_prefix='imglink'):
#     data = None
#     try:
#         with open(get_json_file(name), 'r', encoding='utf8') as f:
#             data = json.loads(f.read())
#             pass
#     except:
#         pass
#     for item in data:
#         get_image(name, item['slug'], item[item_url_prefix])
