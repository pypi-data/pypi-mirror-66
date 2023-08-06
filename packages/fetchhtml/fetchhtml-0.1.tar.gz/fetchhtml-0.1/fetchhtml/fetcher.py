import requests
import os 
class Fetcher:
    def __init__(self):
        self.url = ""
        self.savepath = ""

    def download_html(self,savepath,filename):
       response = requests.get(self.url)
       with open(f"{savepath}/{filename}", "w") as file:
           file.seek(0)
           file.truncate()
           file.write(response.text)
           file.close()
           print(f"{filename} has successfully been saved to: \n{savepath}")

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url 
    
    
        
    
    

