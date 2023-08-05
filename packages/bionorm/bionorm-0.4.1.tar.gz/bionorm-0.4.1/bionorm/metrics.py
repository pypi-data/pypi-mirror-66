#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library imports
import gzip
import logging
import os
import sys

# module imports
from .helper import return_filehandle


def count_gff_features(gff):
    counts = {}
    fh = return_filehandle(gff)  # use magic filehandle method
    if not fh:
        logger.error("could not open {}".format(gff))
        sys.exit(1)
    with fh as fopen:
        for line in fopen:
            if not line or line.isspace() or line.startswith("#"):  # skip comments
                continue
            line = line.rstrip()
            f = line.split("\t")  # get fields
            if f[2] not in counts:  # feature type
                counts[f[2]] = 1
                continue
            counts[f[2]] += 1
    fh.close()
    return counts


if __name__ == "__main__":
    print(
        "import me to use stast for genome_main and gene_models_main."
        + "This should be in a class probably... but its w/e for now"
    )
    sys.exit(1)
