
import click
from os import environ
from pangea_api import (
    Knex,
    User,
)
from .api import upload_cap_uri_list
from .utils import bcify


@click.group()
def pangea():
    pass


@pangea.group()
def upload():
    pass


@upload.command('cap')
@click.option('--endpoint', default='https://pangea.gimmebio.com')
@click.option('--s3-endpoint', default='https://s3.wasabisys.com')
@click.option('-m', '--module-prefix', default='cap1::')
@click.option('-e', '--email', default=environ.get('PANGEA_USER', None))
@click.option('-p', '--password', default=environ.get('PANGEA_PASS', None))
@click.argument('org_name')
@click.argument('lib_name')
@click.argument('uri_list', type=click.File('r'))
def main(endpoint, s3_endpoint, module_prefix, email, password, org_name, lib_name, uri_list):
    """Register a list of S3 URIs with Pangea."""
    knex = Knex(endpoint)
    User(knex, email, password).login()
    for field in upload_cap_uri_list(knex, org_name, lib_name,
                                     (line.strip() for line in uri_list),
                                     endpoint_url=s3_endpoint,
                                     threads=1,
                                     module_prefix=module_prefix):
        click.echo(field, err=True)


@pangea.group()
def s3():
    """Functions involving S3."""
    pass


@s3.command('make-uris')
@click.option('-s', '--sep', default='\t')
@click.option('-f', '--filename-list', type=click.File('r'), default='-')
@click.option('-o', '--outfile', type=click.File('w'), default='-')
@click.argument('prefix')
def make_uri(sep, filename_list, outfile, prefix):
    """Convert a list of filenames to a list suitable for upload to s3.

    filename -> (filename, s3_uri)

    meant for use with xargs as roughly:
        `cat filenames.txt | <this command> | xargs -l <upload_to_s3>`
    """
    assert prefix.startswith('s3://')
    if not prefix.endswith('/'):
        prefix = prefix + '/'
    for line in filename_list:
        path = line.strip()
        fname = path.split('/')[-1]
        print(f'{path}{sep}{prefix}{fname}', file=outfile)


@s3.command('make-cap-uris')
@click.option('-s', '--sep', default='\t')
@click.option('-f', '--filename-list', type=click.File('r'), default='-')
@click.option('-o', '--outfile', type=click.File('w'), default='-')
@click.argument('bucket_name')
def make_uri(sep, filename_list, outfile, bucket_name):
    """Convert a list of filenames to a list suitable for upload to s3.

    filename -> (filename, s3_uri)

    meant for use with xargs as roughly:
        `cat filenames.txt | <this command> | xargs -l <upload_to_s3>`
    """
    prefix = f's3://{bucket_name}/analysis/metasub_cap1/results/'
    for line in filename_list:
        path = line.strip()
        if path.endswith('.flag.registered'):
            continue
        fname = path.split('/')[-1]
        tkns = fname.split('.')
        if len(tkns) < 4:  # sample name, module name, field name, ext+
            continue
        sample_name = bcify(tkns[0])
        fname = sample_name + '.' + '.'.join(tkns[1:])
        print(f'{path}{sep}{prefix}{sample_name}/{fname}', file=outfile)


if __name__ == '__main__':
    pangea()
