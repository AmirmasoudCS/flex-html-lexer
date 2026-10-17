%{
    #include <stdio.h>
%}

digit [0-9]
letter [a-zA-Z]
tag_names ({letter}|{digit})*

%%

"<"{tag_names}">"           {printf("OPENING %s TAG ", yytext);}
"</"{tag_names}">"          {printf("CLOSING %s TAG", yytext);}
"<"{tag_names}[ \t]*"/>"    {printf("SELF CLOSING %s TAG", yytext);}

%%

yywrap(void) {return 1;}

int main(void){

    yylex();
    return 0;
}