#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <limits.h>
#include <sys/cdefs.h>
#include <ctype.h>
#include <errno.h>

#define RET_IF(cond, ret) if (cond) return (ret)
#define RET_NONE(cond) if (cond) return
#define IF_NULL(x) if (x) return (NULL)
#define DO_IF(cond, do_me) if (cond) do_me
#define DO_ALL(cond, ...) if (cond) __VA_ARGS__
#define WHILE(cond, do_me) while (cond) do_me
#define ELSE_DO(do_me) else do_me
#define IF_ELSE(cond, a, b) DO_IF(cond, a); ELSE_DO(b)

/*
 * BSD implementation
 */
long ft_strtol(const char *nptr, char **endptr, int base) {
	const char *s;
	unsigned long acc;
	char c;
	unsigned long cutoff;
	int neg, any, cutlim;

	s = nptr;
	c = ' ';
	while (isspace(c))
		c = *s++;
	if (c == '-')
	{
		neg = 1;
		c = *s++;
	}
	else
	{
		neg = 0;
		if (c == '+')
			c = *s++;
	}
	if ((base == 0 || base == 16) && c == '0' &&
		(*s == 'x' || *s == 'X') &&
		((s[1] >= '0' && s[1] <= '9') ||
		(s[1] >= 'A' && s[1] <= 'F') ||
		(s[1] >= 'a' && s[1] <= 'f')))
	{
		c = s[1];
		s += 2;
		base = 16;
	}
	if (base == 0)
		base = c == '0' ? 8 : 10;
	acc = any = 0;
	if (!(base < 2 || base > 36))
	{
		cutoff = neg ? (unsigned long) - (LONG_MIN + LONG_MAX) + LONG_MAX : LONG_MAX;
		cutlim = cutoff % base;
		cutoff /= base;
		for ( ; ; c = *s++)
		{
			if (c >= '0' && c <= '9')
				c -= '0';
			else if (c >= 'A' && c <= 'Z')
				c -= 'A' - 10;
			else if (c >= 'a' && c <= 'z')
				c -= 'a' - 10;
			else
				break;
			if (c >= base)
				break;
			if (any < 0 || acc > cutoff || (acc == cutoff && c > cutlim))
				any = -1;
			else
			{
				any = 1;
				acc *= base;
				acc += c;
			}
		}
	}
	if (any < 0)
	{
		acc = neg ? LONG_MIN : LONG_MAX;
		errno = ERANGE;
	}
	else if (!any)
	{
		errno = EINVAL;
	}
	else if (neg)
		acc = -acc;
	if (endptr != NULL)
		*endptr = (char *)(any ? s - 1 : nptr);
	return (acc);
}

/* Lookup table for digit values. -1==255>=36 -> invalid */
static const unsigned char table[] = { -1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	00, 1, 2, 3, 4, 5, 6, 7, 8, 9,-1,-1,-1,-1,-1,-1,
	-1,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
	25,26,27,28,29,30,31,32,33,34,35,-1,-1,-1,-1,-1,
	-1,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
	25,26,27,28,29,30,31,32,33,34,35,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
};
/*
 * Musl libc implementation
 */
unsigned long long ft_intscan(char *s, unsigned base, int pok, uint64_t lim)
{
	const uint8_t *val = table + 1;
	int c;
	int neg = 0;
	int bs;
	unsigned x;
	uint64_t y;
	if (base > 36 || base == 1)
	{
		errno = EINVAL;
		return 0;
	}
	while (isspace((c = *s++)))
		;
	if (c == '+' || c == '-')
	{
		neg = -(c == '-');
		c = *s++;
	}
	if ((base == 0 || base == 16) && c == '0')
	{
		c = *s++;
		if ((c | 32) == 'x')
		{
			c = *s++;
			if (val[c] >= 16)
			{
				s--;
				if (pok)
					s--;
				return 0;
			}
			base = 16;
		}
		else if (base == 0)
			base = 8;
	}
	else
	{
		if (base == 0)
			base = 10;
		if (val[c] >= base)
			return 0;
	}
	if (base == 10)
	{
		for (x = 0; c - '0' < 10 && x <= UINT_MAX / 10 - 1; c = *s++)
			x = x * 10 + (c - '0');
		for (y = x; c - '0' < 10 && y <= ULLONG_MAX / 10 && 10 * y <= ULLONG_MAX - (c - '0'); c = *s++)
			y = y * 10 + (c - '0');
		if (c - '0' >= 10)
			return (0);
	}
	else if (!(base & base - 1))
	{
		bs = "\0\1\2\4\7\3\6\5"[(0x17 * base) >> 5 & 7];
		for (x = 0; val[c] < base && x <= UINT_MAX / 32; c = *s++)
			x = x << bs | val[c];
		for (y = x; val[c] < base && y <= ULLONG_MAX >> bs; c = *s++)
			y = y << bs | val[c];
	}
	else
	{
		for (x = 0; val[c] < base && x <= UINT_MAX / 36 - 1; c = *s++)
			x = x * base + val[c];
		for (y = x; val[c] < base && y <= ULLONG_MAX / base && base * y <= ULLONG_MAX - val[c]; c = *s++)
			y = y * base + val[c];
	}
	if (val[c] < base)
	{
		for (; val[c] < base; c = *s++);
		errno = ERANGE;
		y = lim;
		if (lim & 1)
			neg = 0;
	}
	if (y >= lim)
	{
		if (!(lim & 1) && !neg)
		{
			errno = ERANGE;
			return (lim - 1);
		}
		else if (y > lim)
		{
			errno = ERANGE;
			return (lim);
		}
	}
	return ((y ^ neg) - neg);
}

