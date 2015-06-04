#### script to identify ROH regions for all probands

library(recessiveStats)

get_bjobs <- function() {
    args = c("-o", "\"JOBID", "USER", "STAT", "QUEUE", "JOB_NAME", "delimiter=';'\"")
    bjobs = system2("bjobs", args, stdout=TRUE)
    
    # if there aren't any running jobs, return a blank dataframe
    if (length(bjobs) == 1) {
        return(data.frame(JOBID=character(0), USER=character(0), STAT=character(0),
            QUEUE=character(0), JOB_NAME=character(0)))
    }
    
    bjobs = read.table(text=bjobs, sep=";", header=TRUE)
    
    return(bjobs)
}

get_running_jobs <- function() {
    bjobs = get_bjobs()
    return(bjobs = bjobs[bjobs$STAT == "RUN", ])
}

probands = get_undiagnosed_sanger_ids()
for (proband in probands) {
    
    while (nrow(get_bjobs()) > 500) { Sys.sleep(30) }
    
    command = "bsub"
    args = c("-o", "./autozygosity.bjob_output.txt",
        "-q", "normal",
        "-R", "\"select[mem>100] rusage[mem=100]\"",
        "-M", 100,
        "bash", "-c",
        "\"/software/R-3.1.2/bin/Rscript", "./scripts/autozygosity/proband_autozygosity.R",
        "--proband", proband,
        "\"")
    
    system2(command, args)
    Sys.sleep(0.25)
}