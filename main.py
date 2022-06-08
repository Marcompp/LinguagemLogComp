# -*- coding: utf-8 -*-
import sys

class FuncTable:
    def __init__(self):
        self.table = {}
    def getSymbol(self,key):
        #print("KEEEY")
        #print(key)
        if key in self.table:
            return self.table[key][0]
        else:
            print(key)
            print(self.table)
            raise Exception
    def setSymbol(self,key,value):
        if key in self.table:

            self.table[key] = [value]
        else:
            raise Exception
    def declare(self,key,value):
        if key in self.table:
            print(key)
            raise Exception
        self.table[key] = [value]
    def __str__(self):
        stringe = "Keymap = \n"
        for key in self.table:
            stringe += key + " : " + str(self.table[key]) + "\n"
        return stringe
        

ft = FuncTable()

class SymbolTable:
    def __init__(self):
        self.table = {}
    def getSymbol(self,key):
        if key in self.table:
            return self.table[key][0]
        else:
            print(key)
            print(self.table)
            raise Exception
    def setSymbol(self,key,value):
        #if key in self.table:
            self.table[key] = [value]
        #else:
        #    raise Exception
    def declare(self,key):
        if key in self.table:
            raise Exception
        self.table[key] = [""]


class Node:
    def __init__(self,value,children):
        self.value = value
        self.children = children
        #print(f'create: {self.value}')
    def Evaluate(self,st):
        pass
    def __str__(self):
        kids = ""
        if len(self.children) == 0:
            return (f'{self.value}')
        for a in range(len(self.children)):
            kids += str(self.children[a])
            if a == len(self.children) -1:
                #kids += " "
                pass
            else: 
                kids += ","
        return (f'{self.value}:[{kids}]')

class Block(Node):
    def Evaluate(self,st):
        for child in self.children:
            child.Evaluate(st)
            if child.value == "return":
                return

class BinOp(Node):
    def Evaluate(self,st):
        eval1 = self.children[0].Evaluate(st)
        eval2 = self.children[1].Evaluate(st)


        #if self.value == '.':
            #if not (isinstance(eval1, str) and isinstance(eval2, str)):
            #    raise Exception

        
        if self.value == '+':
                return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == '/':
            return int(self.children[0].Evaluate(st) / self.children[1].Evaluate(st))
        elif self.value == '*':
            return int(self.children[0].Evaluate(st) * self.children[1].Evaluate(st))
        elif self.value == '==':
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)
            #if (self.children[0].Evaluate(st) == self.children[1].Evaluate(st)):
            #    return 1
            #else:
            #    return 0
        elif self.value == '>':
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
            #if (self.children[0].Evaluate(st) > self.children[1].Evaluate(st)):
            #    return 1
            #else:
            #    return 0
        elif self.value == '<':
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
            #if (self.children[0].Evaluate(st) < self.children[1].Evaluate(st)):
            #    return 1
            #else:
            #    return 0
        elif self.value == '&&':
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)
            #if (self.children[0].Evaluate(st) and self.children[1].Evaluate(st)):
            #    return 1
            #else:
            #    return 0
        elif self.value == '||':
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
            #if (self.children[0].Evaluate(st) or self.children[1].Evaluate(st)):
            #    return 1
            #else:
            #    return 0
        elif self.value == '.':
            return f"{self.children[0].Evaluate(st)}{self.children[1].Evaluate(st)}"
        else:
            print(self.value)
            raise Exception

class MultOp(Node):
    def Evaluate(self,st):
        evals = []
        truth = True
        for child in self.children:
            truth = truth and child.Evaluate(st)
            if not truth:
                return truth
        return truth

class UnOp(Node):
    def Evaluate(self,st):
        if self.value == '+':
            return self.children[0].Evaluate(st)
        elif self.value == '-':
            return -self.children[0].Evaluate(st)
        elif self.value == '!':
            return not self.children[0].Evaluate(st)
        elif self.value == 'print':
            print(self.children[0].Evaluate(st))
        else:
            print(self.value)
            raise Exception
        
