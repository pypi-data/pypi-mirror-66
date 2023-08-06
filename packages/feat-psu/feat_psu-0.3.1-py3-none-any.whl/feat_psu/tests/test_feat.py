from unittest import TestCase
from feat_psu.feat import Feat

class TestFeat(TestCase):
    def test_is_computing(self):
        
        totals = {
          
            'field_area': 1.0, 
            'crop_start_date': '2019-10-23', 'harvest_date': '2020-06-11', 
            'seeding_rate': 133.0, 
            'n_rate': 72.0, 'p_rate': 67.0, 'k_rate': 121.0, 
            'lime_rate': 0.0, 
            'herbicide_rate': 1.07, 'insecticide_rate': 0.47, 
            'fungicide_rate': 0.0, 'transportation': 0.64, 
            'yield_rate': 4.0, 'residue_rate': 0.0, 
            'moisture_harvest': 0.2, 'moisture_storage': 0.15, 
            'fuel_use_rate': 54.0, 'blue_water_rate': 4218, 

        }
        
        wheat_k_params = {
        "crop_seeding_k": 7.080000000,
        "crop_seeding_ghg_k": 0.400000000,
        "crop_res_k": 1.300000000,
        "crop_storm_hum_k": 0.135000000,
        
        "nrg_n_k": 54.800000000,
        "nrg_p2o5_k": 10.300000000,
        "nrg_k2o_k": 7.000000000,
        "nrg_lime_k": 1.000000000,
        "nrg_seeding_k": 8.650000000,
        "nrg_fungicide_k": 376.00000000,
        "nrg_herbicide_k": 293.000000000,
        "nrg_insecticide_k": 312.20000000,
        "nrg_fuel_use_k": 44.830000000,
        "nrg_hhv_k": 16.600000000,
        "nrg_drying_k": 3.63000000,
        
        "ghg_n_k": 3.900000000,
        "ghg_p2o5_k": 0.91000000,
        "ghg_k2o_k": 0.540000000,
        "ghg_lime_k": 0.350000000,
        "ghg_seeding_k": 0.400000000,
        "ghg_fungicide_k": 6.900000000,
        "ghg_herbicide_k": 16.500000000,
        "ghg_insecticide_k": 22.800000000,
        "ghg_fuel_use_k": 3.300000000,
        "ghg_drying_k": 0.080000000,
        "ghg_transp_k": 0.050000000,
        
        "n2o_gwp_k": 298.000000000,
        "n2o_add_org_k": 0.016000000,
        "n2o_n2o_to_n_k": 1.571428571,
        "n2o_frac_s_k": 0.110000000,
        "n2o_n_vol_k": 0.014000000,
        "n2o_n_lr_k": 0.011000000,
        "n2o_frac_lr_k": 0.24000000,
        "n2o_slope_k": 1.510000000,
        "n2o_intercept_k": 0.520000000,
        "n2o_n_abg_res_k": 0.006000000,
        "n2o_n_beg_res_k": 0.009000000,
        "n2o_n_ab_ratio_res_k": 0.240000000
        }
        
        feat = Feat()
        result = feat.run_analysis(totals, wheat_k_params)
        
        self.assertTrue(result['tot_ghg_kg_crop'], 0.4729781665942373)
        

