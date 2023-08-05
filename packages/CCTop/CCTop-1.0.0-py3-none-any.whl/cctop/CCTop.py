
import sys
import re
from argparse import ArgumentTypeError, ArgumentParser, RawTextHelpFormatter, FileType
import textwrap
from subprocess import Popen, PIPE, DEVNULL
import os

from cctop.sequenceMethods import iupac_code
from cctop.bedInterval import BedInterval
from cctop.sequenceMethods import build_expression, reverse_complement, iupac_code
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.pam import factory
from cctop.offTarget import Offtarget

'''
Run the bowtie command to find hits in the genome
It expects a list of options parameters,
the path to the bowtie binary,
the path to the index incluiding the index name,
a list with the input parameters
and another list with the output parameters
or None if the function should return the output from bowtie
'''
def runBowtie(options, bowtiePath, indexPath, inputParams, outputParams):

    bowtieOutput = []# list of lines
    
    cmd = [bowtiePath + 'bowtie'] + options + [indexPath] + inputParams
    if outputParams is None:# the output from bowtie must be returned as a PIPE
        p = Popen(cmd, stdout=PIPE, stderr=DEVNULL, universal_newlines=True)
        if p.wait() == 0:
            bowtieOutput = bowtieOutput + p.stdout.readlines()
    else:
        cmd = cmd + outputParams
        p = Popen(cmd, stderr=DEVNULL)
    if p.wait() != 0:
        sys.stderr.write("Error running Bowtie (" + str(p.wait()) + ")")
        sys.stderr.write(";".join(cmd))
        raise RuntimeError
    if outputParams is None:
        return bowtieOutput

def getSeqCoords(seq, bowtiePath, indexPath):
    if len(seq) < 500:
        # returns 0-index coordinates, bowtie uses 0-index
        lines = runBowtie(['--quiet'], bowtiePath, indexPath, ['-c', seq], None)
        
        if len(lines)==0: return None
        line = lines[0]
        columns = line.split('\t')
        # [chromosome, start, end, strand]
        return [columns[2], int(columns[3]), int(columns[3]) + len(seq), columns[1]]
    else:
        # 5 prime
        lines = runBowtie(['--quiet'], bowtiePath, indexPath, ['-c', seq[0:100]], None)
        if len(lines)==0: return None
        line = lines[0]
        columns5 = line.split('\t')
        
        # 3 prime
        lines = runBowtie(['--quiet'], bowtiePath, indexPath, ['-c', seq[-100:]], None)
        if len(lines)==0: return None
        line = lines[0]
        columns3 = line.split('\t')
        
        if columns5[2] != columns3[2]:# Not the same chromosome
            return None
        if columns5[1] != columns3[1]:# Not the same strand
            return None
        if int(columns5[3]) < int(columns3[3]):
            start = int(columns5[3])
            end = int(columns3[3])
        else:
             start = int(columns3[3])
             end = int(columns5[3])
        if (end + 100 - start) != len(seq):
            return None
        
        # [chromosome, start, end, strand]
        return [columns5[2], start, end + 100, columns5[1]]

def getFormattedCoords(coords):
    return coords[0] + ":" + coords[1] + "-" + coords[2]
    
def getPlainOTPosition(distance, intragenic):
    if (distance == 0):
        return "Exonic"
    elif(intragenic):
        return "Intronic"
    else:
        return "Intergenic"

