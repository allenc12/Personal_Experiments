/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_getenv.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/02/16 13:47:24 by callen            #+#    #+#             */
/*   Updated: 2019/02/16 14:01:14 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define FT_LOBITS		0x0101010101010101UL
#define FT_HIBITS		0x8080808080808080UL

size_t	ft_strlen(const char *s)
{
	const char		*p;
	const uint64_t	*lp;
	int				i;

	p = s;
	while ((uint64_t)p & (sizeof(long) - 1))
		if (*p++ == '\0')
			return (--p - s);
	lp = (const uint64_t*)p;
	while (1)
	{
		if ((*lp - FT_LOBITS) & FT_HIBITS)
		{
			p = (const char*)(lp);
			i = -1;
			while (++i < 8)
				if (!p[i])
					return (p - s + i);
		}
		lp++;
	}
	return (0);
}

int		ft_memcmp(const void *s1, const void *s2, size_t n)
{
	const uint8_t	*b1;
	const uint8_t	*b2;

	b1 = (const uint8_t *)s1;
	b2 = (const uint8_t *)s2;
	while (n--)
	{
		if (*b1 != *b2)
			return ((int)(*b1 - *b2));
		b1++;
		b2++;
	}
	return (0);
}

char	*ft_getenv_alt(char **envp, char *var)
{
	char	**p;
	size_t	var_len;
	size_t	p_len;

	var_len = ft_strlen(var);
	p = envp;
	while (p && *p)
	{
		p_len = ft_strlen(*p);
		if (p_len >= var_len && ft_memcmp(*p, var, var_len) == 0 &&
		(*p)[var_len] == '=')
			return (&(*p)[var_len + 1]);
		p++;
	}
	return (NULL);
}

const char	*ft_getenv(const char **envp, const char *var)
{
	const char	**p;
	size_t		var_len;
	size_t		p_len;

	var_len = ft_strlen(var);
	p = envp;
	while (p && *p)
	{
		p_len = ft_strlen(*p);
		if (p_len >= var_len && ft_memcmp(*p, var, var_len) == 0 &&
		(*p)[var_len] == '=')
			return (&(*p)[var_len + 1]);
		p++;
	}
	return (NULL);
}

int		main(int argc, char **argv, char **envp)
{
	if (argc)
		printf("(int) argc = %d\n", argc);
	printf("(char **) argv[0] = %s\n", argv[0]);
	char *libcres=NULL,*libftres=NULL;
	libcres = getenv("LSCOLORS");
	libftres = ft_getenv_alt(envp, "LSCOLORS");
	printf("strcmp(libcres, libftres) = %d\n", strcmp(libcres, libftres));
	printf("libcres  = %s\nlibftres = %s\n", libcres, libftres);
	return 0;
}
