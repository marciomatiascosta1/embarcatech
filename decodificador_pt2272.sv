// Decodificador PT2272
module decodificador_pt2272 (
    input clk,              // Clock de entrada com frequência de 3 MHz
    input reset,            // Sinal de reset ativo alto
    input [7:0] A,          // Endereço de entrada (8 bits, representado em formato trinário)
    input cod_i,            // Entrada serial codificada
    output logic [3:0] D,   // Dados decodificados de saída
    output logic dv         // Sinaliza se os dados decodificados são válidos
);

    // Declarações internas
    logic [11:0] pacote;          // Registro que armazena o pacote recebido
    logic [7:0] A_01;             // Saída do bloco comp_endereco para bits não flutuantes
    logic [7:0] A_F;              // Saída do bloco comp_endereco para bits flutuantes
    logic [3:0] estado;           // Estado atual da máquina de estados finita (FSM)

    // Instância do bloco comp_endereco
    // Este bloco processa o endereço de entrada (A) para determinar bits flutuantes e não flutuantes
    comp_endereco comp_inst (
        .A(A),                    // Endereço de entrada
        .A_01(A_01),              // Saída de bits não flutuantes
        .A_F(A_F)                 // Saída de bits flutuantes
    );

    // FSM para decodificação
    // A FSM gerencia a recepção, validação do pacote e extração dos dados
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            estado <= 0;          // Estado inicial após o reset
            D <= 0;               // Zera os dados de saída
            dv <= 0;              // Sinal de dado válido desativado
        end else begin
            case (estado)
                // Estado 0: Recepção do pacote
                0: begin
                    if (cod_i) begin
                        pacote <= {pacote[10:0], cod_i}; // Desloca o bit recebido para o registro do pacote
                        if (pacote[3:0] == 4'b0000)      // Detecta o símbolo SYNC (últimos 4 bits)
                            estado <= 1;                 // Avança para o estado de validação
                    end
                end

                // Estado 1: Validação do pacote
                1: begin
                    if (pacote[11:4] == {A_F, A_01}) begin // Verifica se o endereço recebido é válido
                        D <= pacote[3:0];                  // Extrai os dados recebidos
                        dv <= 1;                           // Ativa o sinal de dado válido
                        estado <= 0;                       // Retorna ao estado inicial
                    end
                end
            endcase
        end
    end

endmodule

// Divisor de clock
module clock_divider #(parameter DIV = 250) (
    input logic clk_in,          // Clock de entrada
    input logic reset,           // Sinal de reset ativo alto
    output logic clk_out         // Clock de saída dividido
);

    logic [15:0] count;          // Contador para dividir o clock

    always_ff @(posedge clk_in or posedge reset) begin
        if (reset) begin
            count <= 0;          // Reinicia o contador
            clk_out <= 0;        // Zera o clock de saída
        end else begin
            if (count == DIV - 1) begin
                count <= 0;      // Reinicia o contador quando atinge o divisor
                clk_out <= ~clk_out; // Alterna o estado do clock de saída
            end else begin
                count <= count + 1; // Incrementa o contador
            end
        end
    end

endmodule

