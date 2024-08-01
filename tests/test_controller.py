import glob, os
import numpy as np
import pandas as pd

import json

class TestControllerPaths:
    '''
    Tests to check if controller works fine.
    '''

    def test_launch_analysts(self):
        from MFPipeline.controller.controller import Controller

        event_list = [#"GaiaDR3-ULENS-018",
                      "GaiaDR3-ULENS-025"]
        config = {
            "python_compiler": "python",
            "group_processing_limit": 3,
            "events_path":
                "tests/test_controller/",
            "software_dir":
                "MFPipeline/analyst/",
            "log_location":
                "tests/test_controller/",
            "log_level": "debug"
            }

        controller = Controller(event_list, config_dict=config)
        controller.launch_analysts()

# class TestControllerDicts:
#     '''
#     Tests to check if controller works fine.
#     '''
#
#     def test_launch_analysts(self):
#         from MFPipeline.controller.controller import Controller
#
#
#
#         event_list = [#"GaiaDR3-ULENS-018",
#                       "GaiaDR3-ULENS-025"]
#
#         event_info = pd.read_csv("tests/test_controller/events_info.csv", header=0)
#
#         analyst_jsons = {}
#         path_lightcurves = "tests/test_controller/light_curves/"
#         os.chdir(path_lightcurves)
#         for event in event_list:
#             dictionary = {}
#             idx = event_info.index[event_info["#event_name"] == event].tolist()
#             dictionary["event_name"] = event
#             dictionary["ra"], dictionary["dec"] = "%f"%event_info["ra"].values[idx][0], "%f"%event_info["dec"].values[idx][0]
#             dictionary["lc_analyst"] = {}
#             dictionary["lc_analyst"]["n_max"] = "%d"%event_info["lc_nmax"].values[idx][0]
#             dictionary["fit_analyst"] = {}
#             dictionary["fit_analyst"]["n_max"] = "%d"%event_info["fit_nmax"].values[idx][0]
#
#             cats = event_info["catalogues"].values[idx][0].split(" ")
#             cat_list = []
#             for catalogue in cats:
#                 dict = {}
#                 dict["name"] = catalogue
#                 dict["bands"] = event_info["bands"].values[idx][0].split(" ")
#                 if (len(event_info["path"].values[idx]) > 0):
#                     dict["cmd_path"] = event_info["path"].values[idx][0]
#                     dict["cmd_separator"] = ","
#                 cat_list.append(dict)
#             dictionary["cmd_analyst"] = {}
#             dictionary["cmd_analyst"]["catalogues"] = cat_list
#
#             light_curves = []
#             for file in glob.glob("*%s*.dat" % event):
#                 light_curve = np.genfromtxt(file, usecols=(0, 1, 2), unpack=True)
#                 light_curve = light_curve.T
#
#                 survey = ""
#                 band = ""
#                 if ("mod" in file):
#                     survey = "Gaia"
#                     txt = file.split(".")
#                     band = txt[0].split("_")[-1]
#                     light_curve[:, 0] = light_curve[:, 0] + 2450000.
#                 elif ("OGLE" in file):
#                     survey = "OGLE"
#                     band = "I"
#                 elif ("KMT" in file):
#                     survey = "KMTNet_" + file[-7]
#                     band = "I"
#
#                 dict = {}
#                 dict["survey"] = survey
#                 dict["band"] = band
#                 dict["lc"] = json.dumps(light_curve.tolist())
#                 light_curves.append(dict)
#
#             dictionary["light_curves"] = light_curves
#             js = json.dumps(dictionary)
#             analyst_jsons[event] = js
#
#         os.chdir("../../../")
#         config = {
#             "python_compiler": "python",
#             "group_processing_limit": 3,
#             "events_path": "/tests/test_controller/",
#             "software_dir": "MFPipeline/analyst/",
#             "log_location":
#                 "/home/katarzyna/Documents/Microlensing_Fitting_Pipeline/Microlensing_Fitting_Pipeline/tests/test_controller/",
#             "log_level": "debug",
#             "log_stream": True,
#             }
#
#         controller = Controller(event_list, config_dict=config, analyst_dicts=analyst_jsons)
#         controller.launch_analysts()