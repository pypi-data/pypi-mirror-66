# Farm GHG calculation based on Penn State University "FEAT" model.
# python3.7+ code by Pasquale Papparella
#
# Contact: pasquale.papparella@pm.me
# see LICENSE file.

import math      
from decimal import getcontext
from numpy import divide, multiply, add, subtract
import feat_psu.feat_nrg as ea
from feat_psu.feat_util import recursive_items

class GHGAnalysis(object):    
    
    '''
    
    Main class for GHG calculation.

    Original FEAT Model from: 
    Camargo, G.G.T., Ryan, M.R., Richard, T.L., 2013. Energy use and greenhouse gas emissions from crop production using the farm energy analysis tool. BioScience, 63, 263-273.
    
    FEAT Model is licensed under a Creative Commons Attribution 4.0 International License.
    
    '''      
                                   
    def ghg_n(self):
        
        '''
        Total GHG emissions: N fertilizer application. [kgCO2e]
        '''
         
        n_year = float(self.ag["n_rate"] * self.field_area * self.k_params["ghg_n_k"])        
        return n_year
    
    def ghg_p2o5(self):
        
        '''
        Total GHG emissions: P2O5 fertilizer application. [kgCO2e]
        '''
        
        p2o5_year = float(self.ag["p_rate"] * self.field_area * self.k_params["ghg_p2o5_k"])        
        return p2o5_year
    
    def ghg_k2o(self):
        
        '''
        Total GHG emissions: K2O fertilizer application. [kgCO2e]
        '''
        
        k2o_year = float(self.ag["k_rate"] * self.field_area * self.k_params["ghg_k2o_k"])        
        return k2o_year
    
    def ghg_lime(self):
        
        '''
        Total GHG emissions: agricultural limestone (CaCO3) application. [kgCO2e]
        '''
            
        lime_year = float(self.ag["lime_rate"]*self.field_area*self.k_params["ghg_lime_k"])        
        return lime_year
    
    def ghg_seeding(self):
        
        '''
        Total GHG emissions: seeding sctivity. [kgCO2e]
        '''
        
        seeding_year = float(self.ag["seeding_rate"] * self.field_area * self.k_params["ghg_seeding_k"])        
        return seeding_year
    
    def ghg_herbicide(self):
        
        '''
        Total GHG emissions: herbicide application. [kgCO2e]
        '''
        
        herb_year = float(self.ag["herbicide_rate"] * self.field_area * self.k_params["ghg_herbicide_k"])        
        return herb_year
    
    def ghg_insecticide(self):    
        
        '''
        Total GHG emissions: insecticide application. [kgCO2e]
        '''
        
        inse_year = float(self.ag["insecticide_rate"] * self.field_area * self.k_params["ghg_insecticide_k"])        
        return inse_year
    
    def ghg_fuel_use(self):
        
        '''
        Total GHG emissions: fuel use in farming activities. [kgCO2e]
        '''
        
        fuel_use_year = float( self.ag["fuel_use_rate"] * self.field_area * self.k_params["ghg_fuel_use_k"] )        
        return fuel_use_year
    
    def ghg_drying(self):
        
        '''
        Total GHG emissions: drying energy. [kgCO2e]
        '''
                
        drying_year = float( self.nrg_drying * self.k_params["ghg_drying_k"] )    
        return drying_year
    
    def ghg_transportation(self):
        
        '''
        Total GHG emissions: transportation of inputs. [kgCO2e]
        '''
        
        ag = self.ag
        del ag['fuel_use_rate']
        
        t = [ float(value) for key,value in recursive_items(ag) if key in self.inputs ]
        total = float( round( sum( t ), 9 ) * self.k_params["ghg_transp_k"] * self.field_area )
        return total
    
    def ghg_n2o_ipcc(self):
        
        '''
        Total GHG emissions: N2O ghg emission from fertilizer application, IPCC. [kgCO2e]
        '''
               
        n_tot = float( self.ag["n_rate"] * self.field_area )
        
        # Auxiliary parameters
        n2o_aux = float( self.k_params["n2o_gwp_k"] * self.k_params["n2o_n2o_to_n_k"] )
        n2o_aux_ab = float( self.k_params["n2o_add_org_k"] * n2o_aux * 1000 )
        n2o_aux_bl = float( self.k_params["n2o_n_lr_k"] * self.k_params["n2o_frac_lr_k"] * n2o_aux * 1000)
        n2o_aux_sl = float( self.ag["crop_dm_production"] * self.k_params["n2o_slope_k"] + self.k_params["n2o_intercept_k"] )
        dm_aux = float( ( 1 - self.ag["residue_rate"] ) )
        
        livestock = float( 0.0 ) # TODO, livestock module
        
        # N2O calculation according to IPCC 2006 directives with 2019 refinement        
        ghg_N2O_ipcc = {    
            
                "n2o_direct_emission_ipcc" : float(n_tot * self.k_params["n2o_add_org_k"] * n2o_aux),
                
                "n2o_indirect_volatization_ipcc" : float( n_tot * n2o_aux * self.k_params["n2o_n_vol_k"] * self.k_params["n2o_frac_s_k"] ),
                
                "n2o_indirect_leaching_ipcc" : float( n_tot * ( n2o_aux_bl * 0.001 ) ), # n2o_aux*self.k_params["frac_lr_k"]*self.k_params["n_lr_k"],
                
                "n2o_manure_ipcc" : livestock,            
                
                "n2o_direct_above_ground_ipcc" : float( ( n2o_aux_sl )* dm_aux * ( self.k_params["n2o_n_abg_res_k"] * n2o_aux_ab ) ),            
                
                "n2o_direct_below_ground_ipcc" : float( ( n2o_aux_sl * dm_aux + self.ag["crop_dm_production"] ) * ( self.k_params["n2o_n_ab_ratio_res_k"] * \
                                                self.k_params["n2o_n_beg_res_k"]) * n2o_aux_ab ),            
                
                "n2o_indirect_above_ground_ipcc" : float( n2o_aux_sl * dm_aux * self.k_params["n2o_n_abg_res_k"] * n2o_aux_bl ),            
                
                "n2o_indirect_below_ground_ipcc" : float( ( n2o_aux_sl * dm_aux + self.ag["crop_dm_production"] ) * ( self.k_params["n2o_n_ab_ratio_res_k"] * \
                                                self.k_params["n2o_n_beg_res_k"]) * n2o_aux_bl )
        }
        
        if self.ag["n_rate"] == 0:
            # set to zero if no N rate
            ghg_N2O_additional = { 
                
                "n2o_from_hoben": float(0.0),                
                "n2o_from_vangr": float(0.0)
            
            }
            
        else:    
            # N2O additional methods from literatures         
            ghg_N2O_additional = {                           
            
                "n2o_from_hoben": float( ( ( 4.55 * math.exp( 0.0064 * self.ag["n_rate"] ) * \
                                          ( self.k_params["n2o_n2o_to_n_k"] * 0.001 ) ) * self.k_params["n2o_gwp_k"] ) * 365.4 ),
                "n2o_from_vangr": float( ( 1.27 + 0.023 * math.exp( 0.0175 * self.ag["n_rate"] )* \
                                         self.k_params["n2o_n2o_to_n_k"] ) * self.k_params["n2o_gwp_k"] )
            }  
        
        # Make an empty self object and populate with results        
        self.ghg_N2O_results = dict()
        self.ghg_N2O_results.update(ghg_N2O_ipcc)
        self.ghg_N2O_results.update(ghg_N2O_additional)   
        
        return float( sum ( list ( ghg_N2O_ipcc.values() ) ) )        
             
        
    def _run_analysis(self, ag, k_params, inputs, tot_nrg_out, nrg_drying):
        
        '''
        
        Run GHG analysis
        
        '''
        
        getcontext().prec = 9
        
        self.ag = dict(ag)
        self.k_params = dict(k_params)
        
        self.inputs = inputs
        self.field_area = self.ag['field_area']
        self.nrg_drying = nrg_drying
        
        # Evaluate every function in ghg class
        y, gR = [], {}
        for f in dir(self):
            result = getattr(self, f)
            if not f.startswith('_') and hasattr(result, '__call__'):
                i = result()
                y.append(i)
                gR[f]=i
                
        y = sum(y)
                
        # Make overall calculations
        self.ghgAnalysis_results = {  
            
            "tot_ghg_crop" : float( y ),
            
            "tot_ghg_ha_crop" : float( y / self.field_area ),
            
            "tot_ghg_ha_day_crop": float( y / ( self.field_area * self.ag['growth_time'] ) ) if self.ag['growth_time'] is not None else 0.0,
            
            "tot_ghg_kg_crop": float( ( y / ( ( self.ag['yield_rate'] * self.field_area * 1000 ) ) ) if self.ag['yield_rate'] != 0.0 else 0.0 ),
            
            "tot_ghg_intensity_crop" : float( ( ( y / self.field_area ) * ( 1 / tot_nrg_out) ) if tot_nrg_out != 0.0 else 0.0 )
        
        }            
        
        self.ghgAnalysis_results.update(gR)
        self.ghgAnalysis_results.update(self.ghg_N2O_results)
        
        return self.ghgAnalysis_results     