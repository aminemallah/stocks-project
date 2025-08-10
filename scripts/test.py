from currency_converter import CurrencyConverter

c = CurrencyConverter()



usd_amount = c.convert(100 , 'CAD', 'USD')

print(usd_amount)