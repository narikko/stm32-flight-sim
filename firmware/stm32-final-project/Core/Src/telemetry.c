/*
 * telemetry.c
 *
 *  Created on: Oct 8, 2026
 *      Author: nh_14
 */

#include "telemetry.h"

uint16_t Fletcher16_Calculate(const uint8_t *data, size_t len){
	uint16_t sum1 = 0xff;
	uint16_t sum2 = 0xff;

	while (len) {
	        // Process in blocks up to 20 to avoid 16-bit accumulator overflow
	        size_t tlen = (len > 20) ? 20 : len;
	        len -= tlen;
	        do {
	            sum1 += *data++;
	            sum2 += sum1;
	        } while (--tlen);

	        sum1 = (sum1 & 0xff) + (sum1 >> 8);
	        sum2 = (sum2 & 0xff) + (sum2 >> 8);
	    }

	    sum1 = (sum1 & 0xff) + (sum1 >> 8);
	    sum2 = (sum2 & 0xff) + (sum2 >> 8);

	    return (sum2 << 8) | sum1;
}

