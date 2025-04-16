#!/usr/bin/python3

import os
import sys
import subprocess

class MicroNM:
    def write(self, data, path):
        buffer= open(path, "w")
        buffer.write(data)
        buffer.close()

nm= MicroNM()

PWD= os.path.expandvars("$PWD")
SPEC=\
"""
SPEC:
~~~~~
spec file example, change this to what suits you

$name {"plugin name"};
$greet {"template-plugin"};
$logic {"logic"};
$version {"1.0"};
"""

LOGIC=\
"""
class Logic:
    def recv(self, ctx):
        data= ctx.data
"""

BUILDER=\
"""
#!/usr/bin/python3

import zipfile
import os

class MicroNM:
    def write(self, data: str, path: str):
        buffer= open(path, "w")
        buffer.write(data)
        buffer.close()

    def read(self, path: str)-> str:
        buffer= open(path, "r")
        data= buffer.read()
        buffer.close()
        return data

nm= MicroNM()

class Lexer:
    def __init__(self, file)-> None:
        self.file= file
        self.processed= ""

        buffer= open(self.file, "r")
        self.data= buffer.read()
        buffer.close()

    def process(self)-> str:
        sline= self.data.split("\\n")
        lines= []
        for line in sline:
            if line == "":
                continue
            if line[0] == "$":
                lines.append(line)
        i= 0
        for line in lines:
            lines[i]= line.split(";")[0]+";"
            i= i+1
        self.data= ""
        for line in lines:
            self.data= self.data + line
        clean_string= self.data.replace("\\n", "").replace("\\t", "")
        stop= False
        final_string= ""
        for c in clean_string:
            if c == '"':
                stop= not stop
            if c == " " and not stop:
                continue
            final_string= final_string + c

        self.processed= final_string
        return final_string

def main_func():
    if os.path.exists("./spec.conf"):
        lex= Lexer("./spec.conf")
        raw= lex.process()
        sections= raw.split("$")
        logic= ""
        name= ""
        version= ""
        for section in sections:
            if "logic" in section:
                logic= section.split("logic{", 1)[1].split("}", 1)[0]
                logic= logic[:-1]
                logic= logic.split(logic[0], 1)[1]
                break
        for section in sections:
            if "name" in section:
                name= section.split("name{", 1)[1].split("}", 1)[0]
                name= name[:-1]
                name= name.split(name[0], 1)[1]
                break
        for section in sections:
            if "version" in section:
                version= section.split("version{", 1)[1].split("}", 1)[0]
                version= version[:-1]
                version= version.split(version[0], 1)[1]
                break

        if name == "":
            print("name not defined in spec.")
            exit(1)

        if version == "":
            print("version not defined in spec.")
            exit(1)

        name= name.replace(" ", "_")
        filename= f"{name}-{version}.ncp".lower()

        if os.path.exists(f"./{logic}.py"):
            try:
                os.mkdir("build")
            except:
                pass

            try:
                zf= zipfile.ZipFile("./build/"+filename, mode="w")
                zf.writestr("spec.conf", nm.read("./spec.conf"))
                zf.writestr(logic+".py", nm.read(f"./{logic}.py"))
                zf.close()
                print("build successful, file: ./build/"+filename)
                exit(0)
            except Exception as e:
                print("build failed, error:")
                print("~~~~~~~~~~~~~~~~~~~~")
                print(e)
                exit(1)
        else:
            print("logic not found.")
            exit(0)
    else:
        print("spec not found.")
        exit(1)

if __name__ == '__main__':
    main_func()
"""

SPEC= SPEC.split("\n", 1)[1]
LOGIC= LOGIC.split("\n", 1)[1]
BUILDER= BUILDER.split("\n", 1)[1]

def main_func(PWD= PWD):
    if os.path.exists(PWD+"/spec.conf"):
        print("this folder already has a NekoConnect plugin.")
        exit(1)
    create_template(PWD)

def create_template(PWD= PWD):
    subprocess.getoutput("git init " + PWD)
    nm.write(SPEC, PWD+"/spec.conf")
    nm.write(LOGIC, PWD+"/logic.py")
    nm.write(BUILDER, PWD+"/make")
    subprocess.getoutput(f"chmod +x {PWD}/make")

if __name__ == '__main__':
    if "--help" in sys.argv or "-h" in sys.argv or "-help" in sys.argv:
        print("NekoConnect Template builder")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("this script builds a ready, git initialized, plugin template for NekoConnect")
        print("you may run this script with no arguments, or a single argument specifying the project name")
        print("")
        print("examples:")
        print("---------")
        print("create_nekoconnect_plugin_template.py")
        print("create_nekoconnect_plugin_template.py project-name")
        exit(0)
    if len(sys.argv) == 2:
        PWD= PWD+"/"+sys.argv[1]
        try:
            os.mkdir(sys.argv[1])
        except:
            pass
        main_func(PWD)
    elif len(sys.argv) >2:
        print("incorrect usage, please refer to the --help")
        exit(0)
    else:
        main_func()
