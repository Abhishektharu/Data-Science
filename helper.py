from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter


extractor = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]


    num_messages = df.shape[0]

    # num of words in messages
    words = []
    for message in df['message']:
        words.extend(message.split())


    #fetch number of media messages

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]


    #fetch number of links shared

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df= round((df['user'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height= 500 , min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=' '))

    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'Missed voice call\n']
    temp = temp[temp['message'] != 'Missed video call\n']

    words = []
    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date_only').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap