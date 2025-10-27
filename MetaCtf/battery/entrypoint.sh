#!/bin/bash
set -euo pipefail

CHAL_HEX="/opt/challenge/battery_controller.hex"
SIMAVR_ROOT="/opt/simavr"
TCP_PORT="${CHAL_PORT:-1337}"

# Locate simduino and libsimavr
SIMDUINO_BIN="${SIMAVR_ROOT}/examples/board_simduino/obj-x86_64-linux-gnu/simduino.elf"
LIBSIM="${SIMAVR_ROOT}/obj-x86_64-linux-gnu/libsimavr.so"

if [[ -z "${SIMDUINO_BIN}" || ! -x "${SIMDUINO_BIN}" ]]; then
  echo "Challenge Failed to Launch. Bother RSTCON Staff. Error 1"; exit 1
fi

if [[ -z "${LIBSIM}" ]]; then
  echo "Challenge Failed to Launch. Bother RSTCON Staff. Error 2"; exit 2
fi

if [[ ! -f "${CHAL_HEX}" ]]; then
  echo "Challenge Failed to Launch. Bother RSTCON Staff. Error 3"; exit 3
fi

SIMDIR="$(dirname "${SIMDUINO_BIN}")"
BOOT_A="${SIMDIR}/ATmegaBOOT_168_atmega328.ihex"
BOOT_B="${SIMDIR}/ATmegaBOOT_168_atmega328p.hex"

# Ensure a real bootloader exists; Dockerfile should have copied it already
if [[ ! -s "${BOOT_A}" && ! -s "${BOOT_B}" ]]; then
  echo "Challenge Failed to Launch. Error 4"; exit 4
fi

# If only the alt name exists, provide the expected one too
if [[ ! -f "${BOOT_A}" && -f "${BOOT_B}" ]]; then
  ln -s "$(basename "${BOOT_B}")" "$(basename "${BOOT_A}")"
fi

# Clean shutdown on exit
SIMPID=""
cleanup(){ 
  set +e; [[ -n "${SIMPID}" ]] && kill "${SIMPID}" 2>/dev/null || true;
  rm -f "${LOGFILE}"
}
trap cleanup EXIT

# echo "[+] Launching simduino (no arguments)…"

cd "${SIMDIR}"
export LD_LIBRARY_PATH="$(dirname "${LIBSIM}"):${LD_LIBRARY_PATH-}"

UNIQUE_LOG_DIR="/tmp/$(mktemp -d)"
mkdir -p "${UNIQUE_LOG_DIR}"
LOGFILE="${UNIQUE_LOG_DIR}/simduino.log"

stdbuf -oL ${SIMDUINO_BIN} > ${LOGFILE}  2>/dev/null &

# Wait for file to exist
while [ ! -f "${LOGFILE}" ]; do
	sleep .25
done

# echo "[+] Log file exists: ${LOGFILE}"
SIMPID=$!

UART_SOCKET=$(cat ${LOGFILE} | head -n 6 | tail -n 2 | head -n 1 | awk -F ' ' '{print $NF}')

# echo "[+] Flashing firmware via avrdude…"
avrdude -qq -p m328p -c arduino -P "${UART_SOCKET}" -U "flash:w:${CHAL_HEX}" > /dev/null 2>&1

socat STDIO ${UART_SOCKET},raw,echo=0,ignoreeof

wait "${SIMPID}"