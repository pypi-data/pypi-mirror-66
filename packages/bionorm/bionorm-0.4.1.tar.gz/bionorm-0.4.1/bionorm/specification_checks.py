#!/usr/bin/env python
# -*- coding: utf-8 -*-

# standard library imports
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
from glob import glob
from os import path

# third-party imports
import requests

# module imports
from .helper import check_file
from .helper import return_filehandle

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class genome_main:
    def __init__(self, detector, **kwargs):
        self.detector = detector
        self.target = detector.target
        self.logger = detector.logger

    def run(self):
        """Runs checks"""
        logger = self.logger
        target = self.target
        logger.info("Performing Naming Checks for {}\n".format(target))
        if not self.check_genome_main():
            logger.error("Naming Check FAILED")
            return False
        logger.info("Naming Looks Correct\n")
        logger.info("Checking Genome FASTA\n")
        if not self.check_genome_fasta():
            logger.error("FASTA Check FAILED")
            return False
        logger.info("ALL GENOME CHECKS PASSED\n")
        return True

    def check_genome_main(self):
        """accepts a list of genome attributes split by "."

           https://github.com/LegumeFederation/datastore/issues/23

           checks these file attributes to ensure they are correct
        """
        target = self.target
        logger = self.logger
        attr = os.path.basename(target).split(".")  # split on delimiter
        if len(attr) != 7:  # should be 7 fields
            logger.error("File did not have 7 fields! {}".format(attr))
            return False
        if len(attr[0]) != 5:  # should be 5 letter prefix
            logger.error("File must have 5 letter prefix, not {}".format(attr[0]))
            return False
        if not attr[2].startswith("gnm"):  # should be gnm type
            logger.error("File should have gnm in field 3, not {}".format(attr[2]))
            return False
        gnm_v = attr[2].replace("gnm", "")
        try:
            int(gnm_v)
        except ValueError:  # best way to check for int in python2
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if len(gnm_v.split(".")) > 1:  # check for float
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if not attr[5] == "fna":  # should be fna type
            logger.error("File should be fna not {}".format(attr[5]))
            return False
        if not attr[6] == "gz":  # should be gzip compressed
            logger.error("Last field should be gz, not {}".format(attr[6]))
            return False
        logger.info("Genome Naming Looks Correct")
        return True

    def check_genome_fasta(self):
        """Confirms that headers in fasta genome_main conform with standard

           PUT SOME RULE REFERENCE HERE
        """
        logger = self.logger
        fasta = self.target  # get fasta file
        attr = os.path.basename(fasta).split(".")  # get attributes for naming
        true_header = ".".join(attr[:3])
        fh = return_filehandle(fasta)  # get file handle, text/gz
        # grab header and description
        re_header = re.compile(r"^>(\S+)\s*(.*)")
        passed = True
        with fh as gopen:
            for line in gopen:
                line = line.rstrip()
                if not line:
                    continue
                if re_header.match(line):  # check for fasta header
                    hid = re_header.search(line)
                    if hid:
                        logger.debug(hid.groups(0))
                        if isinstance(hid, str):  # check for tuple
                            hid = hid.groups(0)
                        else:
                            hid = hid.groups(0)[0]  # get id portion of header
                    else:
                        logger.error("Header {} looks odd...".format(line))
                        return False
                    logger.debug(hid)
                    self.detector.fasta_ids[hid] = 1
                    standard_header = true_header + "." + hid
                    if not hid.startswith(true_header):
                        logger.warning(("Inconsistency {} ".format(hid) + "Should be {}".format(standard_header)))
                        passed = False
        return passed


