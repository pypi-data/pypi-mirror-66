"""
 Contains function that will process queued jobs, among which alignments,
 and orthology inference.
"""

import os
import sys
import time
import subprocess
import multiprocessing as mp
import queue
import gc
import shutil
from typing import Dict, List, Any, Tuple

from sonicparanoid import inpyranoid
from sonicparanoid import sys_tools as systools
from sonicparanoid import colored_output as colout
from sonicparanoid import essentials_c as essentials



__module_name__ = "Workers"
__source__ = "workers.py"
__author__ = "Salvatore Cosentino"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Cosentino Salvatore"
__email__ = "salvo981@gmail.com"



def info():
    """
    Contains functions that will process queued jobs
    """
    print("MODULE NAME:\t%s"%__module_name__)
    print("SOURCE FILE NAME:\t%s"%__source__)
    print("MODULE VERSION:\t%s"%__version__)
    print("LICENSE:\t%s"%__license__)
    print("AUTHOR:\t%s"%__author__)
    print("EMAIL:\t%s"%__email__)



def check_storage_for_mmseqs_dbs(outDir, reqSp=2, gbPerSpecies=0.95, debug=False):
    """Check that there is enough storage for the MMseqs2 index files."""
    if debug:
        print('\ncheck_storage_for_mmseqs_dbs :: START')
        print('Output directory: {:s}'.format(outDir))
        print('Number of databases to be created: {:d}'.format(reqSp))
        print('Required storage for index files: {:0.2f} gigabytes'.format(reqSp * gbPerSpecies))
    availSpaceGb = round(shutil.disk_usage(outDir).free / 1024 ** 3, 2)
    requiredSpaceGb = round(reqSp * gbPerSpecies, 2)
    # set the output variable
    createIdxFiles = True
    if requiredSpaceGb >= availSpaceGb:
        createIdxFiles = False
        infoLn = '{:0.2f} gigabytes required to store the index files for MMseqs2.'.format(requiredSpaceGb)
        colout.colored_info(outLn=infoLn, lnType='i', debug=debug)
        infoLn = 'only {:0.2f} gigabytes avaliable, MMseqs2 index files will not be created.'.format(availSpaceGb)
        colout.colored_info(outLn=infoLn, lnType='w', debug=debug)
        print('Please consider freeing some disk space to take advantage of MMseqs2 index files.')
    if debug:
        print('Available storage in your system (Gigabytes): {:0.2f}'.format(availSpaceGb))
    #sys.exit('DEBUG :: check_storage_for_mmseqs_dbs')
    # return the boolean
    return createIdxFiles



def create_dbs_parallel(jobs_queue, results_queue, inDir, dbDir, create_idx=True):
    """Create a a mmseqs2 database for the species in input dir."""
    while True:
        current_sp = jobs_queue.get(True, 1)
        if current_sp is None:
            break
        # check the query db name
        #queryDBname = os.path.basename(inFasta)
        inQueryPath = os.path.join(inDir, current_sp)
        if not os.path.isfile(inQueryPath):
            sys.stderr.write("ERROR: the input FASTA file \n{:s}\n was not found\n".format(inQueryPath))
            sys.exit(-2)
        queryDBname = "{:s}.mmseqs2db".format(current_sp)
        queryDBpath = "{:s}{:s}".format(dbDir, queryDBname)
        # create the database if does not exist yet
        if not os.path.isfile(queryDBpath):
            start_time = time.perf_counter()
            mmseqs_createdb(inQueryPath, outDir=dbDir, dbType=1, debug=False)
            if create_idx:
                mmseqs_createindex(queryDBpath, threads=3, debug=False)
            end_time = time.perf_counter()
            # add the execution time to the results queue
            results_queue.put((current_sp, str(round(end_time - start_time, 2))))



def consume_mmseqs_search_1cpu(jobs_queue, results_queue, inDir, dbDir, runDir, outDir, keepAlign, sensitivity, cutoff, pPath):
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # extract input paths
        sp1, sp2 = current_pair.split("-", 1)
        inSeq = os.path.join(inDir, sp1)
        dbSeq = os.path.join(inDir, sp2)
        # create temporary directory name
        tmpMMseqsDirName = "tmp_{:s}-{:s}".format(sp1, sp2)
        # it MUST use 1 CPU
        parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=runDir, outDir=outDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAlign, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=1, pythonPath=pPath, debug=False)
        del tot_time
        # exit if the BLAST formatted file generation was not successful
        if not os.path.isfile(parsedOutput):
            sys.stderr.write("\nERROR: the MMseqs2 raw alignments could not be converted into the BLAST format.\n")
            sys.exit(-2)
        # store the execution time in the queue
        results_queue.put((current_pair, search_time, convert_time, parse_time))



