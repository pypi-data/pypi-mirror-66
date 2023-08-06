from urllib.parse import unquote, urlparse
from warnings import warn
from requests.exceptions import Timeout

import quilt3


def store_rasters(dest=None):
    """Save raster data to the local quilt package storage.

    Returns
    -------
    None
        Data will be available in the local quilt registry and available
        for use in interpolation functions from the `harmonize` module.

    """
    quilt3.Package.install("rasters/nlcd", "s3://spatial-ucr", dest=dest)


def fetch_quilt_path(path):
    """Get the path to a raster stored with quilt.

    Parameters
    ----------
    path : str
        string identifying raster from CGS quilt database, or full path to
        a local raster file. Current options include "nlcd_2001", "nlcd_2011",
        or the path to a local file.

    Returns
    -------
    str
        If the input is in the quilt database, then return the full path,
        otherwise return the original path untouched

    """
    if path in ["nlcd_2011", "nlcd_2001"]:
        try:
            from quilt3.data.rasters import nlcd

        except ImportError:
            raise IOError(
                "Unable to locate local raster data. You can store NLCD rasters locally using "
                "the `data.store_rasters()` function (python kernel restart required"
            )

        full_path = unquote(nlcd[path + ".tif"].get())
        parts = urlparse(full_path)
        if parts.hostname:
            full_path = parts.scheme + "://" + parts.hostname + parts.path
        else:
            full_path = parts.path

    else:
        return path
    return full_path
