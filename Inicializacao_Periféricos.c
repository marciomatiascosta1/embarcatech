// Este código configura GPIOs, I2C, ADC e PWM no Raspberry Pi Pico.

#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "hardware/adc.h"
#include "hardware/pwm.h"

void setup_peripherals() {
    // Configuração dos GPIOs para I2C
    i2c_init(i2c0, 400 * 1000); // I2C a 400 kHz
    gpio_set_function(20, GPIO_FUNC_I2C); // SDA
    gpio_set_function(21, GPIO_FUNC_I2C); // SCL
    gpio_pull_up(20);
    gpio_pull_up(21);

    // Configuração do ADC
    adc_init();
    adc_gpio_init(26); // ADC em GPIO26
    adc_gpio_init(27); // ADC em GPIO27

    // Configuração do PWM
    gpio_set_function(15, GPIO_FUNC_PWM);
    uint slice_num = pwm_gpio_to_slice_num(15);
    pwm_set_wrap(slice_num, 255);
    pwm_set_enabled(slice_num, true);
}

