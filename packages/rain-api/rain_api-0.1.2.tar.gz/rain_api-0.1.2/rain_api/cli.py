import click
from . import core as m

timeout = 5


# Get The Next Page or exit
def exit_function(url, page, data):
    if not page['meta']['pagination']['links'].get('next', False):
        return False, data
    return page['meta']['pagination']['links']['next'], data


# get_list(flowers, exit_function)
# get_list(strains, exit_function)
# get_list(extracts, exit_function)
# get_list(products, exit_function)

# get_core_iamges(edibles)
# get_core_iamges(flowers)
# get_core_iamges(strains)
# get_core_iamges(strains)
# get_core_iamges(strains)
# get_as_list(edibles)
# create_strains_nodes('static-upload-site/strains-nodes/')


@click.group()
@click.pass_context
def cli(ctx):
    """
    Welcome Any Project cli tool.\n
    With this tool you can register|monitor|operate rain_api Device please.

    For more information Please read our Docs
    """
    pass


@click.command(name="create")
@click.option('-N', '--name', default='example', help='API name')
@click.option('-N', '--url', default='https://yonimdo.github.io/rain_api/example-api/page-{}.json',
              help='API url Needs to be with {} for page')
def create(name, url):
    """Builds a new Api folder."""
    click.echo('Initialized the service.')
    # from apis.eporner.run import name as eporner
    # from apis.eporner.run import exit_function as exit_eporner
    # from apis.eporner.run import convert_json_to_pages
    # run = __import__('apis.{}.run'.format('eporner'))
    # module = __import__(
    #     'apis.{}.run'.format('eporner'), globals(),
    #     locals(),
    #     ['name', 'exit_function', 'convert_json_to_pages']
    #     , 0)
    m.create_api_folder(name, url)


@click.command()
@click.option('-N', '--name', default='example', help='API name')
@click.option('-L', '--list_prefix', default='data', help='List location')
@click.option('-I', '--id_prefix', default='_id', help='Item Id')
def start(name, list_prefix, id_prefix):
    """Start the listener and download content."""
    click.echo('Initialized the service.')
    # from apis.eporner.run import name as eporner
    # from apis.eporner.run import exit_function as exit_eporner
    # from apis.eporner.run import convert_json_to_pages
    # run = __import__('apis.{}.run'.format('eporner'))
    module = __import__(
        'apis.{}.run'.format(name), globals(),
        locals(),
        ['name', 'exit_function', 'convert_json_to_pages'], 0)
    m.download_list(module.name, module.exit_function, list_prefix=list_prefix,
                    item_id_prefix=id_prefix)


@click.command(name="to-sql")
@click.option('-N', '--name', default="example", help='Daemon mode')
def to_sql(name):
    """Start the listener for changes from the site."""
    click.echo('Initialized the service.')
    module = __import__(
        'apis.{}.run'.format(name), globals(),
        locals(),
        ['name', 'exit_function', 'convert_json_to_pages'], 0)
    # convert_to_sql_file(eporner, convert_json_to_pages)
    m.import_files_to_db(module.name, module.convert_json_to_pages)


@click.command(name="to-html")
@click.option('-N', '--name', default="example", help='Api name')
def to_html(name):
    """Start the listener for changes from the site."""
    click.echo('Initialized the service.')
    module = __import__(
        'apis.{}.run'.format(name), globals(),
        locals(),
        ['name', 'exit_function', 'convert_json_to_pages'], 0)
    m.create_html_website(module.name, module.convert_json_to_pages)


cli.add_command(create)
cli.add_command(start)
cli.add_command(to_sql)
cli.add_command(to_html)

if __name__ == '__main__':
    cli()
