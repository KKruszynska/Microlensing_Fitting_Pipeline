import yaml

from MFPipeline.analyst.event_analyst import EventAnalyst

class Controller:
    '''
    Class that controls other analysts and their corresponding tasks.
    A controller has to be initialized with either config_path or config_dict specified. Otherwise, it will not work.

    :param event_list: list, a list with names of events that need to be analyzed by the pipeline
    :param config_path: string, optional, a path to a YAML file that has the configuration parameters for the controller
    :param config_dict: dictionary, optional, a dictionary containing configuration of the controller
    '''
    def __init__(self,
                 event_list,
                 config_path=None,
                 config_dict=None):
        self.event_list = event_list
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

            config = controller_config.get("input")

        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))
            config = None

        return config

    def create_analysts(self):
        '''
        This function creates a list of :class:`MFPipeline.analyst.event_analyst.EventAnalyst` that get one event from
        the `event_list` assigned to them.
        '''

        self.event_analysts = []
        if self.config != None:
            for event in self.event_list:
                analyst_path = self.config["events_path"]+"/"+str(event)+"/"
                self.event_analysts.append(EventAnalyst(event, analyst_path, config_path=analyst_path+"config.yaml"))


    def launch_analysts(self):
        '''
        This function starts and parallelizes the work of created :class:`MFPipeline.analyst.event_analyst.EventAnalyst`.

        :return: Status of work???
        '''
        # how to parallelize it?
        # put here something like this:
        # set_start_method('fork')
        # iterations = np.random.randint(len(data), size=n_iter)
        # with Pool() as pool:
        #     with tqdm(total=n_iter) as pbar:
        #         for i in pool.imap_unordered(run_single_analyst, iterations):
        #             results.append(i)

        for analyst in self.event_analysts:
            analyst.run_single_analyst()



