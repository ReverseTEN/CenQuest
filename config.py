import configparser

def config():

    config= configparser.ConfigParser()
    config.read('config.ini')
    if config['Censys Api Config']['api'] =='' or config['Censys Api Config']['secret'] == '':
        print("[!] Enter your Api and Secret In Config.ini")
        exit()
    else:
        return config['Censys Api Config']['api'] , config['Censys Api Config']['secret']
