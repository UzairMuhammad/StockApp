from django.shortcuts import render
from django.http import Http404
from .models import Stocks
from .active_stock_scrapper import run
from .management.commands.load_stocks_data import CopyToDatabase
from .scrapeHistorical import ScrapeHistorical
from .neural_stuff import predict_stock


def home(request):
    run()
    CopyToDatabase.handle()
    return render(request, 'home.html')


def activeS(request):
    stocks = Stocks.objects.all()
    return render(request, 'active_stocks.html', {
        'stocks': stocks,
    })


def stock_detail(request, stock_id):
    try:
        # predict_stock('AAPL')
        stock = Stocks.objects.get(id=stock_id)
        csv = ScrapeHistorical(stock.symbol)
    except Stocks.DoesNotExist:
        raise Http404('Stock not found')
    return render(request, 'stock_detail.html', {
        'stock': stock,
        'csv': csv
    })


def idk(request):
    csv = ScrapeHistorical
    return render(request, 'idk.html', {
        'csv': csv
    })


def historical(request):
    return render(request, 'historical.csv')
