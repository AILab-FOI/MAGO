from bowldi import BOWLDIConverter

converter = BOWLDIConverter(
    input_data_path="converted.asl",
    output_data_path="ontology.owl"
)

print(converter.get_response())