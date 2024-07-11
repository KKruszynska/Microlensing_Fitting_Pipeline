import yaml

from MFPipeline.analyst.analyst import Analyst
from MFPipeline.analyst.cmd_analyst import CmdAnalyst

class EventAnalyst(Analyst):
    '''
    This is a class that analyzes one event.
    It is a child of the :class:`MFPipeline.analyst.analyst.Analyst`
    It takes care of other sub-analysts that fit microlensing models to the light curve,
    create colour-magnitude diagrams and perform other additional tasks.

    An Event Analyst needs either a config_path or config_dict, otherwise it will not work.

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

        if(config_path != None):
            self.parse_config(config_path)
            self.parse_event_config(config_path)
        elif(config_dict != None):
            self.add_config_dict(config_dict)
        else:
            print("Error! Event Analyst needs information.")
            quit()

    def parse_event_config(self, config_path):
        '''
        Parse YAML file with configuration, turn it into a dictionary and to

        :param config_path: str, path with YAML file containing additional information
        needed for an Event Analyst.
        '''

        try:
            with open(config_path, 'r') as file:
                event_config = yaml.safe_load(file)

            self.config["cmd_analyst"] = event_config.get("cmd_analyst")

        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))

    def add_config_dict(self, conifg_dict):
        '''
        Adds sections of config relevant to Event Analyst to its configuration file.

        :param conifg_dict: dict, dictionary containing configuration for Event Analyst
        '''

        try:
            self.config["cmd_analyst"] = conifg_dict.get("cmd_analyst")

        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))

    def run_single_analyst(self):
        '''
        Perform tasks assigned to a single Event Analyst. First the event is handeled by a Fit Analyst, searching
        for fitting microlensing models. After fitting is done, output information is passed to a CMD Analyst, that
        creates a CMD plot for specified catalogs and plots the source and blend for each found solution.

        :return: status?
        '''
        # self.light_curve = somehow get lightcurve data
        # self.fit_event = run fits, save fit results somehow
        # when the fit is finished create a cmd
        cmd_plot_status = self.run_cmd_analyst()
        if False in cmd_plot_status:
            # this should be a log statement, and more informative
            print("Error encountered while creating CMD plots.")


    def run_cmd_analyst(self):
        '''
        Launch CMD Analyst to create a CMD plot for all soultions and specified catalogues.

        :return: a list of boolean values corresponding to satuts of the created cmd plots.
        '''
        # todo: probably better log if CMD was succesful instead of returning a list with status???
        cmd_plot_status = []

        for dictionary in self.config["cmd_analyst"]["catalogues"]:
            if "cmd_path" in dictionary:
                path_input = dictionary["cmd_path"]
            else:
                path_input = None

            catalogue = dictionary["name"]
            light_curve_data = {'baseline': {'Gaia_G': 16.12, 'Gaia_BP': 17.78, 'Gaia_RP': 14.88}, 'source': {'Gaia_G': 16.14, 'Gaia_BP': 17.79, 'Gaia_RP': 14.91}, 'blend': {'Gaia_G': 20.37, 'Gaia_BP': 22.78, 'Gaia_RP': 18.69}}

            cmd_analyst = CmdAnalyst(self.config["event_name"], self.analyst_path, catalogue, light_curve_data, config_dict=self.config)

            source_data, source_labels = cmd_analyst.transform_source_data()
            cmd_data, cmd_labels = cmd_analyst.load_catalogue_data()

            plot_status = cmd_analyst.plot_cmd(source_data, source_labels, cmd_data, cmd_labels)
            cmd_plot_status.append(plot_status)

        return cmd_plot_status