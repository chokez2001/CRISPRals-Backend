from api.services.query_services.get_information_of_strain import get_information_by_assembly
from api.services.query_services.get_statistics import *
from api.services.query_services.get_table_data import get_table_data
from api.services.query_services.laboratory_local import analyze_fasta_with_local_db
from api.services.query_services.laboratory_local import search_useless_phages


def get_statistics_resolver(obj, info):
    return get_all_statistics()


def laboratory_analysis_resolver(obj, info, fastaContent, analysisType):
    return analyze_fasta_with_local_db(fastaContent, analysisType)

def get_useless_phages(obj, info, spacers):
    return search_useless_phages(spacers)

def get_infromation_by_assembly_resolver(obj, info, assembly):
    return get_information_by_assembly(assembly)


def get_table_data_resolver(obj, info, currentPage, pageSize,specie, crisprStatus, strainNameOrAssembly):
    return get_table_data(currentPage, pageSize, specie, crisprStatus, strainNameOrAssembly)

