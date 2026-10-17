%{
    #include <stdio.h>
%}

tag_names [a-z0-9]+

%%

<{tag_names}>   {printf("OPENING %s TAG ", yytext);}



%%

yywrap(void) {return 1;}

int main(void){

    yylex();
    return 0;
}