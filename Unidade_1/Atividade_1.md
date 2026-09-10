## WhatsApp

**1. Onde a IA está presente neste app?**
Assistente Meta AI no chat (perguntas, geração de texto/resumos); edição de fotos por IA dentro da conversa (remover/trocar fundo, aplicar estilo) antes de enviar; geração de imagem a partir de descrição em linguagem natural.

**2. Qual problema ela procura resolver?**
A fricção de sair do app para outra ferramenta (editor de imagem, tradutor) e a impossibilidade de ouvir um áudio em determinados contextos — a IA internaliza essas tarefas no próprio fluxo da conversa. Também oferece transcrição de áudio em casos onde o usuário não pode ouvir o som no momento.

**3. Quais dados provavelmente são utilizados?**
Mensagens comuns entre usuários seguem criptografadas ponta a ponta por padrão e não alimentam a IA. O que é processado é o que você envia diretamente ao Meta AI (perguntas, fotos para edição) e metadados de uso.

**4. Qual é o benefício direto para o usuário?**
Elimina etapas: edição de imagem e tradução sem abrir outro app; transcrição resolve o caso de não poder ouvir o áudio no momento.

**5. Existe algum risco ou limitação observável?**
Alucinação (respostas erradas com aparência de certeza, como em qualquer LLM) e fragilidade do consentimento: o uso de dados para treinar IA já foi suspenso judicialmente em jul/2024 por falta de consentimento explícito dos usuários brasileiros.

## Instagram

**1. Onde a IA está presente neste app?**
Quatro sistemas de ranqueamento distintos (Feed, Reels, Stories, Explorar) — não existe "um algoritmo único", segundo o próprio chefe do Instagram; IA generativa para edição e "Reels com IA Conversacional" (sistema de recomendação que sugere vídeos com base no comportamento).

**2. Qual problema ela procura resolver?**
Curadoria em escala: com bilhões de posts, curadoria manual é inviável — o sistema decide relevância combinando interesse inferido, contexto do conteúdo e recência.

**3. Quais dados provavelmente são utilizados?**
Curtidas, salvamentos, compartilhamentos, comentários, tempo de permanência e replays; histórico de contas seguidas/visitadas; conteúdo textual e visual dos posts. Mesmo mecanismo regulatório da Meta responde aqui.

**4. Qual é o benefício direto para o usuário?**
Reduz o custo de busca: conteúdo relevante aparece mesmo vindo de contas não seguidas, sem esforço ativo de curadoria.

**5. Existe algum risco ou limitação observável?**
A otimização por tempo de exibição e replays incentiva formatos de "loop visual" desenhados para manter o usuário em scroll contínuo — não é efeito colateral, é a métrica que o sistema otimiza explicitamente.

## Pinterest

**1. Onde a IA está presente neste app?**
Pinterest Lens (busca visual: foto → itens semelhantes, via modelo de linguagem visual); Pinterest Assistant (busca multimodal imagem+voz+texto, beta EUA); geração automática de palavras-chave de busca a partir de imagens.

**2. Qual problema ela procura resolver?**
"Reconheço mas não sei descrever": o modelo decompõe a imagem e devolve os termos de busca, transformando gosto estético em texto pesquisável.

**3. Quais dados provavelmente são utilizados?**
Imagens salvas/pinadas, fotos capturadas via Lens (inclusive do ambiente físico do usuário, não só da internet), embeddings multimodais imagem+texto, comportamento de clique e compra associado a cada pin.

**4. Qual é o benefício direto para o usuário?**
Encurta a jornada de inspiração até compra — "comprar semelhante" direto a partir de uma imagem, sem depender de vocabulário de busca preciso.

**5. Existe algum risco ou limitação observável?**
Lens processa fotos do ambiente físico do usuário — superfície de coleta mais invasiva que busca textual, podendo capturar objetos ou pessoas de terceiros sem consentimento delas. A plataforma também não garante que a imagem capturada não será usada para retreinar o modelo.

## TikTok

**1. Onde a IA está presente neste app?**
For You Page (FYP): motor de recomendação central, decide o feed sem exigir que o usuário siga ninguém; moderação automática (spam, conteúdo reciclado, penalização de IA genérica de baixa qualidade); classificação de tendências em tempo real.

**2. Qual problema ela procura resolver?**
Cold-start de recomendação: diferente de feeds baseados em "quem você segue", o FYP personaliza usando só sinais comportamentais — funciona para um usuário novo, sem histórico social.

**3. Quais dados provavelmente são utilizados?**
Tempo de visualização por vídeo, taxa de conclusão, replays, velocidade de deslizar/pular, compartilhamento por DM, e metadados do conteúdo (áudio, texto na tela, hashtags).

**4. Qual é o benefício direto para o usuário?**
Alta taxa de acerto de interesse com esforço zero de curadoria: vídeos curtos geram muitos data points por sessão, então o sistema aprende em minutos, não semanas.

**5. Existe algum risco ou limitação observável?**
O mecanismo de ranking (otimização de "Session Value"/tempo de tela, termo usado pela própria indústria em 2026) é estruturalmente desenhado para maximizar consumo — essa é a métrica-alvo, não um efeito colateral. Risco de vício comportamental em usuários jovens.

## Telegram

**1. Onde a IA está presente neste app?**
Sem "algoritmo de feed" central como Instagram/TikTok — a IA aparece via bots opcionais (ativados manualmente, inclusive como "convidados" em qualquer conversa desde mai/2026) e no editor de texto com sugestões.

**2. Qual problema ela procura resolver?**
Automação de atendimento e moderação em grupos grandes (até 200 mil membros): um bot responde perguntas repetidas 24h em qualquer idioma, sem trabalho humano.

**3. Quais dados provavelmente são utilizados?**
O texto enviado diretamente a um bot ou ao editor de IA. Ponto crítico: chats "normais" do Telegram usam criptografia cliente-servidor, não ponta a ponta por padrão — só "Chats Secretos" (individuais) usam e2e criptografia.

**4. Qual é o benefício direto para o usuário?**
Controle explícito de opt-in: o usuário escolhe quando e qual bot ativar, ao invés de um feed que decide por ele.

**5. Existe algum risco ou limitação observável?**
A API do BotFather é aberta — qualquer desenvolvedor publica um "bot de IA" sem curadoria de segurança do Telegram. A responsabilidade por vazamento de dados recai sobre um ecossistema fragmentado de desenvolvedores terceirizados, nem sempre confiáveis.
