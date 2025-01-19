import posixpath
from urllib.parse import urljoin

def url_join(host: str, model: str, *additional_path: str) -> str:
    print(f"Joining: {host}::{model}::{additional_path}")
    suffix = "/".join([x for x in additional_path if x is not None])
    return urljoin(host, posixpath.join(model, suffix))