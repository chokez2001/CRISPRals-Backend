from api.db_models import db, RalstoniaTbl, CrisprTbl
from api.utils.operations import format_accession_number, format_repeat_sequences


def get_table_data(current_page, page_size, specie, crispr_status, strain_name_or_assembly):
    results = []
    filter_by_crispr_status = db.or_(RalstoniaTbl.crispr_array.is_(True), RalstoniaTbl.crispr_array.is_(False), RalstoniaTbl.crispr_array.is_(None))
    strain_name_or_assembly = strain_name_or_assembly.upper()

    if specie == 'ALL':
        specie = ''
    if 'WITH_CRISPR' in crispr_status and 'NO_CRISPR' not in crispr_status:
        filter_by_crispr_status = db.or_(
            RalstoniaTbl.crispr_array.is_(True),
            RalstoniaTbl.crispr_array.is_(None)
        )   
    if 'WITH_CRISPR' not in crispr_status and 'NO_CRISPR' in crispr_status:
         filter_by_crispr_status = db.or_(
            RalstoniaTbl.crispr_array.is_(False),
            RalstoniaTbl.crispr_array.is_(None)
        )   
    table_data_session = db.session.query(
        RalstoniaTbl.strain, RalstoniaTbl.assembly,
        RalstoniaTbl.accession_number_rf,
        RalstoniaTbl.accession_number_genbank,
        RalstoniaTbl.specie,
        RalstoniaTbl.phylotype,
        RalstoniaTbl.consensus,
        RalstoniaTbl.crispr_array,
        RalstoniaTbl.type_of_crispr,
    ).filter(
        RalstoniaTbl.specie.ilike(f"{specie}%"),
        db.or_(
            RalstoniaTbl.assembly.ilike(f"%{strain_name_or_assembly}%"),
            RalstoniaTbl.strain.ilike(f"%{strain_name_or_assembly}%")
        ),
        filter_by_crispr_status
    )
    total_count = table_data_session.count()
    total_pages = (total_count + page_size - 1) // page_size
    query_results = table_data_session.limit(page_size).offset((current_page - 1) * page_size).all()

    for qr in query_results:
        results.append({
            "strain": qr.strain,
            "assembly": qr.assembly,
            "accessionNumber": format_accession_number(qr.accession_number_rf, qr.accession_number_genbank),
            "specie": qr.specie,
            "phylotype": qr.phylotype or '-',
            "consensusRepeatSequences": format_repeat_sequences(qr.consensus),
            "crispr": qr.crispr_array,
            "crisprType": qr.type_of_crispr or '-',
        })
    return {
        'pagination': {
            'currentPage': current_page,
            'totalPages': total_pages

        },
        'rowsData': results
    }
