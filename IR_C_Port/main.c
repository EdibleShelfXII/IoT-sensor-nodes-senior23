#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wiringPi.h>

#define GPIO_IR_RECEIVER 23

int main() {
  
}

int getMessage() {
    uint8_t bytes[] = {0, 0, 0, 0};
    if (IRStart() == 0) {
        delay(0.11);
    } else {
        for (int i = 0; i < 4; i++) {
            bytes[i] = getByte();
            // Start signal is followed by 4 bytes:
            // byte[0] is an 8-bit ADDRESS for receiving
            // byte[1] is an 8-bit logical inverse of the ADDRESS
            // byte[2] is an 8-bit COMMAND
            // byte[3] is an 8-bit logical inverse of the COMMAND
            if ((bytes[0] + bytes[1] == 0xff) && (bytes[2] + bytes[3] == 0xff)) {
                uint16_t message = (bytes[0] << 8) + bytes[2];
                printf("Message Received: %i\n", message);
                return message
            } else { return 0; }
        }
    }
}
