import pymysql.cursors
from .config import DATABASE


def connect():
    # Connect to the database
    return pymysql.connect(
        host=DATABASE['host'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        db=DATABASE['db'],
        cursorclass=pymysql.cursors.DictCursor)


class Page:
    def __init__(self,
                 ID='',
                 meta_image='',
                 meta_image_width='',
                 meta_image_height='',
                 meta_author='',
                 meta_title='',
                 meta_description='',
                 meta_keywords='',
                 meta_more='',
                 meta_addons='',
                 meta_url='',
                 meta_status='',
                 meta_ping='',
                 meta_to_ping='',
                 meta_pinged='',
                 meta_modified='',
                 meta_last_update='',
                 post_name='',
                 post_categories='',
                 post_tags='',
                 meta_lang='',
                 post_embed='',
                 post_start='',
                 post_stars='',
                 post_description='',
                 post_content='',
                 post_parent_guid='',
                 post_images_links='',
                 post_links='',
                 post_more_urls='',
                 post_guid='',
                 post_type='',
                 post_mime_type='',
                 post_related_guids='',
                 post_related_names='',
                 post_related_thumbs='',
                 additional_1='',
                 additional_2='',
                 additional_3='',
                 additional_4='',
                 additional_5='',
                 additional_6='',
                 additional_7='',
                 additional_8='',
                 additional_9='',
                 additional_10=''):
        self.meta_image = meta_image
        self.meta_image_height = meta_image_height,
        self.meta_image_width = meta_image_width,
        self.meta_author = meta_author
        self.meta_title = meta_title
        self.meta_description = meta_description
        self.meta_keywords = meta_keywords
        self.meta_more = meta_more
        self.meta_addons = meta_addons
        self.meta_url = meta_url
        self.meta_status = meta_status
        self.meta_ping = meta_ping
        self.meta_to_ping = meta_to_ping
        self.meta_pinged = meta_pinged
        self.meta_modified = meta_modified
        self.meta_last_update = meta_last_update
        self.post_name = post_name
        self.post_categories = post_categories
        self.post_tags = post_tags
        self.meta_lang = meta_lang
        self.post_embed = post_embed
        self.post_start = post_start
        self.post_stars = post_stars
        self.post_description = post_description
        self.post_content = post_content
        self.post_parent_guid = post_parent_guid
        self.post_images_links = post_images_links
        self.post_links = post_links
        self.post_more_urls = post_more_urls
        self.post_guid = post_guid
        self.post_type = post_type
        self.post_mime_type = post_mime_type
        self.post_related_guids = post_related_guids
        self.post_related_names = post_related_names
        self.post_related_thumbs = post_related_thumbs
        self.additional_1 = additional_1
        self.additional_2 = additional_2
        self.additional_3 = additional_3
        self.additional_4 = additional_4
        self.additional_5 = additional_5
        self.additional_6 = additional_6
        self.additional_7 = additional_7
        self.additional_8 = additional_8
        self.additional_9 = additional_9
        self.additional_10 = additional_10

    def select(self, query):
        if not self.db:
            self.connect()
        return self.db.query(query)

    def get_insert_string(self, db_name, table_name, safe=False):
        names = []
        values = []
        for key, value in self.__dict__.items():
            names.append('`{}`'.format(str(key)))
            values.append('"{}"'.format(
                str(value).replace('`', '"').replace('"', '')))
        res = ''' INSERT INTO `{}`.`{}` ({}) VALUES '''.format(
            db_name, table_name,
            ','.join(names))
        if safe:
            return res + '({}); '.format(
                ','.join(["%s" for key in values])), tuple(values)
        else:
            return res + '({}); '.format(','.join(values))

    def get_All(self, query, *attr):
        db = connect()
        with db.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchall()
        db.close()
        return result

    def get_keywords(self):
        db = connect()
        with db.cursor() as cursor:
            # Read a single record
            sql = "SELECT `meta_keywords` FROM `eporner`"
            cursor.execute(sql)
            result = cursor.fetchall()
        db.close()
        return result


def save(query, args=None):
    db = connect()
    try:
        with db.cursor() as cursor:
            # Create a new record
            cursor.execute(query, args)
            # cursor.
            # cursor.ex
            # connection is not autocommit by default. So you must commit/save
            # your changes.
            db.commit()
    finally:
        db.close()


def savemany(query, args):
    db = connect()
    try:
        with db.cursor() as cursor:
            # Create a new record
            cursor.executemany(query, args)
            # cursor.
            # cursor.ex
            # connection is not autocommit by default. So you must commit/save
            # your changes.
            db.commit()
    finally:
        db.close()


CREATE_STRING = '''
-- CREATE DATABASE IF NOT EXISTS `{}`;

CREATE TABLE IF NOT EXISTS `{}`.`{}` (
  `ID` INT AUTO_INCREMENT PRIMARY KEY,
  `meta_author` text ,
  `meta_image` text ,
  `meta_image_width` text ,
  `meta_image_height` text ,
  `meta_title` text ,
  `meta_description` text,
  `meta_keywords` text ,
  `meta_more` text ,
  `meta_addons` text ,
  `meta_url` text ,
  `meta_status` text ,
  `meta_ping` text ,
  `meta_to_ping` text ,
  `meta_pinged` text ,
  `meta_modified` text  ,
  `meta_last_update` text  ,

  `post_name` text  ,
  `post_categories` text  ,
  `post_tags` text  ,
  `meta_lang` text  ,
  `post_embed` text  ,
  `post_start` text  ,
  `post_stars` text  ,
  `post_description` text  ,
  `post_content` text  ,
  `post_parent_guid` text  ,
  `post_images_links` text  ,
  `post_links` text  ,
  `post_more_urls` text  ,
  `post_guid` text   DEFAULT '',
  `post_type` text   DEFAULT 'post',
  `post_mime_type` text   DEFAULT '',

  `post_related_guids` text  , -- [, , , ]
  `post_related_names` text  , -- [, , , ]
  `post_related_thumbs` text  , -- [, , , ]

  `additional_1` text  ,
  `additional_2` text  ,
  `additional_3` text  ,
  `additional_4` text  ,
  `additional_5` text  ,
  `additional_6` text  ,
  `additional_7` text  ,
  `additional_8` text  ,
  `additional_9` text  ,
  `additional_10` text
)
'''
