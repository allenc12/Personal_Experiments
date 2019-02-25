/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_filestream.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/21 11:19:34 by callen            #+#    #+#             */
/*   Updated: 2019/01/21 11:27:56 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
struct	s_buf
{
	unsigned char	*base;
	int				size;
};
typedef struct s_fstr	t_fstr;
struct	s_fstrx;
struct	s_fstr
{
	unsigned char	*p;
	int				r;
	int				w;
	short			flags;
	short			file;
	struct s_buf	bf;
	int				lbfsize;
	void			*cookie;
	int				(* _Nullable _close)(void *);
	int				(* _Nullable _read)(void *, char *, int);
	fpos_t			(* _Nullable _seek)(void *, fpos_t, int);
	int				(* _Nullable _write)(void *, const char *, int);
	struct s_buf	ub;
	struct s_fstrx	*extra;
	int				ur;
	unsigned char	ubuf[3];
	unsigned char	nbuf[1];
	struct s_buf	lb;
	int				blksize;
	fpos_t			offset;
};