def addCandidateTargets(pamTypeObj, target_size, sgRNA5, sgRNA3, query, strand, candidates, fwdPrimer, revPrimer, maxOT = float('inf')):
    reg_exp = build_expression(pamTypeObj.PAM_str)
    sgRNA5_re = '^' + build_expression(sgRNA5)
    sgRNA3_re = build_expression(sgRNA3) + '$'
    if pamTypeObj.is5prime:
        indices = [m.start() for m in re.finditer('(?=' + reg_exp + ')', query, re.I)]
        for index in indices:
            if (index + target_size + len(pamTypeObj.PAM_str)) > len(query):
                continue
            candidate_sequence = query[index + len(pamTypeObj.PAM_str):index + len(pamTypeObj.PAM_str) + target_size]
            pam_sequence = query[index:index + len(pamTypeObj.PAM_str)]
            if (not re.search(sgRNA5_re, candidate_sequence) is None) and (not re.search(sgRNA3_re, candidate_sequence) is None):
                # we need to transform the index from the reversed sequence to the forward sequence
                if strand == '+':
                    candidates.add(candidate_sequence, pam_sequence + candidate_sequence, index, strand, fwdPrimer, revPrimer, maxOT)
                else:
                    candidates.add(candidate_sequence, pam_sequence + candidate_sequence, len(query) - (index + target_size + len(pamTypeObj.PAM_str)), strand, fwdPrimer, revPrimer, maxOT)
    else:    
        indices = [m.start() for m in re.finditer('(?=' + reg_exp + ')', query, re.I)]
        for index in indices:
            if (index - target_size) < 0:
                continue
            candidate_sequence = query[index - target_size:index]
            pam_sequence = query[index:index + len(pamTypeObj.PAM_str)]
            if (not re.search(sgRNA5_re, candidate_sequence) is None) and (not re.search(sgRNA3_re, candidate_sequence) is None):
                # we need to transform the index from the reversed sequence to the forward sequence
                if strand == '+':
                    candidates.add(candidate_sequence, candidate_sequence + pam_sequence, index - target_size, strand, fwdPrimer, revPrimer, maxOT)
                else:
                    candidates.add(candidate_sequence, candidate_sequence + pam_sequence, len(query) - (index + len(pamTypeObj.PAM_str)), strand, fwdPrimer, revPrimer, maxOT)

def findOT(candidates, pamTypeObj, outputPath, coreMismatches, coreRange, totalMismatches, bowtiePath, indexPath, coordinates, exons, genes):
    seqs = pamTypeObj.getSequencesforBowtie(candidates.getSites())
    with open(outputPath + '/bowtieInput.fasta','w') as bowtieInput:
        bowtieInput.write(seqs)
        
    bowtieOptions = pamTypeObj.getBowtieOptions(coreMismatches, coreRange, totalMismatches)
    runBowtie(bowtieOptions, bowtiePath, indexPath, ['-f', outputPath + '/bowtieInput.fasta'], [outputPath + '/bowtieOutput'])
    
    # process output and add off-target info
    with open(outputPath + '/bowtieOutput', 'r') as bowtieOutput:
        for line in bowtieOutput:
            columns = line.split('\t')
            if pamTypeObj.isBowtieHitConsistent(columns):
                #                     forward?                 chromosome  strand      start            substitutions sequence  lengthSeq      lengthPAM                    coreRange
                offTarget = Offtarget(pamTypeObj.is5prime, columns[2], columns[1], int(columns[3]), columns[7], columns[4], len(columns[4]), len(pamTypeObj.PAM_str), coreRange)
                candidates.getSite(columns[0]).addOffTarget(offTarget, coordinates, exons, genes)
    # cleaning
    try:
        os.remove(outputPath + '/bowtieInput.fasta')
        os.remove(outputPath + '/bowtieOutput')
    except FileNotFoundError:
        pass

def validDinucleotideIUPAC(string):
    validChars = ['A', 'C', 'G', 'T', 'N'] + list(iupac_code.keys())
    string = string.upper()
    if string != ''.join(c for c in string if c in validChars) or len(string) != 2:
        msg = "%r is not a valid dinucleotide sequence" % string
        raise ArgumentTypeError(msg)
    return string

def validOverhang(string):
    validChars = ['A', 'C', 'G', 'T', 'N']
    string = string.upper()
    if string != ''.join(c for c in string if c in validChars) or len(string) > 5:
        msg = "%r is not a valid overhang sequence (up to 5 nt)" % string
        raise ArgumentTypeError(msg)
    return string

