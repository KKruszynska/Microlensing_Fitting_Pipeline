import pytest

scenario_file_cat = {
    "event_name" : "GaiaDR3-ULENS-025",
    "ra" : 260.8781,
    "dec" : -27.3788,
    "analyst_path" : "tests/test_controller/GaiaDR3-ULENS-025/",
    "cmd_analyst": {
        "catalogues" : {
            "catalogue_1" : {
                             "name" : "Gaia_DR3",
                             "band" : ["Gaia_G", "Gaia_BP", "Gaia_RP"],
                             "cmd_path" : "tests/test_cmd/input/gdr3-ulens-025_result.csv",
                             "cmd_separator" : ",",
            },
            "catalogue_2" : {
                            "name" : "Gaia_DR2",
                            "band" : ["Gaia_G", "Gaia_BP", "Gaia_RP"],
                            "cmd_path" : "tests/test_cmd/input/gdr3-ulens-025_result.csv",
                            "cmd_separator" : ",",
            },
        },
    },
    "config_final" : {
        "event_name": "GaiaDR3-ULENS-025",
        "ra": 260.8781,
        "dec": -27.3788,
        "lc_analyst": {
            "n_max": 10,
             },
        "fit_analyst": {
            "n_max": 10,
        },
        "cmd_analyst":
            {"catalogues":
                 [{"name": "Gaia_DR3",
                   "band": ["Gaia_G", "Gaia_BP", "Gaia_RP"],
                   "cmd_path": "/home/katarzyna/Documents/Microlensing_Fitting_Pipeline/Microlensing_Fitting_Pipeline/tests/test_cmd/input/gdr3-ulens-025_result.csv",
                   "cmd_separator": ","},
                ]
             }
    }
}
class testEventAnalyst:
    '''
    Class with Event Analyst tests
    '''
    def __init__(self,
                 scenario):
        self.scenario = scenario

    def test_parse_config(self):
        from MFPipeline.analyst.event_analyst import EventAnalyst

        event_name = self.scenario.get("event_name")
        analyst_path = self.scenario.get("analyst_path")
        event_analyst = EventAnalyst(event_name, analyst_path, 'debug', config_path=analyst_path+"config.yaml", stream=True)
        event_analyst.parse_config(analyst_path+"config.yaml")

        assert type(event_analyst.config) == type(self.scenario.get("config_final"))
        assert event_analyst.config == self.scenario.get("config_final")

def test_run():

    case = scenario_file_cat
    test = testEventAnalyst(case)
    test.test_parse_config()

    # for case in [scenario_file_cat, scenario_gaia]:
    #     test = testCmdAnalyst(case)
    #     test.test_load_source_gaia()
    #     test.test_load_gaia()
    #     test.test_plot_gaia()
