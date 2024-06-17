# Gerenciamento de Estufas Inteligentes

Estufas são utilizadas no cultivo de plantas em condições controladas de temperatura, umidade, luminosidade, nível de CO2, entre outras variáveis. Esta aplicação tem como objetivo configurar, monitorar e controlar as condições da estufa por meio de um gerenciador que se comunica com os sensores e atuadores dentro da estufa e pode receber configurações ou responder consultas de um cliente externo.

## Componentes

### Sensores

- **Temperatura interna:** Mede a temperatura interna da estufa.
- **Umidade do solo:** Mede o nível de umidade do solo.
- **Nível de CO2:** Mede a concentração de CO2 no ambiente da estufa.

### Atuadores

- **Aquecedor:** Aumenta a temperatura quando ligado.
- **Resfriador:** Diminui a temperatura quando ligado.
- **Sistema de irrigação:** Aumenta a umidade do solo quando ligado.
- **Injetor de CO2:** Aumenta a concentração de CO2 quando ligado.

### Gerenciador

O Gerenciador funciona como o servidor da aplicação, responsável por:

- Receber dados dos sensores.
- Controlar os atuadores para manter as condições ideais dentro da estufa.
- Comunicar-se com o cliente para receber configurações e fornecer leituras dos sensores.

### Cliente

O Cliente pode:

- Configurar os parâmetros da estufa (temperatura, umidade, nível de CO2, etc.).
- Requisitar os valores das leituras dos sensores para monitoramento.

## Princípio de Operação

O Gerenciador deve manter as leituras dos sensores entre os valores máximo e mínimo configurados. Para isso, ele monitora continuamente os dados dos sensores e aciona os atuadores conforme necessário para ajustar as condições da estufa:

- **Temperatura:** Se a temperatura estiver abaixo do mínimo configurado, o aquecedor é ligado. Se estiver acima do máximo, o resfriador é acionado.
- **Umidade do solo:** Se a umidade estiver abaixo do mínimo configurado, o sistema de irrigação é ativado.
- **Nível de CO2:** Se a concentração de CO2 estiver abaixo do mínimo configurado, o injetor de CO2 é ligado.

## Como Usar

1. **Configuração Inicial:**
   - O Cliente envia as configurações desejadas (valores máximos e mínimos para temperatura, umidade e CO2) para o Gerenciador.

2. **Monitoramento:**
   - O Gerenciador monitora continuamente os sensores e ajusta os atuadores para manter as condições dentro dos parâmetros configurados.

3. **Consultas:**
   - O Cliente pode solicitar leituras atuais dos sensores a qualquer momento.

## Exemplo de Configuração

```json
{
  "temperatura_min": 20,
  "temperatura_max": 25,
  "umidade_min": 30,
  "umidade_max": 50,
  "co2_min": 300,
  "co2_max": 600
}
