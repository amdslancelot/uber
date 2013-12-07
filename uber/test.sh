num_trip=http://lans-h.com:8000/uber/num/trip/
num_trip_date=http://lans-h.com:8000/uber/num/trip/20131201/20131202/

num_trip_lasthour=http://lans-h.com:8000/uber/num/trip/lastHour/

num_trip=http://lans-h.com:8000/uber/trip/num/
num_trip_date=http://lans-h.com:8000/uber/trip/num/?starttime=20131201&endtime=20131202

num_trip_lasthour=http://lans-h.com:8000/uber/trip/num_last_hour/

num_client=http://lans-h.com:8000/uber/client/num/
num_client_date=http://lans-h.com:8000/uber/client/num/?starttime=20131201&endtime=20131202

num_client_finished=http://lans-h.com:8000/uber/client/num/?finished=true
num_client_finished_date=http://lans-h.com:8000/uber/client/num/?finished=true&starttime=20131201&endtime=20131202

sum_miles_per_client1=http://lans-h.com:8000/uber/client/1/sum_miles/
sum_miles_per_client2=http://lans-h.com:8000/uber/client/2/sum_miles/
sum_miles_per_client3=http://lans-h.com:8000/uber/client/3/sum_miles/
sum_miles_per_client_date1=http://lans-h.com:8000/uber/client/1/sum_miles/?starttime=20131201&endtime=20131202
sum_miles_per_client_date2=http://lans-h.com:8000/uber/client/2/sum_miles/?starttime=20131201&endtime=20131202
sum_miles_per_client_date3=http://lans-h.com:8000/uber/client/3/sum_miles/?starttime=20131201&endtime=20131202

avg_fare_in_city1=http://lans-h.com:8000/uber/city/san_francisco/avg_fare/
avg_fare_in_city2=http://lans-h.com:8000/uber/city/daly_city/avg_fare/
avg_fare_in_city3=http://lans-h.com:8000/uber/city/san_bruno/avg_fare/
avg_fare_in_city4=http://lans-h.com:8000/uber/city/san_mateo/avg_fare/
avg_fare_in_city_date1=http://lans-h.com:8000/uber/city/san_francisco/avg_fare/?starttime=20131201&endtime=20131202
avg_fare_in_city_date2=ttp://lans-h.com:8000/uber/city/daly_city/avg_fare/?starttime=20131201&endtime=20131202
avg_fare_in_city_date3=http://lans-h.com:8000/uber/city/san_bruno/avg_fare/?starttime=20131201&endtime=20131202
avg_fare_in_city_date4=http://lans-h.com:8000/uber/city/san_mateo/avg_fare/?starttime=20131201&endtime=20131202

avg_rating_driver1=http://lans-h.com:8000/uber/driver/11/avg_rating/
avg_rating_driver2=http://lans-h.com:8000/uber/driver/12/avg_rating/
avg_rating_driver3=http://lans-h.com:8000/uber/driver/11/avg_rating/?starttime=20131201&endtime=20131202
avg_rating_driver4=http://lans-h.com:8000/uber/driver/12/avg_rating/?starttime=20131201&endtime=20131202

echo "testing:"
reponse=`curl $num_trip`
