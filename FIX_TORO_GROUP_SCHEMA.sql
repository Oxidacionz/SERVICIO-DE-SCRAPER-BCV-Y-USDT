-- 🛠️ Corrección de Schema para Proyecto TORO GROUP
-- Ejecuta este bloque completo en el Editor SQL de Supabase (Toro Group)

-- 1. Asegurar que existan todas las columnas requeridas por el Scraper
ALTER TABLE public.exchange_rates 
ADD COLUMN IF NOT EXISTS eur_bcv float DEFAULT 0,
ADD COLUMN IF NOT EXISTS usd_bcv float DEFAULT 0,
ADD COLUMN IF NOT EXISTS is_global boolean DEFAULT true;

-- 2. Asegurar que exista el registro "Global" que actualiza Railway
-- El ID '00000000-0000-0000-0000-000000000001' es el que el servicio busca
INSERT INTO public.exchange_rates (id, usd_bcv, eur_bcv, usd_binance_buy, usd_binance_sell, is_global, last_updated)
VALUES ('00000000-0000-0000-0000-000000000001', 0, 0, 0, 0, true, now())
ON CONFLICT (id) DO NOTHING;
