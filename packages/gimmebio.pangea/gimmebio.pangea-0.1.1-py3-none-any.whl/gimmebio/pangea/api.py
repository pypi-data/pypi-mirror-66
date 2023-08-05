
from multiprocessing import Pool
from pangea_api import (
    Organization,
)
from .utils import (
    bcify,
    caching_get_sample,
    caching_get_sample_ar,
)
from .constants import WASABI_URL


def upload_one_cap_uri(lib, uri, endpoint_url=WASABI_URL):
    fname = uri.split('/')[-1]
    sample_name, module_name, field_name = fname.split('.')[:3]
    module_name = 'cap1::' + module_name
    sample_name = bcify(sample_name)
    sample = caching_get_sample(lib, sample_name)
    ar = caching_get_sample_ar(sample, module_name)
    field = ar.field(field_name, {
        '__type__': 's3',
        'endpoint_url': endpoint_url,
        'uri': uri,
    }).idem()
    return field


def upload_cap_uri_list(knex, org_name, lib_name, uri_list, threads=1, endpoint_url=WASABI_URL):
    org = Organization(knex, org_name).get()
    lib = org.sample_group(lib_name, private=True).idem()

    upload_funcs = [
        lambda: upload_one_cap_uri(lib, uri, endpoint_url=endpoint_url)
        for uri in uri_list
    ]
    with Pool(threads) as pool:
        for field in pool.imap_unordered(upload_funcs):
            yield field
