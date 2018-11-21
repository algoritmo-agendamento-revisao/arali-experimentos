## Aplicação de Agendamento de Revisões Utilizando Aprendizado por Reforço - Experimentos
Esse repositório hospeda o código fonte que foi utilizado para realização dos experimentos para comparar e comprovar a 
performance do algoritmo de agendamento de revisões com uma política aleatória.  
O experimento gera um gráfico e uma tabela para cada cenário estipulado, totalizando 81 gŕaficos e 81 tabelas no final 
da execução.  
  
Foram definidos para os testes:
* 3 experimentos para cada cenário
    * Cada experimento composto por 100 episódios
        * Cada episódio composto por 200 passos  
        
Em cada passo o estudante simulado repete todos os 30 cards que estão em seu plano de estudo. Os cards são simulados e 
quando o estudante aprende um card, outro é inserido imediatamente em seu plano de estudo para que sempre o estudante 
tenha 30 cards para estudar.

Os cenários de teste foram combinados de acordo com a variação de 4 fatores que  influem diretamente no algoritmo de 
aprendizado por reforço escolhido: Q-Learning. Esses fatores são:
* Fator de desconto: 0.1, 0.5, 0.9
* Taxa de aprendizagem: 0.1, 0.9, 1/R
* Taxa de Exploração: 0.1, 0.9, 1/R
* Fórmula de recompensa: (encontradas no user_interface/user_interface.py)

### Requisitos de software
* Python 3.6+
* pip3

### Dependências em Python
São especificadas no arquivo requirements.txt

### Rodando o experimento
Executar o script: script_experimento.py  

OBS: O experimento leva em torno de 4 horas para ser completo.