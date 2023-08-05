#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library imports
import gzip
import logging
import os
import re
import subprocess
import sys

# third-party imports
import click
from ruamel.yaml import YAML

# module imports
from ..helper import check_file
from ..helper import check_subprocess_dependencies
from ..helper import create_directories
from ..helper import return_filehandle
from ..helper import setup_logging


def index_fasta(fasta):
    """Indexes the supplied fasta file using bgzip and samtools"""
    compressed_fasta = "{}.gz".format(fasta)  # will now have gz after bgzip
    if not check_file(compressed_fasta):
        cmd = "bgzip -f --index {}".format(fasta)  # bgzip command
        subprocess.check_call(cmd, shell=True)
    cmd = "samtools faidx {}".format(compressed_fasta)  # samtools faidx
    subprocess.check_call(cmd, shell=True)
    return compressed_fasta  # return new compressed and indexed gff


def index_gff3(gff3):
    """Indexes the supplied gff3 file using bgzip and tabix"""
    compressed_gff = "{}.gz".format(gff3)  # will now have gz after bgzip
    if not check_file(compressed_gff):
        cmd = "bgzip -f {}".format(gff3)  # bgzip command
        subprocess.check_call(cmd, shell=True)
    cmd = "tabix -p gff {}".format(compressed_gff)  # tabix index command
    standard_outval = subprocess.call(cmd.split(" "))
    if standard_outval:
        # tabix index command
        cmd = "tabix --csi -p gff {}".format(compressed_gff)
        subprocess.check_call(cmd, shell=True)
    return compressed_gff  # return new compressed and indexed gff


@click.command()
@click.option("--target", type=str, help="""TARGETS can be files or directories or both""")
@click.option(
    "--log_file",
    metavar="<FILE>",
    default="./normalizer_index.log",
    help="""File to write log to. (default:./normalizer_index.log)""",
)
@click.option(
    "--log_level",
    metavar="<LOGLEVEL>",
    default="INFO",
    help="""Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default:INFO)""",
)
def cli(target, log_file, log_level):
    """Determines what type of index to apply to input target"""
    check_subprocess_dependencies()
    logger = setup_logging(log_file, log_level)
    if not target:
        logger.error("--target argument required")
        sys.exit(1)
    target = os.path.abspath(target)
    file_types = ["fna", "fasta", "fa", "gff", "gff3", "faa", "ADD MORE"]
    fasta = ["fna", "fasta", "fa", "faa"]
    gff3 = ["gff", "gff3"]
    file_attributes = target.split(".")
    new_file = False
    if len(file_attributes) < 2:
        error_message = """Target {} does not have a type or attributes.  File must end in either gz, bgz, fasta, fna, fa, gff, or gff3.""".format(
            target
        )
        logger.error(error_message)
        sys.exit(1)
    file_type = file_attributes[-1]
    if file_type == "gz" or file_type == "bgz":
        file_type = file_attributes[-2]
        logger.error("Uncompress file for indexing.  Compression is done specifically for each index type")
        sys.exit(1)
    if file_type not in file_types:
        logger.error("File {} is not a type in {}".format(target, file_types))
        sys.exit(1)
    if file_type in fasta:
        logger.info("Target is a FASTA file indexing...")
        new_file = index_fasta(target)
        logger.info("Indexing done, final file: {}".format(new_file))
    if file_type in gff3:
        logger.info("Target is a gff3 file indexing...")
        new_file = index_gff3(target)
        logger.info("Indexing done, final file: {}".format(new_file))
    if not new_file:
        logger.error("Indexing FAILED.  See Log.")
        sys.exit(1)
    return new_file
