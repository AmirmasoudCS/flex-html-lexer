
%{
    #include <stdio.h>
%}

%x COMMENT

%x DOCTYPE

digit [0-9]
lower [a-z]
upper [A-Z]
whitespace [ \t\n]
punct [.,!?;:]

letter {upper}|{lower}
word {letter}+
sentence ({word}|{whitespace}|{punct})*
tag_names {letter}({letter}|{digit})+
closing_comment "-->"

%%


"<!DOCTYPE"                   { BEGIN(DOCTYPE);}
<DOCTYPE>">"                  { printf("DOCTYPE"); BEGIN(INITIAL);}
<DOCTYPE>.                    {}
<DOCTYPE>\n                   {}
"<!--"                         { BEGIN(COMMENT); }
<COMMENT>"-->"                 { printf("COMMENT"); BEGIN(INITIAL);}
<COMMENT>.                     {}
<COMMENT>\n                    {}
"<"{tag_names}">"              { printf("OPENING %s TAG ", yytext); }
"</"{tag_names}">"             { printf("CLOSING %s TAG", yytext); }
"<"{tag_names}[ \t]*"/>"       { printf("SELF CLOSING %s TAG", yytext); }

%%

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
