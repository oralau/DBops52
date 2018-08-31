import ConfigParser
import logging
import sys
import datetime

class getConfigFile():

    def getStrParameter(self,paraFile,section,parameter):

        try:
            config = ConfigParser.RawConfigParser()
            config.read(paraFile)
            return config.get(section,parameter)

        except Exception as e:

           logging.error(str(e))
           raise


    def getIntParameter(self, paraFile, section, parameter):


        try:
            config = ConfigParser.RawConfigParser()
            config.read(paraFile)
            return config.getint(section,parameter)

        except Exception as e:

            logging.error(str(e))
            raise




    def getFloatParameter(self, paraFile, section, parameter):

        try:
            config = ConfigParser.RawConfigParser()
            config.read(paraFile)
            return config.getfloat(section, parameter)

        except Exception as e:

            logging.error(str(e))
            raise


    def getBooleanParameter(self, paraFile, section, parameter):

        try:
            config = ConfigParser.RawConfigParser()
            config.read(paraFile)
            return config.getboolean(section, parameter)

        except Exception as e:

            logging.error(str(e))
            raise


    def getListParameter(self, paraFile, section, parameter):

        try:
            para_list=[]
            config = ConfigParser.RawConfigParser()
            config.read(paraFile)
            for i in str(config.get(section, parameter)).strip().split(','):
                para_list.append(i.strip())

            return para_list


                
        except Exception as e:

            logging.error(str(e))
            raise