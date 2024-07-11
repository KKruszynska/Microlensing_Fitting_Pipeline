class TestController:
    '''
    Tests to check if controller works fine.
    '''

    def test_launch_analysts(self):
        from MFPipeline.controller.controller import Controller

        event_list = ["GDR3-ULENS-025", "GDR3-ULENS-025_copy"]#"GDR3-ULEN-118"]
        config = {"events_path": "tests/test_controller"}
        controller = Controller(event_list, config_dict=config)
        controller.create_analysts()
        controller.launch_analysts()
