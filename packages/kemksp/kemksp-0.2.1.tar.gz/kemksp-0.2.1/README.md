<h1>KEM</h1>

Kem is a Python 3 based Programm to manage your Mods.
You can add and remove mods to your libary and install and uninstall them afterwards.

When you uninstall a mod it will only remove files which are only in the dependencys of this mod.
so you can easily uninstall mods without watching out for dependencies of other mods.

https://github.com/kontiko/Kerbal-Extension-Manager

Step by step tutorial:
1.  a) use "kme add \<modname> \<file1> \<file2>" with all files which are needed for this mod as argument*
    b) use "kme add \<modname>" without an argument to open the folder and drag all files in there*
    *if the mod depends on another mod put it also into there
2. use "kme install \<modname>" to install it

commands:  
  
add \<modname> \<file1> \<file2> ... -  adds mod with these files  
add \<modname> - adds mods and open modfolder in your Fileexplorer  
remove \<modname> - removes mod  
install \<modname>  
uninstall \<modname>  
list - list all added mods  
installed - list all installed mods   
