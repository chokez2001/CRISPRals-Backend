import pandas as pd
from api.db_models import RalstoniaTbl, db, PhagesTbl, CrisprTbl
import os


def check_null(data):
    if pd.isnull(data):
        return None
    return data


def check_boolean(data):
    if pd.isnull(data) or (data != 'YES' and data != 'NO'):
        return None
    return data == 'YES'


def get_specie(phylotype: str, specie: str) -> str:
    if pd.isnull(phylotype):
        return specie
    if phylotype == '2A' or phylotype == '2B':
        return 'Solanacearum'
    if phylotype == '1' or phylotype == '3':
        return 'Pseudosolanacearum'
    if phylotype == '4':
        return 'Syzygii'
    return specie


def check_consensus_repeat_sequences(data):
    if pd.isnull(data):
        return [None, None]
    return data.split('-')


def update_database_ralstonia():
    rootDir = ''
    df = pd.read_csv(f'{rootDir}')
    data = df.to_dict('records')
    for new_elements in data:

        ralstonia_data = db.session.query(RalstoniaTbl).filter(
            RalstoniaTbl.assembly == new_elements['assembly']).first()
        consensus_repeat_sequences = check_consensus_repeat_sequences(new_elements['consensus_repeat_sequences'])
        if ralstonia_data is None:
            ralstonia_data = RalstoniaTbl(
                strain=new_elements['strain'],
                assembly=new_elements['assembly'],
                subtype='solanacearum',
                level=new_elements['level'],
                scaffold=None,
                consensus_repeat_sequences=consensus_repeat_sequences,
                phylotype=check_null(new_elements['phylotype']),
                accesion_number_rf=check_null(new_elements['accesion_number_rf']),
                accession_number_genbank=check_null(new_elements['accession_number_genbank'])
            )
            db.session.merge(ralstonia_data)
            db.session.commit()
            print(f"inserted {new_elements['assembly']} in RalstoniaTbl")
        else:
            ralstonia_data.consensus_repeat_sequences = consensus_repeat_sequences
            ralstonia_data.phylotype = check_null(new_elements['phylotype'])
            ralstonia_data.accesion_number_rf = check_null(new_elements['accesion_number_rf'])
            ralstonia_data.accession_number_genbank = check_null(new_elements['accession_number_genbank'])
            db.session.commit()
            print(f"updated {new_elements['assembly']} in RalstoniaTbl")


def crispr_phages_update(file_name: str):
    df = pd.read_csv(f'{os.getcwd()}/dataDB/{file_name}')
    data = df.to_dict('records')
    assembly_aux = ''
    for eachData in data:
        if not pd.isnull(eachData['Assembly']):
            assembly_aux = eachData['Assembly']
            print(f'inserting {assembly_aux}  in CRISRtbl')
        if eachData['Phages'] == 'Phages' or pd.isnull(eachData['Phages']) or pd.isnull(eachData['Score']):
            continue
        assembly_data = db.session.query(RalstoniaTbl).filter(RalstoniaTbl.assembly == assembly_aux).first()
        if assembly_data is None:
            print(f'Ignoring {assembly_aux}')
            print(f"Phage {eachData['Phages']} not considered")
            continue

        phage_data = db.session.query(PhagesTbl).filter(PhagesTbl.phage_name == eachData['Phages']).first()

        if phage_data is None:
            phage_data = PhagesTbl(
                phage_name=eachData['Phages'],
            )
            phage_data = db.session.merge(phage_data)
            db.session.commit()
            print(f"inserted {eachData['Phages']} in PhagesTbl")
        post = CrisprTbl(
            assembly_fk=assembly_aux,
            id_phage_fk=phage_data.id_phage,
            position_phage_genome=eachData['PositioninPhageGenome'],
            locus=eachData['Locus'],
            cluster_spacer=eachData['ClusterSpacer'],
            position_bacterial_genome=eachData['PositioninBacterialGenome'],
            spacer_rna=eachData['SpacerRNA'],
            protospacer_sequence=eachData['ProtospacerSequence'],
            score=eachData['Score']

        )
        db.session.add(post)
        db.session.commit()


def ralstonia_update(file_name: str, specie: str):
    df = pd.read_csv(f'{os.getcwd()}/dataDB/{file_name}')
    data = df.to_dict('records')
    print(f"Inserting {file_name} in tbl_ralstonia")
    for new_elements in data:
        ralstonia_data = RalstoniaTbl(
            strain=new_elements['Strain'],
            phylotype=check_null(new_elements['Phylotype']),
            specie=get_specie(new_elements['Phylotype'], specie),
            assembly=new_elements['Assembly'],
            level=new_elements['Level'],
            accession_number_rf=check_null(new_elements['RF']),
            accession_number_genbank=check_null(new_elements['GB']),
            wgs=check_null(new_elements['WGS']),
            scaffolds=check_null(new_elements['Scaffolds']),
            crispr_array=check_boolean(new_elements['CRISPRArray']),
            number_of_crispr_arrays=check_null(new_elements['NumberOfArrays']),
            consensus=check_null(new_elements['Consensus']),
            type_of_crispr=check_null(new_elements['TypeOfCRISPR']),
            observation=check_null(new_elements['Observation']),
            score_crispr_identify=check_null(new_elements['Score (CRISPRidentify)'])
        )
        db.session.merge(ralstonia_data)
    db.session.commit()


def insert_data_into_db():
    ralstonia_files = [
         {
            "file_name": "RalstoniaSolanacearum.csv",
            "specie": "Solanacearum"
        },
        {
            "file_name": "ralstoniaPseudosolanacearum.csv",
            "specie": "Pseudosolanacearum"
        },
        {
            "file_name": "ralstoniaSyzygii.csv",
            "specie": "Syzygii"
        }]
    for ralstonia_info in ralstonia_files:
        ralstonia_update(ralstonia_info["file_name"], ralstonia_info["specie"])

    cispr_files = ["CRISPRSyzygii.csv", "CRISPRPseudosolanacearum.csv", "CRISPRSolanacearum.csv"]
    for crispr_info in cispr_files:
        print(f"\t inserting {crispr_info} \n\n")
        crispr_phages_update(crispr_info)
