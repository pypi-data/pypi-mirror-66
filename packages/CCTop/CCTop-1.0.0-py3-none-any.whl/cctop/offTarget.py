
from cctop.sequenceMethods import reverse_complement

class Offtarget:
    # New offtarget site coming for forward search, TTTN
    def __newFwd(self, chromosome, strand, start, substitutions, sequence, lengthSeq, lengthPAM, coreRange):
        self.chromosome = chromosome
        self.strand = strand
        if strand == "+":  # the search is done with the forward sequence!
            self.sequence = list(sequence)  # to make the string modifiable
        else:
            self.sequence = list(reverse_complement(sequence))  # to make the string modifiable
        self.start = start  # assuming bed coordinates
        self.end = start + lengthSeq
        
        tmp = substitutions.split(",")
        
        self.mismatches = len(tmp) - 1
        self.alignment = ['|'] * (lengthSeq - lengthPAM)
        self.score = 0
        for substitution in tmp:
            [idx, nt] = substitution.split(':')
            idx = int(idx)
            if strand == "+":
                self.sequence[idx] = nt[0]
            else:
                self.sequence[idx] = reverse_complement(nt[0])
            if idx < lengthPAM:  # The mismatch in the PAM is not considered for score calculation of alignment 
                continue
            self.score = self.score + pow(1.2, idx - lengthPAM + 1)
            self.alignment[idx - lengthPAM] = '-'
        if coreRange != "NA" and coreRange > 0:
            self.alignment = "PAM[" + "".join(self.alignment[:coreRange]) + "]" + "".join(self.alignment[coreRange:])
        else:
            self.alignment = "PAM" + "".join(self.alignment)
        self.sequence = "".join(self.sequence)
        # self.sequence = reverse_complement("".join(self.sequence))
        
    # New offtarget site coming for reverse search, NGG and other PAMs
    def __newRev(self, chromosome, strand, start, substitutions, sequence, lengthSeq, lengthPAM, coreRange):
        self.chromosome = chromosome
        if strand == "+":  # the search is done with the reverse complemented sequence!
            self.strand = "-"
            self.sequence = list(sequence)  # to make the string modifiable
        else:
            self.strand = "+"
            self.sequence = list(reverse_complement(sequence))  # to make the string modifiable
        self.start = start  # assuming bed coordinates
        self.end = start + lengthSeq
        
        tmp = substitutions.split(",")
        
        self.mismatches = len(tmp) - 1
        self.alignment = ['|'] * (lengthSeq - lengthPAM)
        self.score = 0
        for substitution in tmp:
            [idx, nt] = substitution.split(':')
            idx = int(idx)
            if strand == "+":
                self.sequence[idx] = nt[0]
            else:
                self.sequence[idx] = reverse_complement(nt[0])
            if idx < lengthPAM:  # The mismatch in the PAM is not considered for score calculation of alignment 
                continue
            self.score = self.score + pow(1.2, lengthSeq - idx)
            self.alignment[lengthSeq - 1 - idx] = '-'
        if coreRange != "NA" and coreRange > 0:
            self.alignment = "".join(self.alignment[:-coreRange]) + "[" + "".join(self.alignment[-coreRange:]) + "]PAM"
        else:
            self.alignment = "".join(self.alignment) + "PAM"
        self.sequence = reverse_complement("".join(self.sequence))
        
        
    def __init__(self, forward, chromosome, strand, start, substitutions, sequence, lengthSeq, lengthPAM, coreRange):
        if(forward):
            self.__newFwd(chromosome, strand, start, substitutions, sequence, lengthSeq, lengthPAM, coreRange)
        else:
            self.__newRev(chromosome, strand, start, substitutions, sequence, lengthSeq, lengthPAM, coreRange)
       
    def setGeneInfo(self, exons, genes):
        closest = exons.closest(self.chromosome, self.start, self.end)
        
        self.geneID = closest[0]
        self.geneName = closest[1]
        self.distance = closest[2]
        self.intragenic = genes.overlaps(self.chromosome, self.start, self.end)
            
    def getGenomicCoordinates(self):
        return [self.chromosome, str(self.start + 1), str(self.end)]
    def getBedCoordinates(self):
        return [self.chromosome, str(self.start), str(self.end)]

