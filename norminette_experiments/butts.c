int main() {
	int ii;
	for (ii = 0; ii < 256; ++ii) {
		if (isxdigit(ii))
			printf("1,");
		else
			printf("0,");
		if (ii % 16 == 15)
			printf("\n");
	}
}
