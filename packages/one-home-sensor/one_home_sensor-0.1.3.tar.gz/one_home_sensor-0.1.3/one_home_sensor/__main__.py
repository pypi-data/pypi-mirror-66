from .onehomesensor import OneHomeSensor
import argparse
import configparser
import os
from os import path
import platform

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""
    Gets temperature, humidity and pressure from BME280 sensor on a Raspberry Pi. 
    Can push informations to a  MongpDB Atlas Storage. 
    """)
    
    # Read running arguments 
    parser.add_argument(
        '--print-only',
        default=False,
        action="store_true",
        help='Will only print the values and will not push to MongpDB Atlas Storage'
    )
    working_dir = os.getcwd()
    conf_file_default = os.path.join(working_dir, "onehomesensor.ini")
    parser.add_argument(
        '-c', '--config-file',
        default=conf_file_default,
        help='Provide custom path to configuration file'
    )
    # TODO : use os logging possibilitis / syslog ... 
    log_file_default = os.path.join("var","log" ,"onehomesensor.log")
    parser.add_argument(
        '-l', '--log-file',
        default=log_file_default,
        help='Provide custom path to logging file'
    )    
    parser.add_argument(
        '-s', '--sensor-name',
        default=platform.node(),
        help='Name of this sensor (default : hostname)'
    )   
    running_args = parser.parse_args()
    

    # Read configuration file if existe 
    mongodb_con = ""
    Config = configparser.ConfigParser()
    config_file = running_args.config_file
    if path.exists(config_file) and not running_args.print_only:
        Config.read(config_file)
        try:
            mdb_name = Config.get('MongoDBAtlasConnection', 'username')
            mdb_pswd = Config.get('MongoDBAtlasConnection', 'password')
            mdb_clus = Config.get('MongoDBAtlasConnection', 'clusterfqdn')
            mongodb_con = "mongodb+srv://{}:{}@{}/test?retryWrites=true&w=majority".format(mdb_name,mdb_pswd,mdb_clus)
        except Exception as e:
            raise Exception("Configuration file invalide : {}".format(e)) 
    elif not path.exists(config_file) and not running_args.print_only:
        raise Exception("Must provide a valide configuration file")


    # Run the app     
    MyApp = OneHomeSensor(running_args,mongodb_con)
    MyApp.run()