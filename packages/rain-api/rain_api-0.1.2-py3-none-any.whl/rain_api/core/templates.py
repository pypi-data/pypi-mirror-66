run = '''
from rain_api import core as m
from rain_api.core.pages import Page
import re


name = '{0}'
page_ptrn = re.compile('page-([0-9]+)')
base_url = '{1}'


# Get The Next Page or exit
def exit_function(url, page, data):
    if page.status_code == 404:
        print('Exit at: {2}'.format(url))
        return False, data
    # page_number = int(page_ptrn.findall(url)[0]) + 1
    print(".", end='')
    return base_url.format(int(page_ptrn.findall(url)[0]) + 1), data


def convert_json_to_pages(data, export=False):
    pages = []
    for key, item in data['nodes'].items():
        gender = 'He' if item.get('gender', 'female') == 'female' else 'She'
        page = Page(
                meta_title='{2} | {2}'.format(
                    name.capitalize(),
                    item.get('name', '')),
                post_guid=item.get('guid', ''),
                post_name=item.get('name', ''),
                meta_image=item.get('picture', ''),
                post_images_links=''.join([item.get('picture', '')]),
                post_description='Company:{2} Email: {2}  Phone: {2} </br> {2}'
                .format(
                    item.get('company', 'Unknown'),
                    item.get('email', 'Unknown'),
                    item.get('phone', 'Unknown'),
                    '{2} likes {2}'
                    .format(gender, item.get('favoriteFruit', 'something')),
                    '{2} balance is ${2}'
                    .format(gender, item.get('balance', 'something')),
                ),
                post_tags=item.get('favoriteFruit', ''),
                meta_last_update=str(m.current_milli_time()),
                post_type='user'
               )
        pages.append(page)
    return pages

'''

example_css = '''
.card {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    max-width: 300px;
    margin: auto;
    text-align: center;
}
.title {
    color: grey;
    font-size: 18px;
}
button {
    border: none;
    outline: 0;
    display: inline-block;
    padding: 8px;
    color: white;
    background-color: #000;
    text-align: center;
    cursor: pointer;
    width: 100%;
    font-size: 18px;
}
a {
    text-decoration: none;
    font-size: 22px;
    color: black;
}
button:hover,
a:hover {
    opacity: 0.7;
}
'''

example_html = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{meta_title} | {post_name}</title>
    <meta property="og:locale" content="en_US" />
    <meta property="og:type" content="{post_type}" />
    <meta property="og:title" content="{post_name}" />
    <meta property="og:description" content="{post_description}" />
    <meta property="og:url" content="{meta_url}" />
    <meta property="og:title" content="{meta_title}" />
    <meta property="og:image" content="{meta_image}" />
    <meta property="og:image:width" content="{meta_image_width}" />
    <meta property="og:image:height" content="{meta_image_width}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:description" content="{post_description}" />
    <meta name="twitter:title" content="{meta_title} | {post_name}" />
    <meta name="twitter:image" content="{meta_image}" />
    <!--
    <meta name="generator" content="Powered by Yonimdo Page Builder." /> -->
    <!-- <link rel="alternate" hreflang="en-US" href="index.html" /> -->
    <link rel="icon" href="favicon.png" sizes="32x32" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <!-- <meta property="al:ios:url" content="ninegag://9gag.com/" />
    <meta property="al:ios:app_store_id" content="545551605" />
    <meta property="al:ios:app_name" content="9GAG" />
    <meta property="al:android:url" content="ninegag://9gag.com/" />
    <meta property="al:android:package" content="com.ninegag.android.app" />
    <meta property="al:android:app_name" content="9GAG" /> -->
    <script>{script}</script>
    <link rel="stylesheet" href="/styles.css">
</head>
<body >
    <div class="card">
        <img src="{meta_image}" alt="John" style="width:100%">
        <h1>{post_name}</h1>
        <p class="title">{additional_1}</p>
        <div>{post_description}</div>
    </div>
</body>

</html>
'''
