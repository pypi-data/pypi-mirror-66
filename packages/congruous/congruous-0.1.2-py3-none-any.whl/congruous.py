import click
import csv
from fuzzywuzzy import fuzz, process
from os import path
from app.database import create_connection, seed_database, get_history
from app.database import describe_records, setup_tables, get_hcd_seed
from app.reports import match_records
from app.common import utils


@click.group()
@click.version_option()
def cli():
    # Initialize sqlite3 connection
    create_connection()
    pass


@click.command()
@click.argument('document')
@click.option('--head', is_flag=True, default=False, help='prints the first 5 records of store')
@click.option('--tail', is_flag=True, default=False, help='prints the last 5 records of store')
@click.option('--count', is_flag=True, default=False, help='prints the number of records in store')
@click.option('--seed', help='pass the file(.csv) to seed the store')
@click.option('--drop', is_flag=True, default=False, help='removes all the records from the store')
def store(document, head, tail, count, seed, drop):

    # validate whether the passed argument is supported type
    if not utils.validate_supported_document(document):
        return

    # seed the file contents to the database based on the document type
    if seed != None and utils.validate_file(seed):
        setup_tables(document)
        file_contents = utils.read_file_contents(seed)
        seed_database(document, file_contents)
        return

    operation = 'head' if head else (
        'tail' if tail else ('count' if count else ('drop' if drop else None)))

    if operation is not None:
        describe_records(document, operation)
    elif operation == 'drop':
        setup_tables(document, True)
    return


@click.command()
@click.argument('document')
@click.option('--fields',  multiple=True, help='matches the mentioned fields alone')
@click.option('--ocrd', help='data(.csv) to be matched with raw human curated data')
@click.option('--hcd', help='data(.csv) Human Curated correct data fields to be matched against')
@click.option('--report', is_flag=True, default=False, help='Generates a report for the test run')
def match(document, fields, hcd, ocrd, report):

    # validate whether the passed argument is supported type
    if not utils.validate_supported_document(document):
        return

    if hcd == None:
        click.secho(
            'congruous : hcd not given , using default store records for comparison', fg='yellow')
        hcd_records = get_hcd_seed(document)
    else:
        hcd_records = utils.read_file_contents(
            hcd) if utils.validate_file(hcd) else None

    if ocrd == None:
        click.secho(
            'congruous : ocrd missing , aborting!, ocr parsed file to be matched must be given', fg='red')
        return

    ocrd_records = utils.read_file_contents(
        ocrd) if utils.validate_file(ocrd) else None

    if len(hcd_records) != len(ocrd_records) and len(ocrd_records) <= 0:
        click.secho(
            'congruous : mismatch number of records in hcd and ocrd ', fg='red')
        click.secho(
            'congruous : hcd ' + str(len(hcd_records)) + ' ocrd ' + str(len(hcd_records)), fg='red')
        return

    cong_report = match_records(document, ocrd.split(
        '/')[-1], hcd_records, ocrd_records)

    click.secho('congruous : unable to generate reports at the moment. aborting !',
                fg='yellow') if report else None
    # generate_match_report(document, file_name, cong_reporget_historyt) if report else None

    return


@click.command()
@click.argument('document')
@click.option('--history', is_flag=True, default=False, help='show 10 recent congruous runs')
def report(document, history):

    # validate whether the passed argument is supported type
    if not utils.validate_supported_document(document):
        return

    get_history(document) if history else None
    return


cli.add_command(store)
cli.add_command(match)
cli.add_command(report)


if __name__ == '__main__':
    cli()
