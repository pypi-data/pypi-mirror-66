import root_optimize
root_optimize.utils.expand_selection('weight_lumi * ((36100 * (run_number < 324320)) + (43800 * (run_number >= 324320)))*(bjets_n > 1.0)*(jets_n > 4.0)*(meff_incl > 8.0)', {})
