#include <stdio.h>
#include "pico/stdlib.h"
#include <math.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"

#include "nec_receive_library/nec_receive.h"
#include "nec_transmit_library/nec_transmit.h"

#define PIN_SDA 4 // I2C Data
#define PIN_SCL 5 // I2C Clock

//IR LED connected to pin 14

const int ADDRESS = 0x44;

// I2C reserves some addresses for special purposes. We exclude these from the scan.
// These are any addresses of the form 000 0xxx or 111 1xxx
bool reserved_addr(uint8_t addr) {
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}



int main() {

    const uint led_pin = 25;

    int time_to_transmit_ms = 5000;
    int time_to_sleep_min = 5;
    int time_to_sleep_ms = (time_to_sleep_min * 60) * 1000;

    // Initialize LED pin
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    // Initialize chosen serial port
    stdio_init_all();

    PIO pio = pio0;                                 // choose which PIO block to use (RP2040 has two: pio0 and pio1)
    uint tx_gpio = 14;                              // choose which GPIO pin is connected to the IR LED
    uint rx_gpio = 15;                              // choose which GPIO pin is connected to the IR detector

    // configure and enable the state machines
    int tx_sm = nec_tx_init(pio, tx_gpio);         // uses two state machines, 16 instructions and one IRQ
    int rx_sm = nec_rx_init(pio, rx_gpio);         // uses one state machine and 9 instructions

    if (tx_sm == -1 || rx_sm == -1) {
        printf("could not configure PIO\n");
        return -1;
    }

    sleep_ms(5000);
    printf("working USB out!");

    // This example will use I2C0 on the default SDA and SCL pins (GP4, GP5 on a Pico)
    i2c_init(i2c0, 100 * 1000);
    gpio_set_function(PIN_SDA, GPIO_FUNC_I2C);
    gpio_set_function(PIN_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(PIN_SDA);
    gpio_pull_up(PIN_SCL);
    
/*
    printf("\nI2C Bus Scan\n");
    printf("   0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\n");

    for (int addr = 0; addr < (1 << 7); ++addr) {
        if (addr % 16 == 0) {
            printf("%02x ", addr);
        }

        // Perform a 1-byte dummy read from the probe address. If a slave
        // acknowledges this address, the function returns the number of bytes
        // transferred. If the address byte is ignored, the function returns
        // -1.

        // Skip over any reserved addresses.
        int ret;
        uint8_t rxdata;
        if (reserved_addr(addr))
            ret = PICO_ERROR_GENERIC;
        else
            ret = i2c_read_blocking(i2c0, addr, &rxdata, 1, false);

        printf(ret < 0 ? "." : "@");
        printf(addr % 16 == 15 ? "\n" : "  ");
    }
    printf("Done.\n");

    sleep_ms(1000);
*/
    
//    printf("read from sht40\n");

    uint8_t tx_bytes;
    uint8_t rx_bytes[6];
    uint16_t t_ticks;
    uint8_t checksum_t;
    uint16_t rh_ticks;
    uint8_t checksum_rh;
    float t_degC;
    float rh_pRH;

    // transmit and receive frames
    // Address changes randomly each time a transmission is sent
    uint8_t tx_address = 0x00, tx_data = 0x00, rx_address, rx_data;

    // init time
    absolute_time_t time = get_absolute_time();

    // init random number generator
    srand(time);


    // Loop forever
    while (true) {

        time = get_absolute_time();
        uint32_t starttime = to_ms_since_boot(time);
        uint32_t endtime = starttime + time_to_transmit_ms;

        while (starttime < endtime) {   
            time = get_absolute_time();
            starttime = to_ms_since_boot(time);

            gpio_put(led_pin, 1);

            tx_bytes = 0xFD;
/*
            for (int i = 0; i <= 6; i++)
                printf("byte %d = %x\n", i, rx_bytes[i]);
*/
            int bytes_written = i2c_write_blocking(i2c0, ADDRESS, &tx_bytes, 1, false);
//            printf("Bytes Written = %d\n", bytes_written);
            sleep_ms(10);
            int bytes_read = i2c_read_blocking(i2c0, ADDRESS, rx_bytes, 6, false);
/*
            printf("Bytes Read = %d\n", bytes_read);
            printf("Buffer = %x\n", rx_bytes);
            for (int i = 0; i <= 6; i++)
                printf("byte %d = %x\n", i, rx_bytes[i]);  
*/
            t_ticks = (rx_bytes[0] * 256) + rx_bytes[1];
            checksum_t = rx_bytes[2];
            rh_ticks = (rx_bytes[3] * 256) + rx_bytes[4];
            checksum_rh = rx_bytes[5];

//           printf("t_ticks = %d\nrh_ticks = %d\n", t_ticks, rh_ticks);

            t_degC = -45 + (175 * ((float)t_ticks/65535));
            rh_pRH = -6 + (125 * ((float)rh_ticks/65535));
            if (rh_pRH > 100)
                rh_pRH = 100;
            if (rh_pRH < 0)
                rh_pRH = 0;

            printf("Temperature: %.2f deg C\nRelative Humidity: %.2f%%\n", t_degC, rh_pRH);

            // randomize address
            tx_address = rand() % 255;
            printf("%x\n", tx_address);
    
            // create a 32-bit frame and add it to the transmit FIFO
            /*
            tx_data = 0xFF; // start command DEPRECATED
            uint32_t tx_frame = nec_encode_frame(tx_address, tx_data);
            pio_sm_put(pio, tx_sm, tx_frame);
            printf("sent: %02x, %02x\n", tx_address, tx_data);

            sleep_ms(30);
            */

            tx_data = rx_bytes[0]; // t part 1
            tx_frame = nec_encode_frame(tx_address, tx_data);
            pio_sm_put(pio, tx_sm, tx_frame);
            printf("sent: %02x, %02x\n", tx_address, tx_data);

            sleep_ms(30);

            tx_data = rx_bytes[1]; // t part 2
            tx_frame = nec_encode_frame(tx_address, tx_data);
            pio_sm_put(pio, tx_sm, tx_frame);
            printf("sent: %02x, %02x\n", tx_address, tx_data);

            sleep_ms(30);

            tx_data = rx_bytes[3]; // rh part 1
            tx_frame = nec_encode_frame(tx_address, tx_data);
            pio_sm_put(pio, tx_sm, tx_frame);
            printf("sent: %02x, %02x\n", tx_address, tx_data);

            sleep_ms(30);

            tx_data = rx_bytes[4]; // rh part 2
            tx_frame = nec_encode_frame(tx_address, tx_data);
            pio_sm_put(pio, tx_sm, tx_frame);
            printf("sent: %02x, %02x\n", tx_address, tx_data);

            sleep_ms(30);

            //gpio_put(led_pin, 0);
            
        }


        

        //sleep_ms(time_to_sleep_ms); // sleep mode to charge super cap
    }
}