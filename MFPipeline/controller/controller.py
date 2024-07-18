import yaml

import subprocess
from concurrent.futures import ProcessPoolExecutor


def run_parallel_analyst(command):
    subprocess.run(command, shell=False)

class Controller:
    '''
    Class that controls other analysts and their corresponding tasks.
    A controller has to be initialized with either config_path or config_dict specified. Otherwise, it will not work.

    :param event_list: list, a list with names of events that need to be analyzed by the pipeline
    :param light_curves: a list of event names and their light curves
    :param config_path: string, optional, a path to a YAML file that has the configuration parameters for the controller
    :param config_dict: dictionary, optional, a dictionary containing configuration of the controller
    '''
    def __init__(self,
                 event_list,
                 config_path=None,
                 config_dict=None,
                 analyst_dicts=None):

        self.event_list = event_list
        self.analyst_dicts = analyst_dicts

        if (config_dict != None):
            # READ config_dict
            self.config = config_dict
        elif (config_path != None):
            # read config path
            self.config = self.parse_config(config_path)
        else:
            # todo: raise custom exception here?
            print("Error! Controller needs information!!!")
            quit()

    def parse_config(self):
        '''
        Function that parses the YAML file with configuration.

        :return: configuration in form of a dictionary.
        '''

        config = {}
        try:
            with open(self.config_path, 'r') as file:
                controller_config = yaml.safe_load(file)

            config["events_path"]  = controller_config.get("events_path")
            config["software_dir"] = controller_config.get("software_dir")
            config["python_compiler"] = controller_config.get("python_compiler")
            config["group_processing_limit"] = controller_config.get("group_processing_limit")


        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))
            config = None

        return config

    def launch_analysts(self):
        '''
        This function starts and parallelizes the :class:`MFPipeline.analyst.event_analyst.EventAnalyst`.

        :return: Status of work???
        '''

        # First create all of the commands to run the analysts
        commands = []
        for event in self.event_list:
            if(self.analyst_dicts == None):
                command = [self.config["python_compiler"], self.config["software_dir"]+"event_analyst.py",
                           "--event_name", event,
                           "--analyst_path",  self.config["events_path"]+str(event)+"/",
                           "--config_path", self.config["events_path"]+str(event)+"/config.yaml"
                           ]
            else:
                command = [self.config["python_compiler"], self.config["software_dir"] + "event_analyst.py",
                           "--event_name", event,
                           "--analyst_path", self.config["events_path"] + str(event) + "/",
                           "--config_dict", str(self.analyst_dicts[event]),
                           ]
            commands.append(command)

        #Running analysts in batches
        with ProcessPoolExecutor(max_workers=self.config["group_processing_limit"] ) as executor:
            executor.map(run_parallel_analyst, commands)
            # for result in executor.map(run_parallel_analyst, commands):
            #     print(result)
            # print(futures.result())


