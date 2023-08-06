"""Callback code."""

import base64
import json
import os
import tempfile

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from logzero import logger
import pandas as pd

from ..conversion import convert_seqs
from ..export import write_excel
from ..workflow import blast_and_haplotype_many, results_to_data_frames
from ..phylo import phylo_analysis
from .settings import FILE_NAME_TO_SAMPLE_NAME, SAMPLE_REGEX

from . import ui


def register_upload(app):
    @app.callback(
        Output("hidden-data", "children"),
        [Input("upload-data", "contents")],
        [State("hidden-data", "children"), State("upload-data", "filename")],
    )
    def data_uploaded(list_of_contents, hidden_data, list_of_names):
        if list_of_contents:
            with tempfile.TemporaryDirectory() as tmpdir:
                paths_reads = []
                for content, name in zip(list_of_contents, list_of_names):
                    paths_reads.append(os.path.join(tmpdir, name))
                    with open(paths_reads[-1], "wb") as tmp_file:
                        logger.info("Writing to %s", paths_reads[-1])
                        _, content = content.split(",", 1)
                        tmp_file.write(base64.b64decode(content))
                seq_files = convert_seqs(paths_reads, tmpdir, FILE_NAME_TO_SAMPLE_NAME)
                results = blast_and_haplotype_many(seq_files)
                df_summary, df_blast, df_haplotyping = results_to_data_frames(results, SAMPLE_REGEX)

                row_select = (df_summary.orig_sequence != "-") & (df_summary.region != "-")
                columns = ["query", "region", "orig_sequence"]
                phylo_result = phylo_analysis(df_summary[row_select][columns])
            return json.dumps(
                {
                    "summary": df_summary.to_dict(),
                    "blast": df_blast.to_dict(),
                    "haplotyping": df_haplotyping.to_dict(),
                    "phylo": phylo_result,
                }
            )


def load_hidden_data(hidden_data):
    raw_data = json.loads(hidden_data)

    def decode(data, key):
        if key in ("summary", "blast", "haplotyping"):
            return pd.DataFrame.from_dict(data)
        else:
            return data

    return {key: decode(raw_data[key], key) for key in raw_data}


def register_computation_complete(app):
    @app.callback(Output("page-content", "children"), [Input("hidden-data", "children")])
    def computation_complete(hidden_data):
        if not hidden_data:
            return ui.render_page_content_empty_children()
        else:
            data = load_hidden_data(hidden_data)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            mime = "application/octet-stream"
            with tempfile.NamedTemporaryFile() as tmpf:
                # df_summary, df_blast, df_haplotyping, path):
                write_excel(data["summary"], data["blast"], data["haplotyping"], tmpf.name)
                tmpf.seek(0)
                xlsx = base64.b64encode(tmpf.read()).decode("utf-8")
            return [
                html.P(
                    children=[
                        html.A(
                            children=[
                                html.I(className="fas fa-file-excel ml-2 mr-2"),
                                "Download XLSX",
                            ],
                            # href="data:text/html,<script>alert('hi');</script>",
                            download="hlso_result.xlsx",
                            target="_blank",
                            href="data:%s;base64,%s" % (mime, xlsx),
                        )
                    ]
                ),
                dbc.Tabs(
                    children=[
                        dbc.Tab(ui.render_tab_summary(data), label="Summary", id="tab-summary"),
                        dbc.Tab(ui.render_tab_blast(data), label="BLAST", id="tab-blast"),
                        dbc.Tab(
                            ui.render_tab_haplotyping(data),
                            label="Haplotyping",
                            id="tab-haplotyping",
                        ),
                        dbc.Tab(
                            ui.render_tab_dendrograms(data),
                            label="Dendrograms",
                            id="tab-dendgrograms",
                        ),
                    ]
                ),
            ]


def register_row_clicks(app):
    @app.callback(
        Output("blast-current-match", "children"),
        [Input("hidden-data", "children"), Input("blast-table", "selected_row_ids")],
    )
    def update_haplotype_match(hidden_data, selected_row_ids):
        # logger.info("Selected %s from %s", selected_row_ids, hidden_data)
        if selected_row_ids and hidden_data:
            selected_row_ids = list(map(str, selected_row_ids))[0]
            data = load_hidden_data(hidden_data)
            df_blast = data["blast"]
            alignment = df_blast.loc[selected_row_ids].alignment
            ncbi_tpl = "%s?DATABASE=nt&PROGRAM=blastn&MEGABLAST=on&QUERY=>%s%%0A%s"
            ncbi_url = ncbi_tpl % (
                "https://blast.ncbi.nlm.nih.gov/Blast.cgi",
                df_blast.loc[selected_row_ids]["query"],
                df_blast.loc[selected_row_ids].orig_sequence,
            )
            return [
                html.P(
                    children=[
                        html.Div(
                            children=[
                                html.A(
                                    children=[
                                        html.I(className="fas fa-external-link-alt"),
                                        " RunNCBI BLAST for this sequence",
                                    ],
                                    href=ncbi_url,
                                )
                            ],
                            className="mt-3",
                        )
                    ]
                ),
                dcc.Markdown("```text\n%s\n```" % alignment, className="mt-3"),
            ]
        return [html.P(["no match selected yet"])]
