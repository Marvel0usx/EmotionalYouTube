#!python
# data analysis

import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def generate_wordcloud(data: list):
    """Function to generate wordmap"""

    text = ' '.join(data[5])
    # backgroud_Image = plt.imread('job.jpg')
    stopwords = set('')
    stopwords.update(['be', 'am', 'are', 'is', 'was', 'were', 'being', 'been', 'can', 'could', 'dare', 'do', 'does',
                      'did', 'have', 'has', 'had', 'having', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should',
                      'will', 'would', 'he', 'she', 'they', 'i', 'me', 'my', 'mine', 'you', 'yours', 'their', 'a'])

    wc = WordCloud(
        background_color='white',
        font_path='C:\Windows\Fonts\Arial.TTF',
        max_words=2000,
        max_font_size=150,
        random_state=30,
        stopwords=stopwords
    )

    wc.generate_from_text(text)

    process_word = WordCloud.process_text(wc, text)
    sort = sorted(process_word.items(), key=lambda e:e[1], reverse=True)
    print(sort[:50])
    img_colors = ImageColorGenerator('white')
    wc.recolor(color_func=img_colors)

    img_name = '{}_wordcloud.png'.format(data[0])
    plt.savefig(img_name, dpi=180)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    return img_name


def calc_sentimental_info(data: list):
    """Function to calculate sentimental information by using Google NLP API
    """

    client = language.LanguageServiceClient()

    text = u'Hello, world!'
    document = types.message(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


if __name__ == '__main__':
    calc_sentimental_info()
