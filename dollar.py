#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gnucashxml
import requests
import time

def main():
  text = requests.get('https://cotacoes.economia.uol.com.br/cambioJSONChart.html?callback=grafico.parseData&type=a&cod=BRL&mt=off').text
  rates = {}
  for rate in eval(text[text.find('[{"ask') : text.find(']);')]):
    rates[time.strftime('%Y-%m-%d', time.gmtime(rate['ts'] / 1000))] = rate['ask']
  diffs = []
  for transaction in gnucashxml.from_filename('/home/marcots/gastos/gastos.gnucash').transactions:
    splits = transaction.splits
    commodity0 = splits[0].account.commodity.name
    commodity1 = splits[1].account.commodity.name
    inverse = 1.0
    if commodity0 == "USD" and commodity1 == "BRL":
      inverse = -1.0
    elif commodity0 != "BRL" or commodity1 != "USD":
      continue
    date = transaction.date.strftime('%Y-%m-%d')
    if date not in rates:
      continue
    diffs.append(rates[date] - (-1.0 * float(transaction.splits[0].quantity) / float(transaction.splits[1].quantity)) ** inverse)
  diffs = sorted(diffs)
  print(diffs[len(diffs) // 2])
  print(sum(diffs) / len(diffs))
  print(diffs)


if __name__ == '__main__':
  main()
