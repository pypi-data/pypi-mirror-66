
from cctop.sequenceMethods import reverse_complement
from cctop.scoreCRISPRater import getScore
from math import log10

class sgRNAbindingSite:    
    def __init__(self, targetSeq, sequence, position, strand, fwdPrimer, revPrimer, maxOT = float('inf')):
        self.sequence = sequence
        if(len(targetSeq)==20):
            self.effi_score = getScore(targetSeq)
        else:
            self.effi_score = None
        self.position = position  # leftmost coordinates, including the PAM if 5'
        self.strand = strand
        self.score = 100
        self.label = None
        self.oligo1 = ""  # leading GG, forward
        self.oligo2 = ""  # leading GG, reverse
        self.oligoAfwd = ""  # adding, forward
        self.oligoArev = ""  # adding, reverse
        self.oligoSfwd = ""  # substituting, forward
        self.oligoSrev = ""  # substituting, reverse
        
        self.offTargets = []
        self.maxOT = maxOT
        
        self.__numOT = 0.0
        self.__sumDistanceToExon = 0
        self.__sumOTscore = 0
        
        # oligos
        if fwdPrimer == "TAGG":  # T7
            if targetSeq[0] == 'G' and targetSeq[1] == 'G':
                self.oligo1 = 'TA' + targetSeq
                self.oligo2 = 'AAAC' + reverse_complement(targetSeq[2:])
            elif targetSeq[0] == 'G' and not targetSeq[1] == 'G':
                self.oligoAfwd = 'TAg' + targetSeq
                self.oligoArev = 'AAAC' + reverse_complement(self.oligoAfwd[4:])
                self.oligoSfwd = 'TAGg' + targetSeq[2:]
                self.oligoSrev = 'AAAC' + reverse_complement(self.oligoSfwd[4:])
            else:
                self.oligoAfwd = 'TAgg' + targetSeq
                self.oligoArev = 'AAAC' + reverse_complement(self.oligoAfwd[4:])
                self.oligoSfwd = 'TAgg' + targetSeq[2:]
                self.oligoSrev = 'AAAC' + reverse_complement(self.oligoSfwd[4:])
        elif fwdPrimer == "CACCG":
            if targetSeq[0] == 'G':
                self.oligo1 = 'CACC' + targetSeq
                self.oligo2 = 'AAAC' + reverse_complement(targetSeq)
            else:
                self.oligoAfwd = 'CACCg' + targetSeq
                self.oligoArev = 'AAAC' + reverse_complement('G' + self.oligoAfwd[5:])
                self.oligoSfwd = 'CACCg' + targetSeq[1:]
                self.oligoSrev = 'AAAC' + reverse_complement('G' + self.oligoSfwd[5:])
        else:
            self.oligo1 = fwdPrimer + targetSeq
            self.oligo2 = revPrimer + reverse_complement(targetSeq)

    def addOffTarget(self, offTarget, coordinates, exons, genes):
        if len(self.offTargets)>self.maxOT:
            return
        
        offTarget.setGeneInfo(exons, genes)
        self.offTargets.append(offTarget)
        
        if not coordinates is None:
            # checking if the "off-target" site is in fact the on-target
            if offTarget.chromosome == coordinates[0] and offTarget.start >= coordinates[1] and offTarget.start <= coordinates[2]:
                return
            
        isThereGeneInfo = len(exons.chroms) > 0
        # off-target sites without gene nearby won't affect the score, unless there is not gene information
        if offTarget.distance == 'NA' and isThereGeneInfo:
            return
        
        self.__numOT = self.__numOT + 1
        self.__sumOTscore = self.__sumOTscore + offTarget.score
            
        if isThereGeneInfo:
            if offTarget.distance != 0:
                try:
                    self.__sumDistanceToExon = self.__sumDistanceToExon + log10(offTarget.distance)
                except ValueError:
                    print(offTarget.distance)
            else:
                self.__sumDistanceToExon = self.__sumDistanceToExon + 0
        
        if self.__numOT > 0:
            self.score = self.__sumOTscore / self.__numOT + self.__sumDistanceToExon / self.__numOT - self.__numOT
        else:
            self.score = 100
            
class sgRNAbindingSites:
    def __init__(self):
        self.sites = dict() # sites indexes by the label
    def add(self, targetSeq, sequence, position, strand, fwdPrimer, revPrimer, maxOT = float('inf')):
        newSite = sgRNAbindingSite(targetSeq, sequence, position, strand, fwdPrimer, revPrimer, maxOT)
        # initial label
        newSite.label = "C" + str(len(self.sites)+1)
        self.sites[newSite.label] = newSite
        
    def getSites(self):
        return list(self.sites.values())
    def getSitesSorted(self):
        # notice that to sort the keys we discard the leading character ('T')
        return [value for (key, value) in sorted(list(self.sites.items()),key= lambda item: int(item[0][1:]))]
        
    def getSite(self, label):
        return self.sites[label]
    def scaleScoreAndRelabel(self):
        maxScore=float('-inf')
        minScore=float('inf')
        
        for site in list(self.sites.values()):
            if site.score > maxScore:
                maxScore = site.score
            if site.score < minScore:
                minScore = site.score
        minScore = float(minScore)
        newDict = dict() # To avoid integer division in python2.7
        sortedSitesByScore = list(self.sites.values())
        sortedSitesByScore.sort(key=lambda site: (site.score), reverse=True)
        if len(sortedSitesByScore) > 1:
            for idx in range(len(sortedSitesByScore)):
                newLabel = 'T' + str(idx + 1)
                sortedSitesByScore[idx].label = newLabel
                if maxScore > minScore:
                    sortedSitesByScore[idx].score = (sortedSitesByScore[idx].score - minScore) / (maxScore - minScore) * 1000
                else:
                    sortedSitesByScore[idx].score = 1000
                newDict[newLabel] = sortedSitesByScore[idx]
        else:
            sortedSitesByScore[0].score = 1000
            sortedSitesByScore[0].label = 'T1'
            newDict['T1'] = sortedSitesByScore[0]
         
        self.sites = newDict
    def sortOffTargets(self):
        for site in list(self.sites.values()):
            site.offTargets.sort(key=lambda offtarget: (offtarget.score,
                                                        (lambda dist: 0 if dist=="NA" else dist)(offtarget.distance)))
            
