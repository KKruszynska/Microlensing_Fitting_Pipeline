import pytest

scenario_gaia = {
        "path_outputs": "tests/test_cmd/output",
        "event_name": "GDR3-ULEN-025",
        "ra": 260.8781,
        "dec": -27.3788,
        "fit_analyst": {
            "n_max" : 15
        }
}

class testFitAnalyst:
    '''
    Class with tests
    '''
    def __init__(self,
                 scenario):
        self.scenario = scenario

    def test_parse_config(self):
        from MFPipeline.analyst.fit_analyst import FitAnalyst

        config = {}
        config["event_name"] = self.scenario.get("event_name")
        path_outputs = self.scenario.get("path_outputs")
        config["ra"], config["dec"] = self.scenario.get("ra"), self.scenario.get("dec")
        config["fit_analyst"] = {}
        dict = self.scenario.get("fit_analyst")
        config["fit_analyst"]["n_max"] = dict.get("n_max")

        analyst = FitAnalyst(config["event_name"], path_outputs, config_dict=config)
        n_max_config = analyst.config["fit_analyst"]["n_max"]

        assert n_max_config == dict.get("n_max")

    def test_run_analyst(self):
        from MFPipeline.analyst.fit_analyst import FitAnalyst

        config = {}
        config["event_name"] = self.scenario.get("event_name")
        path_outputs = self.scenario.get("path_outputs")
        config["ra"], config["dec"] = self.scenario.get("ra"), self.scenario.get("dec")
        config["fit_analyst"] = {}
        dict = self.scenario.get("fit_analyst")
        config["fit_analyst"]["n_max"] = dict.get("n_max")

        analyst = FitAnalyst(config["event_name"], path_outputs, config_dict=config)
        count = analyst.perform_fit()

        assert count == dict.get("n_max")



def test_run():
    case = scenario_gaia
    test = testFitAnalyst(case)
    test.test_parse_config()
    test.test_run_analyst()