class NoOp(Node):
    def Evaluate(self,st):
        pass

class IntVal(Node):
    def Evaluate(self,st):
        return self.value

class StrVal(Node):
    def Evaluate(self,st):
        return self.value

class VarDec(Node):
    def Evaluate(self,st):
        for child in self.children:
            st.declare(child.value)

class Instanciate(Node):
    def Evaluate(self,st):
        st.setSymbol(self.children[0].value,self.children[1].Evaluate(st))

class Indentifier(Node):
    def Evaluate(self,st):
        return st.getSymbol(self.value)

class Scanf(Node):
    def Evaluate(self,st):
        return int(input())

class While(Node):
    def Evaluate(self,st):
        while(self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)

class If(Node):
    def Evaluate(self,st):
        if(self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)

class FuncDec(Node):
    def Evaluate(self,st):
        #print("funcdec")
        #print(self.children)
        ft.declare(self.children[0].children[0],self)

class FuncCall(Node):
    def Evaluate(self,st):
        #print(self)
        #print(ft)
        #print(self.children[0].children[0])
        func = ft.getSymbol(self.children[0].children[0])
        fst = SymbolTable()
        for a in range(len(self.children)-1):
            #print(self.children[a+1])
            self.children[a+1].Evaluate(fst)
        result = func.children[-1].Evaluate(fst)
        return result


class Return(Node):
    def Evaluate(self,st):
        return self.children[0].Evaluate(st)

class Token:
    def __init__(self,typ,value):
        self.typ = typ
        self.value = value

    def printoken(self):
        if self.typ == 'int':
            print(self.value)
        else:
            print(self.typ)

