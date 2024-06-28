import yaml

from analyst.cmd_analyst import CmdAnalyst

class Controller:
    '''
    Controller class that launches other processes.
    '''
    def __init__(self,
                 config_path):
        self.config_path = config_path

    def read_config(self):
        '''
        :return: satus of reading controller configuration file
        '''
        read_config_status = False
        try:
            with open(self.config_path, 'r') as file:
                controller_config = yaml.safe_load(file)

            self.input_config = controller_config.get("input")
            self.output_config = controller_config.get("output")
            read_config_status = True
        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))

        return read_config_status

    def parse_events_configuration(self):
        '''
        :param:
        :return:
        '''
        read_events_status = False
        try:
            events_config = self.input_config.get("events")
            self.event_list_path = events_config.get("path")
            self.events_list_sep = events_config.get("separator")
            read_events_status = True
        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))

        return read_events_status

    def parse_cmds_configuration(self):
        '''
        :param :
        :return:
        '''
        read_cmds_status = False
        try:
            cmds_config = self.input_config.get("cmd")
            self.cmd_catalogues = cmds_config.get("catalogue_name")
            self.cmd_bands = cmds_config.get("band")
            self.events_list_sep = cmds_config.get("separator")
            read_cmds_status = True
        except Exception as err:
            print(f"Unexpected %s, %s" % (err, type(err)))

        return read_cmds_status
