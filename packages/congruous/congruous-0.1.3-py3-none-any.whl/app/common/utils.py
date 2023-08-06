from tabulate import tabulate
from os import path
import csv
import click


def validate_file(input_file):

    # check for valid number of records in the file with headers
    if path.exists(input_file):
        file_ext = input_file[-3:]
        if file_ext == "csv":
            return True
        # return {'is_valid': False, 'message': 'Unsupported file format : ' + str(input_file.split('.')[-1])}
        return False
    else:
        # return {'is_valid': False, 'message': 'File does not exist :' + str(input_file)}
        return False


def read_file_contents(input_file):
    with open(input_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        file_contents = [row for row in reader]
        return file_contents


def pretty_print_table(records, column_names):

    table = [list(row) for row in records]
    click.secho(tabulate(table, column_names, tablefmt="pretty"))
    return


def validate_supported_document(document):

    supported_documents = ['pan']

    # validate whether the passed argument is supported type
    if document not in supported_documents:
        click.secho('congruous: unsupported document-id type: ' +
                    document, err=True, fg='red')
        return False
    return True


# # Suggest the correct document for the wrongly typed document

# def suggest_document_type(document):
#     click.echo("congruous: unsupported document type: {}".format(document))
#     supported_docs = ['pan', 'aadhar', 'driving_license', 'voter_id']
#     probables = process.extract(document, supported_docs, limit=2)
#     click.echo("Did you mean: \n")
#     for doc in probables:
#         click.echo("\t {}".format(doc[0]))
