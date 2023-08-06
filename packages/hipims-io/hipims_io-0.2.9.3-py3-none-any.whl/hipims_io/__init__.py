#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init
To do:
    initialize a package
Created on Wed Apr  1 14:56:15 2020

@author: Xiaodong Ming
"""
import gzip
import pickle
import pkg_resources
import numpy as np
from .InputHipims import InputHipims
from .OutputHipims import OutputHipims
from .Raster import Raster

def demo_input(set_example_inputs=True, figname=None, dpi=200, **kwargs):
    """ A demonstration to generate a hipims input object
    set_example_inputs: (True|False) if True, initial condition, boundary
        condition, rainfall source, and gauge postion will be set to the input 
        object according to sample data.
    figname: (string) if given, a domain map will saved
    """
    dem_file = pkg_resources.resource_filename(__name__,
                                             'sample/Example_DEM.asc')
    obj_in = InputHipims(dem_data=dem_file)
    if set_example_inputs:
        __set_defaul_input(obj_in)
    # show model summary print(obj_in)
    obj_in.Summary.display()
    fig, ax = obj_in.domain_show(relocate=True, scale_ratio=1000, 
                                 cax_str='DEM (m)', **kwargs)
    ax.set_title('The Upper Lee catchment')
    if figname is not None:
        fig.savefig(figname, dpi=dpi)
    return obj_in

def demo_output(case_folder, num_of_sections=1):
    """ A demonstration to generate a hipims output object
    a input folder and files must be created before using this function
    """
    obj_out = OutputHipims(case_folder=case_folder,
                           num_of_sections=num_of_sections)
    return obj_out

def demo_raster(figname=None):
    """ A demonstration to read and show raster files
    figname: the file name to save the figure
    """
    dem_file = pkg_resources.resource_filename(__name__,
                                             'sample/Example_DEM.asc')
    obj_ras = Raster(dem_file)
    fig, ax = obj_ras.mapshow(figname=figname, relocate=True, scale_ratio=1000)
    ax.set_title('The Upper Lee catchment DEM (mAOD)')
    return obj_ras

def get_sample_data():
    """ Get sample data for demonstartion
    Return:
        obj_ras: a DEM raster object
        demo_data: a dictionary with boundary_condition, rain_source, and 
            gauges_pos data
    """
    dem_file = pkg_resources.resource_filename(__name__,
                                             'sample/Example_DEM.asc')
    obj_ras = Raster(dem_file)
    demo_data_file = pkg_resources.resource_filename(__name__,
                                             'sample/Example_data.npy')
    demo_data = np.load(demo_data_file, allow_pickle='TRUE').item()
    return obj_ras, demo_data

def load_object(file_name):
    """ Read a pickle file as an InputHipims/OutputHipims object
    """
    #read an object file
    try:
        with gzip.open(file_name, 'rb') as input_file:
            obj = pickle.load(input_file)
    except:
        with open(file_name, 'rb') as input_file:
            obj = pickle.load(input_file)
    print(file_name+' loaded')
    return obj

def save_object(obj, file_name, compression=True):
    """ Save an InputHipims/OutputHipims object to a pickle file 
    """
    # Overwrites any existing file.
    if compression:
        with gzip.open(file_name, 'wb') as output_file:
            pickle.dump(obj, output_file, pickle.HIGHEST_PROTOCOL)
    else:
        with open(file_name, 'wb') as output_file:
            pickle.dump(obj, output_file, pickle.HIGHEST_PROTOCOL)
    print(file_name+' has been saved')

def clean_output(case_folder, num_of_sections, file_tag='*'):
    """ delete contents in output folder(s)
    """
    import os
    if case_folder[-1]!='/':
            case_folder = case_folder+'/'
    if num_of_sections==1:
        files_to_remove = case_folder+'/output/'+file_tag
        os.system('rm '+files_to_remove)
    else:    
        for i in range(num_of_sections):
            files_to_remove = case_folder+str(i)+'/output/'+file_tag
            os.system('rm '+files_to_remove)

def copy_input_obj(obj_in):
    """Copy the an object of class InputHipims
    """
    import copy
    dem_data = Raster(array=obj_in.Raster.array, header=obj_in.Raster.header)
    num_of_sections = obj_in.num_of_sections
    case_folder = obj_in.case_folder
    # initialize a new object
    obj_copy = InputHipims(dem_data=dem_data, num_of_sections=num_of_sections,
                           case_folder=case_folder)
    attr_dict = copy.deepcopy(obj_in.__dict__)
    del attr_dict['Raster']
    del attr_dict['Boundary']
    del attr_dict['Summary']
    del attr_dict['Sections']
    # set object attributes
    for key in attr_dict.keys():
        obj_copy.__dict__[key] = copy.deepcopy(attr_dict[key])
    # set boundary conditions
    boundary_list = obj_in.Boundary.boundary_list
    outline_boundary = obj_in.Boundary.outline_boundary
    obj_copy.set_boundary_condition(boundary_list, outline_boundary)
    # copy summary
    summary_infor = obj_in.Summary.information_dict
    infor_keys = list(summary_infor.keys())
    iloc = 0
    for i in range(len(infor_keys)):
        if infor_keys[i] == 'gauges_pos':
            iloc = i
    infor_keys = infor_keys[iloc+1:]
    for key in infor_keys:
        obj_copy.Summary.add_items(key, summary_infor[key])
    return obj_copy
    
# =============private functions==================
def __set_defaul_input(obj_in):
    """Set some default values for an InputHipims object
    """
    # load data for the demo
    demo_data_file = pkg_resources.resource_filename(__name__,
                                             'sample/Example_data.npy')
    demo_data = np.load(demo_data_file, allow_pickle='TRUE').item()
    # define initial condition
    h0 = obj_in.Raster.array+0
    h0[np.isnan(h0)] = 0
    h0[h0 < 50] = 0
    h0[h0 >= 50] = 1
    # set initial water depth (h0) and velocity (hU0x, hU0y)
    obj_in.set_parameter('h0', h0)
    obj_in.set_parameter('hU0x', h0*0.0001)
    obj_in.set_parameter('hU0y', h0*0.0002)
    # define boundary condition
    bound_list = demo_data['boundary_condition']
    obj_in.set_boundary_condition(bound_list, outline_boundary='fall')
    # define and set rainfall mask and source (two rainfall sources)
    rain_source = demo_data['rain_source']
    obj_in.set_rainfall(rain_mask=0, rain_source=rain_source)
    # define and set monitor positions
    gauges_pos = demo_data['gauges_pos']
    obj_in.set_gauges_position(gauges_pos)