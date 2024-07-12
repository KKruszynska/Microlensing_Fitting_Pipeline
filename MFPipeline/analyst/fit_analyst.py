import numpy as np

from MFPipeline.analyst.analyst import Analyst

class FitAnalyst(Analyst):
    '''
    This is a class that performs fitting for one event.
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
                 config_dict=None,
                 config_path=None):

        Analyst.__init__(self, event_name, analyst_path, config_dict=config_dict, config_path=config_path)

        if (config_dict != None):
            self.add_fit_config(config_dict)
        elif ("fit_analyst" in self.config):
            self.add_fit_config(self.config)
        else:
            print("Error! Fit Analyst needs information.")
            quit()

    def add_fit_config(self, config):
        '''
        Add Fit configuration fields to analyst config.

        :param config_dict: dict, dictionary with analyst config
        '''

        self.n_max = config["fit_analyst"]["n_max"]

    def perform_fit(self):
        '''
        Placeholder. Counts to n_max.

        :return: number of counts
        '''

        count = 0
        for i in range(self.n_max):
            count += 1

        return count