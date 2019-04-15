%{

#include "y.tab.h"
int yyerror(char *errormsg);

%}

%%

("hi"|"oi")"\n"       { return HI;  }
("tchau"|"bye")"\n"   { return BYE; }
.                     { yyerror("Unknown char");  }

%%

int yywrap(void)
{
   return 0;
}

int yyerror(char *errormsg)
{
    fprintf(stderr, "%s\n", errormsg);
    exit(1);
}