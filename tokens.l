%{
#include <string>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

%%

[ \t\n]                 ;
"if"                    return TOKEN(TIF);
"while"                 return TOKEN(TWHILE);
"print"                 return TOKEN(TPRINTF);
"input"                 return TOKEN(TSCANF);
"return"                return TOKEN(TRETURN);
[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return TIDENTIFIER;
[0-9]+                  SAVE_TOKEN; return TNUMBER;
"="                     return TOKEN(TEQUAL);
"=="                    return TOKEN(TCEQ);
"!"                     return TOKEN(TNOT);
"<"                     return TOKEN(TCLT);
"&&"                    return TOKEN(TCAND);
">"                     return TOKEN(TCGT);
"||"                    return TOKEN(TCOR);
"("                     return TOKEN(TLPAREN);
")"                     return TOKEN(TRPAREN);
"{"                     return TOKEN(TLBRACE);
"}"                     return TOKEN(TRBRACE);
"."                     return TOKEN(TDOT);
","                     return TOKEN(TCOMMA);
"+"                     return TOKEN(TPLUS);
"-"                     return TOKEN(TMINUS);
"*"                     return TOKEN(TMUL);
"/"                     return TOKEN(TDIV);
.                       printf("Unknown token!n"); yyterminate();

%%
