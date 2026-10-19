
%{
    #include <stdio.h>
    #include <string.h>
    char tag_name[256];
%}

%x COMMENT

%x DOCTYPE

%x TAG

%x ATTRIBUTE_VALUE

digit [0-9]
lower [a-z]
upper [A-Z]
whitespace [ \t\n]
punct [.,!?;:]

letter {upper}|{lower}
word {letter}+
sentence ({word}|{whitespace}|{punct})*
tag_names {letter}({letter}|{digit})*
closing_comment "-->"

%%


"<!DOCTYPE"                                         { BEGIN(DOCTYPE);}
<DOCTYPE>">"                                        { printf("DOCTYPE"); BEGIN(INITIAL);}
<DOCTYPE>.                                          {}
<DOCTYPE>\n                                         {}
"<!--"                                              { BEGIN(COMMENT); }
<COMMENT>"-->"                                      { printf("COMMENT"); BEGIN(INITIAL);}
<COMMENT>.                                          {}
<COMMENT>\n                                         {}
"<"{tag_names}                                      { strcpy(tag_name, yytext+1); BEGIN(TAG);}
<TAG>[ \t]*{letter}({letter}|{digit})*"="           { printf("%s ATTRIBUTE", yytext); BEGIN(ATTRIBUTE_VALUE);}
<ATTRIBUTE_VALUE>\"[^"]*\"                              { printf("ATTRIBUTE VALUE %s", yytext); BEGIN(TAG);}
<TAG>[ \t]*">"                                      { printf("OPENING %s TAG", tag_name); BEGIN(INITIAL);}
<TAG>[ \t]*"/>"                                     { printf("SELF CLOSING %s TAG", tag_name); BEGIN(INITIAL);}
"</"{tag_names}">"                                  { printf("CLOSING %s TAG", yytext);}

%%

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