'''
This function parses the content of a file, as the input string, checking that it has a multifasta format
and returns a list for each entry that is itself another list with the name and sequence.
'''
# check that the file is a proper multifasta file
def readMultiFasta(inputFile):
    
    validChars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    
    fileContent = []
    seqLine = ""
    state = 0 # to represent a finate-state machine
              # 0 -> intial state, waiting for a header
              # 1 -> header read, waiting for sequence line
              # 2 -> at least one sequence read, waiting for more or another header
    for line in inputFile:
        line = line.strip()
        if len(line) == 0:
            continue
        if state == 0:
            if len(line) > 1 and line[0] == ">":  # header
                state = 1
                name = ''.join(c for c in line if c in validChars)
                fileContent.append([name])
            else:
                raise Exception("The first line of the file should contain a valid header")
        elif state == 1:
            if re.fullmatch('[ACGTNacgtn]+', line) is not None: # seq
                seqLine = seqLine + line
                state = 2
            else:
                raise Exception("Expected a valid nucleotide sequence after \"%s\"" % fileContent[-1][0])
        elif state == 2:
            if len(line) > 1 and line[0] == ">" and state==2:  # header
                fileContent[-1].append(seqLine)
                seqLine = ""
                name = ''.join(c for c in line if c in validChars)
                fileContent.append([name])
                state = 1
            elif re.fullmatch('[ACGTNacgtn]+', line) is not None: # seq
                seqLine = seqLine + line
                state = 2
            else:
                raise Exception("Invalid line \"%s\"" % line)
    #At the end the state must be 2
    if state==2:
        fileContent[-1].append(seqLine)
    else:
        raise Exception("Unexpected end of the file")
    
    return fileContent

