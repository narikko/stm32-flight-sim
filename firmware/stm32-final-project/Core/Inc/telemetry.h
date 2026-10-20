#ifndef TELEMETRY_H
#define TELEMETRY_H

#include <stdint.h>
#include <stddef.h>

#define TELEMETRY_HEADER_BYTE1  0xAA
#define TELEMETRY_HEADER_BYTE2  0x55

#pragma pack(push, 1)
typedef struct {
    uint8_t header[2];      // 0xAA, 0x55
    float pitch_fused;      // Kalman Pitch
    float pitch_raw;        // Raw Accel Pitch
    float roll_fused;       // Kalman Roll
    float roll_raw;         // Raw Accel Roll
    uint8_t button_state;   // PC13 button
    uint16_t checksum;      // Fletcher-16
} TelemetryPacket;
#pragma pack(pop)

uint16_t Fletcher16_Calculate(const uint8_t *data, size_t len);

#endif /* TELEMETRY_H */
