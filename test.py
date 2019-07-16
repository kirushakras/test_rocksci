from perfomance import Perfomance


my_test =  Perfomance()
start_date = input()
end_date = input()
print(my_test.my())
print(my_test.calculate_asset_performance(start_date,end_date))
print(my_test.calculate_currency_performance(start_date,end_date))
print(my_test.calculate_total_performance(start_date,end_date))

