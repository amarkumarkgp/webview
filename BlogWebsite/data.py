
# import pandas as pd
#
# ser = pd.Series([124,25.0,625.0,None, 458])
# ser2 = pd.Series([x for x in range(5)])
#
# df = pd.DataFrame()
# df['vals'] = ser
# df.index = ser2
#
# df['vals2'] = df.vals.dropna().astype('int64').apply(lambda x: int(x))
# df['vals3'] = df.vals.astype('object')
#
# print(df)




def articles():

    articles = [
        {
            "id": 1,
            "author": "Amar Kumar",
            "text": "I am going to publish a very nice article on the on going problems"
        },

        {
            "id": 2,
            "author": "Jeevan Kumar",
            "text": "I am going to publish a very nice article on the on going problems"
        },

        {
            "id": 3,
            "author": "Nice Kumar",
            "text": "I am going to publish a very nice article on the on going problems"
        }
    ]

    return articles