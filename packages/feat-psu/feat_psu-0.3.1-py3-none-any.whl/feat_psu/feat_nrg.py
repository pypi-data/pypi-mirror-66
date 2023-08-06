# Farm GHG calculation based on Penn State University "FEAT" model.
# python3.7+ code by Pasquale Papparella
#
# Contact: pasquale.papparella@pm.me
# see LICENSE file.

from feat_psu.feat_util import recursive_items, multireplace
from numpy import divide, multiply, add, subtract

class NRGAnalysis(object):
    '''
    Main class for Energy calculation.

    Original FEAT Model from:
    Camargo, G.G.T., Ryan, M.R., Richard, T.L., 2013. Energy use and greenhouse gas emissions from crop production using the farm energy analysis tool. BioScience, 63, 263-273.

    FEAT Model is licensed under a Creative Commons Attribution 4.0 International License.
    '''

    def nrg_n(self):

        '''
        Total energy consumption: N fertilizer application. [ MJ ]
        '''

        n_year = float( self.ag["n_rate"] * self.field_area * self.k_params["nrg_n_k"] )
        return n_year

    def nrg_p2o5(self):

        '''
        Total energy consumption: P2O5 fertilizer application. [ MJ ]
        '''

        p2o5_year = float( self.ag["p_rate"] * self.field_area * self.k_params["nrg_p2o5_k"] )
        return p2o5_year

    def nrg_k2o(self):

        '''
        Total energy consumption: K2O fertilizer application. [ MJ ]
        '''

        k2o_year = float( self.ag["k_rate"] * self.field_area * self.k_params["nrg_k2o_k"] )
        return k2o_year

    def nrg_lime(self):

        '''
        Total energy consumption: agricultural limestone (CaO, CaCO3 et sim.) application. [ MJ ]
        '''

        lime_year = float( self.ag["lime_rate"] * self.field_area * self.k_params["nrg_lime_k"] )
        return lime_year

    def nrg_seeding(self):

        '''
        Total energy consumption for Seeding rate, farm activity. [ MJ ]
        '''

        seeding_year = float( self.ag["seeding_rate"] * self.field_area * self.k_params["nrg_seeding_k"] )
        return seeding_year

    def nrg_herbicide(self):

        '''
        Total energy consumption: Herbicide application. [ MJ ]
        '''

        herb_year = float( self.ag["herbicide_rate"] * self.field_area * self.k_params["nrg_herbicide_k"] )
        return herb_year

    def nrg_insecticide(self):

        '''
        Total energy consumption: Insecticide application. [ MJ ]
        '''

        inse_year = float( self.ag["insecticide_rate"] * self.field_area * self.k_params["nrg_insecticide_k"] )
        return inse_year

    def nrg_fuel_use(self):

        '''
        Total energy consumption due to fuel use in farm activity. [ MJ ]
        '''

        fuel_use_year = float( self.ag["fuel_use_rate"] * self.field_area * self.k_params["nrg_fuel_use_k"] )
        return fuel_use_year

    def nrg_drying(self):

        '''
        Total energy consumption for drying Wet Matter production, if drying is needed. [ MJ ]
        '''

        aux = float( self.ag["moisture_harvest"] - self.ag["moisture_storage"] )
        drying_year = float( self.ag["crop_wm_production"] * aux * self.k_params["nrg_drying_k"] * 1000 )
        return drying_year

    def nrg_transportation(self):

        '''
        Total energy consumption for transportation of inputs ('n','p2o5','k2o','lime','seeding','herbicide','insecticide','fungicide').
        Based on single parameter from 'Wang, M. Development and use of GREET 1.6 fuel-cycle model for transportation fuels and vehicle technologies. 2001'
        '''
        
        ag = self.ag
        del ag['fuel_use_rate']
        
        t = [ float(value) for key, value in recursive_items(ag) if key in self.inputs ]
        total = float( round( sum( t ), 9 ) * self.ag["transportation"] * self.field_area )
        return total     

    def _run_analysis(self, ag, k_params, inputs):

        '''
        Run energy analysis.
        '''        
        
        self.ag = dict(ag)
        self.field_area = self.ag["field_area"]        
        self.inputs = inputs #[ ( multireplace( i, {'_rate': ''} ) ) for i in inputs ]

        # Energy conversion parameters
        self.k_params = dict(k_params)
        
        tR, dR = [], {}
        
        # Evaluate every function in energy class
        for f in dir(self):
            result = getattr(self, f)
            if not f.startswith('_') and hasattr(result, '__call__'):
                i = result()
                tR.append(i)
                dR[f] = i

        tei = sum( tR )
        tO = self.ag["crop_dm_production"] * self.k_params["nrg_hhv_k"] * 1000  # crop energy content

        # Compose results
        self.energyAnalysis = {
            
            "tot_i_nrg_crop": float( tei ),
            "tot_i_nrg_ha_crop": float( tei / self.field_area ),
            "tot_o_nrg_crop": float( tO ),
            "tot_o_nrg_ha_crop": float( tO / self.field_area ),
            "nrg_net_value": float( ( tO / self.field_area ) - ( tei / self.field_area ) ),
            "nrg_net_ratio": float( ( ( tO / self.field_area) / ( tei / self.field_area ) ) if tei > 0 else 0.0 )
        
        }

        self.energyAnalysis_results = {}
        self.energyAnalysis.update(dR)
        
        return self.energyAnalysis
