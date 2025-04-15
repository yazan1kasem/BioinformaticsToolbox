import json
import os

import docker

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from fastapi import requests
from django.conf import settings

from sequencetools.models import SequenceSubmission, ORF
from sequencetools.repo import SubmissionRepository
from sequencetools.utils import handle_file_upload
import requests
from Bio import Phylo
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML


# Create your views here.
def index(request):
    return render(request, "base.html", {"message": "Habibi. willkommen zu meiner Webseite!"})


def submissions(request):
    return render(request, "submissions.html", context={"submissions": SubmissionRepository().get_all_submissions()})


def submit(request):
    if request.method == "POST":
        if is_a_DNA_Sequence(request.POST["text_input"]):
            text_input = request.POST["text_input"]
            file_upload = request.FILES["file_upload"]

            print(text_input)
            print(file_upload)

            newSequenceSubmission = SequenceSubmission(
                text_input=text_input,
                file_upload=file_upload.name,
            )
            newSequenceSubmission.save()

            handle_file_upload(file_upload, file_upload)
            return render(request, "submit.html", context={"info": "Data received"})

        return render(request, "submit.html", context={"info": "Only DNA sequence is allowed"})

    return render(request, "submit.html", context={"info": ""})


@csrf_protect
def ORF_FINDER(request):
    if request.method == "POST":
        if request.POST.get("download") == "true":
            return download_orf_as_txt(request)
        dna_sequence: str = str(request.POST["dna_sequence"].replace("\n", "").replace("\r", "").replace(" ", ""))

        if dna_sequence == "":
            return render(request, "ORF_FINDER.html", context={"info": "Füllen Sie bitte das Formular aus"})
        # ich hasse alles was da steht
        if is_a_DNA_Sequence(dna_sequence):
            min_orf_length = int(request.POST["min_orf_length"])
            both_strands = request.POST.get("both-strands") == "on"
            try:
                # der hat mein Laptop zum Zucken gebracht, als wäre es auf Entzug
                respond = requests.post("http://127.0.0.1:8081/orf-search/",
                                        data=json.dumps(ORF(dna_sequence, min_orf_length, both_strands).__dict__))
                respond.raise_for_status()

                orf_data = respond.json().get('orfs', [])
                request.session['Orf_data'] = orf_data
                if isinstance(orf_data, list):
                    for orf in orf_data:
                        orf['length_nt'] = orf['end'] - orf['start'] + 1
                        orf['length_aa'] = orf['length_nt'] // 3
                else:
                    return render(request, "ORF_FINDER.html", context={"info": "Unerwartete Datenstruktur"})
                print(orf_data)
                orf_sequence = orf_data[0]['sequence'] if orf_data else None
                if orf_sequence:
                    blast_results = perform_blastx(orf_sequence, evalue_threshold=0.001, max_hits=10)
                    print(blast_results)
                    return render(request, "ORF_FINDER.html",
                                  {"results": blast_results, "info": f"{len(orf_data)} ORFs gefunden",
                                   "orf_data": orf_data})
                else:
                    print("orf_sequence is empty")
                    return render(request, "ORF_FINDER.html",
                                  {"info": f"{len(orf_data)} ORFs gefunden",
                                   "orf_data": orf_data})

            except requests.exceptions.HTTPError as err:
                return render(request, "ORF_FINDER.html", context={"info": f"Fehler: {err}"})
            except Exception as e:
                return render(request, "ORF_FINDER.html",
                              context={"info": f"Ein unerwarteter Fehler ist aufgetreten: {e}"})
        else:
            return render(request, "ORF_FINDER.html", context={"info": "Das ist keine DNA-Sequenz"})

    return render(request, "ORF_FINDER.html")


def perform_blastx(orf_sequence, evalue_threshold, max_hits):
    result_handle = NCBIWWW.qblast(
        program="blastn",
        database="nr",
        sequence=orf_sequence,
        expect=evalue_threshold,
        hitlist_size=max_hits)
    blast_records = NCBIXML.parse(result_handle)

    result = []
    for record in blast_records:
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                result.append({
                    'alignment_title': alignment.title,
                    'e_value': hsp.expect,
                    'score': hsp.score,
                    'identity': hsp.identities,
                    'sequence': hsp.sbjct
                })

    return result


def is_a_DNA_Sequence(sequence):
    valid_characters = {'A', 'T', 'C', 'G'}
    sequence = sequence.upper()
    for char in sequence:
        if char not in valid_characters:
            return False
    return True


