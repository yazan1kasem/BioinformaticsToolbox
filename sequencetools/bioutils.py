from sequencetools.bioconstants import sequence


def getCodons(sequence: str, offset: int) -> [str]:
    codons = []

    for i in range(offset, len(sequence), 3):
        if i + 3 > len(sequence):
            codon = sequence[i:] + "X" * (i + 3 - len(sequence))
        else:
            codon = sequence[i:i + 3]
        codons.append(codon)

    return codons


# Test der Funktion
if __name__ == '__main__':
    print(getCodons(sequence, offset=0))