def doSearch(name, query, pamType, targetSize, totalMismatches, coreLength, coreMismatches, sgRNA5, sgRNA3, fwdPrimer, revPrimer, outputFolder, bowtiePath, indexPath, exonsFile, genesFile, maxOT):
     
    if pamType not in ["NGG", "NRG"]:
        coreLength = "NA"
        coreMismatches = "NA"
    totalSeqSize = targetSize + len(pamType) 
    
    pamTypeObj = factory(pamType)
    
    # exons and genes
    exons = BedInterval()
    genes = BedInterval()
    if exonsFile is not None and genesFile is not None:
        try:
            from bx.intervals.intersection import Interval
            exons.loadFile(exonsFile)
            genes.loadFile(genesFile)
        except ImportError:
            sys.stderr.write('The bx-python module is not available. Ignoring exon and gene files!\n')
    
    coordinates = getSeqCoords(query, bowtiePath, indexPath)
    if not coordinates is None:
        # What if the input sequence is in the reverse strand???
        # so we use the reverse complement
        if coordinates[3] == "-":
            query = reverse_complement(query)
    
    candidates = sgRNAbindingSites()
    addCandidateTargets(pamTypeObj, targetSize, sgRNA5, sgRNA3, query, '+', candidates, fwdPrimer, revPrimer)
    addCandidateTargets(pamTypeObj, targetSize, sgRNA5, sgRNA3, reverse_complement(query), '-', candidates, fwdPrimer, revPrimer)
    
    
    if(len(candidates.sites) < 1):
        sys.stderr.write('No candidates found in the query sequence named %s.' % name)
        return
    
    # finding off-target sites
    findOT(candidates, pamTypeObj, outputFolder, coreMismatches, coreLength, totalMismatches, bowtiePath, indexPath, coordinates, exons, genes)
    
    candidates.sortOffTargets()
    # scaling scores to the range [0, 1000]
    candidates.scaleScoreAndRelabel()        
    
    sortedSites = candidates.getSitesSorted()
    
    # reporting
    bedFile = open(outputFolder + os.path.sep + name + '.bed', 'w')
    if coordinates is not None:
        for idx in range(len(candidates.sites)):
            bedFile.write(coordinates[0] + '\t' + str(coordinates[1] + sortedSites[idx].position) + '\t' + str(coordinates[1] + sortedSites[idx].position + totalSeqSize) + '\t' + sortedSites[idx].label + '\t' + str(int(sortedSites[idx].score)) + '\t' + sortedSites[idx].strand + '\n')
    else:
        for idx in range(len(candidates.sites)):
            bedFile.write(name + '\t' + str(sortedSites[idx].position) + '\t' + str(sortedSites[idx].position + totalSeqSize) + '\t' + sortedSites[idx].label + '\t' + str(int(sortedSites[idx].score)) + '\t' + sortedSites[idx].strand + '\n')
    bedFile.close()
    
    with open(outputFolder + os.path.sep + name + '.xls', 'w') as output, open(outputFolder + os.path.sep + name + '.fasta', 'w') as fasta:
    
        output.write("Input:\t" + query + "\n")
        output.write("PAM:\t" + pamType + "\n")
        output.write("Target site length:\t" + str(targetSize) + "\n")
        output.write("Target site 5' limitation:\t" + sgRNA5 + "\n")
        output.write("Target site 3' limitation:\t" + sgRNA3 + "\n")
        output.write("Core length:\t" + str(coreLength) + "\n")
        output.write("Core MM:\t" + str(coreMismatches) + "\n")
        output.write("Total MM:\t" + str(totalMismatches) + "\n\n")    
        
        for idx in range(0, len(candidates.sites)):
            fasta.write('>' + sortedSites[idx].label + '\n')
            fasta.write(sortedSites[idx].sequence + '\n')
            
            if sortedSites[idx].effi_score is None:
                output.write(sortedSites[idx].label + '\t' + sortedSites[idx].sequence + '\t' + str(int(sortedSites[idx].score)) + '\n')
            else:
                output.write(sortedSites[idx].label + '\t' + sortedSites[idx].sequence + '\t' + str(int(sortedSites[idx].score)) + '\tCRISPRater score\t' + str(sortedSites[idx].effi_score) + '\n')
            if sortedSites[idx].oligo1 != '':            
                output.write('Oligo fwd\t' + str(sortedSites[idx].oligo1) + '\n')
                output.write('Oligo rev\t' + str(sortedSites[idx].oligo2) + '\n')
            else:
                output.write('Oligo adding fwd\t' + str(sortedSites[idx].oligoAfwd) + '\n')
                output.write('Oligo adding rev\t' + str(sortedSites[idx].oligoArev) + '\n')
                if sortedSites[idx].oligoSfwd != "" and sortedSites[idx].oligoSrev != "":
                    output.write('Oligo substituting fwd\t' + str(sortedSites[idx].oligoSfwd) + '\n')
                    output.write('Oligo substituting rev\t' + str(sortedSites[idx].oligoSrev) + '\n')
            
            if(pamTypeObj.is5prime):
                output.write('Chromosome\tstart\tend\tstrand\tMM\tPAM\ttarget_seq\talignment\tdistance\tposition\tgene name\tgene id\n')
            else:
                output.write('Chromosome\tstart\tend\tstrand\tMM\ttarget_seq\tPAM\talignment\tdistance\tposition\tgene name\tgene id\n')
            for idx2 in range(0, len(sortedSites[idx].offTargets)):
                offTarget = sortedSites[idx].offTargets[idx2]
                
                output.write("\t".join(offTarget.getGenomicCoordinates()))
                output.write("\t" + offTarget.strand)
                output.write("\t" + str(offTarget.mismatches))
                if(pamTypeObj.is5prime):
                    output.write("\t" + offTarget.sequence[:len(pamType)] + "\t" + offTarget.sequence[len(pamType):])
                else:
                     output.write("\t" + offTarget.sequence[:-len(pamType)] + "\t" + offTarget.sequence[-len(pamType):])
                output.write("\t" + offTarget.alignment + "\t" + str(offTarget.distance) + "\t" + getPlainOTPosition(offTarget.distance, offTarget.intragenic))
                output.write("\t" + offTarget.geneName + "\t" + offTarget.geneID + "\n")
            output.write("\n")
        
    
