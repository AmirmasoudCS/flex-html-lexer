%{
    #include <stdio.h>
%}

digit [0-9]
lower [a-z]
upper [A-Z]
whitespace [ \t\n]
punct [.,!?;:]

letter {upper}|{lower}

word {letter}+

sentence ({word}|{whitespace}|punct)*
tag_names ({letter}|{digit})+



%%

"<!--"{sentence}"-->"     {printf("COMMENT %s", yytext);}
"<"{tag_names}">"           {printf("OPENING %s TAG ", yytext);}
"</"{tag_names}">"          {printf("CLOSING %s TAG", yytext);}
"<"{tag_names}[ \t]*"/>"    {printf("SELF CLOSING %s TAG", yytext);}



%%

yywrap(void) {return 1;}

int main(void){

    yylex();
    return 0;
}