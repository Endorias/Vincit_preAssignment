from flask import Blueprint, render_template, request
from pycoingecko import CoinGeckoAPI
import time
from datetime import date, timedelta, datetime

cg = CoinGeckoAPI()
views = Blueprint('views', __name__)

@views.route('/')

def home():
    return render_template("home.html")

@views.route('/dt', methods=['GET', 'POST']) #downtrend analyzer

def dt():
    if request.method == 'POST':
        startDateRaw = request.form.get('SDate')
        endDateRaw = request.form.get('EDate')

        #remove all - characters from string data
        startDate = startDateRaw.replace('/', '-')
        endDate = endDateRaw.replace('/', '-')
        print('Downwards Trend')
        print('Start Date: ' + startDate, '\nEnd Date: ' + endDate)

        #TODO: Implement price comparisons for days between startDate and endDate with coingecko API
        date0 = date(int(startDate[6:]), int(startDate[3:5]), int(startDate[:2]))
        date1 = date(int(endDate[6:]), int(endDate[3:5]), int(endDate[:2]))
        delta = date1 - date0
        
        finalCount = -1
        count = 0
        prev = -1
        curr = -1
        for i in range(delta.days):
            tmpDate =  date0 + timedelta(days=i)
            jsonData = cg.get_coin_history_by_id(id='bitcoin', date=str(tmpDate.day)+"-"+str(tmpDate.month)+"-"+str(tmpDate.year))
            if i == 0:
                prev = jsonData["market_data"]["current_price"]["eur"]
            else:
                curr = jsonData["market_data"]["current_price"]["eur"]
                if curr < prev:
                    count += 1
                else:
                    if count > finalCount:
                        finalCount = count
                        count = 0
                prev = curr
        
        print(finalCount)

        return render_template('dt.html', text=str(finalCount))
            #DEBUG:
            #print(tmpDate)
            #DEBUG:
            #print('Name: ' + jsonData["id"], 'Price: ' + str(jsonData["market_data"]["current_price"]["eur"]))


    return render_template("dt.html")


@views.route('/hv', methods=['GET', 'POST']) #Highest trading volume

def hv():
    if request.method == 'POST':
        startDateRaw = request.form.get('SDate')
        endDateRaw = request.form.get('EDate')

        #remove all - characters from string data
        startDate = startDateRaw.replace('/', '-') #Originally made for sorting data and directly inputting string into coingecko API, made redundant with time import
        endDate = endDateRaw.replace('/', '-')
        print('Downwards Trend')
        print('Start Date: ' + startDate, '\nEnd Date: ' + endDate)

        #TODO: Implement price comparisons for days between startDate and endDate with coingecko API
        date0 = date(int(startDate[6:]), int(startDate[3:5]), int(startDate[:2]))
        date1 = date(int(endDate[6:]), int(endDate[3:5]), int(endDate[:2]))
        delta = date1 - date0
        
        unixDate0 = str(int(time.mktime(date0.timetuple())))
        unixDate1 = str(int(time.mktime(date1.timetuple())))

        highVol = 0
        highVol_date = 0
        for values in cg.get_coin_market_chart_range_by_id(id="bitcoin", vs_currency="eur", from_timestamp=unixDate0, to_timestamp=unixDate1)['total_volumes']:
            if highVol < values[1]:
                highVol = values[1]
                highVol_date = values[0]
        highVol_date /= 1000 #answer is in milliseconds to fix this has to be divided by 1000
        dt = datetime.fromtimestamp(highVol_date).strftime('%c')
        
        print(dt)
        print(highVol)
        return render_template('hv.html', text=dt, text2=str(highVol))
        #print(jsonData)
    return render_template("hv.html")


@views.route('/bs', methods=['GET', 'POST']) #buy/sell analyzer

def bs():
    if request.method == 'POST':
        startDateRaw = request.form.get('SDate')
        endDateRaw = request.form.get('EDate')

        #remove all - characters from string data
        startDate = startDateRaw.replace('/', '-')
        endDate = endDateRaw.replace('/', '-')
        print('Downwards Trend')
        print('Start Date: ' + startDate, '\nEnd Date: ' + endDate)

        date0 = date(int(startDate[6:]), int(startDate[3:5]), int(startDate[:2]))
        date1 = date(int(endDate[6:]), int(endDate[3:5]), int(endDate[:2]))
        delta = date1 - date0
        

        #TODO: Find the highest and the lowest prices for Bitcoin between startDate and endDate with coingecko API and print the dates of these two values

        high = -1
        high_date = 0
        tmp_low = -1
        tmp_low_date = 0
        low = -1
        low_date = 0
        for i in range(delta.days):
            tmpDate = date0 + timedelta(days=i)
            jsonData = cg.get_coin_history_by_id(id='bitcoin', date=str(tmpDate.day)+"-"+str(tmpDate.month)+"-"+str(tmpDate.year))
            if i == 0:
                tmp_low = jsonData["market_data"]["current_price"]["eur"]
                tmp_low_date = tmpDate
            else:
                currPrice = jsonData["market_data"]["current_price"]["eur"]
                if currPrice < tmp_low:
                    tmp_low = currPrice
                    tmp_low_date = tmpDate
                            
                if high < currPrice and currPrice > tmp_low:
                    low = tmp_low
                    low_date = tmp_low_date
                    high = currPrice
                    high_date = tmpDate
        
        if low != -1 and high != -1:
            return render_template('bs.html', text=str(low_date.day)+"-"+str(low_date.month)+"-"+str(low_date.year), text2=str(high_date.day)+"-"+str(high_date.month)+"-"+str(high_date.year))
            #return render_template('bs.html', 'Sell date and price:', str(high_date.day)+"-"+str(high_date.month)+"-"+str(high_date.year), str(high))
        else:
            return render_template('bs.html', text='Cannot recommend a date to buy', text2='Cannot recommend a date to sell')

        #final_dates = ('buydate', 'selldate')
        #final_dates =  (str(low_date.day)+"-"+str(low_date.month)+"-"+str(low_date.year), str(high_date.day)+"-"+str(high_date.month)+"-"+str(high_date.year))
        #return render_template('bs.html', text=final_dates)
            

    return render_template("bs.html")
