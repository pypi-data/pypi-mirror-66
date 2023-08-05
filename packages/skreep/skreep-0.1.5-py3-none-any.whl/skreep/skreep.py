from selenium import webdriver
from time import sleep
from skreep.download import dl

class Skreep:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--log-level=3')
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        self.driver = webdriver.Chrome(executable_path='.\\chromedriver.exe', options=options)
    
    # -- old version
    def quit(self):
        self.driver.quit()
        
    def get(self, url, sc=0):
    
        if url:
            self.driver.get(url)
            sleep(sc)
            
        else:
            print('error datasheet')
            self.quit()
            
            return
        
    def tag(self, *args, set='default', sc=0):
        if 'default' == set:
            tag_name = self.driver.find_element_by_tag_name(args[0])
            sleep(sc)
            return tag_name

        if 'in' == set:
            tag_name = args[0].find_element_by_tag_name(args[1])
            sleep(sc)
            return tag_name
 
    def cls(self, *args, set='default', sc=0):
        if 'default' == set:
            class_name = self.driver.find_element_by_class_name(args[0])
            sleep(sc)
            return class_name

        if 'in' == set:
            class_name = args[0].find_element_by_class_name(args[1])
            sleep(sc)
            return class_name

    def id(self, *args, set='default', sc=0):
        if 'default' == set:
            id_name = self.driver.find_element_by_id(args[0])
            sleep(sc)
            return id_name
        
        if 'in' == set:
            id_name = args[0].find_element_by_id(args[1])
            sleep(sc)
            return id_name

    def path(self, *args, set='default', sc=0):
        if 'default' == set:
            xpath_name = self.driver.find_element_by_xpath('//*[@'+ args[0] +']')
            sleep(sc)
            return xpath_name

        if 'in' == set:
            xpath_name = args[0].find_element_by_xpath('//*[@'+ args[1] +']')
            sleep(sc)
            return xpath_name

    def paths(self, *args, set='default', sc=0):
        if 'default' == set:
            xpath_name = self.driver.find_elements_by_xpath('//*[@'+ args[0] +']')
            sleep(sc)
            return xpath_name
            
        if 'in' == set:
            xpath_name = args[0].find_elements_by_xpath('//*[@'+ args[1] +']')
            sleep(sc)
            return xpath_name

    def img(self, *args, set="pa", sc=0):
        
        if "pa" == set:
            sleep(sc)
            return [i.get_attribute(args[1]) for i in self.driver.find_elements_by_xpath('//*[@'+ args[0] +']')]

        elif "pta" == set:
            sleep(sc)
            return [i.find_element_by_tag_name(args[1]).get_attribute(args[2]) for i in self.driver.find_elements_by_xpath('//*[@'+ args[0] +']')]

        elif "ota" == set:
            sleep(sc)
            return [i.get_attribute(args[2]) for i in args[0].find_elements_by_tag_name(args[1])]
            
    # -- old version end
    
    def scrape(self, **kwargs):
    
        H = kwargs['WAIT_SECONDS']['H']
        C = kwargs['WAIT_SECONDS']['C']
        F = kwargs['WAIT_SECONDS']['F']
        
        kwargs['IMAGES']['paths']
        kwargs['IMAGES']['tag']
        kwargs['IMAGES']['attr']
        
        if 'TP' == kwargs['TARGET'] :
            DATASHEET = kwargs['DATASHEET']
            DATASHEET_ = open(DATASHEET+'.txt', "rb")
            DATASHEET__ = DATASHEET_.readlines()
            
            for i in DATASHEET__:
                url = i.decode("utf-8").strip()
                self.driver.get(url)
                sleep(H)
                
                elimg = self.driver.find_elements_by_xpath('//*[@'+ kwargs['IMAGES']['paths'] +']')
                for elimg_ in elimg:
                    elimg__ = elimg_.find_element_by_tag_name(kwargs['IMAGES']['tag']).get_attribute(kwargs['IMAGES']['attr'])
                    dl(elimg__)
        