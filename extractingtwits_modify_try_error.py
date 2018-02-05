#Importing necessary libraries

import reader
import tweepy
import csv
import time


#Call to Twitter API using Tweepy with credentials saved in reader File

api = reader.getTweepyAPI()


#Defining the object for the search object including arguments like - datefrom, date to, search keyword

ATLTweet = tweepy.Cursor(api.search, q='#Atlanta'
                         #, since='2017-11-22', until = '2017-11-15'
                         ).items(500)



#Checking Headers in the CSV file, if present move forward else save the csv file with the required headers

header1 = ['Data Source', 'Language', 'Date','Text']


with open('Atlanta.csv', 'w') as csvfile:
    print(csvfile.seek(0))
    #writer = csv.writer(csvfile)
    if csvfile.seek(0) in (None, "", 0):
        writer = csv.writer(csvfile)
        writer.writerows([header1])
                
    else:
        pass

csvfile.close()



# Opening the CSV file to download the data from twitter

while True:
    try:
        tweet_list = []
        csvFile = open('Atlanta.csv', 'a')
        #header = ['id', 'created_at','text', 'lon', 'lat']
        csvWriter = csv.writer(csvFile, delimiter=',')

        for tweet in ATLTweet:
            a_tweet = []
            data_source = 'Twitter'
            a_tweet.append(data_source)

            #Getting the URL of the Tweet
            
            if len(tweet.entities['urls']): #if the list is not empty
                source_full_url = tweet.entities['urls'][0]['expanded_url']
                parsed_hostname = 'www.twitter.com'
                #parsed_hostname = urlparse(source_full_url).hostname
                link_and_source = str(parsed_hostname) + ':' + str(source_full_url)
                #a_tweet.append(link_and_source)
            else:
                #get the tweet itself
                url_to_tweet = 'https://twitter.com/' + str(tweet.author.id) + '/status/' + str(tweet.id)
                #a_tweet.append(url_to_tweet)
        
            a_tweet.append(tweet.lang)
    
            tweet_date = str(tweet.created_at).split()[0]
            tweet_time = str(tweet.created_at).split()[1]
            a_tweet.append(tweet_date)
            
    
            if(tweet.place != None):
                if(tweet.coordinates != None):
                    location = tweet.coordinates['coordinates'] #in longitude and latitude (mind the order)
                else:
                    location = 'N/A'
                country = tweet.place.country
                try:
                    state = tweet.place.full_name.split(',')[1].encode('utf-8')
                    city = tweet.place.full_name.split(',')[0].encode('utf-8')
                except IndexError:
                    state = 'N/A'
                    city = tweet.place.full_name.encode('utf-8')
                    print("An index error has occurred when getting the state and city")
                    print(tweet.place.full_name)        
            else:
                country = 'N/A'
                city = 'N/A'
                state = 'N/A'
                location = 'N/A'

            headlines = 'N/A'
            a_tweet.append(tweet.text.encode('utf-8'))

            #Trying to copy data to the csv, if it is showing error, printing it

            try:
                csvWriter.writerow(a_tweet) 
            except(UnicodeEncodeError):
                print('There was a problem encoding the following tweet.. Continuing..')
                print(a_tweet)

        csvFile.close()
        break

    #If while trying to get data from Twitter, Tweepy API is getting error, wait for some time as it is exhausting the limit giving by Twitter 

    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue


    except StopIteration:
        break






