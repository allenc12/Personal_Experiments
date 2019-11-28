int volume_histogram(int *histogram, int n) {
	int ll=0;
	int rr=n-1;
	int lmax=0;
	int rmax=0;
	int ret=0;
	while (ll <= rr) {
		if (lmax < rmax) {
			if (lmax < histogram[ll]) {
				lmax = histogram[ll];
			} else {
				ret += lmax - histogram[ll];
			}
			++ll;
		} else {
			if (rmax < histogram[rr]) {
				rmax = histogram[rr];
			} else {
				ret += rmax - histogram[rr];
			}
			--rr;
		}
	}
	return ret;
}

#ifdef DEBUG
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#define SIZ(X) (sizeof((X))/sizeof(*(X)))
int main(){
	int arr1[] = {0,1,0,2,0,2};
	int ret1 = volume_histogram(arr1, SIZ(arr1));
	assert(ret1 == 3);
}
#endif
