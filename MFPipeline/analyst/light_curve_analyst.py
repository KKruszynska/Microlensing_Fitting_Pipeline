from time import sleep
import numpy as np

from MFPipeline.analyst.analyst import Analyst

class LightCurveAnalyst(Analyst):
    '''
    This is a class that performs light curve
    It is a child of the :class:`MFPipeline.analyst.analyst.Analyst`
    It follows a flowchart specified here: link link link

    A Fit Analyst needs either a config_path or config_dict, otherwise it will not work.

    :param event_name: str, name of the analyzed event
    :param analyst_path: str, path to the folder where the outputs are saved
    :param config_dict: dictionary, optional, dictionary with Event Analyst configuration
    :param config_path: str, optional, path to the YAML configuration file of the Event Analyst
    '''
    def __init__(self,
                 event_name,
                 analyst_path,
                 light_curves,
                 config_dict=None,
                 config_path=None):

        super().__init__(event_name, analyst_path, config_dict=config_dict, config_path=config_path)
        # Analyst.__init__(self, event_name, analyst_path, config_dict=config_dict, config_path=config_path)

        self.light_curves = light_curves

        if (config_dict != None):
            self.add_lc_config(config_dict)
        elif("lc_analyst" in self.config):
            self.add_lc_config(self.config)
        else:
            print("Error! Light Curve Analyst needs information.")
            quit()


    def add_lc_config(self, config):
        '''
        Add LC configuration fields to analyst config.

        :param config_dict: dict, dictionary with analyst config
        '''

        self.n_max = int(config["lc_analyst"]["n_max"])

    def perform_quality_check(self):
        '''
        Placeholder. Counts to n_max.

        :return: number of counts
        '''

        for lc in self.light_curves:
            #extract np array with the light curve
            # null_entries = self.flag_NULL_entries(lc)
            sleep(5)


    def flag_NULL_entries(light_curve):
        #load light curve into a pandas df
        #find all NaNs using isnull() function
        mask_null = np.where(light_curve[:,1] == "NULL")


