from api.db_models import db, RalstoniaTbl, CrisprTbl, PhagesTbl
from api.utils.operations import get_percentage
from typing import List, Dict



def get_summary_data():
    total_strain = db.session.query(db.func.count()).select_from(RalstoniaTbl).scalar()
    total_phage = db.session.query(db.func.count()).select_from(PhagesTbl).scalar()
    total_crispr_array = db.session.query(db.func.count()).select_from(CrisprTbl).scalar()
    total_accessio_number = db.session.query(
        db.func.count(RalstoniaTbl.accession_number_rf) + db.func.count(RalstoniaTbl.accession_number_genbank)).scalar()
    return {
        'strain': {
            'total': total_strain
        },
        'phage': {
            'total': total_phage
        },
        'crisprArray': {
            'total': total_crispr_array
        },
        'accessionNumber': {
            'total': total_accessio_number
        }
    }


def get_summary_strain(strains) -> List[Dict]:  
    strains_with_crispr = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(crispr_array=True).scalar()

    strains_with_no_crispr = strains['total'] - strains_with_crispr

    total = strains['total']

    percent_with_crispr = get_percentage(strains_with_crispr, total)
    percent_without_crispr = get_percentage(strains_with_no_crispr, total)

    total_solanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Solanacearum').scalar()
    total_seudosolanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Pseudosolanacearum').scalar()
    total_syzygii = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Syzygii').scalar()

    strains_with_solanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Solanacearum', crispr_array=True).scalar()
    strains_with_seudosolanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Pseudosolanacearum', crispr_array=True).scalar()
    strains_with_syzygii = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Syzygii', crispr_array=True).scalar()

    strains_without_solanacearum = total_solanacearum - strains_with_solanacearum
    strains_without_seudosolanacearum = total_seudosolanacearum - strains_with_seudosolanacearum
    strains_without_syzygii = total_syzygii - strains_with_syzygii

    return [
        {
            'label': 'R. solanacearum',
            'withCrispr': strains_with_solanacearum,
            'withoutCrispr': strains_without_solanacearum,
            'total': total_solanacearum,
            'percentWith': percent_with_crispr,
            'percentWithout': percent_without_crispr
        },
        {
            'label': 'R. pseudosolanacearum',
            'withCrispr': strains_with_seudosolanacearum,
            'withoutCrispr': strains_without_seudosolanacearum,
            'total': total_seudosolanacearum,
            'percentWith': get_percentage(strains_with_seudosolanacearum, total_seudosolanacearum),
            'percentWithout': get_percentage(strains_without_seudosolanacearum, total_seudosolanacearum)
        },
        {
            'label': 'R. syzygii',
            'withCrispr': strains_with_syzygii,
            'withoutCrispr': strains_without_syzygii,
            'total': total_syzygii,
            'percentWith': get_percentage(strains_with_syzygii, total_syzygii),
            'percentWithout': get_percentage(strains_without_syzygii, total_syzygii)
        }
    ]




def get_series_data(strains):
    total_solanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Solanacearum').scalar()
    total_seudosolanacearum = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Pseudosolanacearum').scalar()
    total_syzygii = db.session.query(
        db.func.count()).select_from(RalstoniaTbl) \
        .filter_by(specie='Syzygii').scalar()

    return [
        {
            'label': 'R. solanacearum',
            'value': total_solanacearum,
            'percent': get_percentage(total_solanacearum, strains['total']),
        },
        {
            'label': 'R. pseudosolanacearum',
            'value': total_seudosolanacearum,
            'percent': get_percentage(total_seudosolanacearum, strains['total']),
        },
        {
            'label': 'R. syzygii',
            'value': total_syzygii,
            'percent': get_percentage(total_syzygii, strains['total']),
        }
    ]


def get_all_statistics():
    summary_data = get_summary_data()
    summary_strain = get_summary_strain(summary_data['strain'])
    series_data = get_series_data(summary_data['strain'])
    return {
        'summaryData': summary_data,
        'summaryStrain': summary_strain,
        'seriesData': series_data
    }