class gene_models_main:
    def __init__(self, detector, **kwargs):
        self.detector = detector
        self.target = detector.target
        self.logger = detector.logger
        self.fasta_ids = detector.fasta_ids

    def run(self):
        """Run checks"""
        logger = self.logger
        target = self.target
        logger.info("Checking Gene Models File Naming...")
        if not self.check_gene_models_main():
            logger.error("Gene Model File Naming FAILED")
            return False
        logger.info("Naming Looks Correct\n")
        logger.info("Validating GFF3 with gt...")
        if not self.gt_gff3_validate():
            logger.error("gt GFF3 Validation FAILED")
            return False
        logger.info("GFF3 is Valid\n")
        logger.info("Checking Congruency Between Genome and Gene Models...")
        if not self.check_seqid_attributes():
            logger.error("Genome and Gene Models are not Congruent FAILED")
            return False
        logger.info("ALL GENE MODELS CHECKS PASSED\n")
        return True

    def check_gene_models_main(self):
        """accepts a list of annotation attributes split by "."

           https://github.com/LegumeFederation/datastore/issues/23

           checks these file attributes to ensure they are correct
        """
        target = self.target
        logger = self.logger
        attr = os.path.basename(target).split(".")  # split on delimiter
        if len(attr) != 8:  # should be 8 fields
            logger.error("File did not have 7 fields! {}".format(attr))
            return False
        if len(attr[0]) != 5:  # should be 5 letter prefix
            logger.error("File must have 5 letter prefix, not {}".format(attr[0]))
            return False
        if not attr[2].startswith("gnm"):  # should be gnm type
            logger.error("File should have gnm in field 3, not {}".format(attr[2]))
            return False
        gnm_v = attr[2].replace("gnm", "")
        try:
            int(gnm_v)
        except ValueError:  # best way to check for int in python2
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if len(gnm_v.split(".")) > 1:  # check for float
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if not attr[3].startswith("ann"):  # should be gnm type
            logger.error("File should have ann in field 4, not {}".format(attr[2]))
            return False
        ann_v = attr[3].replace("ann", "")
        try:
            int(ann_v)
        except ValueError:  # best way to check for int in python2
            logger.error("ann version must be integer not {}".format(ann_v))
            return False
        if len(ann_v.split(".")) > 1:  # check for float
            logger.error("ann version must be integer not {}".format(gnm_v))
            return False
        if not attr[6] == "gff3":  # should be gff3 type
            logger.error("File should be gff3 not {}".format(attr[6]))
            return False
        if not attr[7] == "gz":  # should be gzip compressed
            logger.error("Last field should be gz, not {}".format(attr[6]))
            return False
        return True

    def gt_gff3_validate(self):
        """Confirms that gff3 files pass gt validation

           https://github.com/LegumeFederation/datastore/issues/23
        """
        gff = self.target
        logger = self.logger
        gff_name = os.path.basename(gff)
        gt_report = "./{}_gt_gff3validator_report.txt".format(gff_name)
        gt_cmd = "(gt gff3validator {} 2>&1) > {}".format(gff, gt_report)
        logger.debug(gt_cmd)
        exit_val = subprocess.call(gt_cmd, shell=True)  # get gt exit_val
        logger.debug(exit_val)
        if exit_val:
            return False
        return True

    def check_seqid_attributes(self):
        """Confirms that gff3 seqid exists in genome_main if provided

           checks ID and Name from gff3 attributes field

           https://github.com/LegumeFederation/datastore/issues/23
        """
        gff = self.target
        logger = self.logger
        fasta_ids = self.fasta_ids  # list of FASTA IDS from Reference
        logger.debug(fasta_ids)
        fh = return_filehandle(gff)
        file_name = os.path.basename(gff)
        # ID should start with this string
        true_id = ".".join(file_name.split(".")[:4])
        true_name = file_name.split(".")[0]  # maybe this should include infra
        #        get_id_name = re.compile("^ID=(.+?);.*Name=(.+?);")
        get_id = re.compile("ID=([^;]+)")
        lines = 0
        seen = {}
        passed = True
        with fh as gopen:
            for line in gopen:
                line = line.rstrip()
                lines += 1
                if not line or line.startswith("#"):
                    continue
                columns = line.split("\t")  # get gff3 fields
                seqid = columns[0]  # seqid according to the spec
                seqid = seqid.rstrip()
                logger.debug(line)
                logger.debug(seqid)
                if self.fasta_ids:  # if genome_main make sure seqids exist
                    if seqid not in fasta_ids:  # fasta header check
                        logger.debug(seqid)
                        if seqid not in seen:
                            logger.error("{} not found in genome_main".format(seqid))
                            seen[seqid] = 1
                        passed = False
                feature_type = columns[2]  # get type
                attributes = columns[8]  # attributes ';' delimited
                logger.debug(feature_type)
                if feature_type != "gene":  # only check genes (for now)
                    continue
                #                if not get_id_name.match(attributes):  # check for ID and Name
                if not get_id.search(attributes):  # check for ID and Name
                    logger.error("No ID and Name attributes. line {}".format(lines))
                    passed = False
                else:
                    #                    groups = get_id_name.search(attributes).groups()
                    feature_id = get_id.search(attributes).group(1)
                    logger.debug(feature_id)
                    #                    if len(groups) != 2:  # should just be ID and Name
                    #                        logger.error('too many groups detected: {}'.format(
                    #                                                                      groups))
                    #                        passed = False
                    #                    (feature_id, feature_name) = groups
                    if not feature_id.startswith(true_id):  # check id
                        logger.error("gene feature id, should start with " + "{} line {}".format(true_id, lines))
                        passed = False
        #                    if not feature_name.startswith(true_name):
        #                        logger.error('feature name, should start with ' +
        #                                     '{} line {}'.format(true_name, lines))
        #                        passed = False
        return passed


