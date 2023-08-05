
import re

model_weight = [0.14177385, 0.06966514, 0.04216254, 0.03303432, 0.02355430, -0.04746424, -0.04878001, -0.06981921, -0.07087756, -0.08160700]
model_offset = 0.6505037

patternCG = re.compile("[CG]")
def getGCFreq(seq):
    cg = len(patternCG.findall(seq))
    return(float(cg)/len(seq))

def calcFeatures(seq):
    feat = [0]*10
    feat[0] = getGCFreq(seq[3:13])
    if(seq[19]=="G"):
        feat[1] = 1
    if(seq[2]=="T" or seq[2]=="A"):
        feat[2] = 1
    if(seq[11]=="G" or seq[11]=="A"):
        feat[3] = 1
    if(seq[5]=="G"):
        feat[4] = 1
    if(seq[3]=="T" or seq[3]=="A"):
        feat[5] = 1
    if(seq[17]=="G" or seq[17]=="A"):
        feat[6] = 1
    if(seq[4]=="C" or seq[4]=="A"):
        feat[7] = 1
    if(seq[13]=="G"):
        feat[8] = 1
    if(seq[14]=="A"):
        feat[9] = 1
    return(feat)

def getScore(seq):
    features = calcFeatures(seq)
    
    score = 0
    for idx in range(0,len(features)):
        score = score + features[idx]*model_weight[idx]
    score = score + model_offset
    return(score)
