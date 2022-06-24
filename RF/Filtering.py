import Globals
import ReadingFasta

acc_list = Globals.initialize_protein_list()

#kmers: set of all possible kmers for the protein
#seqvar: list of Seq class objects (name, sequence = protein sequence, dictionary = kmer freq dictionary)
#pos_counts: key = protein id, value = # pos. interactions with the protein
#neg_counts: key = protein id, value = # neg. interactions with the protein
def richness_protein(kmers, seqvar, pos_counts, neg_counts):
    kmers = list(kmers)

    pos_counts_by_kmer = {}
    neg_counts_by_kmer = {}
    pos_prop_by_kmer = {}
    neg_prop_by_kmer = {}
    for kmer in kmers:
        pos_counts_by_kmer[kmer] = 0
        neg_counts_by_kmer[kmer] = 0

    total_pos = 0
    total_neg = 0

    for seq in seqvar:
        id = seq.name
        freq_dict = seq.dictionary

        total_pos += pos_counts[id] * sum(freq_dict.values())
        total_neg += neg_counts[id] * sum(freq_dict.values())

        for kmer in kmers:
            if (pos_counts[id] > 0) & (kmer in freq_dict):
                pos_counts_by_kmer[kmer] += pos_counts[id] * freq_dict[kmer]
                neg_counts_by_kmer[kmer] += neg_counts[id] * freq_dict[kmer]

    for kmer in kmers:
        pos_prop_by_kmer[kmer] = float(pos_counts_by_kmer[kmer]) / float(total_pos)
        neg_prop_by_kmer[kmer] = float(neg_counts_by_kmer[kmer]) / float(total_neg)

    richness = {}
    for kmer in kmers:
        if neg_counts_by_kmer[kmer] == 0:
            richness[kmer] = 100000
        else:
            richness[kmer] = pos_prop_by_kmer[kmer] / neg_prop_by_kmer[kmer]

    ret = []
    for kmer in kmers:
        if (richness[kmer] < .25) | (richness[kmer] > 4):
            ret.append(kmer)

    return ret

def featurize(seq, k, feat):
    dict = {}

    for i in range(0, len(seq) - k + 1):
        kmer = ""
        for j in range(k):
            kmer += seq[i + j]
        if kmer not in dict:
            dict[kmer] = 0
            feat.add(kmer)
        dict[kmer] += 1
    return dict

"""
kmers = set()
proteins = ['P1', 'P2', 'P3']
seqs = ['aaabbdabb', 'bbdabaaa', 'acaaadabb']

for seq in seqs:
    featurize(seq, 3, kmers)

dicts = [{'abb': 2, 'bda': 1, 'dab': 1, 'aab': 1, 'bbd': 1, 'aaa': 1},
         {'aba': 1, 'aaa': 1, 'dab': 1, 'bbd': 1, 'baa': 1, 'bda': 1},
         {'aad': 1, 'aca': 1, 'aaa': 1, 'dab': 1, 'abb': 1, 'ada': 1, 'caa': 1}]

seqvar = []
for i in range(len(proteins)):
    sv = ReadingFasta.Seq(proteins[i], seqs[i], dicts[i])
    seqvar.append(sv)

print(richness_protein(kmers, seqvar, {"P1": 2, 'P2': 1, 'P3': 1}, {"P1": 5, 'P2': 6, 'P3': 6}))
"""