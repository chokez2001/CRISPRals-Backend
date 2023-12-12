import json
import re
import os
import uuid
from Bio.Blast.Applications import NcbiblastnCommandline
import subprocess
import csv
from multiprocessing import Pool, Manager
import zipfile
import base64
import shutil



def analyze_sequence(sequence, database_path, database_path2, analysis_type, results, zip_files, cas_summary, spacers):
    unique_filename = str(uuid.uuid4())
    last_sequence_file_path = f"last_sequence_{unique_filename}"
    zip_filename = None  
    count = 0

    # Save the last sequence in a file

    with open(last_sequence_file_path, "w") as last_sequence_file:
        fasta_lines = sequence.split('\n')

        for line in fasta_lines:
            if line.startswith('>'):
                count += 1

        qseqid_original = fasta_lines[0][1:].strip()

        last_sequence_file.write(sequence)
        
        print("fragments:", count)

    # Run the analysis
    # Sequevar determination

    if analysis_type == 'Sequevar determination':

        blast_cline = NcbiblastnCommandline(
            query=last_sequence_file_path,
            db=database_path,
            outfmt="6",
        )
        stdout, stderr = blast_cline()
        blast_output_lines = stdout.strip().split('\n')

        empty = True
        best_row = None
        pident = 0.0
        best_pident = 0.0

        # Get the best result

        for blast_output_line in blast_output_lines:
            blast_values = blast_output_line.split('\t')

            if len(blast_values) == 12:
                qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = blast_values
                pident = float(pident)
                empty = False

            if pident >= 99.5 and pident > best_pident and not empty:
                best_row = {
                    'Sequence': qseqid_original,
                    'Sequevar': sseqid.replace("-", " "),
                    'Length': int(length),
                    'Similarity': float(pident),          
                    'Mismatch': int(mismatch),
                    'Start alignment': int(qstart),
                    'End alignment': int(qend),
                }
                best_pident = pident
                continue

            if (best_pident == 100 and pident == 100 and not empty):
                also = {
                    'Sequence': qseqid_original,
                    'Sequevar': sseqid.replace("-", " "),
                    'Length': int(length),
                    'Similarity': float(pident),    
                    'Mismatch': int(mismatch),
                    'Start alignment': int(qstart),
                    'End alignment': int(qend),
                }
                results.append(json.dumps(also))

        # If there is no result

        if best_row is not None:
                results.insert(0, json.dumps(best_row))
        else:
            empty_row = {
                'Sequence': qseqid_original,
                'Sequevar': 'Not found',
                'Length':"-",
                'Similarity': "-",
                'Mismatch': "-",
                'Start alignment': "-",
                'End alignment': "-",
            }
            results.append(json.dumps(empty_row))

    # Phylotype determination

    elif analysis_type == 'Phylotype determination':

        blast_cline = NcbiblastnCommandline(
            query=last_sequence_file_path,
            db=database_path2,
            word_size=21,
            outfmt="6",
        )
        stdout, stderr = blast_cline()
        blast_output_lines = stdout.strip().split('\n')
        empty = True

        for blast_output_line in blast_output_lines:
            blast_values = blast_output_line.split('\t')

            if len(blast_values) == 12:
                qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = blast_values
                pident = float(pident)
                empty = False

            if empty == False and pident == 100:
                result = {
                    'Sequence': qseqid_original,
                    'Phylotype': sseqid.replace("-IV"," 4").replace("-III"," 3").replace("-II"," 2").replace("-I", " 1"),
                    'Start alignment': int(qstart),
                    'End alignment': int(qend),
                }
                results.append(json.dumps(result))

            # If there is no result

            else:
                empty_row = {
                    'Sequence': qseqid_original,
                    'Phylotype': 'Not found',
                    'Start alignment': "-",
                    'End alignment': "-",
                }
                results.append(json.dumps(empty_row))

    # CRISPRidentify analysis

    elif analysis_type == 'CRISPRidentify analysis':

        # Check if the sequence is too long

        if count > 100:
            to_long = {
                        'Summary': 'The analysis of this sequence would take a long time due to fragmentation. We suggest to run it locally.',
                    }
            results.append(json.dumps(to_long))

        # Run the analysis 

        else:
            bash_code = f"""
                #!/bin/sh
                cd ./CRISPRidentify
                condash="$HOME/miniconda3/etc/profile.d/conda.sh"
                . "$condash"
                conda activate crispr_identify_env
                python CRISPRidentify.py --file ../{last_sequence_file_path} --fast_run True --cas True  --result_folder "../crispr_identify_results/{qseqid_original}"
            """
            
            try:
                subprocess.run(bash_code, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

            except subprocess.CalledProcessError as e:
                print(f"Error with shell code: {e}")
        
            result_dir = f"./crispr_identify_results/{qseqid_original}"

            # Check which is the result folder

            if os.path.exists(os.path.join(result_dir, last_sequence_file_path)):
                print("last_sequence_file_path exists")
                result_dir = os.path.join(result_dir, last_sequence_file_path)

            # Sumary

            if os.path.exists(os.path.join(result_dir, "Complete_summary.csv")):
                print("Complete_summary.csv exists")
                with open(os.path.join(result_dir, "Complete_summary.csv"), mode='r', newline='') as csvfile:
                    lines = csvfile.readlines()
                    if len(lines) == 1 and lines[0].strip() == "No arrays found":
                        no_founds = {
                            'Sequence': qseqid_original,
                            'Summary': 'No arrays found',
                        }
                        print("no_founds")
                        results.append(json.dumps(no_founds))
                    else:
                        csv_reader = csv.DictReader(lines)
                        for row in csv_reader:
                            results.append(json.dumps({key: value for key, value in row.items()}))
            
            elif os.path.exists(os.path.join(result_dir, "Summary.csv")):   
                print("Summary.csv exists")
                with open(os.path.join(result_dir, "Summary.csv"), mode='r', newline='') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        results.append(json.dumps({key: value for key, value in row.items()}))
                    
            else:
                empty_row = {
                        'Sequence': qseqid_original,
                        'Summary': 'No summary available',
                    }
                results.append(json.dumps(empty_row))


             # Cas summary

            if os.path.exists(os.path.join(result_dir, "Complete_Cas_summary.csv")):
                with open(os.path.join(result_dir, "Complete_Cas_summary.csv"), mode='r', newline='') as csvfile:
                    lines = csvfile.readlines()
                    if len(lines) == 1 and lines[0].strip() == "No arrays found":
                        no_founds = {
                            'Sequence': qseqid_original,
                            'Summary': 'No cas summary found',
                        }
                        cas_summary.append(json.dumps(no_founds))
                    else:
                        csv_reader = csv.DictReader(lines)
                        for row in csv_reader:
                            cas_summary.append(json.dumps({key: value for key, value in row.items()}))

            elif os.path.exists(os.path.join(result_dir, "Cas_Summary.csv")):   
                with open(os.path.join(result_dir, "Cas_Summary.csv"), mode='r', newline='') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        cas_summary.append(json.dumps({key: value for key, value in row.items()}))

            # Phage spacers extracion

            for root, dirs, files in os.walk(result_dir):
                for file in files:
                    file_path = os.path.join(root, file)

                    if file == "Bona-Fide_Candidates.txt" or file == "Possible_Candidates.txt":
                        with open(file_path, mode='r', newline='') as csvfile:
                            in_crispr_section = False
                            for line in csvfile:
                                if line.startswith("CRISPR:") or line.startswith("Possible CRISPR:"):
                                    in_crispr_section = True
                                    print("in_crispr_section")

                                if line.startswith("______"):
                                    in_crispr_section = False

                                if in_crispr_section:
                                    match = re.search(r"([ACGT]{1,})( )*s:", line)

                                    if match:
                                        sequence = match.group(1)
                                        spacer = {'Spacer': sequence}
                                        spacers.append(json.dumps(spacer))
                                        print("spacer")
           
                                       
            # Zip the results
            
            zip_filename = f"results_{unique_filename}.zip"
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                for folderName, subfolders, filenames in os.walk(result_dir):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipf.write(filePath, os.path.relpath(filePath, result_dir))
                shutil.rmtree(f"./crispr_identify_results/{qseqid_original}") 
                            
            with open(zip_filename, "rb") as zip_file:
                zip_base64 = base64.b64encode(zip_file.read()).decode()
                zip_file = {
                        'Sequence': qseqid_original,
                        'Zip': zip_base64,
                    }
                zip_files.append(json.dumps(zip_file))
                
                os.remove(zip_filename)  

    os.remove(last_sequence_file_path)


# Function to search useless phages
def search_phages_for_sequence(sequence, phages, db_path):
    # Local environment variable
    os.environ["sequence_variable"] = sequence
    blast_command = f'echo "$sequence_variable" | blastn -db {db_path} -task blastn -outfmt 6'
    result = subprocess.run(blast_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    blast_output = result.stdout.strip().split('\n')
    print(blast_output)
  
    no_match = True
    for line in blast_output:
        fields = line.split('\t')
        phage_name = fields[1]
        pident = float(fields[2])
        mismatch = int(fields[4])
        if pident > 88.5 and mismatch < 5:
            phage = {
                'Spacer sequence': sequence,
                'Phage name': phage_name.replace("_", " "),  
                'Similarity': float(pident),
                'Mismatch': int(mismatch),   
            }
            no_match = False
            phages.append(json.dumps(phage))

    if no_match: 
        phage = {
            'Spacer sequence': sequence,
            'Phage name': 'Not found',
            'Similarity': '-',
            'Mismatch': '-',   
        }
        phages.append(json.dumps(phage))


    # comando para crear una base de datos con blast
    makeblastdb_cmd = f"makeblastdb -in {db_path} -dbtype nucl -out {db_path}"

def search_useless_phages(sequence_spacers):
    protospacers_phage_database_path = "dataDB/protospacers_phage_db/protospacers_phage_db"
     
    
    phages = Manager().list()
    with Pool() as pool:
        for sequence in sequence_spacers:  
            pool.apply_async(search_phages_for_sequence, args=(sequence, phages, protospacers_phage_database_path))
        pool.close()
        pool.join()
        print(phages)
    return {'uselessPhages': list(phages)}
   

# Main function to analyze a fasta file with a local database            

def analyze_fasta_with_local_db(fasta_contents, analysis_type):
    results = Manager().list()
    zip_files = Manager().list()
    cas_summary = Manager().list()
    spacers = Manager().list()
    sequevar_database_path = "dataDB/sequevars_db/sequevars_db"
    philotype_database_path = "dataDB/phylotypes_db/phylotypes_db"

    with Pool() as pool:
        for sequence in fasta_contents:
            pool.apply_async(analyze_sequence, args=(sequence, sequevar_database_path, philotype_database_path, analysis_type, results, zip_files, cas_summary, spacers))
        print(spacers)
        pool.close()
        pool.join()
    return {
        'fastaAnalisis': list(results), 
        'zipFiles': list(zip_files),
        'casSummary': list(cas_summary),    
        'spacers': list(spacers),
    }