from ariadne import load_schema_from_path, make_executable_schema, ObjectType
from .queries import *

query = ObjectType("Query")
# mutation = ObjectType("Mutation")

query.set_field("getStatistics", get_statistics_resolver)
query.set_field("getTableData", get_table_data_resolver)
query.set_field("getInformationByAssembly", get_infromation_by_assembly_resolver)
query.set_field("laboratoryAnalysis", laboratory_analysis_resolver)
query.set_field("getUselessPhages", get_useless_phages)

# mutation.set_field("createPost", create_post_resolver)

type_defs = load_schema_from_path("api/graphql/schema.graphql")
schema = make_executable_schema(
    type_defs, query,  # mutation
)
