import struct
import serial

PORT = "COM5"  # Match your ST-Link port
BAUD = 115200


def fletcher16(data: bytes) -> int:
    sum1 = 0xFF
    sum2 = 0xFF

    for b in data:
        sum1 += b
        sum2 += sum1

    # End-around carry reduction matching C implementation
    sum1 = (sum1 & 0xFF) + (sum1 >> 8)
    sum2 = (sum2 & 0xFF) + (sum2 >> 8)

    sum1 = (sum1 & 0xFF) + (sum1 >> 8)
    sum2 = (sum2 & 0xFF) + (sum2 >> 8)

    return (sum2 << 8) | sum1


ser = serial.Serial(PORT, BAUD, timeout=1)
ser.reset_input_buffer()
print(f"Listening on {PORT}...")

try:
  while True:
    # 1. Sync on header 0xAA, 0x55
    if ser.read(1) != b"\xaa":
      continue
    if ser.read(1) != b"\x55":
      continue

    # 2. Read the remaining 11 bytes: 4B pitch + 4B roll + 1B btn + 2B chk
    raw = ser.read(11)
    if len(raw) < 11:
      continue

    payload = raw[:9]
    (chk_recv,) = struct.unpack("<H", raw[9:])
    chk_calc = fletcher16(payload)

    if chk_calc == chk_recv:
      pitch, roll, btn = struct.unpack("<ffB", payload)
      print(
          f"\r[OK] Pitch: {pitch:6.1f}° | Roll: {roll:6.1f}° | Btn: {btn}   ",
          end="",
          flush=True,
      )
    else:
      print(
          f"\n[ERR] Checksum mismatch! Calc: {hex(chk_calc)} Recv:"
          f" {hex(chk_recv)}"
      )

except KeyboardInterrupt:
  ser.close()
  print("\nDone.")