class protein:
    def __init__(self, detector, **kwargs):
        self.detector = detector
        self.target = detector.target
        self.logger = detector.logger

    def run(self):
        """Run Checks for protein"""
        logger = self.logger
        logger.info("protein check {}".format(self.target))
        if not self.check_protein():
            logger.error("protein file naming checks FAILED")
            return False
        logger.info("ALL protein CHCEKS PASSED")
        return True

    def check_protein(self):
        """accepts a list of annotation attributes split by "."

           https://github.com/LegumeFederation/datastore/issues/23

           checks these file attributes to ensure they are correct
        """
        target = self.target
        logger = self.logger
        attr = os.path.basename(target).split(".")  # split on delimiter
        if len(attr) != 8:  # should be 8 fields
            logger.error("File did not have 7 fields! {}".format(attr))
            return False
        if len(attr[0]) != 5:  # should be 5 letter prefix
            logger.error("File must have 5 letter prefix, not {}".format(attr[0]))
            return False
        if not attr[2].startswith("gnm"):  # should be gnm type
            logger.error("File should have gnm in field 3, not {}".format(attr[2]))
            return False
        gnm_v = attr[2].replace("gnm", "")
        try:
            int(gnm_v)
        except ValueError:  # best way to check for int in python2
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if len(gnm_v.split(".")) > 1:  # check for float
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if not attr[3].startswith("ann"):  # should be gnm type
            logger.error("File should have ann in field 4, not {}".format(attr[2]))
            return False
        ann_v = attr[3].replace("ann", "")
        try:
            int(ann_v)
        except ValueError:  # best way to check for int in python2
            logger.error("ann version must be integer not {}".format(ann_v))
            return False
        if len(ann_v.split(".")) > 1:  # check for float
            logger.error("ann version must be integer not {}".format(gnm_v))
            return False
        if not attr[6] == "faa":  # should be gff3 type
            logger.error("File should be gff3 not {}".format(attr[6]))
            return False
        if not attr[7] == "gz":  # should be gzip compressed
            logger.error("Last field should be gz, not {}".format(attr[6]))
            return False
        return True


