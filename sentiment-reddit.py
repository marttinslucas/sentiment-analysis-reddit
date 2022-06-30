import argparse
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from googletrans import Translator
import praw
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sys

def word_cloud(wd_list, title):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        random_state=42,
        colormap='jet',
        max_words=100).generate(all_words)

    plt.figure(figsize=(10, 5))
    plt.axis('off')
    plt.title(title, fontsize=20)
    plt.imshow(wordcloud, interpolation="bilinear");


def main(subredt, topic, sort_topic, search_limit, CLIENT_ID, SECRET_KEY, USER):
    nltk.download('vader_lexicon')
    vader_model = SentimentIntensityAnalyzer()
    translate_model = Translator()

    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET_KEY, user_agent=USER)

    posts ={'headline': []} 
    for sub in reddit.subreddit(subredt).search(topic, sort=sort_topic, limit=search_limit):
        posts['headline'].append(sub.title)

    for i in range(search_limit):
        for key, value in posts.items():
            phrase = value[i]
            src = translate_model.detect(phrase).lang
            if src == 'en':
                continue
            else:
                posts[key][i] = translate_model.translate(phrase, src = src, dest='en').text

    posts_df = pd.DataFrame.from_dict(posts)

    posts_df['scores'] = posts_df['headline'].apply(lambda headline: vader_model.polarity_scores(headline))
    posts_df['neg'] = [vader_model.polarity_scores(x)['neg'] for x in posts_df.headline]
    posts_df['neu'] = [vader_model.polarity_scores(x)['neu'] for x in posts_df.headline]
    posts_df['pos'] = [vader_model.polarity_scores(x)['pos'] for x in posts_df.headline]
    posts_df['compound']  = posts_df['scores'].apply(lambda score_dict: score_dict['compound'])
    posts_df['comp_score'] = posts_df['compound'].apply(lambda compound: 'positivo' if compound>0.05 else 'negativo' if compound<-0.5 else 'neutro')

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1,2, figsize=(10,5))
    sns.barplot(posts_df['comp_score'].value_counts().index, posts_df['comp_score'].value_counts().values, alpha=0.8, ax=axes[0])
    axes[0].set_title(f'Análise de sentimento dos HeadLines do Reddit baseado no tópico {topic}', fontsize=20)
    axes[0].set_ylabel('Frequência', fontsize=12)
    axes[0].set_xlabel('Sentimento', fontsize=12)
    posts_df['comp_score'].value_counts().plot.pie(autopct='%.1f%%',ax=axes[1]);
    

    print(posts_df.sort_values(by='compound', ascending=True)[:posts_df.comp_score[posts_df.comp_score == 'negativo'].value_counts().sum()])

    for col, row in posts_df.sort_values(by='compound', ascending=True)[:posts_df.comp_score[posts_df.comp_score == 'negativo'].value_counts().sum()].iteritems():
        if col == 'headline':
            negative_phrases = row.values

    print(f'frases negativas:\n----------\n{negative_phrases}')

    word_cloud(negative_phrases, 'Conjunto de palavras que mais aparecem nas frases negativas')
    word_cloud(posts_df.headline, 'Conjunto de palavras que mais aparecem em todos os posts')
    word_cloud(posts_df.headline[posts_df.comp_score == 'positivo'], 'Conjunto de palavras que mais aparecem nas frases positivas')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analise de sentimentos do reddit')
    parser.add_argument('-sub', '--subredt', dest='subredt', type=str, default='all', help='Nome do subreddit que se está buscando. Opcional', required=False)
    parser.add_argument('-t', '--topic', dest='topic', type=str, help='topico desejado para busca. Obrigatorio', required=True)
    parser.add_argument('-s', '--sort_topic',dest='sort_topic', type=str, default='relevance', help="Ordenamento dos posts, podem ser:\n 'relevance', 'date', 'hot', 'top', 'new' ou 'comments'. (default: 'relevance').",
                            required=False)
    parser.add_argument('-l', '--search_limit', type=int, dest='search_limit',
                        default=50, help='Limite de busca de topicos. Default: 50. Caso se esteja buscando topicos que nao em ingles, evitar grande quantidade.', required=False)
    parser.add_argument('-client', '--CLIENT_ID', dest='CLIENT_ID', type=str, help='Código do cliente, pode ser gerado no reddit.', required=True)
    parser.add_argument('-key', '--SECRET_KEY', dest='SECRET_KEY', type=str, help='Chave do cliente, também gerada no reddit.', required=True)
    parser.add_argument('-user', '--USER', dest='USER', type=str, help='Nome do usuário', required=True)

    
    args = parser.parse_args()

    main(args.subredt, args.topic, args.sort_topic, args.search_limit, args.CLIENT_ID, args.SECRET_KEY, args.USER)