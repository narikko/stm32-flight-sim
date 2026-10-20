import struct
import threading
from collections import deque
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import serial

PORT = "COM5"  # Match your ST-Link port
BAUD = 115200

# 2 header bytes + 4 floats (p_fused, p_raw, r_fused, r_raw) + 1 byte (btn) + 2 bytes (chk) = 21 bytes
PACKET_FORMAT = "<BBffffBH"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)
HEADER = (0xAA, 0x55)

MAX_LEN = 200
data_pitch_fused = deque([0.0] * MAX_LEN, maxlen=MAX_LEN)
data_pitch_raw = deque([0.0] * MAX_LEN, maxlen=MAX_LEN)
data_roll_fused = deque([0.0] * MAX_LEN, maxlen=MAX_LEN)
data_roll_raw = deque([0.0] * MAX_LEN, maxlen=MAX_LEN)

data_lock = threading.Lock()


def fletcher16(data: bytes) -> int:
  sum1, sum2 = 0xFF, 0xFF
  for b in data:
    sum1 += b
    sum2 += sum1
  sum1 = (sum1 & 0xFF) + (sum1 >> 8)
  sum2 = (sum2 & 0xFF) + (sum2 >> 8)
  sum1 = (sum1 & 0xFF) + (sum1 >> 8)
  sum2 = (sum2 & 0xFF) + (sum2 >> 8)
  return (sum2 << 8) | sum1


def serial_reader():
  try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    ser.reset_input_buffer()
    print(f"Connected to {PORT} at {BAUD} baud.")
  except Exception as e:
    print(f"Error opening serial port: {e}")
    return

  while True:
    header_candidate = ser.read(2)
    if len(header_candidate) < 2:
      continue

    if (
        header_candidate[0] == HEADER[0]
        and header_candidate[1] == HEADER[1]
    ):
      payload_and_chk = ser.read(PACKET_SIZE - 2)
      if len(payload_and_chk) < (PACKET_SIZE - 2):
        continue

      full_packet = header_candidate + payload_and_chk
      fields = struct.unpack(PACKET_FORMAT, full_packet)

      calc_chk = fletcher16(full_packet[2:-2])
      recv_chk = fields[7]

      if calc_chk == recv_chk:
        p_fused, p_raw, r_fused, r_raw = (
            fields[2],
            fields[3],
            fields[4],
            fields[5],
        )
        with data_lock:
          data_pitch_fused.append(p_fused)
          data_pitch_raw.append(p_raw)
          data_roll_fused.append(r_fused)
          data_roll_raw.append(r_raw)


thread = threading.Thread(target=serial_reader, daemon=True)
thread.start()

# 2 Subplots: Top for Pitch, Bottom for Roll
fig, (ax_pitch, ax_roll) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Pitch Axis
(line_pitch_raw,) = ax_pitch.plot(
    [], [], label="Raw Accel Pitch", color="red", alpha=0.45, linewidth=1
)
(line_pitch_fused,) = ax_pitch.plot(
    [], [], label="Kalman Pitch", color="cyan", linewidth=2
)
ax_pitch.set_ylim(-90, 90)
ax_pitch.set_xlim(0, MAX_LEN)
ax_pitch.set_ylabel("Pitch (deg)")
ax_pitch.set_title("Pitch Orientation: Raw vs Filtered")
ax_pitch.grid(True, linestyle="--", alpha=0.5)
ax_pitch.legend(loc="upper right")

# Roll Axis
(line_roll_raw,) = ax_roll.plot(
    [], [], label="Raw Accel Roll", color="orange", alpha=0.45, linewidth=1
)
(line_roll_fused,) = ax_roll.plot(
    [], [], label="Kalman Roll", color="lime", linewidth=2
)
ax_roll.set_ylim(-90, 90)
ax_roll.set_ylabel("Roll (deg)")
ax_roll.set_xlabel("Recent Frames (100 Hz)")
ax_roll.set_title("Roll Orientation: Raw vs Filtered")
ax_roll.grid(True, linestyle="--", alpha=0.5)
ax_roll.legend(loc="upper right")

plt.tight_layout()


def update(frame):
  with data_lock:
    yp_raw = list(data_pitch_raw)
    yp_fused = list(data_pitch_fused)
    yr_raw = list(data_roll_raw)
    yr_fused = list(data_roll_fused)

  x = range(len(yp_raw))
  line_pitch_raw.set_data(x, yp_raw)
  line_pitch_fused.set_data(x, yp_fused)
  line_roll_raw.set_data(x, yr_raw)
  line_roll_fused.set_data(x, yr_fused)
  return line_pitch_raw, line_pitch_fused, line_roll_raw, line_roll_fused


ani = animation.FuncAnimation(fig, update, interval=20, blit=True)
plt.show()