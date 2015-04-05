class Config():
    #XXX
    dict = {}
    with open("config") as configFile:
            for line in configFile:
                key = line.split("=")[0]
                value = line.split("=")[1]
                dict[key] = value
          
    @staticmethod
    def getDatapath():
        return Config.dict["datapath"].rstrip()
    
    @staticmethod
    def doPreprocess():
        return Config.dict["preprocess"] == "1"
    
    @staticmethod
    def getYamlFilename():
        return Config.dict["yaml"].rstrip() + ".yaml"