def consume_alignment_jobs(jobs_queue, results_queue, runDir: str, dbDir: str, alnDir: str, keepAln: bool, sensitivity: float, cutoff: float, pPath: str) -> None:
    """
    Perform essential or complete alignments for a pair of proteomes.
    Only one complete alignment is performed if it is intra-proteome alignment.
    """
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        # extract job information
        pairTpl: Tuple[str, str] = ("", "")
        cntA: int = 0
        cntB: int = 0
        pairTpl: Tuple[str, str] = ("", "")
        inDir: str = os.path.join(runDir, "mapped_input")
        jobType: int = -1
        threads: int = 1
        pairTpl, jobType, threads, cntA, cntB = current_input
        tmpA: str = ""
        tmpB: str = ""
        tmpA, tmpB = pairTpl
        pair: str = "{:s}-{:s}".format(tmpA, tmpB)
        invPair: str = "{:s}-{:s}".format(tmpB, tmpA)
        pairAlnDir: str = ""
        # debug should be set only internally and should not be passed as a parameter
        debug: bool = False
        # will contain the results from the alignment job
        resList: List[Tuple[str, float, float, float, float, float]] = []
        # Given the pair A-B execute the alignments based on the following values
        # 0 -> A-B
        # 1 -> B-A only (essentials)
        # 2 -> A-B and B-A (essentials)
        # 3 -> B-A only (complete)
        # 4 -> A-B and B-A (complete)
        # execute the job based on the job type
        if (jobType == 0) or (jobType == 2) or (jobType == 4): # The first complete alignment
            if debug:
                print("\nComplete (FASTEST) alignment for pair {:s}".format(pair))
            # create main directories and paths
            pairAlnDir: str = os.path.join(alnDir, pair)
            systools.makedir(pairAlnDir)
            inSeq = os.path.join(inDir, tmpA)
            dbSeq = os.path.join(inDir, tmpB)
            # define the for the temporary directory
            tmpMMseqsDirName = "tmp_{:s}".format(pair)
            # perfom the complete alignment
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=runDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=threads, pythonPath=pPath, debug=False)
            del tot_time
            # exit if the BLAST formatted file generation was not successful
            if not os.path.isfile(parsedOutput):
                sys.stderr.write("\nERROR: the MMseqs2 raw alignments for {:s} could not be converted into the BLAST format.\n".format(pair))
                sys.exit(-2)
            # add execution times to the output list
            resList.append((pair, search_time, convert_time, parse_time, 0., 0., 0.))
        # perform the essential alignments if required
        if (jobType == 3) or (jobType == 4): # Complete alignments
            if debug:
                print("Complete alignment for pair {:s}".format(invPair))
            # create main directories and paths
            pairAlnDir: str = os.path.join(alnDir, invPair)
            systools.makedir(pairAlnDir)
            inSeq = os.path.join(inDir, tmpB)
            dbSeq = os.path.join(inDir, tmpA)
            # define the for the temporary directory
            tmpMMseqsDirName = "tmp_{:s}".format(invPair)
            # perfom the complete alignment
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(inSeq, dbSeq, dbDir=dbDir, runDir=runDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=threads, pythonPath=pPath, debug=False)
            del tot_time
            # exit if the BLAST formatted file generation was not successful
            if not os.path.isfile(parsedOutput):
                sys.stderr.write("\nERROR: the MMseqs2 raw alignments for {:s} could not be converted into the BLAST format.\n".format(invPair))
                sys.exit(-2)
            # add execution times to the output list
            resList.append((invPair, search_time, convert_time, parse_time, 0., 0., 0.))
        elif (jobType == 1) or (jobType == 2): # Essential alignments
            if debug:
                print("Essential alignment for pair {:s}".format(invPair))
            reductionDict: Dict[int, List[str]] = {}
            # output directory for the single run
            pairAlnDir: str = os.path.join(alnDir, invPair)
            systools.makedir(pairAlnDir)
            tmpDir: str = os.path.join(runDir, "mapped_input")
            tmpPathAB: str = os.path.join(alnDir, "{:s}-{:s}".format(tmpA, tmpB))
            # if the reference alignment does not exist yet
            if not os.path.isfile(tmpPathAB):
                sys.stderr.write("\nERROR: the reference alignment for pair {:s} does not exist.".format(os.path.basename(tmpPathAB)))
                sys.stderr.write("\nYou must create the alignment for {:s} before aligning the pair {:s}.".format(pair, invPair))
                results_queue.put((pair, 0., 0., 0., 0., 0., 0.))
                continue
            # start timer for reduction files creation
            reductionTime: float = time.perf_counter()
            # create the subsets
            reductionDict, pctB, pctA = essentials.create_essential_stacks(tmpPathAB, alnDir, cntA, cntB, debug=False)
            del tmpPathAB
            # extract sequences for A
            fastaPath: str = os.path.join(tmpDir, tmpA)
            reducedAPath: str = os.path.join(pairAlnDir, tmpA)
            essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpA)], reducedAPath, debug=False)
            # extract sequences for B
            fastaPath = os.path.join(tmpDir, tmpB)
            reducedBPath: str = os.path.join(pairAlnDir, tmpB)
            essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpB)], reducedBPath, debug=False)
            # create mmseqs database files
            mmseqs_createdb(reducedBPath, outDir=pairAlnDir, debug=False)
            dbPathA: str = mmseqs_createdb(reducedAPath, outDir=pairAlnDir, debug=False)[-1]
            # force the indexing to use at least 2 threads per job
            if threads == 1:
                mmseqs_createindex(dbPathA, threads=2, debug=False)
            else:
                mmseqs_createindex(dbPathA, threads=threads, debug=False)
            # end time for reduction files creation creation
            reductionTime = round(time.perf_counter() - reductionTime, 3)
            # create temporary directory name
            tmpMMseqsDirName = 'tmp_{:s}'.format(invPair)
            # perform the alignments
            parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(reducedBPath, reducedAPath, dbDir=pairAlnDir, runDir=pairAlnDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=threads, pythonPath=pPath, debug=False)
            # add execution times to the output list
            resList.append((invPair, search_time, convert_time, parse_time, pctA, pctB, reductionTime))

        # add the results in the output queue
        results_queue.put(resList)



def consume_essential_alignments(jobs_queue, results_queue, runDir: str, alnDir: str, keepAln: bool, sensitivity: float, cutoff: float, pPath: str) -> None:
    """Perform single essential allignments."""
    while True:
        current_input = jobs_queue.get(True, 1)
        if current_input is None:
            break
        # extract job information
        pairTpl: Tuple[str, str] = ("", "")
        cntA: int = 0
        cntB: int = 0
        pairTpl, cntA, cntB = current_input
        tmpA: str = pairTpl[0]
        tmpB: str = pairTpl[1]
        reductionDict: Dict[int, List[str]] = {}

        # output directory for the single run
        pair: str = "{:s}-{:s}".format(tmpA, tmpB)
        pairAlnDir: str = os.path.join(alnDir, pair)
        systools.makedir(pairAlnDir)
        tmpDir: str = os.path.join(runDir, "mapped_input")
        tmpPathBA: str = os.path.join(alnDir, "{:s}-{:s}".format(tmpB, tmpA))
        # if the reference alignment does not exist yet
        if not os.path.isfile(tmpPathBA):
            sys.stderr.write("\nERROR: the reference alignment for pair {:s} does not exist.".format(os.path.basename(tmpPathBA)))
            sys.stderr.write("\nYou create the alignment for {:s} before aligning the pair {:s}.".format(os.path.basename(tmpPathBA), pair))
            results_queue.put((pair, 0., 0., 0., 0., 0., 0.))
            continue
        # start timer for reduction files creation
        reductionTime: float = time.perf_counter()
        # create the subsets
        reductionDict, pctB, pctA = essentials.create_essential_stacks(tmpPathBA, alnDir, cntB, cntA, debug=False)
        del tmpPathBA
        # extract sequences for A
        fastaPath: str = os.path.join(tmpDir, tmpA)
        reducedAPath: str = os.path.join(pairAlnDir, tmpA)
        essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpA)], reducedAPath, debug=False)
        # extract sequences for B
        fastaPath = os.path.join(tmpDir, tmpB)
        reducedBPath: str = os.path.join(pairAlnDir, tmpB)
        essentials.extract_essential_proteins(fastaPath, reductionDict[int(tmpB)], reducedBPath, debug=False)
        # create mmseqs database files
        mmseqs_createdb(reducedAPath, outDir=pairAlnDir, debug=False)
        dbPathB: str = mmseqs_createdb(reducedBPath, outDir=pairAlnDir, debug=False)[-1]
        mmseqs_createindex(dbPathB, debug=False)
        # end time for reduction files creation creation
        reductionTime = round(time.perf_counter() - reductionTime, 3)
        # create temporary directory name
        tmpMMseqsDirName = 'tmp_{:s}'.format(pair)
        # perform the alignments
        parsedOutput, search_time, convert_time, parse_time, tot_time = mmseqs_1pass(reducedAPath, reducedBPath, dbDir=pairAlnDir, runDir=pairAlnDir, outDir=alnDir, tmpDirName=tmpMMseqsDirName, keepAlign=keepAln, sensitivity=sensitivity, evalue=1000, cutoff=cutoff, threads=1, pythonPath=pPath, debug=False)
        del parsedOutput, tot_time
        # add results to the queue
        results_queue.put((pair, search_time, convert_time, parse_time, pctA, pctB, reductionTime))



