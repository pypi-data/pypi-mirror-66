import pandas as pd
import os


_local_dir = os.path.dirname(__file__)
_file_path = '/'.join([_local_dir, 'amino_acid_data.csv'])

schemas = pd.read_csv(_file_path)


def get_schema(schema):
    sub_df = schemas[['amino_acid', schema]].copy()
    sub_df.rename(columns={schema: 'value'}, inplace=True)
    return sub_df


def list_schema_names():
    names = list()
    for col in schemas.columns:
        if col not in ['amino_acid']:
            names.append(col)
    return names
