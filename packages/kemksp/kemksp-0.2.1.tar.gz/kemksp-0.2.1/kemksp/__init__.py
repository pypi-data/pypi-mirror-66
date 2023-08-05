import os
import shutil
import json
import platform
import subprocess

config = {}
import platform
import subprocess

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
def is_modinstalled(modname):
    if update_config():
        return
    if not os.path.isfile(config["ksppath"]+"kem/installed.txt"):
        os.makedirs(config["ksppath"]+"kem/",exist_ok=True)
        open(config["ksppath"]+"kem/installed.txt", 'a').close()
    file=open(config["ksppath"]+"kem/installed.txt","r")
    list=[i.replace("\n","") for i in file.readlines()]
    file.close()
    return modname in list
def update_config():
    global config
    try:
        if os.path.dirname(__file__)=="":
            with open('config.json') as json_data_file:
                config = json.load(json_data_file)
        else:
            with open(os.path.dirname(__file__)+'/config.json') as json_data_file:
                config = json.load(json_data_file)
        return False
        
    except:
        print("can't open Config file")
        return True



def add(data):
    if update_config():
        return
    modname=data[0]
    filepaths=data[1:]
    if os.path.exists(config["ksppath"]+"kem/"+modname+"/"):
        print("Mod with these name already exists")
        return
    os.makedirs(config["ksppath"]+"kem/"+modname+"/", exist_ok = True)
    for filepath in filepaths:
        print(filepath)
        
        if os.path.isfile(filepath):
            shutil.copyfile(filepath,config["ksppath"]+"kem/"+modname+"/"+filepath.split("/")[-1])
        elif os.path.isdir(filepath):
            shutil.copytree(filepath,config["ksppath"]+"kem/"+modname+"/"+filepath.split("/")[-1])
        else:
            shutil.rmtree(config["ksppath"]+"kem/"+modname+"/")
            print("File/directory '"+filepath+"' not exist end process is aborted")
    if len(filepaths)==0:
        open_file(config["ksppath"]+"kem/"+modname+"/")


def remove(modname):
    if update_config():
        return
    if os.path.exists(config["ksppath"]+"kem/"+modname):
        shutil.rmtree(config["ksppath"]+"kem/"+modname)
    else:
        print("Mod is not Available")
    update()


def new_ksppath(newpath):
    if update_config():
        return
    config["ksppath"]=newpath
    print(config["ksppath"])
    print(os.path.dirname(__file__))
    with open(os.path.dirname(__file__)+'/config.json', 'w') as outfile:
        json.dump(config,outfile)
    
def ksppath():
    if update_config():
        return
    print(config["ksppath"])
def list():
    if update_config():
        return
    os.makedirs(config["ksppath"]+"kem/",exist_ok=True)
    for mod in [f.path for f in os.scandir(config["ksppath"]+"kem") if f.is_dir()]:
        print(mod.split("/")[-1])
        
        

def install(modname):
    if update_config():
        return
    if not (config["ksppath"]+"kem/"+modname in [f.path for f in os.scandir(config["ksppath"]+"kem") if f.is_dir()]):
        print("mod not avaialable")
        return
    if is_modinstalled(modname):
        print("Mod is allready installed")
        return
    installlist=open(config["ksppath"]+"kem/installed.txt","a")
    installlist.write(modname+"\n")
    installlist.close()
    shutil.copytree(config["ksppath"]+"kem/"+modname,config["ksppath"]+"/GameData/",dirs_exist_ok=True)
    
    

def help():
    print("""helppage
add <modname> <file1> <file2> ... - adds mod with these files
remove <modname> - removes mod
install <modname>
uninstall <modname>
list - list all added mods
installed - list all installed mods
""")
def uninstall(modname):
    if update_config():
        return
    if not is_modinstalled(modname):
        print(modname+" is not installed")
        return
    file=open(config["ksppath"]+"kem/installed.txt","r")
    list=[i.replace("\n","") for i in file.readlines()]
    file.close()
    list.remove(modname)
    print(list)
    os.remove(config["ksppath"]+"kem/installed.txt")
    file=open(config["ksppath"]+"kem/installed.txt","w")
    for mod in list:
        file.write(mod + "\n")
    file.close()
    
    update()
def installed():
    if update_config():
        return
    if not os.path.isfile(config["ksppath"]+"kem/installed.txt"):
         os.makedirs(config["ksppath"]+"kem/",exist_ok=True)
         open(config["ksppath"]+"kem/installed.txt","a").close()
    file=open(config["ksppath"]+"kem/installed.txt","r")
    list=[i.replace("\n","") for i in file.readlines()]
    file.close()
    for mod in list:
        print(mod)
def update():
    dirlist=os.listdir(config["ksppath"]+"/GameData/")
    dirlist.remove("Squad")
    dirlist.remove("SquadExpansion")
    for fdir in dirlist:
        if os.path.isfile(config["ksppath"]+"GameData/"+fdir):
            os.remove(config["ksppath"]+"GameData/"+fdir)
        else:
            shutil.rmtree(config["ksppath"]+"GameData/"+fdir)
    file=open(config["ksppath"]+"kem/installed.txt","r")
    list=[i.replace("\n","") for i in file.readlines()]
    file.close()
    file=open(config["ksppath"]+"kem/installed.txt","w")
    for mod in list:
        if os.path.isdir(config["ksppath"]+"kem/"+mod):
            install(mod)
            file.write(mod+"\n")
    file.close() 