def consume_orthology_inference_sharedict(jobs_queue, results_queue, inDir, outDir=os.getcwd(), sharedDir=None, sharedWithinDict=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Perform orthology inference in parallel."""
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # create the output directory if needed
        # prepare the run
        sp1, sp2 = current_pair.split('-', 1)
        runDir = os.path.join(outDir, current_pair)
        systools.makedir(runDir)
        inSp1 = os.path.join(inDir, sp1)
        inSp2 = os.path.join(inDir, sp2)
        # check that the input files do exist
        if not os.path.isfile(inSp1):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path".format(sp1))
            sys.exit(-2)
        if not os.path.isfile(inSp2):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path".format(sp2))
            sys.exit(-2)
        # prepare the names of the required alignments
        # AB
        AB = '{:s}-{:s}'.format(sp1, sp2)
        shPathAB = os.path.join(sharedDir, AB)
        if not os.path.isfile(shPathAB):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(AB))
            sys.exit(-2)
        # BA
        BA = '{:s}-{:s}'.format(sp2, sp1)
        shPathBA = os.path.join(sharedDir, BA)
        if not os.path.isfile(shPathBA):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(BA))
            sys.exit(-2)
        #sys.exit('DEBUG :: workers :: consume_orthology_inference_sharedict :: all-vs-all exstance check')

        # prepare paths for output tables
        outTable = os.path.join(runDir, 'table.{:s}'.format(current_pair))

        # infer orthologs
        # use perf_counter (includes time spent during sleep)
        orthology_prediction_start = time.perf_counter()
        inpyranoid.infer_orthologs_shared_dict(inSp1, inSp2, alignDir=sharedDir, outDir=runDir, sharedWithinDict=sharedWithinDict, confCutoff=confCutoff, lenDiffThr=lenDiffThr, debug=False)

        #check that all the files have been created
        if not os.path.isfile(outTable):
            sys.stderr.write('WARNING: the ortholog table file %s was not generated.'%outTable)
            outTable = None
        #everything went ok!
        end_time = time.perf_counter()
        orthology_prediction_tot = round(end_time - orthology_prediction_start, 2)
        # add the execution time to the results queue
        results_queue.put((current_pair, str(orthology_prediction_tot)))
        if debug:
            sys.stdout.write('\nOrthology prediction {:s} (seconds):\t{:s}\n'.format(current_pair, str(orthology_prediction_tot)))



# DEBUG-FUNCTION: this should be removed in future releases
'''
def consume_orthology_inference(jobs_queue, results_queue, inDir, outDir=os.getcwd(), sharedDir=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Perform orthology inference in parallel."""
    while True:
        current_pair = jobs_queue.get(True, 1)
        if current_pair is None:
            break
        # create the output directory iof needed
        # prepare the run
        sp1, sp2 = current_pair.split('-', 1)
        runDir = os.path.join(outDir, current_pair)
        systools.makedir(runDir)
        inSp1 = os.path.join(inDir, sp1)
        inSp2 = os.path.join(inDir, sp2)
        # check that the input files do exist
        if not os.path.isfile(inSp1):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path.\n".format(sp1))
            sys.exit(-2)
        if not os.path.isfile(inSp2):
            sys.stderr.write("ERROR: The input file for {:s} was not found, please provide a valid path.\n".format(sp2))
            sys.exit(-2)
        # prepare the names of the required alignments
        # copy AA
        AA = '{:s}-{:s}'.format(sp1, sp1)
        shPathAA = os.path.join(sharedDir, AA)
        if not os.path.isfile(shPathAA):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(AA))
            sys.exit(-2)
        # copy BB
        BB = '{:s}-{:s}'.format(sp2, sp2)
        shPathBB = os.path.join(sharedDir, BB)
        if not os.path.isfile(shPathBB):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(BB))
            sys.exit(-2)
        # copy AB
        AB = '{:s}-{:s}'.format(sp1, sp2)
        shPathAB = os.path.join(sharedDir, AB)
        if not os.path.isfile(shPathAB):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(AB))
            sys.exit(-2)
        # copy BA
        BA = '{:s}-{:s}'.format(sp2, sp1)
        shPathBA = os.path.join(sharedDir, BA)
        if not os.path.isfile(shPathBA):
            sys.stderr.write("ERROR: The alignment file for {:s} was not found, please generate the alignments first.\n".format(BA))
            sys.exit(-2)
        #sys.exit('DEBUG :: workers :: consume_orthology_inference_jobs :: after files copy')

        # prepare paths for output tables
        outTable = os.path.join(runDir, 'table.{:s}'.format(current_pair))

        # infer orthologs
        # use perf_counter (includes time spent during sleep)
        orthology_prediction_start = time.perf_counter()
        inpyranoid.infer_orthologs(inSp1, inSp2, alignDir=sharedDir, outDir=runDir, confCutoff=confCutoff, lenDiffThr=lenDiffThr, debug=False)
        #check that all the files have been created
        if not os.path.isfile(outTable):
            sys.stderr.write('WARNING: the ortholog table file %s was not generated.'%outTable)
            outTable = None
        #everything went ok!
        # use perf_counter (includes time spent during sleep)
        end_time = time.perf_counter()
        orthology_prediction_tot = round(end_time - orthology_prediction_start, 2)
        # add the execution time to the results queue
        results_queue.put((current_pair, str(orthology_prediction_tot)))
        if debug:
            sys.stdout.write('\nOrthology prediction {:s} (seconds):\t{:s}\n'.format(current_pair, str(orthology_prediction_tot)))
