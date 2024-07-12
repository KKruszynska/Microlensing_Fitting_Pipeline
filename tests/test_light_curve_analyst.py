import pytest

scenario_gaia = {
        "path_outputs": "tests/test_cmd/output",
        "event_name": "GDR3-ULEN-025",
        "ra": 260.8781,
        "dec": -27.3788,
        "lc_analyst": {
            "n_max" : 15
        }
}

class testLCAnalyst:
    '''
    Class with tests
    '''
    def __init__(self,
                 scenario):
        self.scenario = scenario

    def test_parse_config(self):
        from MFPipeline.analyst.light_curve_analyst import LightCurveAnalyst

        config = {}
        config["event_name"] = self.scenario.get("event_name")
        path_outputs = self.scenario.get("path_outputs")
        config["ra"], config["dec"] = self.scenario.get("ra"), self.scenario.get("dec")
        config["lc_analyst"] = {}
        dict = self.scenario.get("lc_analyst")
        config["lc_analyst"]["n_max"] = dict.get("n_max")

        analyst = LightCurveAnalyst(config["event_name"], path_outputs, config_dict=config)
        n_max_config = analyst.config["lc_analyst"]["n_max"]

        assert n_max_config == dict.get("n_max")

    def test_run_analyst(self):
        from MFPipeline.analyst.light_curve_analyst import LightCurveAnalyst

        config = {}
        config["event_name"] = self.scenario.get("event_name")
        path_outputs = self.scenario.get("path_outputs")
        config["ra"], config["dec"] = self.scenario.get("ra"), self.scenario.get("dec")
        config["lc_analyst"] = {}
        dict = self.scenario.get("lc_analyst")
        config["lc_analyst"]["n_max"] = dict.get("n_max")

        analyst = LightCurveAnalyst(config["event_name"], path_outputs, config_dict=config)
        count = analyst.perform_quality_check()

        assert count == dict.get("n_max")



def test_run():
    case = scenario_gaia
    test = testLCAnalyst(case)
    test.test_parse_config()
    test.test_run_analyst()