# Aula 06 – Programação Assistida por Inteligência Artificial

**Texto-base:** Vibe coding: programming through conversation with artificial intelligence – Advait Sarkar e Ian Drosos

**Estudante:** Lazim Francisco de Oliveira Junior

---

## Trechos que chamaram minha atenção

**1. O caso do app de câmbio (seção 3.2.2).** O usuário pediu dados históricos e a IA fez um seletor para uma data só, quando ele queria um intervalo. Como funcionou, ele aceitou. Depois, quando pediu o intervalo de forma explícita, a IA continuou gerando código em cima da primeira ideia. Os autores chamam isso de "context momentum". Achei interessante porque mostra que aceitar uma coisa "quase certa" no começo pode atrapalhar o projeto inteiro depois.

**2. A forma como os programadores leem o código gerado (seção 3.5.1).** Eles não leem linha por linha, só olham o tamanho do diff, os nomes das funções e as chamadas de API. Teve um caso em que a pessoa aceitou várias alterações em uns dois segundos. Isso só funciona porque ela já conhecia muito bem o próprio código. Para alguém sem essa experiência, isso seria aceitar no escuro.

---

## Questão 1 – Até que ponto podemos confiar no código produzido pela IA?

Pelo que o artigo mostra, a confiança no código da IA não deve ser automática. Ela vai sendo construída conforme o código é revisado e testado. Mesmo sendo vídeos de "vibe coding", nenhum dos programadores analisados aceitava tudo sem olhar, como o Karpathy descreve no tweet dele. O programador do YT21, por exemplo, diz que chega a 80 ou 90% da solução com a IA, mas que revisa as mudanças para continuar no controle.

Antes de aceitar um código gerado, acredito que o básico seja entender o que ele faz, testar além do caso que já funciona e conferir se as bibliotecas e funções usadas realmente existem na versão do projeto. Esse último ponto aparece no artigo: no YT21 a IA gerou propriedades que não existiam, e no YT22 a documentação veio baseada no Next.js 14, sendo que o projeto usava o 15. Também é importante ver se a alteração afeta outras partes do sistema, porque a IA não enxerga tudo o que o programador sabe sobre o projeto.

O principal risco de aceitar sem revisão é o erro aparecer só depois, em produção, ou virar algo estrutural, como no caso do app de câmbio. Além disso, a equipe perde o entendimento do próprio código, e aí qualquer manutenção passa a depender da IA de novo.

---

## Questão 2 – A IA reduz a necessidade de conhecimento em programação ou transforma o tipo de conhecimento necessário?

Na minha leitura, ela transforma. Essa é uma das conclusões principais do artigo: o conhecimento não some, ele muda de lugar. O programador escreve menos código e passa mais tempo orientando, revisando e corrigindo o que a IA fez.

O que percebi é que todas as coisas que os programadores fizeram bem nos vídeos dependiam de conhecimento técnico. Quando a tela ficou em branco no YT22, o criador abriu o console e identificou o erro na hora. Também foi ele quem percebeu que o sistema estava tentando conectar no PostgreSQL em vez do Supabase e corrigiu direto no arquivo de ambiente. No YT15, o programador notou que a IA estava "reinventando a roda" em vez de usar uma biblioteca. Nada disso seria possível sem saber programar.

Então as competências que ganham importância são leitura rápida de código, depuração, visão de como as partes do sistema se conectam e saber explicar bem o que se quer. Além disso entra o conhecimento sobre a própria IA, como saber quando abrir uma conversa nova ou dividir a tarefa em partes menores.

Um ponto que achei importante é que os próprios autores admitem que só analisaram programadores experientes. Então não dá para dizer que alguém sem base teria o mesmo resultado. Para quem ainda está estudando, como eu, isso acende um alerta: se a gente usar a IA para tudo, pode não desenvolver justamente o conhecimento que é necessário para usá-la bem.

---

## Questão 3 – Quando é melhor utilizar a IA e quando é melhor assumir o controle manualmente?

O artigo mostra que os próprios programadores nem sempre tinham um critério claro para isso. Com base no que eles fizeram, eu pensaria em três situações.

Faz sentido delegar para a IA tarefas repetitivas e fáceis de verificar, como estrutura inicial de projeto, telas simples e protótipos. Se der errado, o custo é baixo e o erro é fácil de perceber.

Trabalhar em conjunto funciona melhor em funcionalidades médias, divididas em etapas. O YT22 fazia isso pedindo "só a fase um" para a IA não se perder. O TW1 também comentou que esperar uma resposta perfeita da IA é um erro: o ideal é ela chegar perto e o programador ajustar o resto.

Já o trabalho manual é melhor em alterações pequenas, quando escrever o prompt dá mais trabalho do que fazer a mudança. O YT21 desistiu de usar a IA para editar uma única linha. Também vale fazer manualmente quando a IA não entende o que se quer depois de algumas tentativas, e em partes críticas como autenticação, pagamento e dados sensíveis.

Resumindo, se a equipe não consegue validar o que a IA entregou, ela não deveria ter delegado aquela tarefa.

---

## Estudo de caso

O problema do caso é que passar em um teste inicial só mostra que o código funciona no cenário mais simples. Isso é parecido com o "Accept All" do Karpathy, só que em um projeto real. No artigo, até o streamer do TW1 revisava o pull request antes de publicar uma página simples, justamente porque não queria código ruim entrando em um sistema grande.

Antes de incorporar o código, a equipe deveria:

1. Fazer uma revisão por alguém que não gerou o código, garantindo que pelo menos uma pessoa consiga explicar como ele funciona.
2. Conferir as dependências adicionadas: se existem, se são compatíveis com a versão do projeto e se não têm vulnerabilidades conhecidas.
3. Verificar pontos de segurança, como validação de entrada, tratamento de erros e credenciais no código.
4. Criar mais testes, incluindo casos de erro e testes de integração com as partes do sistema que a funcionalidade afeta.
5. Ajustar o que estiver fora do padrão do projeto ou complexo demais, para não virar dívida técnica.

As responsabilidades que continuam sendo humanas são decidir o que deve ser construído, validar se o código está correto e seguro, aprovar se ele vai para produção e responder pelos problemas que ele causar. Como o criador do YT22 disse, a IA é só uma ferramenta.

---

## Boas práticas

1. Não colocar no projeto código que ninguém da equipe consegue explicar.
2. Dividir as tarefas em partes menores e dar contexto claro para a IA, como a documentação oficial e a versão das tecnologias usadas.
3. Fazer manualmente as partes críticas do sistema e as alterações pequenas.

## Síntese

"Programar com IA de maneira responsável não significa apenas saber pedir código; significa também..."

...entender o que foi gerado, testar e assumir a responsabilidade pelo resultado. O artigo mostra que a IA não substitui o conhecimento em programação, só muda a forma como ele é usado: o programador passa a revisar, corrigir e decidir quando é melhor fazer por conta própria. A confiança na IA precisa ser construída a cada entrega, e não assumida desde o começo. Aceitar um código só porque ele parece funcionar pode trazer problemas maiores depois. A IA ajuda a ganhar velocidade, mas as decisões continuam sendo nossas.
