import numpy as np
import pandas as pd
from astroquery.gaia import Gaia

from astropy.coordinates.sky_coordinate import SkyCoord

from matplotlib import pyplot as plt

class CmdAnalyst:
    '''
    Analyst handling a single CMD.
    '''
    def __init__(self, ra, dec, catalogue_name, radius = 3. / 60., file_path=None):
        self.ra = ra
        self.dec = dec
        self.catalogue_name = catalogue_name
        self.radius = radius
    def load_catalogue_data(self):
        '''
        Based on the catalogue name, select sources within radius.
        :return: array with data to create a cmd plus labels
        '''

        if "Gaia" in self.catalogue_name:
            data, labels = self.load_gaia_data(self)

        return data, labels

    def load_gaia_data(self, parallax_quality=5):
        table_name = ""
        if "DR3" in self.catalogue_name:
            table_name = "gaiadr3"
        if "DR2" in self.catalogue_name:
            table_name = "gaiadr2"
        if "DR1" in self.catalogue_name:
            table_name = "gaiadr1"

        if "DR3" in sel.catalogue_name:
            adql_query = ("SELECT sourceid, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag \
                                 FROM %s.gaia_source \
                                 WHERE parallax_over_error > %d AND \
                                 ruwe < 1.4 AND \
                                 CONTAINS(POINT(ra, dec), CIRCLE(%f, %f, %f))=1;" %
                          (table_name, parallax_quality, self.ra, self.dec, self.radius))
        else:
            adql_query = ("SELECT sourceid, phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag \
                         FROM %s.gaia_source \
                         WHERE parallax_over_error > %d \
                         CONTAINS(POINT(ra, dec), CIRCLE(%f, %f, %f))=1;"%
                          (table_name, parallax_quality, self.ra, self.dec, self.radius))

        job = Gaia.launch_job_async(adql_query)
        result = job.get_results()

        data = {"Gaia_G" : result["phot_g_mean_mag"],
                "Gaia_BP" : result["phot_bp_mean_mag"],
                "Gaia_RP" : result["phot_rp_mean_mag"]
                }
        data_frame = pd.DataFrame(data=d)
        labels = "Gaia_G", "Gaia_BP", "Gaia_RP"

        return data_frame, labels

        return result[]