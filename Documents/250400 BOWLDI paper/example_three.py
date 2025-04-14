from bowldi import BOWLDIConverter

converter = BOWLDIConverter(
    input_data_path="onto_example.rdf",
    output_data_path="converted.asl"
)

converter.get_response()