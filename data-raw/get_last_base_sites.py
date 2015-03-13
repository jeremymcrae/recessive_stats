""" identify all the sites in the genome at the last base in a exon, where the
coding sequence is a G.

The rationale is that the last base in an exon is fairly conserved as G, and
modifying this base may have a loss-of-function consequence. Gencode contains
coordinates for all exons, so we get the psoitions of the exons, find which is
the last base (depending on the gene's strand), and check if the sequence at
that site is a G.

We will later run the clinical filteting code, incorporating these sites, and
modifying any missense or synonymous variants at these sites to a LoF
consequence (splice_donor_variant).
"""

from __future__ import print_function

import sys
import gzip
import json
import argparse

from pyfaidx import Fasta

IS_PYTHON3 = sys.version[0] == "3"

def get_options():
    """ get the command line options
    """
    
    parser = argparse.ArgumentParser(description="finds sites at the last base \
        of exons (strand specific) with the correct base.")
    parser.add_argument("--fasta",
        default="/software/ddd/resources/v1.2/hs37d5.fasta",
        help="genome reference assembly sequence to use.")
    parser.add_argument("--gencode",
        default="/nfs/users/nfs_j/jm33/reference_data/gencode.v19.annotation.gtf.gz", \
        help="path to gencode positions (including exon coordinates)")
    parser.add_argument("--base", default="G",
        help="base that the reference genome must be at the last position of the exons")
    parser.add_argument("--out",
        default="/lustre/scratch113/projects/ddd/users/jm33/last_base_sites.json",
        help="path to write sites to")
    
    args = parser.parse_args()
    
    return args

def remove_header(handle):
    """ remove the header from the gencode file
    """
    
    current = handle.tell()
    
    while handle.readline().startswith("#"):
        current = handle.tell()
    
    handle.seek(current)

def parse_gencode_attributes(string):
    """ parse gencode attributes into a dictionary
    """
    
    string = string.strip().split(";")
    
    if string[-1] == "":
        a = string.pop()
    
    pairs = {}
    for item in string:
        item = item.strip().split(" ")
        key = item[0]
        value = item[1].strip("\"")
        pairs[key] = value
    
    return pairs


def convert_chromosome(chrom):
    """ make sure the chromosome string matches the genome fasta format
    """
    
    chrom = chrom.replace("chr", "")
    
    if chrom == "M":
        chrom = "MT"
    
    return(chrom)

def check_site(genome, chrom, position, strand, required="G"):
    """ check if a single genome position has a last base G
    
    Args:
        genome: Fasta object, to extract sequence from
        position: position of end of exon (gencode coordinate)
        strand: "+" or "-", for the strand of the transcript
        required: the required base to match, typically a guanine.
    """
    
    position = int(position) - 1
    site = genome[chrom][position]
    
    base = site.seq
    if strand == "-":
        base = site.complement.seq
    
    return base == required

def get_last_base_sites(genome, gencode, output_path, base):
    """ find the last base in exons where the base is a G (strand specific).
    """
    
    sites = []
    used = set([])
    for line in gencode:
        line = line.split("\t")
        chrom = line[0]
        source = line[1]
        feature = line[2]
        start = line[3]
        end = line[4]
        strand = line[6]
        attributes = line[8]
        
        if feature == "exon":
            key = (chrom, end)
            if key in used:
                continue
            
            chrom = convert_chromosome(line[0])
            attributes = parse_gencode_attributes(attributes)
            
            # only use the last base (strand specific)
            pos = end
            if strand == "-":
                pos = start
            
            if check_site(genome, chrom, pos, strand, base):
                sites.append([chrom, pos])
            
            used.add(key)
    
    # write the sites to a json file
    with open(output_path, "w") as output:
        json.dump(sites, output, indent=4, sort_keys=True)

def main():
    """
    """
    
    options = get_options()
    
    gencode = gzip.open(options.gencode)
    if IS_PYTHON3:
        gencode = gzip.open(options.gencode, "rt")
    remove_header(gencode)
    
    genome = Fasta(options.fasta)
    
    get_last_base_sites(genome, gencode, options.out, options.base)


if __name__ == "__main__":
    main()
