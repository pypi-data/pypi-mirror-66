"""

This script contains functions to write the inversion dictionaries to the
filesystem.

:copyright:
    Lucas Sawade (lsawade@princeton.edu)
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)

Last Update: June 2019

"""

from gcmt3d.data.management.inversion_dicts \
    import create_full_inversion_dict_list
from gcmt3d.data.management.inversion_dicts \
    import create_g3d_inversion_dict_list
from gcmt3d.data.management.inversion_dicts import write_inversion_dicts
import yaml
import os


def read_yaml_file(filename):
    """read yaml file"""
    with open(filename) as fh:
        return yaml.load(fh, Loader=yaml.FullLoader)


def inversion_dictionaries(cmt_file_db, param_path):
    """ This function writes the inversion dictionaries

    :param cmt_file_db:
    :return:
    """

    # Processing param dir
    process_obs_dir = os.path.join(param_path, "ProcessObserved")
    process_syn_dir = os.path.join(param_path, "ProcessSynthetic")

    # Window param dir
    window_process_dir = os.path.join(param_path, "CreateWindows")

    # Create inversion dictionaries
    inv_dict_list, filename_list = \
        create_full_inversion_dict_list(cmt_file_db,
                                        process_obs_dir,
                                        process_syn_dir,
                                        window_process_dir)

    # Write the dictionaries
    write_inversion_dicts(inv_dict_list, filename_list)


def grid_search_dictionaries(cmt_file_db, param_path):
    """ This function writes the inversion dictionaries

    :param cmt_file_db:
    :return:
    """

    # Processing param dir
    process_obs_dir = os.path.join(param_path, "ProcessObserved")
    process_syn_dir = os.path.join(param_path, "ProcessSynthetic")

    # Window param dir
    window_process_dir = os.path.join(param_path, "CreateWindows")

    # Create inversion dictionaries
    inv_dict_list, filename_list = \
        create_g3d_inversion_dict_list(cmt_file_db,
                                       process_obs_dir,
                                       process_syn_dir,
                                       window_process_dir)

    # Write the dictionaries
    write_inversion_dicts(inv_dict_list, filename_list)
