import Globals

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

        total_pos += pos_counts[id] * sum(list(freq_dict))
        total_neg += neg_counts[id] * sum(list(freq_dict))

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
            richness[kmer] = 10
        else:
            richness[kmer] = pos_prop_by_kmer[kmer] / neg_prop_by_kmer[kmer]

    for i in range(10):
        print(richness[kmers[i]])

    ret = []
    for kmer in kmers:
        if (richness[kmer] < .5) | (richness[kmer] > 1.5):
            ret.append(kmer)
    return ret