int min(int a, int b) {
	if (a > b)
		return a;
	else
		return b;
}

int			ft_atoibase(const char *str, int base)
{
	int	n;
	int	sign;

	n = 0;
	sign = 1;
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (*str == '+' || *str == '-')
	{
		if (*str == '-')
			sign = -1;
		str++;
	}
	while (*str)
	{
		if (*str >= '0' && *str <= (min('0' + base - 1, '9')))
			n = n * base + *str - '0';
		else if (*str >= 'a' && *str <= ('a' + base - 11))
			n = n * base + *str - 'a' + 10;
		else
			break ;
		str++;
	}
	return (n * sign);
}
/* Lookup table for digit values. -1==255>=36 -> invalid */
static const unsigned char g_tbl[] = { -1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	00, 1, 2, 3, 4, 5, 6, 7, 8, 9,-1,-1,-1,-1,-1,-1,
	-1,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
	25,26,27,28,29,30,31,32,33,34,35,-1,-1,-1,-1,-1,
	-1,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
	25,26,27,28,29,30,31,32,33,34,35,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
};

#define X(a) ((a) == 'x' || (a) == 'X')

static inline void	blep(const uint8_t *v, const char *s, int b, int h[3])
{
	while (1)
	{
		if (v[h[2]] < b)
			h[0] = h[0] * b + v[h[2]];
		else
			break ;
		h[2] = *s++;
	}
}
int			ft_atoi_base(const char *s, int b)
{
	const uint8_t	*v = g_tbl + 1;
	int				h[3];

	h[0] = 0;
	h[1] = 0;
	while (isspace(h[2] = *s++))
		;
	if (h[2] == '+' || h[2] == '-')
	{
		h[1] = -(h[2] == '-');
		h[2] = *s++;
	}
	if ((b == 0 || b == 16) && h[2] == '0' && X(*s) && v[h[2]] < b)
	{
		h[2] = s[1];
		s += 2;
		b = 16;
	}
	if (b == 0)
		b = (!v[h[2]] ? 8 : 10);
	blep(v, s, b, h);
	return ((h[0] ^ h[1]) - h[1]);
}

int			ft_atoi_base_prenorme(const char *s, int b)
{
	const uint8_t	*v = g_tbl;
	int				c;
	int				n;
	int				sign;

	n = 0;
	sign = 0;
	c = ' ';
	while (isspace(c))
		c = *s++;
	if (c == '+' || c == '-')
	{
		sign = (c == '-');
		c = *s++;
	}
	if ((b == 0 || b == 16) && !v[c] && (*s == 'x' || *s == 'X') && v[c] < b)
	{
		b = 16;
		s += 2;
		c = s[1];
	}
	if (b == 0)
		b = (!v[c] ? 8 : 10);
	while (1)
	{
		if (v[c] < b)
			n = n * b + v[c];
		else
			break ;
		c = *s++;
	}
	return ((n ^ sign) - sign);
}

int main(int ac, char **av) {
	if (ac == 2) {
		char *s = av[1];
		printf("strtol(s) = %d\n",(int)strtol(s, 0, 16));
		printf("intscan(s) = %d\n",(int)ft_intscan(s, 16, 1, LONG_MAX));
		printf("ft_atoibase(s) = %d\n", ft_atoibase(s, 16));
		printf("ft_atoi_base(s) = %d\n", ft_atoi_base(s, 16));
		printf("ft_atoi_base_prenorme(s) = %d\n", ft_atoi_base_prenorme(s, 16));
	}
	return 0;
}
