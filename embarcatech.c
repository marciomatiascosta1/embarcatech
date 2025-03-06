#include "pico/stdlib.h"     // Biblioteca padrão do Raspberry Pi Pico
#include "hardware/i2c.h"    // Biblioteca para comunicação I2C
#include "hardware/adc.h"    // Biblioteca para conversão analógico-digital
#include "hardware/pwm.h"    // Biblioteca para controle de PWM

// Configuração dos periféricos
void setup_peripherals() {
    // Configuração do I2C
    i2c_init(i2c0, 400000); // Inicializa o I2C a 400 kHz
    gpio_set_function(20, GPIO_FUNC_I2C); // Configura GPIO20 como SDA
    gpio_set_function(21, GPIO_FUNC_I2C); // Configura GPIO21 como SCL
    gpio_pull_up(20); // Habilita pull-up no SDA
    gpio_pull_up(21); // Habilita pull-up no SCL

    // Configuração do ADC
    adc_init();                  // Inicializa o ADC
    adc_gpio_init(26);           // Configura GPIO26 para entrada analógica
    adc_gpio_init(27);           // Configura GPIO27 para entrada analógica

    // Configuração do PWM
    gpio_set_function(15, GPIO_FUNC_PWM); // Configura GPIO15 como saída PWM
    uint slice_num = pwm_gpio_to_slice_num(15); // Obtém o número do slice PWM
    pwm_set_wrap(slice_num, 255); // Define o valor máximo do contador PWM
    pwm_set_enabled(slice_num, true); // Habilita o PWM
}

// Função para ler a tensão em um pino ADC
float read_voltage(uint adc_pin) {
    adc_select_input(adc_pin); // Seleciona o canal ADC
    uint16_t raw_value = adc_read(); // Lê o valor do ADC
    return (raw_value * 3.3) / 4096.0; // Converte o valor bruto para volts
}

// Função para ler a corrente de um sensor no pino ADC
float read_current(uint adc_pin) {
    adc_select_input(adc_pin); // Seleciona o canal ADC
    uint16_t raw_value = adc_read(); // Lê o valor do ADC
    return ((raw_value * 3.3) / 4096.0) - 2.5; // Ajusta para sensor ACS712
}

// Função para controlar o motor via PWM
void control_motor(int duty_cycle) {
    uint slice_num = pwm_gpio_to_slice_num(15); // Obtém o slice do PWM
    pwm_set_gpio_level(15, duty_cycle); // Define o duty cycle
}

// Função principal
int main() {
    setup_peripherals(); // Configura os periféricos

    while (true) {
        // Leitura de sensores
        float voltage = read_voltage(26); // Lê a tensão no GPIO26
        float current = read_current(27); // Lê a corrente no GPIO27

        // Controle do motor baseado na tensão
        if (voltage < 12.0) {
            control_motor(128); // Define 50% do duty cycle
        } else {
            control_motor(0); // Desliga o motor
        }

        sleep_ms(1000); // Aguarda 1 segundo
    }

    return 0;
}

