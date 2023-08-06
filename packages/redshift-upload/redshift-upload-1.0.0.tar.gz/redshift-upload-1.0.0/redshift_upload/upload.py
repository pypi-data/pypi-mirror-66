import csv
import io
import boto3
import gzip
from typing import Iterable, List, Any, Dict, Tuple
from uuid import uuid4
from .queries import *

PrimaryKeyInfo = Tuple[Tuple[int, str]]

s3 = boto3.client("s3")


class RedshiftUpload(object):
    def __init__(self, connection, s3_bucket: str, region: str, prefix: str):
        self.connection = connection
        self.s3_bucket = s3_bucket
        self.prefix = prefix
        self.region = region

    def upload(self, table_name: str, schema: str, primary_key: PrimaryKeyInfo,
               rows: Iterable[Dict[Any, Any]],
               replace: bool,
               iam_role: str):
        table = RedshiftTable(self.connection, primary_key, table_name, schema)
        rows = RedshiftUpload.filter_rows(table, rows, replace)
        fieldnames = [k for k in rows[0]] if rows else []
        key = self.upload_rows(table, fieldnames, rows)
        # note: important to delete existing BEFOREHAND
        if replace:
            table.drop_existing(rows)
        self.copy_rows(table, fieldnames, key, iam_role)
        self.connection.commit()

    @staticmethod
    def filter_rows(table, rows, replace):
        rows = table.unique(rows)
        if replace:
            return rows
        return table.non_existing(rows)

    def upload_rows(self, table, fieldnames, rows):
        upload_id = uuid4()
        output = io.StringIO()
        w = csv.DictWriter(output, fieldnames=fieldnames, delimiter='|')
        w.writerows(rows)
        gzipped = gzip.compress(bytes(output.getvalue(), encoding='utf-8'))
        output.close()
        gz_filepath = f"{upload_id}.csv.gz"
        key = '/'.join(tuple([self.prefix, table.table_name, gz_filepath]))
        s3.put_object(Key=key, Bucket=self.s3_bucket, Body=gzipped)
        return key

    def copy_rows(self, table, fieldnames, key, iam_role):
        s3_path = '/'.join(tuple([self.s3_bucket, key]))
        path = f"s3://{s3_path}"
        cur = self.connection.cursor()
        cur.execute(
            copy_csv_data(table_name=table.table_name, fieldnames=fieldnames,
                          schema=table.schema),
            dict(resource_path=path,
                 iam_role=iam_role,
                 region=self.region))


class RedshiftTable:
    def __init__(self, connection, primary_key: PrimaryKeyInfo,
                 table_name, schema):
        self.connection = connection
        self.table_name = table_name
        self.primary_key_column_positions = list(map(lambda key: key[0],
                                                     primary_key))
        self.primary_key_column_names = list(
            map(lambda key: key[1], primary_key))
        self.schema = schema

    def existing_primary_keys(self):
        cur = self.connection.cursor()
        q = find_distinct_column_permutations(self.table_name,
                                              self.schema,
                                              *self.primary_key_column_names)
        cur.execute(q)
        rows = cur.fetchall()
        return [self.primary_key(row) for row in rows]

    def primary_key(self, row):
        return tuple([row[k] for k in self.primary_key_column_names])

    def unique(self, rows: Iterable[List[Any]]):
        results = []
        keys = set([])
        for row in rows:
            key = self.primary_key(row)
            if key in keys:
                continue
            keys.add(key)
            results.append(row)
        return results

    def non_existing(self, rows: Iterable[List[Any]]):
        existing_keys = set(self.existing_primary_keys())
        if not len(existing_keys):
            return rows
        return list(
            filter(lambda row: self.primary_key(row) not in existing_keys,
                   rows))

    def existing_keys(self, rows: Iterable[List[Any]]):
        existing_keys = set(self.existing_primary_keys())
        keys = {self.primary_key(row) for row in rows}
        return keys.intersection(existing_keys)

    def drop_existing(self, rows: Iterable[List[Any]]):
        existing = self.existing_keys(rows)
        if not existing:
            return
        q = drop_primary_keys_in(self.table_name, self.schema, existing,
                                 self.primary_key_column_names)
        cur = self.connection.cursor()
        cur.execute(q)
