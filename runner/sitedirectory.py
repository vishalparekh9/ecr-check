import os
import importlib
from importlib.machinery import SourceFileLoader
import sys
sys.path.append('/usr/src/app/scrapers/')
class SITEDIRECTORY(object):
    def __init__(self,site):
        self.site = site
        self.folderpath = "/usr/src/app/scrapers"
        self.foldername = "scrapers."

    #Function will get all files names
    def get_py_files(self, src):
        cwd = os.getcwd() # Current Working directory
        py_files = [] 
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(cwd, root, file))
        return py_files


    #Function will import the script automatically based on token
    def get_object(self):
        my_py_files = self.get_py_files(self.folderpath)
        output = []
        files = []
        for py_file in my_py_files:
            module_name = py_file.replace(self.folderpath+'/' , '').replace('.py','')
            #commented on 22-02-2022
            #module_name = os.path.split(py_file)[-1].strip(".py")
            try:
                imported_module =  SourceFileLoader(module_name,"/usr/src/app/scrapers/"+module_name+".py").load_module()
                output.append(imported_module.token)
                files.append(module_name+".py")
            except:
                pass

        return output, files