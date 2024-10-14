import numpy as np
import json
import time

from MFPipeline.analyst.analyst import Analyst

from MFPipeline.fitting_support.pyLIMA import fit_pyLIMA


class FitAnalyst(Analyst):
    """
    This is a class that performs fitting for one event.
    It is a child of the :class:`MFPipeline.analyst.analyst.Analyst`
    It follows a flowchart specified here: link link link

    A Fit Analyst needs either a config_path or config_dict, otherwise it will not work.

    :param event_name: str, name of the analyzed event
    :param analyst_path: str, path to the folder where the outputs are saved
    :param light_curves: dict, dictionary containing light curves, observatory name, and filter
    :param log: logger instance, log started by Event Analyst
    :param config_dict: dictionary, optional, dictionary with Event Analyst configuration
    :param config_path: str, optional, path to the YAML configuration file of the Event Analyst
    """
    def __init__(self,
                 event_name,
                 analyst_path,
                 light_curves,
                 log,
                 config_dict=None,
                 config_path=None):

        super().__init__(event_name, analyst_path, config_dict=config_dict, config_path=config_path)

        self.log = log
        self.light_curves = light_curves

        self.best_results = {}
        self.start_time = time.time()

        if config_dict is not None:
            self.parse_config(config_dict)
            self.add_fit_config(config_dict)
        elif "fit_analyst" in self.config:
            self.parse_config(self.confing)
            self.add_fit_config(self.config)
        else:
            self.log.error("Fit Analyst: Error! Fit Analyst needs information.")
            quit()

    def add_fit_config(self, config):
        """
        Add Fit configuration fields to analyst config.

        :param config: dict, dictionary with analyst config
        """

        self.log.debug("Fit Analyst: Reading fit config.")
        self.config["fitting_package"] = config["fit_analyst"]["fitting_package"]
        self.log.debug("Fit Analyst: Finished reading fit config.")

    def perform_ongoing_check(self):
        """
        Function that performs initial fit and checks if the event is ongoing.

        :return: status of the fitting procedures.
        """

        self.log.debug("Fit Analyst: Time elapsed for setting up the analyst: {:.2f} s".format(
            time.time() - self.start_time))
        self.log.info("Fit Analyst: Starting ongoing check fit.")
        self.log.info("Find PSPL starting parameters.")
        time_of_peak = self.find_time_of_peak()
        starting_params = {"ra": self.config["ra"],
                           "dec": self.config["dec"],
                           "t_0": time_of_peak,
                           "u_0": 0.1,
                           "t_E": 40.,
                           }

        self.log.info("Perform PSPL fit without blend and parallax.")
        results = self.fit_PSPL(self.analyst_path+"_PSPL_no_blend_no_piE",
                                starting_params,
                                False,
                                False,
                                return_norm_lc=True,
                                )
        fit_params_PSPL_nopar = results[0]
        aligned_data, residuals = results[1], results[2]
        self.log.info("Fit Analyst:  Finished fitting.")

        # Saving the result not to perform this fit again
        self.best_results["PSPL_no_blend_no_piE"] = fit_params_PSPL_nopar

        self.log.info("Identify ongoing event.")
        baseline_mag = fit_params_PSPL_nopar["baseline_magnitude"]
        self.start_time = time.time()
        ongoing = self.check_ongoing(aligned_data, residuals, baseline_mag)
        self.log.debug("Fit Analyst: Time elapsed for ongoing check: {:.2f} s".format(
            time.time() - self.start_time
        ))

        return ongoing

    def placeholder(self):
        """
        Placeholder function to put in parts of the code that are not complete.
        :return:
        """

        count = 0
        for i in range(self.n_max):
            count += 1

        return count

    def find_time_of_peak(self):
        """
        Find the time of peak among all the light curves.

        :return: time of peak in JD
        """

        time_of_peak = 0.
        mag_tof = 99.
        for entry in self.light_curves:
            lc = np.asarray(entry[1])
            idx_max = np.argmin(lc[:, 1])
            mag_max = lc[idx_max, 1]
            time_max = lc[idx_max, 0]

            if mag_max < mag_tof:
                mag_tof, time_of_peak = mag_max, time_max

        return time_of_peak

    def fit_PSPL(self, fit_name, starting_params, parallax, blend, return_norm_lc=False, use_boundaries=None):
        """
        Perform a Point Source Point Lens fit.

        :param fit_name: str, label of the fit
        :param starting_params: list, starting parameters for the fit
        :param parallax: boolean, use parallax?
        :param blend: boolean, should blending be fitted?
        :param return_norm_lc: boolean, optional, should the fit returned the aligned light curves?
        :param use_boundaries: dictionary, optional, contains boundaries to be used for fitting

        :return: list with fitted parameters and if requested, aligned data
        """

        self.start_time = time.time()
        results = {}
        if self.config["fitting_package"] == "pyLIMA":
            fit_pspl = fit_pyLIMA.fitPyLIMA(self.log)
            results = fit_pspl.fit_PSPL(fit_name, self.light_curves, starting_params, parallax, blend,
                                        return_norm_lc=return_norm_lc, use_boundaries=use_boundaries)

        self.log.debug("Fit Analyst: Time elapsed for fitting: {:.2f} s".format(
            time.time() - self.start_time
        ))

        return results

    def check_ongoing(self, aligned_data, residuals, baseline_mag):
        """
        Checks if the event is over or not.

        :return: boolean, is the event over?
        """
        ongoing = False

        # find standard deviation
        sigmas = []
        for data in residuals:
            sigmas.append(np.std(data[:, 1]))
        sigmas = np.asarray(sigmas)
        std_mag = np.sqrt(np.sum(sigmas ** 2))

        # Find last data point
        t_last = 0
        for data in aligned_data:
            if data[-1, 0] > t_last:
                t_last = data[-1, 0]
                if np.abs(data[-1, 1] - baseline_mag) > std_mag:
                    ongoing = True

        return ongoing

    def perform_ongoing_fit(self):
        """
        Perform fitting procedure for an ongoing event.
        According to the Software Requirements, the analyst
        has to perform PSPL fit with blending and with/without parallax.
        Then they are evaluated. If the blend fit is not okay, fit without
        blend is performed. The results are appended to a dictionary and
        gathered for evaluation.
        """

        self.log.info("Fit Analyst: Starting ongoing event fit.")
        self.log.info("Find PSPL starting parameters.")
        time_of_peak = self.find_time_of_peak()
        starting_params = {"ra": self.config["ra"],
                           "dec": self.config["dec"],
                           "t_0": time_of_peak,
                           "u_0": 0.1,
                           "t_E": 40., }

        self.log.info("Perform PSPL fit.")
        results = self.fit_PSPL(self.analyst_path+"_PSPL_blend_no_piE",
                                starting_params,
                                False,
                                True,
                                )
        self.best_results["PSPL_blend_no_piE"] = results

        self.log.info("Evaluate PSPL fit.")

        self.log.info("Perform PSPL+piE fit.")
        starting_params["pi_EN"] = 0.0
        starting_params["pi_EE"] = 0.0
        results = self.fit_PSPL(self.analyst_path+"_PSPL_blend_piE",
                                starting_params,
                                True,
                                True,
                                )
        self.best_results["PSPL_blend_piE"] = results

        self.log.info("Evaluate PSPL+piE fit.")
        model_ok = self.evaluate_PSPL(results)
        if not model_ok:
            self.log.info("Perform PSPL with parallax without blend fit.")
            results = self.fit_PSPL(self.analyst_path+"_PSPL_noblend_par",
                                    starting_params,
                                    True,
                                    False,
                                    )
            self.best_results["PSPL_noblend_par"] = results

        self.log.info("Fit Analyst:  Finished fitting.")
        self.log.debug("Best models:", self.best_results)

    def perform_finished_fit_PSPL(self):
        """
        Perform fitting procedure for a finished event.
        According to the Software Requirements, the analyst
        has to perform PSPL fit with blending and with/without parallax.
        The results are appended to a dictionary and
        gathered for evaluation.
        """

        self.log.info("Fit Analyst: Starting finished event fit.")
        self.log.info("Find PSPL starting parameters.")
        time_of_peak = self.find_time_of_peak()
        starting_params = {"ra": self.config["ra"],
                           "dec": self.config["dec"],
                           "t_0": time_of_peak,
                           "u_0": 0.1,
                           "t_E": 40., }

        self.log.info("Perform PSPL with blend fit.")
        results = self.fit_PSPL(self.analyst_path+"_PSPL_blend_no_piE",
                                starting_params,
                                False,
                                True,
                                )
        self.best_results["PSPL_blend_no_piE"] = results
        self.log.info("Finished fitting PSPL with blend fit.")

        self.log.info("Perform PSPL+piE fit.")

        starting_params["t_0"] = self.best_results["PSPL_blend_no_piE"]["t0"]

        starting_u_0s = [-0.1, 0.1]
        starting_pi_ens = [-0.1, 0.1]
        starting_pi_ees = [-0.1, 0.1]

        for u_0 in starting_u_0s:
            for pi_en in starting_pi_ens:
                for pi_ee in starting_pi_ees:
                    starting_params["u_0"] = u_0
                    starting_params["pi_EN"] = pi_en
                    starting_params["pi_EE"] = pi_ee
                    boundaries = {
                        "tE_lower": 0.,
                        "tE_upper": 3000.
                    }
                    signs = ""
                    for element in [u_0, pi_en, pi_ee]:
                        if element > 0.:
                            signs += "p"
                        else:
                            signs += "m"

                    if u_0 > 0.:
                        boundaries["u0_lower"] = 0.
                        boundaries["u0_upper"] = 2.
                    else:
                        boundaries["u0_lower"] = -2.
                        boundaries["u0_upper"] = 0.

                    if pi_en > 0.:
                        boundaries["piEN_lower"] = 0.
                        boundaries["piEN_upper"] = 2.0
                    else:
                        boundaries["piEN_lower"] = -2.0
                        boundaries["piEN_upper"] = 0.
                    if pi_ee > 0.:
                        boundaries["piEE_lower"] = 0.0
                        boundaries["piEE_upper"] = 2.0
                    else:
                        boundaries["piEE_lower"] = -2.0
                        boundaries["piEE_upper"] = 0.0

                    self.log.info("Fit Analyst:  Starting fitting model {:s}".format("PSPL_blend_piE_"+signs))
                    results = self.fit_PSPL(self.analyst_path+"_PSPL_blend_piE_" + signs,
                                            starting_params,
                                            True,
                                            True,
                                            use_boundaries=boundaries,
                                            )
                    self.best_results["PSPL_blend_piE_"+signs] = results

                    self.log.info("Fit Analyst:  Finished fitting model {:s}".format("PSPL_blend_piE_"+signs))

        # self.log.debug("Fit Analyst: Best models:")
        # for model in self.best_results:
        #     params = self.best_results[model]
        #     if "piEN" in params:
        #         self.log.debug("Fit Analyst: {:s} : t0={:.2f}, u0={:.2f}, tE={:.2f}, piEN={:.2f}, piEE={:.2f}".format(
        #           model, params["t0"], params["u0"], params["tE"], params["piEN"], params["piEE"]
        #         ))
        #     else:
        #         self.log.debug("Fit Analyst: {:s} : t0={:.2f}, u0={:.2f}, tE={:.2f}".format(
        #             model, params["t0"], params["u0"], params["tE"]
        #         ))


    def perform_anomaly_finder(self):
        """
        Perform an anomaly finder.

        :return: boolean flag, if an anomaly was detected
        """

        anomaly_found = False

        return anomaly_found

    def evaluate_model(self):
        """
        Evaluate all found models.

        :return: return the key for the best model
        """
        best_model_name = ""

        return best_model_name

    def evaluate_PSPL(self, model_params):
        """
        Check if model doesn't have negative or low blend flux.
        Lifted from mop.toolbox.fittols.test_quality_of_model_fit

        :return: boolean flag if the event is okay
        """
        fit_ok = True

        cov_fit = model_params['fit_covariance']

        if (np.abs(model_params['blend_magnitude']) < 3.0 * cov_fit[4, 4] ** 0.5) or \
                (np.abs(model_params['source_magnitude']) < 3.0 * cov_fit[3, 3] ** 0.5) or \
                (np.abs(model_params['tE']) < 3. * cov_fit[2, 2] ** 0.5):
            fit_ok = False

        return fit_ok

    def perform_fit(self):
        """
        Perform fitting flow.

        :return: dictionary with all found models
        """

        ongoing = self.perform_ongoing_check()

        if ongoing:
            self.perform_ongoing_fit()
            # perform model evaluation here
            # perform anomaly finder on best model

        else:
            self.perform_finished_fit_PSPL()
            # perform model evaluation here
            # perform anomaly finder on best model
            # if anomaly: perform_finished_fit_multiple()
            # else if peak covered: perform_finished_FSPL()
            # evaluate models
            # anomaly finder

        self.log.debug("Fit Analyst: Best models:")
        for model in self.best_results:
            params = self.best_results[model]
            if "piEN" in params:
                self.log.debug(
                    "Fit Analyst: {:s} : t0={:.2f}, u0={:.2f}, tE={:.2f}, piEN={:.2f}, piEE={:.2f}".format(
                        model, params["t0"], params["u0"], params["tE"], params["piEN"], params["piEE"]
                    )
                )
            else:
                self.log.debug("Fit Analyst: {:s} : t0={:.2f}, u0={:.2f}, tE={:.2f}".format(
                    model, params["t0"], params["u0"], params["tE"]
                )
                )
        # Save results
        self.log.debug("Fit Analyst: Saving results.")
        # Save results to a file
        file_name = self.analyst_path + "fit_results.json"
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self.best_results, file, ensure_ascii=False, indent=4)
        self.log.debug("Fit Analyst: Results saved to {:s}.".format(file_name))

        # Save best results statistics
        file_name = self.analyst_path + "fit_stats.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write("{:20s} : {:7s} {:7s} {:7s} {:7s} {:7s} {:7s} {:7s}\n".format(
                "# name", "chi2", "red_chi2", "SW", "AD", "KS", "AIC", "BIC"
            ))
            file.write("#--------------------------------------------------------------------------------\n")
            for model in self.best_results:
                params = self.best_results[model]
                file.write("{:20s} : {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f}\n".format(
                    model, params["chi2"], params["red_chi2"], params["sw_test"], params["ad_test"],
                    params["ks_test"], params["aic_test"], params["bic_test"]
                ))

        return self.best_results