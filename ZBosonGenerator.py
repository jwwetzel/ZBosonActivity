from ROOT import TFile, TTree, TRandom, TH1F
from ROOT import gROOT
from array import array
import random
from random import shuffle

##############################
######### GENERATION #########
##############################

gROOT.ProcessLine(
                  "struct MyStruct {\
                  Float_t     f_muonMass1;\
                  Float_t     f_muonMass2;\
                  Float_t     f_muonMass3;\
                  Float_t     f_muonMass4;\
                  };" )

from ROOT import MyStruct
mystruct = MyStruct()

f = TFile( 'ZBosonNtuple.root', 'RECREATE' )
tree = TTree( 'T', 'Z Boson Data' )
tree.Branch( 'muons', mystruct, 'f_muonMass1/F:f_muonMass2:f_muonMass3:f_muonMass4' )

rand = TRandom()

muonMass = {}

for i in range(10000):
    muonMass[0] = rand.Exp(30)*90
    muonMass[1] = abs(rand.Gaus(91.2,1.3) - muonMass[0])
    muonMass[2] = rand.Exp(30)
    muonMass[3] = rand.Exp(30)
    
    muons = [[i] for i in range(4)]
    for i in range(4):
        muons[i] = muonMass[i]
    shuffle(muons)

    mystruct.f_muonMass1   = muons[0]
    mystruct.f_muonMass2   = muons[1]
    mystruct.f_muonMass3   = muons[2]
    mystruct.f_muonMass4   = muons[3]

    tree.Fill()




############################
######### ANALYSIS #########
############################
allMuonHist = TH1F("allMuonHist","All Muon Mass",1000,0,1000)
diMuonHist12 = TH1F("diMuonHist12","Di Muon Mass",500,0,500)
diMuonHist23 = TH1F("diMuonHist23","Di Muon Mass",500,0,500)
diMuonHist34 = TH1F("diMuonHist34","Di Muon Mass",500,0,500)
bestDiMuonPair = TH1F("bestDiMuonHist","Best Di Muon Pair Mass",500,0,500)

branch = tree.GetBranch("muons")

for event in f.T:
    muonOne = event.f_muonMass1
    muonTwo = event.f_muonMass2
    muonThree = event.f_muonMass3
    muonFour = event.f_muonMass4
    
    ##################################
    ### STEP 1 - sum all muon mass ###
    ##################################
    allMuonHist.Fill(muonOne + muonTwo + muonThree + muonFour)
    
    
    ###############################################################
    ### STEP 2 - sum muon masses in pairs (notice peak at ~90?) ###
    ###############################################################
    diMuonHist12.Fill(muonOne + muonTwo)
    diMuonHist23.Fill(muonTwo + muonThree)
    diMuonHist34.Fill(muonThree + muonFour)
    
    ###########################################
    ### STEP 3 - algorithms focusing on ~90 ###
    ###########################################
    combinedMass = muonOne + muonTwo

    if (abs(combinedMass - 90) > abs(muonOne + muonThree - 90)):
        combinedMass = muonOne + muonThree
    if (abs(combinedMass - 90) > abs(muonOne + muonFour - 90)):
        combinedMass = muonOne + muonFour
    if (abs(combinedMass - 90) > abs(muonTwo + muonThree - 90)):
        combinedMass = muonTwo + muonThree
    if (abs(combinedMass - 90) > abs(muonTwo + muonFour - 90)):
        combinedMass = muonTwo + muonFour
    if (abs(combinedMass - 90) > abs(muonThree + muonFour - 90)):
        combinedMass = muonThree + muonFour
    
    bestDiMuonPair.Fill(combinedMass)

    ##################################
    ### Fitting...ETC...
    ##################################

f.Write()
f.Close()





























































































