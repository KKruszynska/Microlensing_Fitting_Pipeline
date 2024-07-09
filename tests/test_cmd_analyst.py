import pandas as pd

scenario_file = {
        "path_input" : "tests/test_cmd/input/gdr3-ulens-025_result.csv",
        "path_outputs": "tests/test_cmd/output",
        "event_name": "GDR3-ULEN-025",
        "ra": 260.8781,
        "dec": -27.3788,
        "catalogue_name": "Gaia_DR3",
        "light_curve_data": {
            "baseline": {
                "Gaia_G": 16.12,
                "Gaia_BP": 17.78,
                "Gaia_RP": 14.88
            },
            "source": {
                "Gaia_G": 16.14,
                "Gaia_BP": 17.79,
                "Gaia_RP": 14.91
            },
            "blend": {
                "Gaia_G": 20.37,
                "Gaia_BP": 22.78,
                "Gaia_RP": 18.69
                },
            }
}

scenario_gaia = {
        "path_outputs": "tests/test_cmd/output",
        "event_name": "GDR3-ULEN-025",
        "ra": 260.8781,
        "dec": -27.3788,
        "catalogue_name": "Gaia_DR3",
        "light_curve_data": {
            "baseline": {
                "Gaia_G": 16.12,
                "Gaia_BP": 17.78,
                "Gaia_RP": 14.88
            },
            "source": {
                "Gaia_G": 16.14,
                "Gaia_BP": 17.79,
                "Gaia_RP": 14.91
            },
            "blend": {
                "Gaia_G": 20.37,
                "Gaia_BP": 22.78,
                "Gaia_RP": 18.69
                },
            }
}

class testCmdAnalyst():
    '''
    Class with tests
    '''
    def __init__(self,
                 scenario):
        self.scenario = scenario

    def test_plot_gaia(self):
        from MFPipeline.analyst.cmd_analyst import CmdAnalyst

        catalogue_name = self.scenario.get("catalogue_name")
        path_outputs = self.scenario.get("path_outputs")
        event_name = self.scenario.get("event_name")
        ra, dec = self.scenario.get("ra"), self.scenario.get("dec")
        light_curve_data = self.scenario.get("light_curve_data")
        print(light_curve_data)

        if self.scenario.get("path_input") is not None:
            path_input = self.scenario.get("path_input")
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data, file_path=path_input)
        else:
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data)

        source_data, source_labels = analyst.transform_source_data()
        cmd_data, cmd_labels = analyst.load_catalogue_data()
        plot_status = analyst.plot_cmd(source_data, source_labels, cmd_data, cmd_labels)

        assert plot_status == True


    def test_load_gaia(self):
        from MFPipeline.analyst.cmd_analyst import CmdAnalyst

        catalogue_name = self.scenario.get("catalogue_name")
        path_outputs = self.scenario.get("path_outputs")
        event_name = self.scenario.get("event_name")
        ra, dec = self.scenario.get("ra"), self.scenario.get("dec")
        light_curve_data = self.scenario.get("light_curve_data")

        if self.scenario.get("path_input") is not None:
            path_input = self.scenario.get("path_input")
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data, file_path=path_input)
        else:
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data)

        cmd_data, cmd_labels = analyst.load_catalogue_data()

        assert type(cmd_data) == pd.DataFrame
        assert type(cmd_labels) == list

    def test_load_source_gaia(self):
        from MFPipeline.analyst.cmd_analyst import CmdAnalyst

        catalogue_name = self.scenario.get("catalogue_name")
        path_outputs = self.scenario.get("path_outputs")
        event_name = self.scenario.get("event_name")
        ra, dec = self.scenario.get("ra"), self.scenario.get("dec")
        light_curve_data = self.scenario.get("light_curve_data")

        if self.scenario.get("path_input") is not None:
            path_input = self.scenario.get("path_input")
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data, file_path=path_input)
        else:
            analyst = CmdAnalyst(path_outputs, event_name, ra, dec, catalogue_name, light_curve_data)

        source_data, source_labels = analyst.transform_source_data()

        assert type(source_data) ==  pd.DataFrame
        assert type(source_labels) ==  list

def test_run():

    for case in [scenario_file, scenario_gaia]:
        test = testCmdAnalyst(case)
        test.test_load_source_gaia()
        test.test_load_gaia()
        test.test_plot_gaia()