class Tokeniser:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        #print(self.position)
        self.actual = Token('','')
        self.previous = [0,Token('','')]
        self.reserved = ["print","if","else","while","input","return","var"]
        #self.types = ["int","str","void"]

    def consume(self):
        self.actual = Token('','')
        
    def selectPrevious(self):
        self.position = self.previous[0]
        self.actual = Token(self.previous[1],self.previous[2])

    def selectNext(self):
        self.previous = [self.position,self.actual.typ,self.actual.value]
        isnumber = False
        isident = False
        isstr = False
        ivalor = ""
        nvalor = 0
        while self.position < len(self.origin):
            if isstr:
                if self.origin[self.position]=='"':
                    self.position += 1
                    self.actual = Token('str',ivalor)
                    return
                else:
                    ivalor += self.origin[self.position]
            else:

                if self.origin[self.position].isalpha() or self.origin[self.position]=='_':
                    isident = True
                if isident:
                    if isnumber:
                        raise Exception
                    if self.origin[self.position].isalpha() or self.origin[self.position]=='_' or self.origin[self.position].isdigit():
                        ivalor += self.origin[self.position]
                    else:
                        isident = False
                        #print("Position: "+str(self.position))
                        #self.actual.printoken()
                        if ivalor in self.reserved:
                            self.actual = Token(ivalor,'')
                        #elif ivalor in self.types:
                        #    self.actual = Token('type',ivalor)
                        else:
                            self.actual = Token('ident',ivalor)
                        return
                else:
                    if self.origin[self.position].isdigit():
                        isnumber = True
                        nvalor = nvalor*10+int(self.origin[self.position])
                    elif isnumber:
                        self.actual = Token('int',nvalor)
                        isnumber = False
                        #print("Position: "+str(self.position))
                        #self.actual.printoken()
                        return
                if self.origin[self.position] == "/":
                    self.actual = Token('/','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "*":
                    self.actual = Token('*','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "-":
                    self.actual = Token('-','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "+":
                    self.actual = Token('+','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "(":
                    self.actual = Token('(','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == ")":
                    self.actual = Token(')','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "{":
                    self.actual = Token('{','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "}":
                    self.actual = Token('}','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == '\n':
                    self.actual = Token(';','')
                    self.position += 1
                    return
                if self.origin[self.position] == ";":
                    self.actual = Token(';','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == ">":
                    self.actual = Token('>','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "<":
                    self.actual = Token('<','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == "!":
                    self.actual = Token('!','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == ".":
                    self.actual = Token('.','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return
                if self.origin[self.position] == ",":
                    self.actual = Token(',','')
                    self.position += 1
                    #print("Position: "+str(self.position))
                    #self.actual.printoken()
                    return

                if self.origin[self.position] == "&":
                    self.position += 1
                    if self.origin[self.position] == "&":
                        self.actual = Token('&&','')
                        self.position += 1
                    else:
                        raise Exception
                    return
                if self.origin[self.position] == "|":
                    self.position += 1
                    if self.origin[self.position] == "|":
                        self.actual = Token('||','')
                        self.position += 1
                    else:
                        raise Exception
                    return
                if self.origin[self.position] == "=":
                    self.position += 1
                    if self.origin[self.position] == "=":
                        self.actual = Token('==','')
                        self.position += 1
                    else:
                        self.actual = Token('=','')
                    return


                if self.origin[self.position] == '"':
                    isstr = True
            self.position += 1

        return
        
            
            

class Parser:
    def __init__(self,origin):
        self.tokens = None

    def parseProgram(self):
        kids = []
        #print("enter program token: "+ self.tokens.actual.typ)
        while self.tokens.position < len(self.tokens.origin):
            if (self.tokens.actual.typ) != 'ident':
                self.tokens.selectNext()
            kids.append(self.parseDeclaration())
        kids.append(FuncCall("main",[VarDec("void",["main"])]))
        return Block('',kids)

    def parseDeclaration(self):
        kids = []
        #print("enter declar token: "+ self.tokens.actual.typ)
        #if self.tokens.actual.typ == 'def':
        #    typ = self.tokens.actual.value
        #    self.tokens.selectNext()
        if self.tokens.actual.typ == 'ident':
                ident = self.tokens.actual.value
                kids.append(VarDec(self.tokens.actual.value,[self.tokens.actual.value]))
                self.tokens.selectNext()
                if self.tokens.actual.typ == '(':
                    self.tokens.selectNext()
                    if self.tokens.actual.typ != ')':
                        kids.append(self.parseRelExpression())
                        while  self.tokens.actual.typ == ',':
                            self.tokens.selectNext()
                            kids.append(self.parseRelExpression())
                    if self.tokens.actual.typ == ')':
                        self.tokens.selectNext()
        kids.append(self.parseBlock())


        return FuncDec(ident,kids)

    def parseBlock(self):
        while(self.tokens.actual.typ == ';'):
            self.tokens.selectNext()
        kids = []
        #print("enter block token: "+ self.tokens.actual.typ)
        if self.tokens.actual.typ == '{':
            self.tokens.selectNext()
            while self.tokens.actual.typ != '}':
                #print(self.tokens.actual.typ)
                kids.append(self.parseStatement())
                #print(kids[-1])
                if self.tokens.actual.typ != '}':
                    self.tokens.selectNext()
                #self.tokens.selectNext()
            self.tokens.selectNext()
            #print(Block('',kids))
            return Block('',kids)
        else:
            print(self.tokens.actual.typ)
            print(self.tokens.actual.value)
            raise Exception

    def parseStatement(self):
        #print("enter statement token: "+ self.tokens.actual.typ)
        if self.tokens.actual.typ == ';':
            return NoOp(self.tokens.actual.typ,[])
        elif self.tokens.actual.typ == 'ident':
            ident = Indentifier(self.tokens.actual.value,[])
            self.tokens.selectNext()
            if self.tokens.actual.typ == '=':
                self.tokens.selectNext()
                resultado = Instanciate('=',[ident,self.parseRelExpression()])
                #print("exit statement token: "+ self.tokens.actual.typ)
                if self.tokens.actual.typ == ';':
                    #print("Statement: "+ str(resultado))
                    return resultado
                else:
                    print(self.tokens.actual.typ)
                    raise Exception
            elif self.tokens.actual.typ == '(':
                kids =[]
                self.tokens.selectNext()
                if self.tokens.actual.typ != ')':
                    kids.append(self.parseRelExpression())
                    while  self.tokens.actual.typ == ',':
                        self.tokens.selectNext()
                        kids.append(self.parseRelExpression())
                if self.tokens.actual.typ == ')':
                        self.tokens.selectNext()
                resultado = FuncCall(ident,kids)
                #print("exit statement token: "+ self.tokens.actual.typ)
                if self.tokens.actual.typ == ';':
                        #print("Statement: "+ str(resultado))
                        return resultado
                else:
                        print(self.tokens.actual.typ)
                        raise (Exception)
            else:
                print(self.tokens.actual.typ)
                print(self.tokens.actual.value)
                #return BinOp('=',["EERRRROORR",IntVal(0,[])])
                raise Exception
        elif self.tokens.actual.typ == 'print':
            self.tokens.selectNext()
            if self.tokens.actual.typ == '(':
                self.tokens.selectNext()
                resultado = UnOp('print',[self.parseRelExpression()])
                #print("exit statement token: "+ self.tokens.actual.typ)
                if self.tokens.actual.typ == ')':
                        self.tokens.selectNext()
                if self.tokens.actual.typ == ';':
                        #print("Statement: "+ str(resultado))
                        return resultado
                else:
                        print(self.tokens.actual.typ)
                        raise (Exception)
            else:
                print(self.tokens.actual.typ)
                raise (Exception)
        elif self.tokens.actual.typ == 'while':
            self.tokens.selectNext()
            if not (self.tokens.actual.typ == '('):
                raise Exception
            self.tokens.selectNext()
            condit = self.parseRelExpression()
            if self.tokens.actual.typ == ')':
                self.tokens.selectNext()
            resultado = While('while',[condit,self.parseStatement()])
            #print(resultado)
            if self.tokens.actual.typ != '}':
                self.tokens.selectPrevious()
                if self.tokens.actual.typ == '}':
                    self.tokens.consume()
            #    self.tokens.selectNext()
            #print("Statement: "+ str(resultado))
            return resultado
        elif self.tokens.actual.typ == 'if':
            self.tokens.selectNext()
            if not (self.tokens.actual.typ == '('):
                raise Exception

            #self.tokens.selectNext()
            kids = [self.parseRelExpression()]

            if self.tokens.actual.typ == ')':
                self.tokens.selectNext()
            while self.tokens.actual.typ == ';':
                self.tokens.selectNext()
            kids.append(self.parseStatement())
            while self.tokens.actual.typ == ';':
                self.tokens.selectNext()
            if self.tokens.actual.typ == 'else':
                self.tokens.selectNext()
                kids.append(self.parseStatement())
                if self.tokens.actual.typ == 'else':
                    raise Exception
            #else:
            self.tokens.selectPrevious()
                #print(self.tokens.actual.typ)
            if self.tokens.actual.typ == '}':
                    self.tokens.consume()
            resultado = If('if',kids)
            #print("Statement: "+ str(resultado))
            return resultado

        elif self.tokens.actual.typ == 'return':
            if self.tokens.actual.typ == '(':
                self.tokens.selectNext()
                resultado = Return('return',[self.parseRelExpression()])
                #print("exit statement token: "+ self.tokens.actual.typ)
                if self.tokens.actual.typ == ')':
                        self.tokens.selectNext()
                if self.tokens.actual.typ == ';':
                        #print("Statement: "+ str(resultado))
                        return resultado
                else:
                        print(self.tokens.actual.typ)
                        raise (Exception)
        else:
            #print("BLOOCK")
            #print(self.tokens.actual.typ)
            return self.parseBlock()

    def parseRelExpression(self):
        #print("enter relexpression token: "+ self.tokens.actual.typ)
        resultados = []
        
        resultado = self.parseExpression()
        prevExp = resultado
        while self.tokens.actual.typ == '==' or self.tokens.actual.typ == '<' or self.tokens.actual.typ == '>':
            if (self.tokens.position > len(self.tokens.origin)-1):
                raise Exception
            optype = self.tokens.actual.typ
            self.tokens.selectNext()
            newExp = self.parseExpression()
            resultados.append(BinOp(optype,[prevExp,newExp]))
            prevExp = newExp
        if len(resultados)>0:
            return MultOp("",resultados)
        #print("RelExpression: "+ str(resultado))
        return resultado


    def parseExpression(self):
        #print("enter expression token: "+ self.tokens.actual.typ)
        resultado = self.parseTerm()
        #if self.tokens.actual.typ == ')':
                #print("Expression: "+str(resultado))
        #        self.tokens.selectNext()
                #return resultado

        #repeats = 0
        while self.tokens.actual.typ == '+' or self.tokens.actual.typ == '-' or self.tokens.actual.typ == '||' or self.tokens.actual.typ == '.':
            #repeats +=1
            #print("repeats: "+str(repeats))

            if (self.tokens.position > len(self.tokens.origin)-1):
                raise Exception
            optype = self.tokens.actual.typ
            #print("node1: " + str(resultado.value))
            self.tokens.selectNext()
            resultado = BinOp(optype,[resultado,self.parseTerm()])
            #print("node2: " + str(resultado.children[1].value))
            #print("node3: " + str(resultado.value))

            #self.tokens.selectNext()

            #if self.tokens.actual.typ == ')':
                #print("Expression): "+str(resultado))
                #return resultado

        #print("Expression: "+ str(resultado))
        return resultado



    def parseTerm(self):
        #print("enter term token: "+ self.tokens.actual.typ)
        resultado = self.parseFactor()
        if self.tokens.actual.typ == '{':
            return resultado
        self.tokens.selectNext()
        #print(self.tokens.actual.typ)
                
        while self.tokens.actual.typ == '*' or self.tokens.actual.typ == '/' or self.tokens.actual.typ == '&&':
            
            if (self.tokens.position > len(self.tokens.origin)-1):
                raise Exception
            
            #print("node1: " + str(resultado.value))
            optype = self.tokens.actual.typ
            self.tokens.selectNext()
            resultado = BinOp(optype,[resultado,self.parseFactor()])
            #print("node2: " + str(resultado.children[1].value))
            #print("node3: " + str(resultado.value))

            #self.tokens.selectNext()
            #if self.tokens.actual.typ == ')':
                #return resultado
            if (self.tokens.actual.typ != '*') and (self.tokens.actual.typ != '/') and (self.tokens.actual.typ != '&&'):
                self.tokens.selectNext()
                
        #print("Term: "+str(resultado))
        return resultado

    def parseFactor(self):
        #print("enter factor token: "+ self.tokens.actual.typ)
        
        if self.tokens.actual.typ == 'int':
            #print("node: " + str(resultado.value))
            resultado = IntVal(self.tokens.actual.value,[])
        elif self.tokens.actual.typ == 'str':
            resultado = StrVal(self.tokens.actual.value,[])
        elif self.tokens.actual.typ == 'ident':
            #print("node: " + str(resultado.value))
            ident = self.tokens.actual.value
            self.tokens.selectNext()
            if self.tokens.actual.typ != '(':
                self.tokens.selectPrevious()
                resultado = Indentifier(ident,[])
            else:
                kids =[]
                self.tokens.selectNext()
                if self.tokens.actual.typ != ')':
                    kids.append(self.parseRelExpression())
                    while  self.tokens.actual.typ == ',':
                        self.tokens.selectNext()
                        kids.append(self.parseRelExpression())
                if self.tokens.actual.typ == ')':
                        self.tokens.selectNext()
                resultado = FuncCall(ident,kids)
            

        
        elif self.tokens.actual.typ == '+' or self.tokens.actual.typ == '-' or self.tokens.actual.typ == '!':
            optype = self.tokens.actual.typ
            self.tokens.selectNext()
            resultado = UnOp(optype,[self.parseFactor()])
            #print("node: " + str(resultado.value))
        elif self.tokens.actual.typ == '(':
            #self.tokens.selectNext()
            self.tokens.selectNext()
            resultado = self.parseRelExpression()
            #print(resultado)
            #print("node: " + str(resultado.value))
            #print(self.tokens.actual.typ)
            #if self.tokens.actual.typ == ')':
            #    self.tokens.selectNext()
            
            #print(self.tokens.actual.typ)
            #    raise Exception
            #self.tokens.selectNext()
        #elif self.tokens.actual.typ == ')':
            #self.tokens.selectNext()
            #resultado = NoOp('',[])
        #    raise Exception
        elif self.tokens.actual.typ == 'input':
            self.tokens.selectNext()
            if self.tokens.actual.typ != '(':
                raise Exception
            self.tokens.selectNext()
            if self.tokens.actual.typ != ')':
                raise Exception
            resultado = Scanf('Scanf',[])
        else:
            print(self.tokens.actual.typ)
            raise Exception
        
        #print("Factor: "+str(resultado))
        return resultado

    def run(self,origin):
        prepro = PrePro()

        st = SymbolTable()

        origin=prepro.filter(origin)

        #print(origin)

        self.tokens = Tokeniser(origin)
        self.tokens.selectNext()
        resultado = self.parseProgram()
        #print('saiu')
        #if self.tokens.actual.typ == ')':
        #    raise Exception
        #if self.tokens.position < len(origin)-1:
        #    raise Exception

        #print(resultado)

        resultado.Evaluate(st)




class PrePro:
    def __init__(self):
        prepare = True

    

    def filter(self,argument):
        comment = False
        nargument = ""
        parOpen = 0
        parClose =0
        chavOpen =0
        chavClose=0
        asps=0
        #print(argument)
        for a in range(len(argument)):
            if not comment:
                if argument[a] == '{':
                    chavOpen +=1
                if argument[a] == '}':
                    chavClose +=1
                if argument[a] == '(':
                    parOpen +=1
                if argument[a] == ')':
                    parClose +=1
                if argument[a] == '"':
                    asps +=1
                if a < len(argument)-1 and argument[a] == '/' and argument[a+1] == '*':
                    comment = True
                #elif a < len(argument)-1 and not argument[a].isdigit() and not argument[a+1].isdigit() and argument[a] != ' ' and argument[a+1] != ' ':
                elif a < len(argument)-1 and (argument[a] == '/' or argument[a] == '*') and (argument[a+1] == '/' or argument[a+1] == '*'):
                    raise Exception
                if not comment:
                    nargument += argument[a]
            else:
                if a > 0 and argument[a] == '/' and argument[a-1] == '*':
                    comment = False

        if comment:
                raise Exception

        #print("Open:" + str(parOpen))
        #print(f"Close: {parClose}")
        if parOpen != parClose or chavOpen != chavClose or asps%2 != 0:
                raise Exception

        nargument = str(nargument).replace('\r',' ')#.replace('\n',' ')
        self.checkTokens(nargument)
        #nargument = str(nargument).replace(" ","").replace('\n','').replace('\r','')

        return nargument


    def checkTokens(self,argument):
        lnot = True
        lop = True
        for a in range(len(argument)):
            if a <= len(argument):
                if not argument[a].isdigit():
                    lnot = True
                    if argument[a] != ' ':
                        lop = True
                elif lnot:
                   if not lop:
                        raise Exception
                   lnot = False
                   lop = False

#for real
arquivo = open(sys.argv[1],'r')
argument = arquivo.read()
arquivo.close()
argument = argument.strip()


#for testing
#argument = sys.argv[1].strip()


parse = Parser(argument)


#result = (argument)
parse.run(argument)
