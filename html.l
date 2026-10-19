
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
attribute_names {letter}({letter}|{digit}|[-_:])*
closing_comment "-->"

%%

"<!DOCTYPE"                                         { BEGIN(DOCTYPE);}
<DOCTYPE>">"                                        { printf("DOCTYPE\n"); BEGIN(INITIAL);}
<DOCTYPE>.                                          {}
<DOCTYPE>\n                                         {}

"<!--"                                              { BEGIN(COMMENT); }
<COMMENT>"-->"                                      { printf("COMMENT\n"); BEGIN(INITIAL);}
<COMMENT>.                                          {}
<COMMENT>\n                                         {}

"<"{tag_names}                                      { strcpy(tag_name, yytext+1); BEGIN(TAG);}

<TAG>[ \t\n]*{attribute_names}[ \t\n]*"="           { printf("ATTRIBUTE NAME %s\n", yytext); BEGIN(ATTRIBUTE_VALUE);}
<TAG>[ \t\n]*{attribute_names}                      { printf("BOOLEAN ATTRIBUTE %s\n", yytext);}
<TAG>[ \t\n]*">"                                    { printf("OPENING %s TAG\n", tag_name); BEGIN(INITIAL);}
<TAG>[ \t\n]*"/>"                                   { printf("SELF CLOSING %s TAG\n", tag_name); BEGIN(INITIAL);}

<ATTRIBUTE_VALUE>[ \t\n]*\"[^"]*\"                  { printf("ATTRIBUTE VALUE %s\n", yytext); BEGIN(TAG);}
<ATTRIBUTE_VALUE>[ \t\n]*\'[^']*\'                  { printf("ATTRIBUTE VALUE %s\n", yytext); BEGIN(TAG);}
<ATTRIBUTE_VALUE>[ \t\n]*[^ \t\n"'=<>`]+            { printf("ATTRIBUTE VALUE %s\n", yytext); BEGIN(TAG);}

"</"{tag_names}[ \t\n]*">"                          { printf("CLOSING %s TAG\n", yytext);}

%%

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
