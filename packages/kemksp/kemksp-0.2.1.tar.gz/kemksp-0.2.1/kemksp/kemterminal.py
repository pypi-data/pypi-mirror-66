import sys
import kemksp as cmd
def main():
    if len(sys.argv)==1 or sys.argv[1]=="help":
        cmd.help()
    elif sys.argv[1]=="add":
        if len(sys.argv)==1:
            print("Not enough arguments")
            return
        cmd.add(sys.argv[2:])
    elif sys.argv[1]=="config":
        if len(sys.argv)==1:
            print("Not enough arguments")
            return
        if sys.argv[2]=="-p"or sys.argv[2]=="--ksppath":
            if len(sys.argv)==3:
                cmd.ksppath()
            else:
                cmd.new_ksppath(sys.argv[3])
    elif sys.argv[1]=="remove":
        if len(sys.argv)==3:
            cmd.remove(sys.argv[2])
        else:
            print ("Wrong argument number. Remove has <Name of Mod> as argument")
    elif sys.argv[1]=="list":
        cmd.list()
    elif sys.argv[1]=="installed":
        cmd.installed()
    elif sys.argv[1]=="install":
        if len(sys.argv)==3:
            cmd.install(sys.argv[2])
        else:
            print ("Wrong argument number. Install has <Name of Mod> as argument")
    elif sys.argv[1]=="uninstall":
        if len(sys.argv)==3:
            cmd.uninstall(sys.argv[2])
        else:
            print ("Wrong argument number. Install has <Name of Mod> as argument")
    else:
        print("Unknown command. try <kme help>")

if __name__=="__main__":
    main()
