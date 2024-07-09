class TestController:
    '''
    Tests to check if controller works fine.
    '''

    def test_launch_analysts(self):
        from MFPipeline.controller.controller import Controller

        event_list = ["GDR3-ULENS-025", "GDR3-ULENS-025_copy"]#"GDR3-ULEN-118"]
        # / home / katarzyna / Documents / Microlensing_Fitting_Pipeline / Microlensing_Fitting_Pipeline / tests / test_controller / GDR3 - ULENS - 025 / config.yaml
        config = {"events_path": "/home/katarzyna/Documents/Microlensing_Fitting_Pipeline/Microlensing_Fitting_Pipeline/tests/test_controller"}
        controller = Controller(event_list, config_dict=config)
        controller.create_analysts()
        controller.launch_analysts()
