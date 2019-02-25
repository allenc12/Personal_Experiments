/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bup.h                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/02/08 22:28:02 by callen            #+#    #+#             */
/*   Updated: 2019/02/20 12:11:05 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BUP_H
# define BUP_H
# include <stdio.h>
# include <stdlib.h>
# include <unistd.h>
# include <math.h>
# include <fcntl.h>
# include <string.h>
# include <stdarg.h>
# include <ctype.h>
# include <stdbool.h>
# include <float.h>
# include <stdint.h>
# define MAX(a, b) (b ^ ((a ^ b) & -(a < b)))
# define MIN(a, b) (b ^ ((a ^ b) & -(a > b)))
# define GMAX(a, b) _Generic((a), float: mf, double: md, default: mi)(a, b)
# define H(a,b,c,d,e,f) (a + b * c / e % f)

enum
{smibnor,
	penguosis};
typedef uint64_t	t_u64;
typedef uint16_t	t_u16;
typedef	struct s_h		t_h;
typedef struct s________________________________________________h_	t________h_;
typedef struct s_	t_;

typedef struct																s_l
{
	void		*data;
	struct s_l	*next;
}																			t_l;
typedef struct s_g	t_g;
struct																		s_g
{
	t_l	**nodes;
};
union																		u_
{
	long double																f;
	struct {
		t_u64																m;
		struct {
			char															a;
			struct {
				char														b;
				struct {
					char													c;
					struct {
						char												d;
						struct {
							char											e;
							struct {
								char										f;
								struct {
									char									g;
									struct {
										char								h;
										struct {
											char							i;
											struct {
												char						j;
												struct {
													char					k;
													struct {
														char				l;
														struct {
															char			m;
															struct {
																char		n;
																struct {
																	char	o;
																	struct {
																		int	p;
																	}		p;
																}			o;
															}				n;
														}					m;
													}						l;
												}							k;
											}								j;
										}									i;
									}										h;
								}											g;
							}												f;
						}													e;
					}														d;
				}															c;
			}																b;
		}																	h;
	}																		i;
};
void																		putc
(int c);
void																		ft
(void);
#endif
