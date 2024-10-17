from time import sleep
import numpy as np

from MFPipeline.analyst.analyst import Analyst

class LightCurveAnalyst(Analyst):
    """
    This is a class that performs light curve
    It is a child of the :class:`MFPipeline.analyst.analyst.Analyst`
    It follows a flowchart specified here: link link link

    A Fit Analyst needs either a config_path or config_dict, otherwise it will not work.

    :param event_name: str, name of the analyzed event
    :param analyst_path: str, path to the folder where the outputs are saved
    :param light_curves: list, a list containing light curves, observatory name, and filter
    :param log: logger instance, log started by Event Analyst
    :param config_dict: dictionary, optional, dictionary with Event Analyst configuration
    :param config_path: str, optional, path to the YAML configuration file of the Event Analyst
    """
    def __init__(self,
                 event_name,
                 analyst_path,
                 light_curves,
                 log,
                 config_dict=None,
                 config_path=None):

        super().__init__(event_name, analyst_path, config_dict=config_dict, config_path=config_path)
        # Analyst.__init__(self, event_name, analyst_path, config_dict=config_dict, config_path=config_path)

        self.light_curves = light_curves
        self.log = log

        if (config_dict != None):
            self.add_lc_config(config_dict)
        elif("lc_analyst" in self.config):
            self.add_lc_config(self.config)
        else:
            self.log.error("LC Analyst: Error! Light Curve Analyst needs information.")
            quit()


    def add_lc_config(self, config):
        """
        Add LC configuration fields to analyst config.

        :param config_dict: dict, dictionary with analyst config
        """

        self.log.debug("LC Analyst: Reading lc config.")
        self.n_max = int(config["lc_analyst"]["n_max"])
        self.log.debug("LC Analyst: Finished reading lc config.")

    def perform_quality_check(self):
        """
        Performing a quality check of the light curve and applying masks to invalid entries.
        A cleaned light curve will replace the old entry.

        :return:
        """

        status = False

        self.log.info("LC Analyst: Start quality check.")
        for entry in self.light_curves:
            #extract np array with the light curve
            lc = np.array(entry["lc"])
            self.log.debug("LC Analyst: Masking negative errors.")
            mask_neg_err = self.flag_negative_errorbars(lc)
            self.log.debug("LC Analyst: Applying negative error mask.")
            cleaned_lc = lc[mask_neg_err]
            entry["lc"] = cleaned_lc
        self.log.info("LC Analyst: Quality check ended.")


    def flag_NULL_entries(self, light_curve):
        #load light curve into a pandas df
        #find all NaNs using isnull() function
        mask_null = np.where(light_curve[:,1] == "NULL")

    def flag_huge_errorbars(self, light_curve):
        """
        :param light_curve: numpy array, an array containing JD, magnitude and error
        :return: mask containing entries that have huge uncertianity values
        """

        return 0.

    def flag_negative_errorbars(self, light_curve):
        """
        :param light_curve: numpy array, an array containing JD, magnitude and error
        :return: array with entries that don't have negative uncertianities
        """
        mask_neg_err = np.where(light_curve[:, 2] > 0)

        return mask_neg_err

