import yaml

from MFPipe.analyst.event_analyst import EventAnalyst

class Controller:
    '''
    Controller class that launches other processes.
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
            print("Error! Controller needs information!!!")
            quit()

    def parse_config(self):
        '''
        :return: satus of reading controller configuration file
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
        Create analysts to work.
        :return:
        '''

        self.event_analysts = []
        if self.config != None:
            for event in self.event_list:
                analyst_path = self.config["events_path"]+"/"+str(event)+"/"
                self.event_analysts.append(EventAnalyst(event, analyst_path, config_path=analyst_path+"config.yaml"))


    def launch_analysts(self):
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



