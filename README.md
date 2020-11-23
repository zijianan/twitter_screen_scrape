# twitter_screen_scrape
1. this project could screen scrape twitter replies through browser controller. it has two mode: real-time collection and given object collection.
2. create new conda enviroment: 'conda create --name screen_scrape python=3.7'
3. activate new enviroment: 'conda activate screen_scrape'
4. cd to the path of the twitter_screen_scrape
5. install requirements: 'pip install -r requirements.txt'
6. add twitter account credential by editting line38 and line40 in screen_scrape.py. 'account_flag' is the variable to record your account property(e.g. activate democrats)
7. if you want to use streaming.py to collect real-time replies you need to have a twitter dev account and add your info to line6-9 in streaming.py
8. a given object collection patten is: obj_list.csv
9. a given real-time collection patten is: streaming_target.csv
10. if you want to run streaming.py, after you given the twitter dev info you can just run 'python streaming.py' in the meantime run another terminal and use 'python screen_scrape.py -md real-time' to make collection
11. if you have already given info to 'obj_list.csv', just run 'python screen_scrape.py'