def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description="CCTop is the CRISPR/Cas9 Target online predictor.", epilog=textwrap.dedent('''\
        If you use this tool please cite it as:
        
        Stemmer, M., Thumberger, T., del Sol Keyer, M., Wittbrodt, J. and Mateo, J.L.
        CCTop: an intuitive, flexible and reliable CRISPR/Cas9 target prediction tool.
        PLOS ONE (2015). doi:10.1371/journal.pone.0124633
        
        Have fun using CCTop!
        '''))
    parser.add_argument("--input", metavar="<file>", type=FileType('r'), help="Fasta file containing the sequence(s) to be scanned for sgRNA candidates.", required=True)
    parser.add_argument("--index", metavar="<file>" , help="Path to the bowtie index files including the name of the index.", required=True)
    parser.add_argument("--bowtie", metavar="<folder>", help="Path to the folder where the executable bowtie is.", default="")
    parser.add_argument("--targetSize", metavar="<int>", help="Target site length. (default: %(default)s)", default=20, type=int)
    parser.add_argument("--pam", help="PAM type. (default: %(default)s)", default="NGG", choices=['NGG', 'NRG', 'TTTN', 'NNGRRT', 'NNNNGATT', 'NNAGAAW', 'NAAAAC'])
    parser.add_argument("--sgRNA5", metavar="<sequence>", type=validDinucleotideIUPAC, help="Filter candidates target sites with the most 5 prime nucleotides defined by this sequence. IUPAC code allowed. (default: %(default)s)", default="NN")
    parser.add_argument("--sgRNA3", metavar="<sequence>", type=validDinucleotideIUPAC, help="Filter candidates target sites with the most 5 prime nucleotides defined by this sequence. IUPAC code allowed. (default: %(default)s)", default="NN")
    parser.add_argument("--fwdOverhang", metavar="<sequence>", type=validOverhang, help="Sequence of the 5 prime forward cloning oligo. (default: %(default)s)", default="TAGG")
    parser.add_argument("--revOverhang", metavar="<sequence>", type=validOverhang, help="Sequence of the 5 prime reverse cloning oligo. (default: %(default)s)", default="AAAC")
    parser.add_argument("--totalMM", metavar="<int>", help="Number of total maximum mismatches allowed in the off-target sites. (default: %(default)s)", default=4, type=int)
    parser.add_argument("--coreLength", metavar="<int>", help="Number of bases that enclose the core of the target site. (default: %(default)s)", default=12, type=int)
    parser.add_argument("--coreMM", metavar="<int>", help="Number of maximum mismatches allowed in the core of the off-target sites. (default: %(default)s)", default=2, type=int)
    parser.add_argument("--maxOT", metavar="<int>", help="Maximum number of off-target sites to be reported. (default: %(default)s)", default=float("inf"), type=int)
    parser.add_argument("--output", metavar="<folder>", help="Output folder. (default: %(default)s)", default="." + os.path.sep)
    parser.add_argument("--exonsFile", metavar="<file>", help="Path to the pseudo-bed file containing the coordinate of exons in the target genome. (default: NotUsed)", default=None)
    parser.add_argument("--genesFile", metavar="<file>", help="Path to the pseudo-bed file containing the coordinate of genes in the target genome. (default: NotUsed)", default=None)
    args = parser.parse_args()
    
    
    with args.input:
        fileContent = readMultiFasta(args.input)
    
    for sequence in fileContent:
        sys.stdout.write("Working on sequence '%s'\n" % sequence[0])
        doSearch(sequence[0], sequence[1], args.pam, args.targetSize, args.totalMM, args.coreLength, args.coreMM, args.sgRNA5, args.sgRNA3, args.fwdOverhang, args.revOverhang, args.output, args.bowtie, args.index, args.exonsFile, args.genesFile, args.maxOT)
