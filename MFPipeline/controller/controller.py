import yaml

import subprocess
from concurrent.futures import ProcessPoolExecutor

from MFPipeline import logs

def run_parallel_analyst(command):
    subprocess.run(command, shell=False)

class Controller:
    '''
    Class that controls other analysts and their corresponding tasks.
    A controller has to be initialized with either config_path or config_dict specified. Otherwise, it will not work.

    :param event_list: list, a list with names of events that need to be analyzed by the pipeline
    :param config_path: string, optional, a path to a YAML file that has the configuration parameters for the controller
    :param config_dict: dictionary, optional, a dictionary containing configuration of the controller
    :param analyst_dicts: dictionary, optional, dictionary containing jsons with information for analysts
    :param stream: optional, boolean, should the log be accessible through Kubernetes?
    '''
    def __init__(self,
                 event_list,
                 config_path=None,
                 config_dict=None,
                 analyst_dicts=None):

        self.event_list = event_list
        self.analyst_dicts = analyst_dicts

        if config_dict is not None:
            # READ config_dict
            self.config = config_dict
            if "log_stream" in self.config:
                self.log = logs.start_log(self.config["log_location"],
                                          self.config["log_level"],
                                          stream=self.config["log_stream"])
            else:
                self.log = logs.start_log(self.config["log_location"],
                                          self.config["log_level"])
        elif config_path is not None:
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
            config["log_location"] = controller_config.get("log_location")
            config["log_level"] = controller_config.get("log_level")
            if "log_stream" in controller_config:
                config["log_stream"] = controller_config.get("log_stream")

        except Exception as err:
            self.log.exception(f"Controller: %s, %s" % (err, type(err)))
            config = None

        return config

    def launch_analysts(self):
        '''
        This function starts and parallelizes the :class:`MFPipeline.analyst.event_analyst.EventAnalyst`.

        :return: Status of work???
        '''

        self.log.info(f"Controller: Start processing.")
        # First create all the commands to run the analysts
        commands = []
        self.log.debug(f"Controller: Creating the commands to launch analysts.")
        for event in self.event_list:
            command = [self.config["python_compiler"],
                       self.config["software_dir"]+"event_analyst.py",
                       "--event_name", event,
                       "--analyst_path",  self.config["events_path"]+str(event)+"/",
                       "--log_level", self.config["log_level"],
                       ]

            if "log_stream" in self.config:
                command.append("--stream")
                command.append(str(self.config["log_stream"]))

            if self.analyst_dicts is not None:
                self.log.debug(f"Controller: Analyst dicts specified.")
                command.append("--config_dict")
                command.append(str(self.analyst_dicts[event]))
            else:
                self.log.debug(
                    f"Controller: Analyst dicts not specified, will look for information in their config files."
                )
                command.append("--config_path")
                command.append(self.config["events_path"] + str(event) + "/config.yaml")

            commands.append(command)

        #Running analysts in batches
        self.log.info(f"Controller: Commands created. Spawning processes.")
        self.log.debug(f"Controller: Max workers set as: %d."%self.config["group_processing_limit"])
        with ProcessPoolExecutor(max_workers=self.config["group_processing_limit"] ) as executor:
            self.log.debug(f"Controller: New process spawned.")
            executor.map(run_parallel_analyst, commands)
            # for result in executor.map(run_parallel_analyst, commands):
            #     print(result)
            # print(futures.result())

        self.log.info(f"Controller: Processing finished.")
        logs.close_log(self.log)


