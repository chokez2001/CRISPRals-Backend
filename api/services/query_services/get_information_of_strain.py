from api.db_models import db, RalstoniaTbl, CrisprTbl, PhagesTbl
from api.utils.operations import format_repeat_sequences


def get_information_by_assembly(assembly):
    ralstonia_information = RalstoniaTbl.query.get(assembly).to_dict()
    phages_in_crispr = db.session.query(PhagesTbl.phage_name).join(
        CrisprTbl
    ).filter(
        CrisprTbl.assembly_fk == assembly
    ).all()
    phages_in_crispr = [name[0] for name in phages_in_crispr]
    potential_phages = db.session.query(PhagesTbl.phage_name).join(
        CrisprTbl
    ).filter(
        CrisprTbl.assembly_fk != assembly
    ).group_by(PhagesTbl.phage_name).all()
    potential_phages = [{"phageName": name[0]} for name in potential_phages]

    return {
        'strain': ralstonia_information['strain'],
        'assembly': ralstonia_information['assembly'],
        'accessionNumberRf': ralstonia_information['accession_number_rf'] or '-',
        'accessionNumberGenBank': ralstonia_information['accession_number_genbank'] or '-',
        'specie': ralstonia_information['specie'],
        'phylotype': ralstonia_information['phylotype'] or '-',
        'consensusRepeatSequences': format_repeat_sequences(ralstonia_information['consensus']),
        'phagesInCrisprArray': phages_in_crispr,
        'availablePhages': len(potential_phages),
        'lengthCrisprArray': ralstonia_information['number_of_crispr_arrays'] or 0,
        'listPotentialPhages': potential_phages,
        'isCrispr':ralstonia_information['crispr_array'],
        'crisprType': ralstonia_information['type_of_crispr'] or '-',
        'observation':ralstonia_information['observation'] or '-',
        'scoreCrisprIdentify': ralstonia_information['score_crispr_identify'] or '-'   
    }
