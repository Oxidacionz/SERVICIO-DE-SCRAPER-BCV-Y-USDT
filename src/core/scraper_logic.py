import requests
from typing import List, Optional
from datetime import datetime
from src.core.domain_models import ExchangeRate

# Constantes
BINANCE_API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def _fetch_binance_p2p(trade_type: str, limit: int = 5) -> list[float]:
    """
    Función auxiliar privada para conectar con Binance.
    Retorna lista cruda de precios.
    """
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": trade_type,
        "page": 1,
        "rows": 10,  # Pedimos un poco más para filtrar
        "filterType": "all",
        "countries": [],
        "payTypes": []
    }

    try:
        response = requests.post(
            BINANCE_API_URL, 
            json=payload, 
            headers=headers, 
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data or 'data' not in data:
            return []

        # Lógica de filtrado: Ignoramos el primero (suele ser anuncio destacado/falso positivo)
        # y tomamos los siguientes 'limit' anuncios
        anuncios = data['data'][1 : limit + 1]
        
        precios = [float(ad['adv']['price']) for ad in anuncios]
        return precios

    except Exception as e:
        print(f"⚠️ Error conectando con Binance ({trade_type}): {e}")
        return []

def get_binance_rates() -> Optional[ExchangeRate]:
    """
    Orquesta la obtención de datos de compra y venta y retorna un objeto de dominio unificado.
    """
    print("🔄 Consultando Binance P2P...")
    
    # Obtener precios de VENTA (Lo que paga el usuario para tener USDT) -> Es el precio 'Real' del dólar
    # En P2P: 'BUY' es anuncios de gente vendiendo (Tú compras)
    prices_buy_usdt = _fetch_binance_p2p("BUY")
    
    # Obtener precios de COMPRA (Lo que recibe el usuario al vender USDT)
    # En P2P: 'SELL' es anuncios de gente comprando (Tú vendes)
    prices_sell_usdt = _fetch_binance_p2p("SELL")

    if not prices_buy_usdt or not prices_sell_usdt:
        print("❌ Fallo obteniendo tasas completas de Binance")
        return None

    # Calcular promedios
    avg_price_buy = sum(prices_buy_usdt) / len(prices_buy_usdt)
    avg_price_sell = sum(prices_sell_usdt) / len(prices_sell_usdt)

    return ExchangeRate(
        currency_pair="USDT/VES",
        price_buy=avg_price_buy,  # Promedio de anuncios de venta (precio alto)
        price_sell=avg_price_sell, # Promedio de anuncios de compra (precio bajo)
        source="Binance P2P",
        last_updated=datetime.now()
    )

async def fetch_financial_data() -> dict:
    """
    Función principal llamada por el orquestador.
    Agrupa todos los scrapers (Binance, BCV, etc.)
    Retorna un diccionario listo para ser insertado en BD.
    """
    rates = {}
    
    # 1. Binance
    binance_rate = get_binance_rates()
    if binance_rate:
        # Estructura compatible con tu tabla 'exchange_rates' actual
        rates["binance_p2p"] = {
            "buy": binance_rate.price_buy,
            "sell": binance_rate.price_sell,
            "last_updated": binance_rate.last_updated.isoformat()
        }
    
    # Aquí agregaríamos BCV en el futuro
    
    return rates
