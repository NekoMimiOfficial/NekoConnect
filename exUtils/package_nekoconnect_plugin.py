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
        sline= self.data.split("\n")
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
        clean_string= self.data.replace("\n", "").replace("\t", "")
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
