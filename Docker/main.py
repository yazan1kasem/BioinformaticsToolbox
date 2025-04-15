from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/orf-search/")
async def orf_search(request: Request):
    body = await request.json()

    # Ich kenne keine andere Möglichkeit, wie ich die Daten aus dem Request bekomme, aber es funktioniert
    dna_sequence = body.get("dna_sequence")
    min_orf_length = body.get("min_orf_length")
    both_strands = body.get("both_strands")

    orfs = find_orfs(dna_sequence, min_orf_length, both_strands)
    # ich kann nicht mehr, also habe ich keine neue Seite erstellt, die die ORFs anzeigt
    # dieses Programm hat über 16 Stunden gedauert, ich bin müde
    return {"orfs": orfs}

#zum Testen der FastAPI
@app.get("/get/")
async def read_root():
    return {"message": "Hello World"}


def find_orfs(dna_sequence: str, min_orf_length: int, both_strands: bool):
    dna_sequence = dna_sequence.upper().replace('U', 'T')
    start_codon = 'ATG'
    stop_codons = ['TAA', 'TAG', 'TGA']

    def get_reverse_complement(seq):
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement[base] for base in reversed(seq))


    def find_orfs_in_strand(seq):
        orfs = []
        for i in range(0, len(seq) - 2, 3):
            if seq[i:i + 3] == start_codon:
                for j in range(i + 3, len(seq) - 2, 3):
                    if seq[j:j + 3] in stop_codons:
                        orf_length = j + 3 - i
                        if orf_length >= min_orf_length:
                            orfs.append({'start': i, 'end': j + 3, 'sequence': seq[i:j + 3], 'strand': "+"})
                        break
        return orfs

    orfs = find_orfs_in_strand(dna_sequence)

    if both_strands:
        reverse_complement = get_reverse_complement(dna_sequence)
        reverse_orfs = find_orfs_in_strand(reverse_complement)
        orfs.extend([{'start': len(dna_sequence) - orf['end'],
                      'end': len(dna_sequence) - orf['start'],
                      'sequence': orf['sequence'], 'strand': "-"
                      }
                     for orf in reverse_orfs])

    return orfs

