#include "norme.tab.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <sys/stat.h>
#include <sys/cdefs.h>

#include <fts.h>
#include <grp.h>
#include <limits.h>
#include <pwd.h>
#include <termcap.h>
#include <signal.h>
#ifdef __APPLE__
#include <sys/acl.h>
#include <sys/xattr.h>
#include <sys/param.h>
#include <get_compat.h>
#endif

#define OPTSTR "hf:"

#define YYDEBUG 1

extern int yyparse(void);
extern FILE *yyin, *yyout;
/* extern FILE *yyerr; */

const char *bin;

/* command line flags */
int is_tty = 0;
char *f_name = 0;
int f_network = 0;
int f_file = 0;

int fncount = 0;
int varcount = 0;

static int parse_file(const char *filename) {
	FILE *fp;
	int ret = 0;

	if (strcmp(filename, "stdin")) {
		fp = fopen(filename, "r");
	} else {
		fp = stdin;
	}

	if (fp != NULL)
		yyin = fp;

	if (is_tty)
		fprintf(yyout, "\e[1m");

	fprintf(yyout, "Norme: %s\n", filename);

	if (is_tty)
		fprintf(yyout, "\e[0m");

	ret = yyparse();

#ifdef YYDEBUG
	fprintf(yyout, "\tret: %d\n", ret);
	fprintf(yyout, "\tfncount: %d\n", fncount);
	fprintf(yyout, "\tvarcount: %d\n", varcount);
#endif

	fclose(fp);
	return ret;
}

static int usage(int ch) {
	fprintf(stderr, "%s: [-%s] [file ...]\n", bin, OPTSTR);
	return ch != 'h';
}

static void traverse(int argc, const char *argv[]) {
	int ii;

	if (f_file)
		parse_file(f_name);

	for (ii = 0; ii < argc; ++ii) {
		if (parse_file(argv[ii]) == 0 && is_tty)
			fprintf(yyout, "\r");
	}
}

int main(int argc, const char *argv[]) {
	int ch;

	yyin = stdin, yyout = stdout;
	is_tty = isatty(STDOUT_FILENO);
	bin = *argv;
	if (argc > 1) {
		while ((ch = getopt(argc, (char * const*)argv, OPTSTR)) != -1) {
			switch (ch) {
				case 'f':
					if (optarg != NULL) {
						/* queue? */
						f_name = optarg;
						f_file = 1;
					} else {
						f_file = 0;
						if (errno)
							perror(bin);
						else
							fprintf(stderr, "%s: Error %s ack\n", bin, optarg);
					}
					break;
				case 'n':
					f_network = 1;
					break;
				case 'h':
				case '?':
				default :
					return usage(ch);
					break;
			}
		}
	} else {
		// open pwd and traverse
		parse_file("butts.c");
		parse_file("pass.c");
	}
	argc -= optind;
	argv += optind;
	traverse(argc, argv);
}
