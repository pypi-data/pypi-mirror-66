"""
#
# Script to Validate NSG.
#
# Copyright(c) 2020, Ciena. All rights reserved.
#
"""

import glob as g
import os

import hcl


# #################VARIABLES#######################
sec_rule = 'azurerm_network_security_rule'
scope = 'source_address_prefix'
pathname = os.path.dirname(os.path.realpath('__file__'))
file_ignore = 'nsg_ignore_list'
# #################################################


def read_ignorefile(pathname, file_ignore):

    """
    It will read a file(say nsgignore passed in argument) to be ignored
    in NSG validation check. Filname would be passed as the argument
     and will store this into file variable

    """

    list_of_sg_rules_ignored = []
    try:
        with open(pathname + '/' + file_ignore, 'r') as fp:
            for line in fp:
                list_of_sg_rules_ignored.append(line.rstrip('\n'))
    except FileNotFoundError:
        pass
    return list_of_sg_rules_ignored

def scan_tf_files(pathname):
    """
    Scan or look for all the *.tf format files placed(Path passed in agument).
    It will return a list of all the files found in directory/subdirectories.
    """
    tf_filenames = []
    for tf_file in g.glob(pathname + '/**/*.tf', recursive=True):
        tf_filenames.append(tf_file)
    return tf_filenames


def read_all_files(tf_filenames):
    """
    Iterate through all the files and read all the tf files. Create a
    (tf_database)database dictionary with Key as tf filename
    and value as tf file dictionary data.

    There could be 'n' number of tf files and in case of issue in
    1 particular file it will skip that nor break.
    It is mainly because hcl load module fails in case of empty tf files.
    """
    tf_database = {}
    for tf_file in tf_filenames:
        with open(tf_file, 'r') as fp:
            try:
                tf_data = hcl.load(fp)
                tf_database[tf_file] = tf_data
            except ValueError:
                print(f'{tf_file} is not in standard terraform format')
    return tf_database


def validate_sg():
    """
    Iterate through (tf_database)database dictionary and check whether
    resource block exist in the file. Then look for further conditions
    for security rule validation for good and bad security group.
    """
    ignore_list = read_ignorefile(pathname, file_ignore)
    tf_filenames = scan_tf_files(pathname)
    tf_database = read_all_files(tf_filenames)
    
    bad_rule = 0
    for tf_file, tf_data in tf_database.items():
        for key in tf_data.keys():
            if key == 'resource':
                if sec_rule in tf_data['resource'].keys():
                    for tf_sec_resource, rule_param in tf_data['resource'][sec_rule].items():                           # noqa
                     #   print(ignore_list)
                        if rule_param['name'] not in ignore_list:
                            if rule_param['direction'].lower() == 'inbound' and rule_param['access'].lower() == 'allow':# noqa
                                if rule_param.get(scope) != '*':
                                    pass
                                else:
                                    print(f'Failure: rule {tf_sec_resource} in {tf_file}: exposed to internet.')        # noqa
                                    bad_rule += 1
                            elif rule_param['direction'].lower() == 'inbound' and rule_param['access'].lower() == 'deny': # noqa
                                print(f'Warning Deny rule defined in {tf_file}')

    """
    To avoid exit of program on finding single bad rule, using variable badrule
    Once all the security group scanned only then exit the program.
    """

    if bad_rule > 0:
        exit(1)


if __name__ == '__main__':
    validate_sg()