'''



def get_mmseqs_path():
    """Return the directory in which MMseqs2 binaries are stored."""
    #import platform
    mmseqsPath = None
    pySrcDir = os.path.dirname(os.path.abspath(__file__))
    mmseqsPath = os.path.join(pySrcDir, 'bin/mmseqs')
    if not os.path.isfile(mmseqsPath):
        sys.stderr.write('\nERROR: mmseqs2 was not found, please install it and execute setup_sonicparanoid.py.')
        sys.exit(-5)
    # return the path
    return mmseqsPath



def mmseqs_1pass(inSeq, dbSeq, dbDir=os.getcwd(), runDir=os.getcwd(), outDir=os.getcwd(), tmpDirName=None, keepAlign=False, sensitivity=4.0, evalue=1000, cutoff=40, threads=4, pythonPath=sys.executable, debug=False):
    """Execute the 1-pass alignment mmseqs2 similar to the one implemented in core-inparanoid."""
    if debug:
        print("\nmmseqs_1pass :: START")
        print("Input query FASTA file:\t{:s}".format(inSeq))
        print("Input target FASTA file:\t{:s}".format(dbSeq))
        print("mmseqs2 database directory:\t{:s}".format(dbDir))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Output directory:\t{:s}".format(outDir))
        print("MMseqs2 tmp directory:\t{:s}".format(tmpDirName))
        print("Do not remove alignment files:\t{:s}".format(str(keepAlign)))
        print("MMseqs2 sensitivity (-s):\t{:s}".format(str(sensitivity)))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Threads:\t{:d}".format(threads))
        print("Python3 binaries for parsing:\t{:s}".format(pythonPath))

    # create the directory in which the alignment will be performed
    pair: str = "{:s}-{:s}".format(os.path.basename(inSeq), os.path.basename(dbSeq))
    pairAlnDir: str = os.path.join(outDir, pair)
    systools.makedir(pairAlnDir)

    #start the timing which will also include the time for the index, database creation (if required) and parsing
    # create mmseqs alignment conveted into blastp tab-separated format
    blastLikeOutput, search_time, convert_time = mmseqs_search(inSeq, dbSeq, dbDir=dbDir, outDir=pairAlnDir, tmpDirName=tmpDirName, sensitivity=sensitivity, evalue=1000, threads=threads, cleanUp=False, debug=debug)
    parserPath = os.path.join(outDir, "mmseqs_parser_cython.py")
    prevDir = os.getcwd()
    os.chdir(outDir)
    # check cutoff
    if cutoff < 30:
        cutoff = 40

    # start timing the parsing
    # use perf_counter (includes time spent during sleep)
    start_time = time.perf_counter()
    # prepare now the parsing
    # EXAMPLE: python3 mmseqs_parser_cython.py --input mmseqs2blast.A-B --query A --db B --output A-B --cutoff 40
    parsedOutput: str = blastLikeOutput.rsplit(".", 1)[-1]
    parsedOutput = os.path.join(pairAlnDir, parsedOutput)

    # READ LENGTHS OR HDRS FROM FILE
    parseCmd = "{:s} {:s} --input {:s} --query {:s} --db {:s} --output {:s} --cutoff {:d} --run-dir {:s}".format(pythonPath, parserPath, blastLikeOutput, inSeq, dbSeq, parsedOutput, cutoff, runDir)
    if debug:
        print('Parse CMD:\n{:s}'.format(parseCmd))

    #execute the system call for parsing
    subprocess.run(parseCmd, shell=True)
    # use perf_time (includes time spent during sleep)
    parse_time = round(time.perf_counter() - start_time, 2)
    tot_time = round(search_time + convert_time + parse_time, 2)
    if debug:
        sys.stdout.write('\nMMseqs2 alignment and parsing elapsed time (seconds):\t%s\n'%str(tot_time))
    # Temporary final name
    tmpFinalPath: str = os.path.join(outDir, "_{:s}".format(pair))
    systools.copy(parsedOutput, tmpFinalPath)
    # remove the aligment directory if required
    if keepAlign:
        for r, d, files in os.walk(pairAlnDir):
            for name in files:
                tPath = os.path.join(r, name)
                if os.path.isfile(tPath) and name[0] == "m":
                    systools.move(tPath, outDir)
            break
    # remove directory content
    shutil.rmtree(pairAlnDir)
    parsedOutput = os.path.join(outDir, pair)
    os.rename(tmpFinalPath, parsedOutput)
    # reset original working directory
    os.chdir(prevDir)
    return (parsedOutput, search_time, convert_time, parse_time, tot_time)



def mmseqs_createdb(inSeq, outDir=os.getcwd(), dbType:int = 1, debug=False):
    """Create a database file for mmseqs2 from the input sequence file."""
    if debug:
        print("mmseqs_createdb :: START")
        print("Input FASTA file:\t%s"%inSeq)
        print("Database type:\t%d"%dbType)
        print("Outdir:\t%s"%outDir)
    #check that the input file and the database exist
    if not os.path.isfile(inSeq):
        sys.stderr.write("The file %s was not found, please provide the path to a valid FASTA file."%inSeq)
        sys.exit(-2)
    #check if the database exists
    if outDir[-1] != "/":
        outDir += "/"
    # create dir if not already exists
    systools.makedir(outDir)
    # check the set db name
    dbName = os.path.basename(inSeq)
    dbName = dbName.split(".")[0] # take the left part of the file name
    dbName = "%s.mmseqs2db"%dbName
    dbPath = "%s%s"%(outDir, dbName)
    # command to be executed
    # EXAMPLE; mmseqs createdb in.fasta /outdir/mydb
    makeDbCmd = f"{get_mmseqs_path()} createdb {inSeq} {dbPath} -v 0"
    if debug:
        print("mmseqs2 createdb CMD:\t%s"%makeDbCmd)
    #execute the system call
    process = subprocess.Popen(makeDbCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()
    if debug:
        print("STDOUT:\n%s\n"%stdout_val)
        print("STDERR:\n%s\n"%stderr_val)
    #return a tuple with the results
    return(stdout_val, stderr_val, makeDbCmd, dbPath)



def mmseqs_createindex(dbPath, threads: int=6, debug=False):
    """Create a index from a mmseq2 database file."""
    if debug:
        print("mmseqs_createindex :: START")
        print("Input mmseqs2 db file:\t%s"%dbPath)
        print("Threads:\t{:d}".format(threads))
    #check that the database file exist
    if not os.path.isfile(dbPath):
        sys.stderr.write("The file %s was not found, please provide the path to a mmseqs2 database file"%dbPath)
        sys.exit(-2)
    # Prepare file names and commands
    tmpBname = os.path.basename(dbPath)
    tmpDir = "{:s}/tmp_{:s}/".format(os.path.dirname(dbPath), os.path.basename(tmpBname.split(".", 1)[0]))
    systools.makedir(tmpDir)
    # command to be executed
    # EXAMPLE; mmseqs createindex in.mmseqs2_db
    makeIdxCmd = "{:s} createindex {:s} {:s} --threads {:d} -v 0".format(get_mmseqs_path(), dbPath, tmpDir, threads)
    if debug:
        print("mmseqs2 createindex CMD:\t%s"%makeIdxCmd)
    #execute the system call
    process = subprocess.Popen(makeIdxCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_val, stderr_val = process.communicate() #get stdout and stderr
    process.wait()
    if debug:
        print("STDOUT:\n%s\n"%stdout_val)
        print("STDERR:\n%s\n"%stderr_val)
    # make sure that the 3 idx files have been properly created
    idx1: str = "%s.idx"%dbPath
    if not os.path.isfile(idx1):
        sys.stderr.write("The MMseqs2 index file %s could not be created."%idx1)
        sys.exit(-2)
    idx2: str = "%s.idx.index"%dbPath
    if not os.path.isfile(idx2):
        sys.stderr.write("\nWARNING: The MMseqs2 index file %s could not be created."%idx2)
        sys.exit(-2)
    # remove the temporary directory
    shutil.rmtree(path=tmpDir)
    # return a output tuple
    return(stdout_val, stderr_val, makeIdxCmd, idx1, idx2)



def mmseqs_search(inSeq, dbSeq, dbDir=os.getcwd(), outDir=os.getcwd(), tmpDirName=None, sensitivity=4.0, evalue=1000, threads=4, cleanUp=False, debug=False):
    """Align protein sequences using mmseqs2."""
    if debug:
        print("\nmmseqs_search :: START")
        print("Input query FASTA file:\t%s"%inSeq)
        print("Input target FASTA file:\t%s"%dbSeq)
        print("mmseqs2 database directory:\t%s"%dbDir)
        print("Output directory:\t%s"%outDir)
        print("MMseqs2 tmp directory:\t{:s}".format(tmpDirName))
        print("MMseqs2 sensitivity (-s):\t%s"%str(sensitivity))
        print("Threads:\t%d"%threads)
        print("Remove temporary files:\t%s"%cleanUp)
    #check that the input file and the database exist
    if not os.path.isfile(inSeq):
        sys.stderr.write("The query file %s was not found, please provide the path to a valid FASTA file"%inSeq)
        sys.exit(-2)
    if not os.path.isfile(dbSeq):
        sys.stderr.write("The target file %s was not found, please provide the path to a valid FASTA file"%dbSeq)
        sys.exit(-2)
    # check sensitivity
    if (sensitivity < 1) or sensitivity > 7.5:
        sys.stderr.write("\nERROR: the sensitivity value for MMseqs2 must be a value between 1.0 and 7.5.\n")
        sys.exit(-5)
    # create directory if not previously created
    systools.makedir(outDir)
    systools.makedir(dbDir)
    # set the tmp dir
    tmpDir = None
    if tmpDirName is None:
        tmpDir = os.path.join(outDir, "tmp_mmseqs")
    else:
        tmpDir = os.path.join(outDir, tmpDirName)
    systools.makedir(tmpDir)
    # check the query db name
    queryDBname = os.path.basename(inSeq)
    queryDBname = queryDBname.split(".")[0] # take the left part of the file name
    queryDBname = "%s.mmseqs2db"%queryDBname
    queryDBpath = os.path.join(dbDir, queryDBname)
    # create the database if does not exist yet
    if not os.path.isfile(queryDBpath):
        mmseqs_createdb(inSeq, outDir=dbDir, debug=debug)
        mmseqs_createindex(queryDBpath, threads=threads, debug=debug)
    # check the target db name
    targetDBname = os.path.basename(dbSeq)
    targetDBname = targetDBname.split(".")[0] # take the left part of the file name
    targetDBname = "%s.mmseqs2db"%targetDBname
    targetDBpath = os.path.join(dbDir, targetDBname)
    # create the database if does not exist yet
    if not os.path.isfile(targetDBpath):
        mmseqs_createdb(dbSeq, outDir=dbDir, debug=debug)
        mmseqs_createindex(targetDBpath, threads=threads, debug=debug)
    # set output name
    pairName = "%s-%s"%(os.path.basename(inSeq), os.path.basename(dbSeq))
    rawOutName = "mmseqs2raw.%s"%pairName
    rawOutPath = os.path.join(outDir, rawOutName)
    blastOutName = "mmseqs2blast.%s"%pairName
    blastOutPath = os.path.join(outDir, blastOutName)
    # start measuring the execution time
    # use perf_counter (includes time spent during sleep)
    start_time = time.perf_counter()
    # command to be executed
    minUngappedScore = 15
    # EXAMPLE: mmseqs search queryDBfile targetDBfile outputFile tmpDir -s 7.5 -e 100000 --theads threads
    searchCmd: str = f"{get_mmseqs_path()} search {queryDBpath} {targetDBpath} {rawOutPath} {tmpDir} -s {str(sensitivity)} --threads {threads:d} -v 0 --seed-sub-mat nucl:nucleotide.out,aa:blosum62.out --min-ungapped-score {minUngappedScore} --alignment-mode 2 --alt-ali 10"
    # This prevents MMseqs2 to crush when running at high sensitivity
    if sensitivity > 6:
        searchCmd = "{:s} --db-load-mode 3".format(searchCmd)
    if debug:
        print("mmseqs2 search CMD:\t%s"%searchCmd)
    # use run (or call)
    subprocess.run(searchCmd, shell=True)

    # output an error if the Alignment did not finish correctly
    if threads > 1: # multiple raw files are generated
        if not os.path.isfile("{:s}.0".format(rawOutPath)):
            sys.stderr.write("\nERROR [mmseqs_search()]: the MMseqs2 raw alignment file\n{:s}\nwas not generated.\n".format(rawOutPath))
            sys.exit(-2)
    else: # a single raw file is created
        if not os.path.isfile(rawOutPath):
            sys.stderr.write("\nERROR [mmseqs_search()]: the MMseqs2 raw alignment file\n{:s}\nwas not generated.\n".format(rawOutPath))
            sys.exit(-2)

    # stop counter
    # use perf_counter (includes time spent during sleep)
    end_search = time.perf_counter()
    search_time = round(end_search - start_time, 2)
    # convert the output to tab-separated BLAST output
    # EXAMPLE: mmseqs convertalis query.db target.db query_target_rawout query_target_blastout
    # Only output specific files in the BLAST-formatted output
    # query,target,qstart,qend,tstart,tend,bits
    columns: str = "query,target,qstart,qend,tstart,tend,bits"
    convertCmd = f"{get_mmseqs_path()} convertalis {queryDBpath} {targetDBpath} {rawOutPath} {blastOutPath} -v 0 --format-mode 0 --search-type 1 --format-output {columns}"


    # perform the file conversion
    subprocess.run(convertCmd, shell=True)
    if debug:
        print("mmseqs2 convertalis CMD:\t%s"%convertCmd)
    # exec time conversion
    # use perf_counter (includes time spent during sleep)
    convert_time = round(time.perf_counter() - end_search, 2)
    # output an error if the Alignment could not be converted
    if not os.path.isfile(blastOutPath):
        sys.stderr.write("\nERROR: the MMseqs2 raw alignments could not be converted into the BLAST format.\n{:s}\n".format(blastOutPath))
        sys.exit(-2)
    return (blastOutPath, search_time, convert_time)



def perform_parallel_dbs_creation(spList, inDir, dbDir, create_idx=True, threads=4, debug=False):
    """Create MMseqs2 databases in parallel"""
    # create the queue and start adding
    make_dbs_queue = mp.Queue(maxsize=len(spList) + threads)

    # fill the queue with the processes
    for sp in spList:
        sys.stdout.flush()
        make_dbs_queue.put(os.path.basename(sp))

    # add flags for completed jobs
    for i in range(0, threads):
        sys.stdout.flush()
        make_dbs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(spList))

    # call the method inside workers
    runningJobs = [mp.Process(target=create_dbs_parallel, args=(make_dbs_queue, results_queue, inDir, dbDir, create_idx)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    while True:
        try:
            sp, tot_time = results_queue.get(False, 0.01)
            #ofd.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(p, str(s_time), str(c_time), str(p_time)))
            if debug:
                sys.stdout.write('{:s} database created:\t{:s}\n'.format(sp, tot_time))
        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_mmseqs_multiproc_alignments(requiredAln, inDir, outDir, dbDir, runDir, create_idx=True, sensitivity=4., cutoff=40, threads=4, keepAlign=False, firstCicle: bool=True, debug=False):
    system_cpus = mp.cpu_count()
    # check threads count
    if threads > system_cpus:
        threads = system_cpus

    if debug:
        print("\nperform_mmseqs_multiproc_alignments :: START")
        print("Pairs to be aligned:\t{:d}".format(len(requiredAln)))
        print("Directory with input proteomes: {:s}".format(inDir))
        print("Output directory with alignment files: {:s}".format(outDir))
        print("Directory alignments MMseqs DB files: {:s}".format(dbDir))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Create MMseqs index files:\t{:s}".format(str(create_idx)))
        print("Sensitivity:\t{:.2f}".format(sensitivity))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Threads:\t{:d}".format(threads))
        print("Keep alignment files:\t{:s}".format(str(keepAlign)))
        print("First cicle of alignments:\t{:s}".format(str(firstCicle)))

    # create dictionary with species involved in alignments
    reqSpDict = {}
    for pair in requiredAln:
        sp1, sp2 = pair.split('-', 1)
        if not sp1 in reqSpDict:
            reqSpDict[sp1] = None
        if not sp2 in reqSpDict:
            reqSpDict[sp2] = None

    # Make sure there is enough storage to crate the index files
    # overwrites the create_idx variable
    if create_idx:
        create_idx = check_storage_for_mmseqs_dbs(outDir, reqSp=len(reqSpDict), gbPerSpecies=1, debug=debug)

    # create databases
    sys.stdout.write('\nCreating {:d} MMseqs2 databases...\n'.format(len(reqSpDict)))
    # timer for databases creation
    start_time: float = time.perf_counter()

    # create databases in parallel
    perform_parallel_dbs_creation(list(reqSpDict.keys()), inDir, dbDir, create_idx=create_idx, threads=threads, debug=debug)
    # end time for databases creation
    end_time: float = time.perf_counter()
    sys.stdout.write('\nMMseqs2 databases creation elapsed time (seconds):\t{:s}\n'.format(str(round(end_time - start_time, 3))))
    # delete timers
    del start_time, end_time
    # calculate cpu-time for alignments
    align_start: float = time.perf_counter()
    # find the mmseqs2 parser in the source directory
    pySrcDir = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, outDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(outDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            systools.copy(os.path.join(pySrcDir, el), outDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir

    # create the queue and start adding
    align_queue = mp.Queue(maxsize=len(requiredAln) + threads)

    # fill the queue with the processes
    for pair in requiredAln:
        sys.stdout.flush()
        align_queue.put(pair)
    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        align_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredAln))

    # get the path to python3 executable
    pythonPath = sys.executable
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_mmseqs_search_1cpu, args=(align_queue, results_queue, inDir, dbDir, runDir, outDir, keepAlign, sensitivity, cutoff, pythonPath)) for i_ in range(threads)]

    # run the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    alnCicle: int = 1
    if not firstCicle:
        alnCicle = 2
    execTimeOutPath: str = os.path.join(outDir, "aln_ex_times_ca{:d}_{:s}.tsv".format(alnCicle, os.path.basename(runDir.rstrip("/"))))
    ofd = open(execTimeOutPath, 'w', buffering=1)
    del alnCicle, firstCicle

    # write some message...
    sys.stdout.write('\nPerforming the required {:d} MMseqs2 alignments...'.format(len(requiredAln)))
    # write output when available
    while True:
        try:
            p, s_time, c_time, p_time = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t100\t100\t0\n'.format(p, s_time, c_time, p_time))
            #ofd.write('{:s}\t{:s}\t{:s}\t{:s}\n'.format(p, str(s_time), str(c_time), str(p_time)))

        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()

    # stop the counter for the alignment time
    sys.stdout.write('\nAll-vs-all alignments elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - align_start, 3))))
    #sys.exit("DEBUG :: workers :: perform_mmseqs_multiproc_alignments")
'''



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_parallel_essential_alignments(requiredAln: Dict[str, float], protCntDict: Dict[str, int], runDir: str, alnDir: str, create_idx: bool=False, sensitivity: float=4.0, cutoff: int=40, threads: int=4, keepAln: bool=False, debug: bool=False) -> None:
    """Create FASTA subsets in parallel."""
    if debug:
        print("\nperform_parallel_essential_alignments :: START")
        print("Alignments to be performed:\t{:d}".format(len(requiredAln)))
        print("Proteomes:\t{:d}".format(len(protCntDict)))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Directory with alignments: {:s}".format(alnDir))
        print("Create MMseqs index files:\t{:s}".format(str(create_idx)))
        print("MMseqs sensitivity:\t{:.2f}".format(sensitivity))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Threads:\t{:d}".format(threads))
        print("Keep alignment files:\t{:s}".format(str(keepAln)))

    # find the mmseqs2 parser in the source directory
    pySrcDir: str = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, alnDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(alnDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            systools.copy(os.path.join(pySrcDir, el), alnDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir

    # create the queue and start adding
    essential_queue = mp.Queue(maxsize=len(requiredAln) + threads)
    # directory with the original alignments
    originalAlnDir = os.path.join(os.path.dirname(os.path.dirname(runDir)), "alignments")
    if not os.path.isdir(originalAlnDir):
        sys.stderr.write("\nERROR: The directory with alignments was not found.")
        sys.exit(-2)

    # fill the queue with the file paths
    tmpA: str = ""
    tmpB: str = ""
    for pair, weight in requiredAln.items():
        tmpA, tmpB = pair.split("-", 1)
        # proteome pair as tuple: e.g. "1-2" as ("1", "2")
        # and sequence counts for each proteomes
        essential_queue.put(((tmpA, tmpB), protCntDict[tmpA], protCntDict[tmpB]))

    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        essential_queue.put(None)

    # Queue to contain the execution times
    results_queue = mp.Queue(maxsize=len(requiredAln))

    # get the path to python3 executable
    pythonPath = sys.executable
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_essential_alignments, args=(essential_queue, results_queue, runDir, alnDir, keepAln, sensitivity, cutoff, pythonPath)) for i_ in range(threads)]

    # execute the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    execTimeOutPath: str = os.path.join(alnDir, "aln_ex_times_ra_{:s}.tsv".format(os.path.basename(runDir.rstrip("/"))))
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # calculate cpu-time for alignments
    align_start = time.perf_counter()

    # write some message...
    sys.stdout.write('\nPerforming {:d} essential MMseqs2 alignments...'.format(len(requiredAln)))

    # write output when available
    while True:
        try:
            p, s_time, c_time, p_time, seq_pct_a, seq_pct_b, reduction_time = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.2f}\t{:.2f}\t{:.3f}\n'.format(p, s_time, c_time, p_time, seq_pct_a, seq_pct_b, reduction_time))

        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()
    # stop the counter for the alignment time
    sys.stdout.write('\nAll-vs-all alignments elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - align_start, 3))))
'''



def perform_parallel_essential_alignments_plus(requiredAln: Dict[str, Tuple[float, int, int]], protCntDict: Dict[str, int], runDir: str, dbDir: str, alnDir: str, create_idx: bool=True, sensitivity: float=4.0, cutoff: int=40, essentialMode: bool=True, threads: int=4, keepAln: bool=False, debug: bool=False) -> None:
    """Create FASTA subsets in parallel."""
    if debug:
        print("\nperform_parallel_essential_alignments_plus :: START")
        print("Alignments jobs to be performed:\t{:d}".format(len(requiredAln)))
        print("Proteomes:\t{:d}".format(len(protCntDict)))
        print("Directory with run supplementary files: {:s}".format(runDir))
        print("Directory with shared MMseqs2 databases: {:s}".format(dbDir))
        print("Directory with alignments: {:s}".format(alnDir))
        print("Create MMseqs index files:\t{:s}".format(str(create_idx)))
        print("MMseqs sensitivity:\t{:.2f}".format(sensitivity))
        print("Bitscore cutoff:\t{:d}".format(cutoff))
        print("Essential mode:\t{:s}".format(str(essentialMode)))
        print("Threads:\t{:d}".format(threads))
        print("Keep alignment files:\t{:s}".format(str(keepAln)))

    # identify the species for which the DB should be created
    # Consider only the job in COMPLETE mode
    # Given the pair A-B execute the job type has following values:
    # 0 -> A-B
    # 1 -> B-A only (essentials)
    # 2 -> A-B and B-A (essentials)
    # 3 -> B-A only (complete)
    # 4 -> A-B and B-A (complete)
    reqSpDict: Dict[str, Any] = {}
    for pair, tpl in requiredAln.items():
        jobType = tpl[1]
        if (jobType == 0) or (jobType == 2) or (jobType == 3) or (jobType == 4):
            sp1, sp2 = pair.split('-', 1)
            if not sp1 in reqSpDict:
                reqSpDict[sp1] = None
            if not sp2 in reqSpDict:
                reqSpDict[sp2] = None
            # exit if all the possible species have been inserted
            if len(reqSpDict) == len(protCntDict):
                break

    if len(reqSpDict) > 0:
        fastaDir: str = os.path.join(runDir, "mapped_input")
        # create the directory which will contain the databases
        systools.makedir(dbDir)
        # Make sure there is enough storage to crate the index files
        # overwrites the create_idx variable
        if create_idx:
            create_idx = check_storage_for_mmseqs_dbs(dbDir, reqSp=len(reqSpDict), gbPerSpecies=0.95, debug=debug)

        # create databases
        sys.stdout.write('\nCreating {:d} MMseqs2 databases...\n'.format(len(reqSpDict)))
        # timer for databases creation
        start_time: float = time.perf_counter()

        # create databases in parallel
        perform_parallel_dbs_creation(list(reqSpDict.keys()), fastaDir, dbDir, create_idx=create_idx, threads=threads, debug=debug)
        # end time for databases creation
        end_time: float = time.perf_counter()
        sys.stdout.write('\nMMseqs2 databases creation elapsed time (seconds):\t{:s}\n'.format(str(round(end_time - start_time, 3))))
        # delete timers
        del start_time, end_time

    # find the mmseqs2 parser in the source directory
    pySrcDir: str = os.path.dirname(os.path.abspath(__file__))
    mmseqsparser: str = os.path.join(pySrcDir, 'mmseqs_parser_cython.py')
    # copy the file to the output directory
    systools.copy(mmseqsparser, alnDir, metaData=False, debug=False)
    mmseqsparser = os.path.join(alnDir, 'mmseqs_parser_cython.py')
    os.chmod(mmseqsparser, 0o751)
    # find and copy the parser module
    parserModuleFound: bool = False
    if debug:
        print("Searching parser file...")
    for el in os.listdir(pySrcDir):
        if el.startswith('mmseqs_parser_c.'):
            if el.endswith('.pyx') or el.endswith('.c'):
                continue
            if debug:
                print("Found parser module:", el)
            systools.copy(os.path.join(pySrcDir, el), alnDir, metaData=False, debug=False)
            parserModuleFound = True
            break
    del parserModuleFound, pySrcDir

    # create the queue and start adding
    essential_queue = mp.Queue(maxsize=len(requiredAln) + threads)
    # directory with the original alignments
    originalAlnDir = os.path.join(os.path.dirname(os.path.dirname(runDir)), "alignments")
    if not os.path.isdir(originalAlnDir):
        sys.stderr.write("\nERROR: The directory with alignments was not found.")
        sys.exit(-2)
    # fill the queue with the file paths
    tmpA: str = ""
    tmpB: str = ""
    for pair, tpl in requiredAln.items():
        # tpl contains the following information
        # tpl[0]: float => job weight
        # tpl[1]: int => type of job (e.g, 0-> 1-2 only, 1-> 1-2 and 2-1, etc.)
        # tpl[2]: int => number of threads to be used for the alignment
        tmpA, tmpB = pair.split("-", 1)
        # proteome pair as tuple: e.g. "1-2" as ("1", "2")
        # and sequence counts for each proteomes
        essential_queue.put(((tmpA, tmpB), tpl[1], tpl[2], protCntDict[tmpA], protCntDict[tmpB]))

    # add flags for ended jobs
    for i in range(0, threads):
        sys.stdout.flush()
        essential_queue.put(None)

    # Queue to contain the execution times
    results_queue = mp.Queue(maxsize=len(requiredAln))
    # get the path to python3 executable
    pythonPath = sys.executable
    # perform the alignments
    runningJobs = [mp.Process(target=consume_alignment_jobs, args=(essential_queue, results_queue, runDir, dbDir, alnDir, keepAln, sensitivity, cutoff, pythonPath)) for i_ in range(threads)]

    # execute the jobs
    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    # use the parent directory name of the database directory as suffix
    alnExTimeFileName: str = "aln_ex_times_ra_{:s}.tsv".format(os.path.basename(runDir.rstrip("/")))
    if not essentialMode:
        alnExTimeFileName = "aln_ex_times_ca_{:s}.tsv".format(os.path.basename(runDir.rstrip("/")))
    execTimeOutPath: str = os.path.join(alnDir,alnExTimeFileName )
    del alnExTimeFileName
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # calculate cpu-time for alignments
    align_start = time.perf_counter()
    # write some message...
    if debug:
        sys.stdout.write('\nPerforming {:d} alignment jobs...'.format(len(requiredAln)))
    # will contain the results from an alignment job
    resList: List[Tuple[str, float, float, float, float, float]] = []

    # write output when available
    while True:
        try:
            resList = results_queue.get(False, 0.01)
            for resTpl in resList:
                ofd.write('{:s}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.2f}\t{:.2f}\t{:.3f}\n'.format(*resTpl))
        #except queue.Empty:
        except:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    # this joins the processes after we got the results
    for proc in runningJobs:
        while proc.is_alive():
            proc.join()

    # stop the counter for the alignment time
    sys.stdout.write('\nAll-vs-all alignments elapsed time (seconds):\t{:s}\n'.format(str(round(time.perf_counter() - align_start, 3))))



# DEBUG-FUNCTION: this should be removed in future releases
'''
def perform_parallel_orthology_inference(requiredPairsDict, inDir, outDir=os.getcwd(), sharedDir=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Execute orthology inference for the required pairs."""
    if debug:
        print('\nperform_parallel_orthology_inference :: START')
        print('Proteome pairs to be processed:\t{:d}'.format(len(requiredPairsDict)))
        print('Input directory:{:s}'.format(inDir))
        print('Outdir:{:s}'.format(outDir))
        print('Alignment directory:{:s}'.format(sharedDir))
        print('Cutoff:\t{:d}'.format(cutoff))
        print('Confidence cutoff for paralogs:\t{:s}'.format(str(confCutoff)))
        print('Length difference filtering threshold:\t{:s}'.format(str(lenDiffThr)))
        print('CPUs (for mmseqs):\t{:d}'.format(threads))
    # make sure that the directory with alignments exists
    if not os.path.isdir(sharedDir):
        sys.stderr.write("ERROR: The directory with the alignment files\n{:s}\nwas not found, please provide a valid path.\n".format(sharedDir))
        sys.exit(-2)
    if not os.path.isdir(inDir):
        sys.stderr.write("ERROR: The directory with the input files\n{:s}\nwas not found, please provide a valid path.\n".format(inDir))
        sys.exit(-2)
    #create the output directory if does not exist yet
    if outDir != os.getcwd():
        if not os.path.isdir(outDir):
            systools.makedir(outDir)
    if outDir[-1] != '/':
        outDir += '/'
    # check if the output directory differs from the input one
    if os.path.dirname(inDir) == os.path.dirname(outDir):
        sys.stderr.write("\nERROR: the output directory {:s}\nmust be different from the one in which the input files are stored\n{:s}\n".format(outDir, inDir))
        sys.exit(-3)
    # check cutoff
    if cutoff < 30:
        cutoff = 40
    # create the queue and start adding the jobs
    jobs_queue = mp.Queue()

    # fill the queue with the processes
    for pair in requiredPairsDict:
        jobs_queue.put(pair)
    # add flags for eneded jobs
    for i in range(0, threads):
        jobs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredPairsDict))
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_orthology_inference_jobs, args=(jobs_queue, results_queue, inDir, outDir, sharedDir, cutoff, confCutoff, lenDiffThr, threads, debug)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    execTimeOutPath = os.path.join(sharedDir, 'orthology_ex_time_{:s}.tsv'.format(os.path.basename(outDir.rstrip('/'))))
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # get the results from the queue without filling the Pipe buffer
    while True:
        try:
            p, val = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:s}\n'.format(p, str(val)))
        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    for proc in runningJobs:
        while proc.is_alive():
            proc.join()
'''



def perform_parallel_orthology_inference_shared_dict(requiredPairsDict, inDir, outDir=os.getcwd(), sharedDir=None, sharedWithinDict=None, cutoff=40, confCutoff=0.05, lenDiffThr=0.5, threads=8, debug=False):
    """Execute orthology inference for the required pairs."""
    if debug:
        print('\nperform_parallel_orthology_inference_shared_dict :: START')
        print('Proteome pairs to be processed:\t{:d}'.format(len(requiredPairsDict)))
        print('Input directory:{:s}'.format(inDir))
        print('Outdir:{:s}'.format(outDir))
        print('Alignment directory:{:s}'.format(sharedDir))
        print('Shared within-align dictionaries :{:d}'.format(len(sharedWithinDict)))
        print('Cutoff:\t{:d}'.format(cutoff))
        print('Confidence cutoff for paralogs:\t{:s}'.format(str(confCutoff)))
        print('Length difference filtering threshold:\t{:s}'.format(str(lenDiffThr)))
        print('CPUs (for mmseqs):\t{:d}'.format(threads))
    # make sure that the directory with alignments exists
    if not os.path.isdir(sharedDir):
        sys.stderr.write("ERROR: The directory with the alignment files\n{:s}\nwas not found, please provide a valid path\n".format(sharedDir))
        sys.exit(-2)
    if not os.path.isdir(inDir):
        sys.stderr.write("ERROR: The directory with the input files\n{:s}\nwas not found, please provide a valid path\n".format(inDir))
        sys.exit(-2)
    #create the output directory if does not exist yet
    if outDir != os.getcwd():
        if not os.path.isdir(outDir):
            systools.makedir(outDir)
    # check if the output directory differs from the input one
    if os.path.dirname(inDir) == os.path.dirname(outDir):
        sys.stderr.write("\nERROR: the output directory {:s}\nmust be different from the one in which the input files are stored\n{:s}\n".format(outDir, inDir))
        sys.exit(-2)
    # check cutoff
    if cutoff < 30:
        cutoff = 40
    # create the queue and start adding the jobs
    jobs_queue = mp.Queue()

    # fill the queue with the processes
    for pair in requiredPairsDict:
        jobs_queue.put(pair)
    # add flags for eneded jobs
    for i in range(0, threads):
        jobs_queue.put(None)

    # Queue to contain the execution time
    results_queue = mp.Queue(maxsize=len(requiredPairsDict))
    # call the method inside workers
    runningJobs = [mp.Process(target=consume_orthology_inference_sharedict, args=(jobs_queue, results_queue, inDir, outDir, sharedDir, sharedWithinDict, cutoff, confCutoff, lenDiffThr, threads, debug)) for i_ in range(threads)]

    for proc in runningJobs:
        proc.start()

    # open the file in which the time information will be stored
    execTimeOutPath = os.path.join(sharedDir, 'orthology_ex_time_{:s}.tsv'.format(os.path.basename(outDir.rstrip('/'))))
    ofd = open(execTimeOutPath, 'w', buffering=1)

    # update the shared dictionary
    # and remove the shared dictionary if required
    # get the results from the queue without filling the Pipe buffer
    gcCallSentinel: int = 2 * threads
    whileCnt: int = 0
    wtCnt: int = 0
    gcCallCnt: int = 0
    while True:
        try:
            p, val = results_queue.get(False, 0.01)
            ofd.write('{:s}\t{:s}\n'.format(p, str(val)))
            whileCnt += 1
            wtCnt += 1
            #'''
            sp1, sp2 = p.split('-', 1)
            # decrease the counters in the shared dictionaries
            sharedWithinDict[sp1][0] -= 1
            if sharedWithinDict[sp1][0] == 0:
                del sharedWithinDict[sp1]
                # call the garbage collector to free memory explicitly
                gc.collect()
                if debug:
                    print('Removed dictionary for {:s}'.format(sp1))
                    print('Remaining shared dictionaries:\t{:d}'.format(len(sharedWithinDict)))
            sharedWithinDict[sp2][0] -= 1
            if sharedWithinDict[sp2][0] == 0:
                del sharedWithinDict[sp2]
                gc.collect()
                if debug:
                    print('Removed dictionary for {:s}'.format(sp2))
                    print('Remaining shared dictionaries:\t{:d}'.format(len(sharedWithinDict)))
            # call the garbage collector if a given number ortholog tables
            # has been generated
            if whileCnt == gcCallSentinel:
                gc.collect()
                whileCnt = 0
                gcCallCnt += 1
                if debug:
                    print("\ngc.collect() call:\t{:d}\nCompleted tables:\t{:d}".format(gcCallCnt, wtCnt))

        except queue.Empty:
            pass
        allExited = True
        for t in runningJobs:
            if t.exitcode is None:
                allExited = False
                break
        if allExited & results_queue.empty():
            break
    ofd.close()

    for proc in runningJobs:
        while proc.is_alive():
            proc.join()