def download_orf_as_txt(request):
    orf_data = request.session.get("Orf_data", [])
    orf_lines = [f"{len(orf_data)} ORFs gefunden\n"]
    for orf in orf_data:
        orf_lines.append(
            f"Start: {orf['start']}, Ende: {orf['end']}, Länge (nt): {orf.get('length_nt', 'N/A')} nt, Länge (aa): {orf.get('length_aa', 'N/A')} aa")
        orf_lines.append(f"Strang: {orf.get('strand', 'N/A')}")
        orf_lines.append(f"Sequenz: {orf['sequence']}\n")
    response = HttpResponse("\n".join(orf_lines), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="orf_data.txt"'
    return response


def msa3(request):
    if request.method == "POST":
        msa_input = request.POST.get("MSAInput", "").strip()
        if not msa_input:
            return HttpResponse("Die Eingabesequenz darf nicht leer sein.", status=400)

        container_path = os.path.join(settings.BASE_DIR, "containerfiles")
        os.makedirs(container_path, exist_ok=True)

        input_file = os.path.join(container_path, "msa3A.fasta")
        with open(input_file, "w") as file:
            file.write(msa_input)

        client = docker.from_env()
        try:
            if request.POST.get("alignmentTool") == "MUSCLE":
                print("MUSCLE")
                containerModel = client.containers.run(
                    image="biocontainers/muscle:v1-3.8.1551-2-deb_cv1",
                    command="muscle -in /containerfiles/msa3A.fasta -out /containerfiles/output.html -html",
                    volumes={container_path: {"bind": "/containerfiles/", "mode": "rw"}},
                    remove=True
                )
            elif request.POST.get("alignmentTool") == "ClustalW":
                print("ClustalW")
                containerModel = client.containers.run(
                    image="biocontainers/clustalw:v2.1lgpl-6-deb_cv1",
                    command="clustalw -infile=/containerfiles/msa3A.fasta -outfile=/containerfiles/output.aln -output=CLUSTAL",
                    volumes={os.path.join(os.getcwd(), "containerfiles"): {"bind": "/containerfiles/", "mode": "rw"}},
                    remove=True
                )

            else:
                return HttpResponse("Alignment Tool nicht unterstützt.", status=400)
        except docker.errors.ContainerError as e:
            return HttpResponse(f"Container-Fehler: {e}", status=500)
        except Exception as e:
            return HttpResponse(f"Ein unerwarteter Fehler ist aufgetreten: {e}", status=500)

        output_file = os.path.join(container_path, "output.html")
        with open(output_file, "r") as file:
            content = file.read()
            return HttpResponse(content, content_type="text/html")

    return render(request, "msa3A.html")


def validate_fasta(file_path):
    try:
        with open(file_path, "r") as handle:
            records = list(SeqIO.parse(handle, "fasta"))
            if len(records) < 2:
                return False, "Die Datei enthält weniger als zwei Sequenzen."
            for record in records:
                if len(record.seq) == 0:
                    return False, f"Sequenz {record.id} ist leer."
        return True, "Eingabedatei ist gültig."
    except Exception as e:
        return False, f"Fehler bei der Überprüfung: {str(e)}"


def Phylogenetischer_Baum(request):
    if request.method == "POST":
        sequences: str = request.POST.get("sequences")
        if not sequences:
            return HttpResponse("Fehler: Keine Sequenzen eingegeben.", status=400)
        sequences.replace("\r", "").replace(" ", "").replace("\n", "")
        container_path = os.path.join(os.getcwd(), "containerfiles")
        os.makedirs(container_path, exist_ok=True)
        input_file = os.path.join(container_path, "input.fasta")

        with open(input_file, "w") as file:
            file.write(sequences)

        valid, message = validate_fasta(input_file)
        if not valid:
            return HttpResponse(f"Fehler bei der Eingabedatei: {message}", status=400)

        client = docker.from_env()
        try:
            for file in os.listdir(container_path):
                if file.startswith("RAxML_"):
                    os.remove(os.path.join(container_path, file))

            client.containers.run(
                image="biocontainers/raxml:v8.2.12dfsg-1-deb_cv1",
                command="raxmlHPC -m GTRGAMMA -p 12345 -s /containerfiles/input.fasta -n output -w /containerfiles",
                volumes={container_path: {"bind": "/containerfiles", "mode": "rw"}},
                remove=True
            )

            tree_file = os.path.join(container_path, "RAxML_bestTree.output")
            if not os.path.exists(tree_file):
                return HttpResponse("Fehler: Die Ausgabedatei wurde nicht erstellt.", status=500)

            tree = Phylo.read(tree_file, "newick")
            output_image = os.path.join(container_path, "phylo_tree.png")
            Phylo.draw(tree, do_show=False)
            plt.savefig(output_image)
            plt.close()
            with open(output_image, "rb") as img_file:
                return HttpResponse(img_file.read(), content_type="image/png")

        except docker.errors.ContainerError as e:
            error_message = e.stderr.decode("utf-8") if e.stderr else str(e)
            return HttpResponse(f"Container-Fehler: {error_message}", status=500)
        except Exception as e:
            return HttpResponse(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}", status=500)
    return render(request, "Phylogenetischer Baum.html")
