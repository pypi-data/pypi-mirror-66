# Farm GHG calculation based on Penn State University "FEAT" model.
# python3.7+ code by Pasquale Papparella
#
# Contact: pasquale.papparella@pm.me
# see LICENSE file.

import feat_psu.feat_util as fu
import feat_psu.feat_ghg as ga
import feat_psu.feat_nrg as ea

from numpy import divide, multiply, add, subtract
from datetime import datetime

class Feat(object):
    
    '''
    
    FEAT Agroecological Model -> http://www.ecologicalmodels.psu.edu/agroecology/feat/about.htm    
    Main FEAT analysis class. It calls both EnergyAnalysis and GHGAnalysis for the given input data.
    
    '''

    __author__ = 'Pasquale Papparella'
    __info__ = 'https://github.com/apparell/farm-energy-analysis-tool'
    __about__ = 'http://www.ecologicalmodels.psu.edu/agroecology/feat/about.htm'
    __date__ = '03.2020'
    __model_version__ = '1.2.7'
    __version__ = '0.3.1'
    __license__ = 'MIT'

    def run_analysis(self, farm_data: dict, k_params: dict):

        '''        
        
        Run analysis according to FEAT methodology.
        
        '''
              
        try:
            
            if not all([ farm_data['crop_start_date'], farm_data['harvest_date'] ]):
                farm_data['growth_time'] = None
            else:
                gt = abs( ( datetime.strptime( farm_data['crop_start_date'], self.DATE_FORMAT ) - \
                           datetime.strptime( farm_data['harvest_date'], self.DATE_FORMAT ) ) )
                farm_data['growth_time'] = gt.days               

            farm_data['crop_wm_production'] = float( farm_data['yield_rate'] * farm_data['field_area'] )
            farm_data['crop_dm_production'] = float( farm_data['crop_wm_production'] * (1 - farm_data['moisture_storage'] ) )
            farm_data['residue_dm_production'] = farm_data['crop_wm_production'] * farm_data['residue_rate'] * \
                                            k_params['crop_res_k'] * ( float(1) - k_params['crop_storm_hum_k'] )

            re = ea.NRGAnalysis()._run_analysis(farm_data, k_params, self.inputs)
            rg = ga.GHGAnalysis()._run_analysis(farm_data, k_params, self.inputs, re['tot_i_nrg_ha_crop'], re['nrg_drying'])
            
            re.update(rg)

            return re

        except Exception as e:
            raise e

    
    def __init__(self):
        
        self.DATE_FORMAT = "%Y-%m-%d"

        # define inputs
        self.inputs = ['n_rate',
                       'p_rate',
                       'k_rate',
                       'lime_rate',
                       'seeding_rate',
                       'herbicide_rate',
                       'insecticide_rate',
                       'fuel_use_rate']

        # official units for calculation
        self.adim_unit = 'adimensional'
        self.area_unit = 'hectares'
        self.weight_unit = 'Mg'
        self.weight_dm_unit = 'Mg DM'
        self.weight_dm_ha_unit = 'Mg DM / ha'
        self.weight_ha_unit = 'Mg / ha'
        self.nrg_unit = 'MJ'
        self.nrg_ha_unit = 'MJ / ha'
        self.ghg_unit = 'kgCO2e'
        self.ghg_kg_unit = 'kgCO2e / kg'
        self.ghg_ha_unit = 'kgCO2e / ha'
        self.ghg_day_unit = 'kgCO2e / day'
        self.ghg_intensity_unit = 'kgCO2 / MJoutput'
        