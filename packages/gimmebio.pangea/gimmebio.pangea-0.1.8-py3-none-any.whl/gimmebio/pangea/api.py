
from multiprocessing import Pool, Lock
from pangea_api import (
    Organization,
    RemoteObjectOverwriteError,
)
from .utils import (
    bcify,
    caching_get_sample,
    caching_get_sample_ar,
)
from .constants import WASABI_URL


def upload_one_cap_uri(lib, uri, endpoint_url=WASABI_URL, module_prefix='', lock=None):
    fname = uri.split('/')[-1]
    sample_name, module_name, field_name = fname.split('.')[:3]
    module_name = module_prefix + module_name
    sample_name = bcify(sample_name)
    if lock:
        lock.acquire()
    sample = caching_get_sample(lib, sample_name)
    ar = caching_get_sample_ar(sample, module_name)
    if lock:
        lock.release()
    field = ar.field(field_name, {
        '__type__': 's3',
        'endpoint_url': endpoint_url,
        'uri': uri,
    }).idem()
    return field


def upload_one_cap_uri_wrapper(args):
    try:
        return upload_one_cap_uri(
            args[0], args[1], endpoint_url=args[2], module_prefix=args[3], lock=args[4]
        )
    except RemoteObjectOverwriteError:
        pass


def upload_cap_uri_list(knex, org_name, lib_name, uri_list, threads=1, endpoint_url=WASABI_URL, module_prefix=''):
    org = Organization(knex, org_name).get()
    lib = org.sample_group(lib_name).get()
    lock = Lock()
    upload_args = [(lib, uri, endpoint_url, module_prefix, lock) for uri in uri_list]
    if threads == 1:
        for args in upload_args:
            field = upload_one_cap_uri_wrapper(args)
            if field:
                yield field
    else:  # currently broken
        with Pool(threads) as pool:
            for field in pool.imap_unordered(upload_one_cap_uri_wrapper, upload_args):
                yield field
