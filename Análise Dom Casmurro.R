## Analise exploratoria de Dom Casmurro
library(NLP)
library(tm)
library(syuzhet)
library(RColorBrewer)
library(wordcloud)
library(stargazer)
library(kableExtra)
library(tidyverse)
library(xtable)

## Le o texto dom casmurro
texto <- scan(file = "https://raw.githubusercontent.com/programminghistorian/jekyll/gh-pages/assets/domCasmurro.txt", fileEncoding = "UTF-8", what = character(), sep = "\n", allowEscapes = T)

## Transforma o texto em um vetor de caracteres, cada elemento uma palavra
texto_palavras <- get_tokens(texto)

## Extrai os sentimentos das palavras do texto
sentimentos_df <- get_nrc_sentiment(texto_palavras, lang="portuguese")

head(sentimentos_df)

summary(sentimentos_df)

tabela_sentimentos <- kable(summary(sentimentos_df), format = "latex", booktabs = TRUE, caption = "Análise de Sentimentos NRC") %>%
  kable_styling(latex_options = c("hold_position", "striped"))

## Grafico de barras das emocoes
barplot(
  colSums(prop.table(sentimentos_df[, 1:8])),
  space = 0.2,
  horiz = FALSE,
  las = 1,
  cex.names = 0.6,
  col = brewer.pal(n = 8, name = "Set3"),
  main = "'Dom Casmurro' de Machado de Assis",
  xlab="emoções", ylab = NULL)

## Contando quantas vezes cada palavra relacionada a tristeza aparece no romance
palavras_tristeza <- texto_palavras[sentimentos_df$sadness > 0]
palavras_tristeza_ordem <- sort(table(unlist(palavras_tristeza)), decreasing = TRUE)
head(palavras_tristeza_ordem, n = 12)
head(palavras_tristeza_ordem, n = 12)

## Criando nuvens de palavras
nuvem_emocoes_vetor <- c(
  paste(texto_palavras[sentimentos_df$sadness> 0], collapse = " "),
  paste(texto_palavras[sentimentos_df$joy > 0], collapse = " "),
  paste(texto_palavras[sentimentos_df$anger > 0], collapse = " "),
  paste(texto_palavras[sentimentos_df$fear > 0], collapse = " "))

nuvem_emocoes_vetor <- iconv(nuvem_emocoes_vetor, "latin1", "UTF-8")
nuvem_corpus <- Corpus(VectorSource(nuvem_emocoes_vetor))

nuvem_tdm <- TermDocumentMatrix(nuvem_corpus)
nuvem_tdm <- as.matrix(nuvem_tdm)
head(nuvem_tdm)

colnames(nuvem_tdm) <- c('tristeza', 'alegria', 'raiva', 'confiança')
head(nuvem_tdm)

set.seed(757) # pode ser qualquer número
comparison.cloud(nuvem_tdm, random.order = FALSE,
                 colors = c("green", "red", "orange", "blue"),
                 title.size = 1, max.words = 50, scale = c(2.5, 1), rot.per = 0.4)

## Evolucao dos sentimentos no texto
sentimentos_valencia <- (sentimentos_df$negative * -1) + sentimentos_df$positive
grafico_valencia <- simple_plot(sentimentos_valencia)