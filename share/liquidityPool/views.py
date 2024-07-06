from django.shortcuts import render

# Create your views here.
def add_liquidity(request):
    return render(request, 'liquidityPool/add_liquidity.html')

def remove_liquidity(request):
    return render(request, 'liquidityPool/remove_liquidity.html')

def swap_token(request):
    return render(request, 'liquidityPool/swap_token.html')

def liquidity_reserves(request):
    return render(request, 'liquidityPool/liquidity.html')
