% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/calculate_autozygosity.R
\name{check_autozygosity_in_chrom}
\alias{check_autozygosity_in_chrom}
\title{identify chromosomal regions where a proband has runs-of-homozygosity}
\usage{
check_autozygosity_in_chrom(bcf_path, proband, chrom, map)
}
\arguments{
\item{bcf_path}{path to a BCF for the full genome across all probands}

\item{proband}{ID for the proband to analyse}

\item{chrom}{chromosome to analyse}

\item{map}{genetic recombination map for the given chromosome}
}
\value{
dataframe of proband ID, chromosome, start and end coordinates.
}
\description{
identify chromosomal regions where a proband has runs-of-homozygosity
}

