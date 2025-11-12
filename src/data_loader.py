from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class ProcessOptions:
    template: str | None = None
    labels: Mapping[str, str] | None = None
    sep: str = ' '
    fillna: str = ''
    dropna_subset: Sequence[str] | None = None
    encoding: str = 'utf-8'


DEFAULT_OPTS = ProcessOptions()


class CSVDataLoader:
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(
        self, target_cols: Sequence[str], opts: ProcessOptions | None = None
    ) -> str:
        if opts is None:
            opts = DEFAULT_OPTS
        df = pd.read_csv(self.original_csv, opts.encoding, on_bad_lines='skip')

        if opts.dropna_subset:
            df = df.dropna(subset=opts.dropna_subset)

        missing = set(target_cols) - set(df.columns)
        if missing:
            raise ValueError('missing columns in CSV data')

        df[target_cols] = df[target_cols].fillna(opts.fillna).astype(str)

        if opts.template:
            # Fully custom format string, e.g. "Title: {Name} Overview: {synapsis} Genres: {Genres}"
            # Only pass the columns planning to use.
            df['combined'] = df[target_cols].apply(
                lambda row: opts.template.format(**row.to_dict()), axis=1
            )
        elif opts.labels:
            parts = []
            for col in target_cols:
                label = opts.labels.get(col, col)
                parts.append(label + ': ' + df[col])
            df['combined'] = pd.concat(parts, axis=1).agg(opts.sep.join, axis=1)
        else:
            df['combined'] = df[target_cols].agg(opts.sep.join, axis=1)

        df[['combined']].to_csv(self.processed_csv, index=False, encoding=opts.encoding)
        return self.processed_csv
