# .____________________.
# |                  |
# |  F3V3R DR34M     |
# |  W4R THUND3R     |
# |  D0CK3R B41LD    |
# |                  |
# |  [2025 RUL3Z!]   |
# |__________________|
#
# CR3D1TZ:
# - M4ST3R: Z4R1G4T4
# - T34M: F3V3R DR34M

# Use official Python runtime as base image
FROM python:3.10-slim-bullseye

# [*] S3T UP TH3 H4CK3R Z0N3
LABEL maintainer="F3V3R DR34M T34M <z4r1g4t4@f3v3rdr34m.com>"
LABEL version="1.0.0"
LABEL description="W4R THUND3R D1SC0RD B0T - ULT1M4T3 TR4CK3R"

# [*] PR3P4R3 TH3 B4TTL3F13LD
WORKDIR /app

# [*] 1NST4LL TH3 W34P0NRY
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# [*] DR0P TH3 C0D3 B0MBS
COPY bot.py .
COPY config.json .
COPY match_history.json .

# [*] S3T UP TH3 C0MM4ND C3NT3R
ENV PYTHONUNBUFFERED=1

# [*] PR3P4R3 F0R D3PL0YM3NT
EXPOSE 8000

# [*] TR1GG3R TH3 M1SS10N
CMD ["python", "bot.py"]

# [*] H4CK TH3 PL4N3T! 
# [*] F3V3R DR34M RUL3Z!
