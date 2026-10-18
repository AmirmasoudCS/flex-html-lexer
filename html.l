
%{
    #include <stdio.h>
%}

%x COMMENT

%x DOCKTYPE

digit [0-9]
lower [a-z]
upper [A-Z]
whitespace [ \t\n]
punct [.,!?;:]

letter {upper}|{lower}
word {letter}+
sentence ({word}|{whitespace}|{punct})*
tag_names ({letter}|{digit})+
closing_comment "-->"

%%


"<!DOCKTYPE"                   { BEGIN(DOCKTYPE);}
<DOCKTYPE>">"                  { BEGIN(INITIAL);}
<DOCKTYPE>.                    {}
<DOCKTYPE>\n                   {}
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
