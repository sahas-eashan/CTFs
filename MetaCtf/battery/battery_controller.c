/*
 * battery_controller.c
 *
 * This program replaces the previous flow controller challenge with a new
 * battery configuration challenge. The core logic comes from a challenge
 * authored by a friend, which includes some deliberate bugs and
 * vulnerabilities. The code has been integrated into the existing
 * UART/AVR scaffolding so it can run both on a desktop and on an
 * ATmega328P (or similar) microcontroller. When compiled for desktop
 * targets the UART helpers wrap stdio; on AVR the helpers talk to the
 * hardware UART.  No attempt has been made to fix any of the logic
 * errors from the original challenge.
 *
 * Build for desktop (test):
 *   gcc -std=c99 -O2 -o battery_controller battery_controller.c
 *
 * Build for AVR (ATmega328P):
 *   avr-gcc -mmcu=atmega328p -DF_CPU=16000000UL -Os -o battery_controller.elf battery_controller.c
 *   avr-objcopy -O ihex battery_controller.elf battery_controller.hex
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

/* UART helpers: use hardware UART on AVR, stdio on desktop */
#ifdef __AVR__
#  include <avr/io.h>
#  include <util/delay.h>
#  define F_CPU 16000000UL
#  define BAUD 9600
#  define MYUBRR ((F_CPU/16/BAUD)-1)
#else
/* Desktop: nothing special */
#endif

/* ----------------- UART helpers ----------------- */
static void uart_init(void);
static void uart_tx(char c);
static void uart_print(const char *s);
static char uart_rx(void);
static void uart_readline(char *buf, size_t max);
static void uart_read_n(char *buf, size_t n);

#ifdef __AVR__
/* AVR implementation */
static void uart_init(void) {
    uint16_t ubrr = (uint16_t)MYUBRR;
    UBRR0H = (uint8_t)(ubrr >> 8);
    UBRR0L = (uint8_t)(ubrr & 0xff);
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);  // enable rx/tx
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00); // 8N1
}

static void uart_tx(char c) {
    while (!(UCSR0A & (1 << UDRE0))) ;
    UDR0 = (uint8_t)c;
}

static void uart_print(const char *s) {
    while (*s) uart_tx(*s++);
}

static char uart_rx(void) {
    while (!(UCSR0A & (1 << RXC0))) ;
    return (char)UDR0;
}

/* Reads up to max-1 chars, stops on CR/LF. Echoes input. */
static void uart_readline(char *buf, size_t max) {
    size_t i = 0;
    while (i < max - 1) {
        char c = uart_rx();
        if (c == '\r' || c == '\n') break;
        buf[i++] = c;
        uart_tx(c);
    }
    buf[i] = '\0';
}

/* Reads exactly n bytes (no newline semantics) */
static void uart_read_n(char *buf, size_t n) {
    for (size_t i = 0; i < n; i++) {
        buf[i] = uart_rx();
    }
}

#else
/* Desktop stdio implementation */
static void uart_init(void) {
    /* Unbuffered streams help interactive behavior */
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

static void uart_tx(char c) {
    putchar((int)c);
}

static void uart_print(const char *s) {
    fputs(s, stdout);
}

static char uart_rx(void) {
    int c = getchar();
    if (c == EOF) return '\0';
    return (char)c;
}

/* Desktop version of uart_readline: reads up to max-1 characters and stops on CR/LF. Echoes input. */
static void uart_readline(char *buf, size_t max) {
    size_t i = 0;
    while (i < max - 1) {
        char c = uart_rx();
        if (c == '\r' || c == '\n') break;
        buf[i++] = c;
        uart_tx(c); // echo
    }
    if (i >= max - 1) i = max - 2;
    buf[i] = '\0';
}

/* Reads exactly n bytes from UART (no newline semantics) */
static void uart_read_n(char *buf, size_t n) {
    for (size_t i = 0; i < n; i++) {
        buf[i] = uart_rx();
    }
}
#endif
/* ----------------- end UART helpers ----------------- */

/* Platform-appropriate address-sized integer. Not used in this challenge but defined
 * to mirror the flow controller example. On AVR this is 16-bit, on desktop uintptr_t.
 */
#ifdef __AVR__
typedef uint16_t addr_t;
#else
typedef uintptr_t addr_t;
#endif

#define NAME_LEN 16

#define MAX_BUF_LEN NAME_LEN+16
typedef void (*VoidFunc)(void);
char buffer[MAX_BUF_LEN];
int target_voltage;
 
struct Monitor {
    char name[NAME_LEN]; 
    VoidFunc cb;
};
 
void set_voltage(unsigned int v){
	if (v > 999){
		printf("\nVoltage too big: %s\n", target_voltage);
	}else{
		printf("\nTarget Voltage Set: %d\n", target_voltage);
	}
}
 
void get_voltage(char* v_out)
{
    uart_print("\nEnter target voltage (0-999):\n>");
	uart_readline(buffer, MAX_BUF_LEN);
	memcpy(buffer, v_out, NAME_LEN);
}
 
 
void voltage_handler(){
	unsigned int volts;
	char voltage_str[NAME_LEN];
 
	get_voltage(voltage_str);
	volts = (unsigned int) strtol(voltage_str, NULL, 10);
	set_voltage(volts);
}
 
void version_handler(){
	 uart_print("\nVersion: 2.0.25\n");
}

void easter_egg(){
    uart_print("\nCheck out Jordan Moore's Styx Emulator talk at 1300 on Saturday!\n");
}

void win(){
    uart_print("rstcon{thisisplaceholdertestflag}");
}
 
 
VoidFunc is_valid_command(char* cmd) {

	if (!strncmp(cmd, "volts", strlen("volts"))){
		return voltage_handler;
	}else if (!strncmp(cmd, "version", strlen("version"))){
		return version_handler; 
    }else if (!strncmp(cmd, "egg", strlen("egg"))){
		return easter_egg;
	}else {
		return (VoidFunc) NULL;
	}
}
 
 
int runner(){
	struct Monitor m;
	int cmd_len;
	VoidFunc handler;


    uart_print("\nEnter Command:\n>");
	uart_readline(buffer, MAX_BUF_LEN);
 
	// check size
	cmd_len = strlen(buffer);
	if (cmd_len >= NAME_LEN) {
		uart_print("\nCommand too long\n");
		return 1;
	}

	while ((handler=is_valid_command(buffer))==NULL) {
		uart_print("\nUnknown command\n>");
		uart_readline(buffer, MAX_BUF_LEN);
	}
 
	m.cb = handler;
	strcpy(m.name, buffer);
 
	m.cb();
}

/* Program entry: initialize UART and run commands in a loop. */
int main(void) {
    uart_init();
    uart_print("\r\n --- Battery Controller Panel ---\r\n");
    /* Simple REPL loop: repeatedly run commands. */
    while (1) {
        runner();
    }
    return 0;
}
