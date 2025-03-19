class Lexer:
    def __init__(self, file)-> None:
        self.file= file

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
        return final_string

if __name__ == "__main__":
    # For debug only, don't run main
    lex= Lexer("../plugins/example/spec.conf")
    print(lex.process())
