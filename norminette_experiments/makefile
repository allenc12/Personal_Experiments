NAME = cnorme
LEX = flex
YACC = bison -d --debug
LDFLAGS = -L/nfs/2018/c/callen/.brew/opt/flex/lib -lfl

all: $(NAME)

$(NAME): lex.yy.o norme.tab.o
	$(CC) $(LDFLAGS) -o $@ $^ norme.c

norme.tab.c: norme.y
	$(YACC) $<

lex.yy.c: norme.tab.c
lex.yy.c: norme.l
	$(LEX) norme.l

.PHONY: clean k
clean k:
	-$(RM) $(NAME) lex.yy.c lex.yy.o norme.o norme.tab.c norme.tab.h norme.tab.o norme.output

.PHONY: re
re: clean all
