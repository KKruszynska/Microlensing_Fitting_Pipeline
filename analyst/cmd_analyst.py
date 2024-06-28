import numpy as np
import pandas as pd
from astroquery.gaia import Gaia

from plotly import graph_objs as go

import os

class CmdAnalyst:
    '''
    analyst handling a single CMD.
    '''
    def __init__(self,
                 path_outputs,
                 event_name,
                 ra, dec,
                 catalogue_name,
                 light_curve_data,
                 optional=None,
                 radius = 30. / 60.,
                 file_path=None):

        self.path_outputs = path_outputs
        self.event_name = event_name
        self.ra = ra
        self.dec = dec
        self.catalogue_name = catalogue_name
        self.light_curve_data = light_curve_data
        self.radius = radius
        self.optional_kwargs = optional
        self.catalogue_file_path = file_path
        # Optional kwargs can include for example parallax_quality parameter for Gaia CMDs

    def transform_source_data(self):
        if "Gaia" in self.catalogue_name:
            data, labels = self.transform_source_gaia_data()

        return data, labels

    def transform_source_gaia_data(self):
        '''
        Transforms a dictionary passed by the user to dataframe holding information from the light curve.
        :return: returns a pandas dataframe with rows of object and its magnitudes in passed filters
        '''

        try:
            d = []
            l = []
            for key in self.light_curve_data:
                row = [key]
                for inner_key in self.light_curve_data[key]:
                    row.append(self.light_curve_data[key][inner_key])
                    l.append(inner_key)
                d.append(row)

            labels = l[:len(d[0][:]) - 1]
            cols = ['object']
            for l in labels:
                cols.append(l)
            data = pd.DataFrame(d, columns=cols)

        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))
            data = None
            labels = None

        return data, labels

    def load_catalogue_data(self):
        '''
        Based on the catalogue name, select sources within radius.
        :return: array with data to create a cmd plus labels
        '''

        if self.catalogue_file_path is not None:
            if (self.optional_kwargs != None and "separator" in self.optional_kwargs):
                data, labels = self.load_catalogue_from_file_data(separator=self.optional_kwargs["separator"])
            else:
                data, labels = self.load_catalogue_from_file_data()
        else:
            if "Gaia" in self.catalogue_name:
                if (self.optional_kwargs != None and "parallax_quality" in self.optional_kwargs):
                    data, labels = self.load_gaia_data(parallax_quality=self.optional_kwargs["parallax_quality"])
                else:
                    data, labels = self.load_gaia_data()


        return data, labels

    def load_gaia_data(self, parallax_quality=5):
        table_name = ""
        if "DR3" in self.catalogue_name:
            table_name = "gaiadr3"
        if "DR2" in self.catalogue_name:
            table_name = "gaiadr2"
        if "DR1" in self.catalogue_name:
            table_name = "gaiadr1"

        try:
            if "DR3" in self.catalogue_name:
                adql_query = ("SELECT source_id, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag \
                                     FROM %s.gaia_source \
                                     WHERE parallax_over_error > %d AND \
                                     ruwe < 1.4 AND \
                                     CONTAINS(POINT(ra, dec), CIRCLE(%f, %f, %f))=1;" %
                              (table_name, int(parallax_quality), self.ra, self.dec, self.radius))
            else:
                adql_query = ("SELECT source_id, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag \
                             FROM %s.gaia_source \
                             WHERE parallax_over_error > %d \
                             CONTAINS(POINT(ra, dec), CIRCLE(%f, %f, %f))=1;"%
                              (table_name, int(parallax_quality), self.ra, self.dec, self.radius))

            tables = Gaia.load_tables(only_names=True)
            job = Gaia.launch_job_async(adql_query)
            result = job.get_results()

            data = {"Gaia_G" : result["phot_g_mean_mag"],
                    "Gaia_BP" : result["phot_bp_mean_mag"],
                    "Gaia_RP" : result["phot_rp_mean_mag"]
                    }
            data_frame = pd.DataFrame(data=data)
            labels = ["Gaia_G", "Gaia_BP", "Gaia_RP"]

        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))
            data_frame = None
            labels = None

        return data_frame, labels

    def load_catalogue_from_file_data(self, separator=","):
        '''
        Load a file with information needed for a CMD
        :return: data and labels of the CMD background
        '''

        data = pd.read_csv(self.catalogue_file_path, sep=separator)
        labels = data.columns.tolist()

        return data, labels


    def plot_cmd(self, source_data, source_labels, cmd_data, cmd_labels):
        '''
        Create a CMD.
        :param source_data: pandas dataframe with light curve information
        :param source_labels: labels of filters in the source_data
        :param cmd_data: pandas dataframe with cmd background information from survey
        :param cmd_labels: labels of filters in the cmd_data
        :return: status of creating a cmd plot
        '''

        if "Gaia" in self.catalogue_name:
            cmd_plot_status = self.plot_gaia_cmd(source_data, source_labels, cmd_data, cmd_labels)

        return cmd_plot_status

    def plot_gaia_cmd(self, source_data, source_labels, cmd_data, cmd_labels):
        '''
        Plot a Gaia CMD.
        :param source_data: data frame with Gaia data
        :param source_labels: labels of filters in the source_data
        :param cmd_data: pandas dataframe with cmd background information from Gaia
        :param cmd_labels: labels of filters in the cmd_data
        :return: status of creating a cmd plot
        '''


        for i in range(len(cmd_labels)):

            colours = {"baseline": "#000000", # black
                       "source": "#E69F00", # orange
                       "blend": "#56B4E9", #sky blue
                       "bluish_green": "#009E73", #blueish green
                       "yellow" : "#F0E442", # yellow
                       "blue": "#0072B2", # blue
                       "vermillon": "D55E00", # vermillon
                       "reddish_purple": "#CC79A7"} # reddish_purple Wong colour palette, https://www.nature.com/articles/nmeth.1618
            try:
                fig = go.Figure()

                fig.add_trace(go.Scatter(x=cmd_data[cmd_labels[1]] - cmd_data[cmd_labels[2]],
                                         y=cmd_data[cmd_labels[i]],
                                         mode="markers",
                                         marker=dict(
                                             color="grey",
                                             size=5,
                                             opacity=0.5, ),
                                         name=self.catalogue_name,
                                         showlegend=True
                                         ), )

                for j in range(len(source_data['object'].values[:])):
                    fig.add_trace(go.Scatter(x=[source_data[cmd_labels[1]].iloc[j] - source_data[cmd_labels[2]].iloc[j]],
                                             y=[source_data[cmd_labels[i]].iloc[j]],
                                             mode="markers",
                                             marker=dict(
                                                 color=colours[source_data['object'].iloc[j]],
                                                 size=10,
                                                 ),
                                             name=source_data['object'].iloc[j],
                                             showlegend=True
                                             ), )

                fig.update_layout(
                    title="%s CMD" % self.event_name,
                    title_x=0.5,
                    xaxis_title="%s - %s" % (cmd_labels[1], cmd_labels[2]),
                    yaxis_title=cmd_labels[i],
                    legend_title="Legend",
                    font=dict(
                        family="arial",
                        size=18,
                        color="black"
                    ),
                    width=600,
                    height=600,
                    yaxis=dict(autorange="reversed"),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )

                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
                fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor="lightgray")

                os.makedirs(self.path_outputs, exist_ok=True)
                fig.write_html("%s/%s_CMD_%s.html"%(self.path_outputs, self.event_name, cmd_labels[i]))

                cmd_status = True

            except Exception as err:
                print(f"Unexpected %s, %s"%(err, type(err)))
                cmd_status = False

        return cmd_status





