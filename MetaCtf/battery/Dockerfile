##########################################
# Dockerfile for the AVR battery challenge
#
# This image builds the AVR simulator (simavr) from source,
# compiles the battery controller firmware, and packages a
# runtime environment that launches the simulator, flashes the
# firmware and bridges its UART to a TCP port.  The simulator
# must find a valid bootloader image in its working directory
# or it will crash; we install the Arduino core package to
# provide that bootloader and copy it into place during the
# build.

FROM debian:bookworm-slim AS build

# Avoid interactive debconf prompts
ARG DEBIAN_FRONTEND=noninteractive

# Install toolchain and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc-avr \
        binutils-avr \
        avr-libc \
        avrdude \
        make \
        git \
        libelf-dev \
        arduino-core-avr \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Fetch simavr and build only the core and simduino board example.
# Building other examples pulls in OpenGL/glut which are not
# available in slim images.
RUN git clone --depth=1 https://github.com/buserror/simavr.git /opt/simavr && \
    make -C /opt/simavr/simavr SIMAVR_HAVE_GDB=1 -j"$(nproc)" && \
    make -C /opt/simavr/examples/board_simduino clean && \
    make -C /opt/simavr/examples/board_simduino -j"$(nproc)"

# Copy an Arduino bootloader into the simduino directory if both
# the simulator and the bootloader exist.  The simulator expects
# ATmegaBOOT_168_atmega328.ihex in its CWD.  If we cannot find
# simduino or the bootloader, this step is skipped silently and
# the runtime entrypoint will attempt to copy it again.
RUN set -eux; \
    sd="$(dirname $(find /opt/simavr -type f -name simduino.elf -print -quit || echo ''))"; \
    bl="/usr/share/arduino/hardware/arduino/avr/bootloaders/atmega/ATmegaBOOT_168_atmega328.hex"; \
    if [ -n "$sd" ] && [ -f "$bl" ]; then \
        cp -f "$bl" "$sd/ATmegaBOOT_168_atmega328.ihex"; \
    else \
        echo "bootloader copy skipped (sd='$sd', bl='$bl')"; \
    fi

# Build the battery controller firmware
WORKDIR /opt/challenge
COPY battery_controller.c ./

# Compile the firmware for the ATmega328P at 16 MHz
RUN avr-gcc -mmcu=atmega328p -DF_CPU=16000000UL -Os -o battery_controller.elf battery_controller.c && \
    avr-objcopy -O ihex battery_controller.elf battery_controller.hex

# Final runtime stage
FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive

# Install runtime utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        avrdude \
        socat \
        netcat-openbsd \
        ca-certificates \
        python3 \
        arduino-core-avr && \
    rm -rf /var/lib/apt/lists/*

# Copy simulator and compiled firmware from build stage
COPY --from=build /opt/simavr /opt/simavr
COPY --from=build /opt/challenge/battery_controller.hex /opt/challenge/battery_controller.hex

# Copy the entrypoint script
COPY entrypoint.sh /opt/entrypoint.sh
COPY run.sh /opt/run.sh

RUN chmod +x /opt/entrypoint.sh
RUN chmod +x /opt/run.sh

# Use the entrypoint script to start the simulator
ENTRYPOINT ["/opt/run.sh"]