class protein_primaryTranscript:
    def __init__(self, detector, **kwargs):
        self.detector = detector
        self.target = detector.target
        self.logger = detector.logger

    def run(self):
        """Run Checks for protein_primaryTranscript"""
        logger = self.logger
        logger.info("protein_primaryTranscript check {}".format(self.target))
        if not self.check_protein_primaryTranscript():
            logger.error("protein_primaryTranscript naming checks FAILED")
            return False
        logger.info("ALL protein_primaryTranscript CHCEKS PASSED")
        return True

    def check_protein_primaryTranscript(self):
        """accepts a list of annotation attributes split by "."

           https://github.com/LegumeFederation/datastore/issues/23

           checks these file attributes to ensure they are correct
        """
        target = self.target
        logger = self.logger
        attr = os.path.basename(target).split(".")  # split on delimiter
        if len(attr) != 8:  # should be 8 fields
            logger.error("File did not have 7 fields! {}".format(attr))
            return False
        if len(attr[0]) != 5:  # should be 5 letter prefix
            logger.error("File must have 5 letter prefix, not {}".format(attr[0]))
            return False
        if not attr[2].startswith("gnm"):  # should be gnm type
            logger.error("File should have gnm in field 3, not {}".format(attr[2]))
            return False
        gnm_v = attr[2].replace("gnm", "")
        try:
            int(gnm_v)
        except ValueError:  # best way to check for int in python2
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if len(gnm_v.split(".")) > 1:  # check for float
            logger.error("gnm version must be integer not {}".format(gnm_v))
            return False
        if not attr[3].startswith("ann"):  # should be gnm type
            logger.error("File should have ann in field 4, not {}".format(attr[2]))
            return False
        ann_v = attr[3].replace("ann", "")
        try:
            int(ann_v)
        except ValueError:  # best way to check for int in python2
            logger.error("ann version must be integer not {}".format(ann_v))
            return False
        if len(ann_v.split(".")) > 1:  # check for float
            logger.error("ann version must be integer not {}".format(gnm_v))
            return False
        if not attr[6] == "faa":  # should be gff3 type
            logger.error("File should be gff3 not {}".format(attr[6]))
            return False
        if not attr[7] == "gz":  # should be gzip compressed
            logger.error("Last field should be gz, not {}".format(attr[6]))
            return False
        return True


class readme_md:  # need to populate this correctly later
    def __init__(self, detector, **kwargs):
        self.detector = detector
        self.target = detector.target
        self.logger = detector.logger
        self.fasta_ids = detector.fasta_ids

    def validate_checksum(self, md5_file, check_me):
        """Get md5 checksum for file and compare to expected"""
        logger = self.logger
        fh = return_filehandle(md5_file)
        hash_md5 = hashlib.md5()
        check_sum_target = ""
        switch = 0
        with fh as copen:
            for line in copen:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                fields = line.split()
                check_sum = fields[0]
                filename = fields[1]
                logger.debug("check_sum: {}, filename: {}".format(check_sum, filename))
                if not check_sum and filename:
                    logger.error("Could not find sum and name for {}".format(line))
                if filename == os.path.basename(check_me):
                    logger.info("Checksum found for {}".format(filename))
                    check_sum_target = check_sum
                    switch = 1
        if not switch:
            logger.error("Could not find checksum for {}".format(check_me))
            sys.exit(1)
        with open(check_me, "rb") as copen:
            for chunk in iter(lambda: copen.read(4096), b""):  # 4096 buffer
                hash_md5.update(chunk)
        target_sum = hash_md5.hexdigest()  # get sum
        logger.debug(target_sum)
        logger.debug(check_sum_target)
        if target_sum != check_sum_target:  # compare sums
            logger.error(
                ("Checksum for file {} {} ".format(check_me, target_sum) + "did not match {}".format(check_sum_target))
            )
            sys.exit(1)
        logger.info("Checksums checked out, moving on...")

    def validate_doi(self, readme):
        """Parse README.<key>.yml and get publication or dataset DOIs

           Uses http://www.doi.org/factsheets/DOIProxy.html#rest-api
        """
        logger = self.logger
        publication_doi = ""
        dataset_doi = ""
        object_dois = {}
