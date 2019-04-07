/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   todo_libft.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/04/02 20:07:49 by callen            #+#    #+#             */
/*   Updated: 2019/04/02 20:09:11 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <ft_ssl.h>
#include <libft.h>
#include <limits.h>
#define BITOP(a,b,op) \
((a)[(size_t)(b)/(8*sizeof(*(a)))] op (size_t)1<<((size_t)(b)%(8*sizeof(*(a)))))

size_t	ft_strspn(const char *s, const char *c)
{
	const char	*a = s;
	size_t		byteset[32 / sizeof(size_t)];

	ft_bzero(byteset, sizeof byteset);
	if (!c[0])
		return (0);
	if (!c[1])
	{
		while (*s == *c)
			s++;
		return (s - a);
	}
	while (*c && BITOP(byteset, *(unsigned char*)c, |=))
		c++;
	while (*s && BITOP(byteset, *(unsigned char*)s, &))
		s++;
	return (s - a);
}

#define ALIGN (sizeof(size_t))
#define ONES ((size_t) - 1 / UCHAR_MAX)
#define HIGHS (ONES * (UCHAR_MAX / 2 + 1))
#define HASZERO(x) ((x) - ONES & ~(x) & HIGHS)

char	*ft_strchrnul_(const char *s, int c)
{
	c = (unsigned char)c;
	if (!c)
		return ((char*)s + ft_strlen(s));
	while (*s && *(unsigned char*)s != c)
		s++;
	return ((char*)s);
}

size_t	ft_strcspn(const char *s, const char *c)
{
	const char	*a = s;
	size_t		byteset[32 / sizeof(size_t)];

	if (!c[0] || !c[1])
		return (ft_strchrnul_(s, *c) - a);
	memset(byteset, 0, sizeof byteset);
	while (*c && BITOP(byteset, *(unsigned char*)c, |=))
		c++;
	while (*s && !BITOP(byteset, *(unsigned char*)s, &))
		s++;
	return (s - a);
}

char	*ft_strtok(char *restrict s, const char *restrict sep)
{
	static char *p;

	if (!s && !(s = p))
		return (NULL);
	s += ft_strspn(s, sep);
	if (!*s)
		return (p = 0);
	p = s + ft_strcspn(s, sep);
	if (*p)
		*p++ = 0;
	else
		p = 0;
	return (s);
}
