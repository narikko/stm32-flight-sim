#ifndef TELEMETRY_H
#define TELEMETRY_H

#include <stdint.h>
#include <stddef.h>

#define TELEMETRY_HEADER_BYTE1  0xAA
#define TELEMETRY_HEADER_BYTE2  0x55

#pragma pack(push, 1)
typedef struct {
    uint8_t  header[2];      // Fixed framing bytes: 0xAA, 0x55
    float    pitch;          // 4 bytes IEEE 754
    float    roll;           // 4 bytes IEEE 754
    uint8_t  button_state;   // 1 byte
    uint16_t checksum;       // 2 bytes Fletcher-16
} TelemetryPacket;           // Exactly 13 bytes
#pragma pack(pop)

uint16_t Fletcher16_Calculate(const uint8_t *data, size_t len);

#endif /* TELEMETRY_H */
