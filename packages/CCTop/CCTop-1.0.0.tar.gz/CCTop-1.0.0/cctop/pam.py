
from cctop.sequenceMethods import reverse_complement

class PAM(object):
    '''
    Generic class to define the different PAM types and the methods needed
    The seed for Bowtie will be always 5
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.coreAllowed = False  # By default a PAM is not compatible with the core region
        self.is5prime = False # Is the PAM at the 5' end, by default it is false
        self.PAM_str = self.__class__.__name__
        self.PAM_rev = reverse_complement(self.PAM_str)  # any ambiguous base is turned into N
        self.mismatchesPAM = self.PAM_rev.count('N')
        self.mismatchesInSeed = min(3,self.PAM_rev[0:5].count('N')) # Value for the -n parameter of Bowtie
        
    '''
    Received a list of sgRNAbindingSite objects and return a string with the
    fasta sequences formatted to perform the search of off-target sites with
    Bowtie
    '''
    def getSequencesforBowtie(self, sites):
        # By default all PAM are in the 3' end and the sequence is reversed to match the seed definition of Bowtie
        fasta = ""
        for candidate in sites:
            fasta = fasta + ">" + candidate.label + "\n"
            fasta = fasta + self.PAM_rev + reverse_complement(candidate.sequence[:-len(self.PAM_str)]) + "\n"
        return fasta
            
    def getBowtieOptions(self, coreMismatches, coreRange, totalMismatches):
        if not self.coreAllowed or coreMismatches == "NA" or coreRange == "NA":
            return ["-a", "--quiet", "-y", "-n" + str(self.mismatchesInSeed), "-l5", "-e" + str((totalMismatches + self.mismatchesPAM) * 30)]
        else:
            if (coreMismatches + self.mismatchesPAM)>3:
                raise ValueError('The value for the parameter coreMismatches is not valid: ' + str(coreMismatches))
            if coreMismatches > totalMismatches:
                raise ValueError('The value for coreMismatches cannot be greater than totalMismatches:' + str(coreMismatches) + ">" + str(totalMismatches))
            return ["-a", "--quiet", "-y", "-n" + str(coreMismatches + self.mismatchesPAM),
                    "-l" + str(coreRange + len(self.PAM_str)), "-e" + str((totalMismatches + self.mismatchesPAM) * 30)]
        
    def isBowtieHitConsistent(self, bowtieLineColumns):
        '''
        Tells if the hit found show a set of mismatches, if any, consistent with the variable positions in the PAM
        ''' 
        # This generic version works for PAMs (5' or 3') where only the first position is an N
        # and the other position are not variables
        # NGG, NGA, NGCG, TTTN, NAAAAC
        # This is also fine for NRG because we search twice for NGG and NAG
        # The same for YTN (CTN, TTN)
        mismatches = bowtieLineColumns[7].split(',')
        posFirstMM = int(mismatches[0].split(":")[0])
        return posFirstMM >= (len(self.PAM_str) - 1)


        
def factory(type):

    class NGG(PAM):
        def __init__(self):
            super(NGG, self).__init__()
            self.coreAllowed = True
            self.mismatchesInSeed = 3
    
    class NRG(PAM):
        def __init__(self):
            super(NRG, self).__init__()
            self.coreAllowed = True
            self.mismatchesPAM = 1
            self.mismatchesInSeed = 3
            
        def getSequencesforBowtie(self, sites):
            # As there are too many variable positions it is necessary to search two sequences fixing the 'R' with 'A' or 'G' in each case         
            fasta = ""
            for candidate in sites:
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "CCN" + reverse_complement(candidate.sequence[:-len(self.PAM_str)]) + "\n"
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "CTN" + reverse_complement(candidate.sequence[:-len(self.PAM_str)]) + "\n"
            return fasta
    
    class NGA(PAM):
        def __init__(self):
            super(NGA, self).__init__()
            self.coreAllowed = True
            self.mismatchesInSeed = 3
    
    class NGCG(PAM):
        def __init__(self):
            super(NGCG, self).__init__()
            self.coreAllowed = True
            self.mismatchesInSeed = 2
    
    class TTTN(PAM):
        def __init__(self):
            super(TTTN, self).__init__()
            self.mismatchesInSeed = 2
            self.is5prime = True

        def getSequencesforBowtie(self, sites):
            # In this case the PAM is 5'
            fasta = ""
            PAM_str = self.__class__.__name__
            for candidate in sites:
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + PAM_str + candidate.sequence[len(PAM_str):] + "\n"
            return fasta
        
    class YTN(PAM):
        def __init__(self):
            super(YTN, self).__init__()
            self.mismatchesPAM = 1
            self.mismatchesInSeed = 3
            self.is5prime = True

        def getSequencesforBowtie(self, sites):
            # In this case the PAM is 5'
            fasta = ""
            PAM_str = self.__class__.__name__
            for candidate in sites:
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "TTN" + candidate.sequence[len(PAM_str):] + "\n"
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "CTN" + candidate.sequence[len(PAM_str):] + "\n"
            return fasta
    
    class TTN(PAM):
        def __init__(self):
            super(TTN, self).__init__()
            self.mismatchesPAM = 1
            self.mismatchesInSeed = 3
            self.is5prime = True

        def getSequencesforBowtie(self, sites):
            # In this case the PAM is 5'
            fasta = ""
            PAM_str = self.__class__.__name__
            for candidate in sites:
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + PAM_str + candidate.sequence[len(PAM_str):] + "\n"
            return fasta
    
    class NNNRRT(PAM):
        def __init__(self):
            super(NNNRRT, self).__init__()
            # One of the variable position will be fixed so that the number or real mismatches is one less 
            self.mismatchesPAM = 4
            
        def getSequencesforBowtie(self, sites):
            # As there are too many variable positions it is necessary to search two sequences fixing the most 3' 'R' with 'A' or 'G' in each case         
            fasta = ""
            for candidate in sites:
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "ACNNNN" + reverse_complement(candidate.sequence[:-len(self.PAM_str)]) + "\n"
                fasta = fasta + ">" + candidate.label + "\n"
                fasta = fasta + "ATNNNN" + reverse_complement(candidate.sequence[:-len(self.PAM_str)]) + "\n"
            return fasta

        def isBowtieHitConsistent(self, bowtieLineColumns):
            mismatches = bowtieLineColumns[7].split(',')
            firstMM = mismatches[0].split(":")
            posFirstMM = int(firstMM[0])
            if posFirstMM > 2:
                return True
            if posFirstMM == 2:
                if bowtieLineColumns[1] == '+':
                    return firstMM[1][0] in 'CT'
                else:
                    return firstMM[1][0] in 'AG'
            
            return False
    
    class NNGRRT(PAM):
        def isBowtieHitConsistent(self, bowtieLineColumns):
            mismatches = bowtieLineColumns[7].split(',')
            firstMM = mismatches[0].split(":")
            posFirstMM = int(firstMM[0])
            if posFirstMM > 3:
                return True
            if posFirstMM == 1:
                return (bowtieLineColumns[1] == '-' and (mismatches[0][2] in 'CT' and mismatches[1][2] in 'CT')) or (bowtieLineColumns[1] == '+' and (mismatches[0][2] in 'AG' and mismatches[1][2] in 'AG'))
            return False
    
    class NNNNGATT(PAM):
        def isBowtieHitConsistent(self, bowtieLineColumns):
            return True
    
    class NNAGAAW(PAM):
        def isBowtieHitConsistent(self, bowtieLineColumns):
            mismatches = bowtieLineColumns[7].split(',')
            firstMM = mismatches[0].split(":")
            posFirstMM = int(firstMM[0])
            if posFirstMM > 4:
                return True
            if posFirstMM == 0:
                return (mismatches[0][2] in 'AT')
            return False
    
    class NAAAAC(PAM):
        def isBowtieHitConsistent(self, bowtieLineColumns):
            return True
    
    class NNNNRYAC(PAM):
        def isBowtieHitConsistent(self, bowtieLineColumns):
            mismatches = bowtieLineColumns[7].split(',')
            firstMM = mismatches[0].split(":")
            posFirstMM = int(firstMM[0])
            if posFirstMM > 3:
                return True
            if posFirstMM == 2:
                return (bowtieLineColumns[1] == '+' and (mismatches[0][2] in 'AG' and mismatches[1][2] in 'CT')) or (bowtieLineColumns[1] == '-' and (mismatches[0][2] in 'CT' and mismatches[1][2] in 'AG'))
            return False
    
    if type == "NGG": return NGG()
    if type == "NRG": return NRG()
    if type == "NGA": return NGA()
    if type == "NGCG": return NGCG()
    if type == "TTTN": return TTTN()
    if type == "YTN": return YTN()
    if type == "TTN": return TTN()
    if type == "NNNRRT": return NNNRRT()
    if type == "NNGRRT": return NNGRRT()
    if type == "NNNNGATT": return NNNNGATT()
    if type == "NNAGAAW": return NNAGAAW()
    if type == "NAAAAC": return NAAAAC()
    if type == "NNNNRYAC": return NNNNRYAC()
    assert 0, "Wrong PAM type: " + type

    
