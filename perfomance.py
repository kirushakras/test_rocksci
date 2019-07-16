import pandas as pd


class Perfomance:
    """This class that calculates portfolio performance"""

    def __init__(self):
        """This method is constructor that loads data"""
        self.weights = pd.read_csv("weights.csv", index_col=0)
        self.price = pd.read_csv("prices.csv", index_col='date')
        self.exch = pd.read_csv("exchanges.csv", index_col=0)
        self.currencies = pd.read_csv("currencies.csv", index_col=0)

    def data_clean(self) -> Tuple[pd.DataFrame]:
        """This method clean data"""
        hendler_names = self.currencies.index.tolist()
        for name in hendler_names:
            new_name = self.currencies.loc[self.currencies.index == name]['currency'].tolist()[0]
            self.weights.rename(columns={name: "weights "+name+new_name}, inplace=True)
            self.price.rename(columns={name: "price"+name+" "+new_name}, inplace=True)
        return self.price, self.weights

    def calculate_asset_performance(self, start_date: str, end_date: str) -> int:
        """This method calculate assets perfomance"""
        price = self.data_clean()[0]
        weights = self.data_clean()[1]
        my_df = pd.merge(price, weights, right_index=True, left_index=True, how='outer')
        my_df.fillna(method='ffill', inplace=True)
        my_df.fillna(method='bfill', inplace=True)
        date_all = pd.DataFrame(my_df.loc[start_date:end_date].index, columns=["date"])
        frame = my_df.loc[start_date:end_date].reset_index(drop=True)
        frame = pd.merge(frame, date_all, right_index=True, left_index=True)
        start_day = frame[:1]
        price_1 = (start_day["priceAT0000A18XM4 SW CHF"]).tolist()[0]
        price_2 = (start_day["priceBE0974268972 BB EUR"]).tolist()[0]
        price_3 = (start_day["priceDE0007164600 GR EUR"]).tolist()[0]
        price_4 = (start_day["priceUS0527691069 US USD"]).tolist()[0]
        price_5 = (start_day["priceUS6092071058 US USD"]).tolist()[0]
        asset_performance = 0
        frame = frame[1:]
        for row in frame.iterrows():
            price1 = row[1]["priceAT0000A18XM4 SW CHF"]
            w1 = row[1]["weights AT0000A18XM4 SWCHF"]
            price2 = row[1]["priceBE0974268972 BB EUR"]
            w2 = row[1]["weights BE0974268972 BBEUR"]
            price3 = row[1]["priceDE0007164600 GR EUR"]
            w3 = row[1]["weights DE0007164600 GREUR"]
            price4 = row[1]["priceUS0527691069 US USD"]
            w4 = row[1]["weights US0527691069 USUSD"]
            price5 = row[1]["priceUS6092071058 US USD"]
            w5 = row[1]['weights US6092071058 USUSD']
            r1 = (price1-price_1)/price_1
            price_1 = price1
            r2 = (price2-price_2)/price_2
            price_2 = price2
            r3 = (price3-price_3)/price_3
            price_3 = price3
            r4 = (price4-price_4)/price_4
            price_4 = price4
            r5 = (price5-price_5)/price_5
            price_5 = price5
            asset_performance += (r1*w1+r2*w2+r3*w3+r4*w4+r5*w5)
        return asset_performance

    def calculate_currency_performance(self, start_date: str, end_date: str) -> int:
        """This method calculate currency perfomance"""
        weights = self.data_clean()[1]
        df = pd.merge(self.exch, weights, right_index=True, left_index=True, how='outer')
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        frame = df.loc[start_date:end_date].reset_index(drop=True)
        currency_performance = 0
        first_day = frame[:1]
        frame = frame[1:]
        before_eur = first_day["EUR"][0]
        before_chf = first_day["CHF"][0]
        for row in frame.iterrows():
            eur = row[1]["EUR"]
            chf = row[1]["CHF"]
            cr_eur = (eur - before_eur)/before_eur
            cr_chf = (chf - before_chf)/before_chf
            before_chf, before_eur = chf, eur
            w_chf = row[1][2]
            w_eur = row[1][3]+row[1][5]
            currency_performance += cr_chf*w_chf + cr_eur*w_eur
        return currency_performance

    def calculate_total_performance(self, start_date: str, end_date: str) -> int:
        """This method calculate total perfomance"""
        price = self.data_clean()[0]
        weights = self.data_clean()[1]
        my_df = pd.merge(price, weights, right_index=True, left_index=True, how='outer')
        df = pd.merge(my_df, self.exch, right_index=True, left_index=True, how='outer')
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        frame = df.loc[start_date:end_date].reset_index(drop=True)
        total_perfomance = 0
        first_day = frame[:1]
        frame = frame[1:]
        before_eur = first_day["EUR"][0]
        before_chf = first_day["CHF"][0]
        price_1 = (first_day["priceAT0000A18XM4 SW CHF"]).tolist()[0]
        price_2 = (first_day["priceBE0974268972 BB EUR"]).tolist()[0]
        price_3 = (first_day["priceDE0007164600 GR EUR"]).tolist()[0]
        price_4 = (first_day["priceUS0527691069 US USD"]).tolist()[0]
        price_5 = (first_day["priceUS6092071058 US USD"]).tolist()[0]
        for row in frame.iterrows():
            eur = row[1]["EUR"]
            chf = row[1]["CHF"]
            price1 = row[1]["priceAT0000A18XM4 SW CHF"]
            r1 = (chf*price1-before_chf*price_1)/(before_chf*price_1)
            price_1 = price1
            w1 = row[1]["weights AT0000A18XM4 SWCHF"]
            price2 = row[1]["priceBE0974268972 BB EUR"]
            r2 = (eur*price2-before_eur*price_2)/(before_eur*price_2)
            price_2 = price2
            w2 = row[1]["weights BE0974268972 BBEUR"]
            price3 = row[1]["priceDE0007164600 GR EUR"]
            r3 = (eur*price3-before_eur*price_3)/(before_eur*price_3)
            price_3 = price3
            w3 = row[1]["weights DE0007164600 GREUR"]
            price4 = row[1]["priceUS0527691069 US USD"]
            r4 = (price4-price_4)/price_4
            price_4 = price4
            w4 = row[1]["weights US0527691069 USUSD"]
            price5 = row[1]["priceUS6092071058 US USD"]
            w5 = row[1]['weights US6092071058 USUSD']
            r5 = (price5-price_5)/price_5
            price_5 = price5
            before_chf, before_eur = chf, eur
            total_perfomance = w1*r1+w2*r2+w3*r3+w4*r4+w5*r5
        return total_perfomance
