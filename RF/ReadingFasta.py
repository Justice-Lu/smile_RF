# Import featurize function
from Kmerizing import *
import Globals

#Creating sequence class
class Seq:
    def __init__(self, name, sequence, dictionary):
        self.name = name
        self.sequence = sequence
        self.dictionary = dictionary
    def __repr__(self):
        return self.name

#Initialize Set of Features
Globals.initialize()

def makematrix(fasta, seqvar, feat, mat):
    i = 0
    j = 0
    for line in fasta:
        if line[0] == '>':
            name = line.replace('\n','')
            seqvar.append(Seq(name, '', featurize('',5,feat)))
            i += 1
        else:
            sequence = line.replace('\n','')
            seqvar[i-1].sequence = seqvar[i-1].sequence + sequence
            seqvar[i-1].dictionary = featurize(seqvar[i-1].sequence,5,feat)
        j += 1

    #This prints all of the k-mers identified in the sequences
    #print(Globals.features)

    #This prints the number of k-mers identified in all of the sequences
    #print(len(Globals.features))

    #This prints number of sequences
    #print(len(Globals.seq))

    for seq in seqvar:
        newseq = []
        for kmer in feat:
            if kmer not in seq.dictionary:
                seq.dictionary[kmer] = 0
            newseq.append(seq.dictionary.get(kmer))
        mat.append(newseq)

    #Prints a matrix with columns corresponding to k-mers and rows corresponding to proteins
    #print(Globals.matrix)

    #Prints protein names
    #print(Globals.seq)

# Read fasta file
fasta1 = open("/home/users/sml96/bin/project-protein-fold/AminoAcidSequences/categorized.fasta")
# Make the matrix
makematrix(fasta1, Globals.seqs, Globals.features, Globals.matrix)
# View output
print(Globals.seqs)