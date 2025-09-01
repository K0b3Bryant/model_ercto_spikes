def ta(window:int=3, high:str="high", low:str="low", close:str="close", open:str="open", volume:str="volume")--> pd.DataFrame:
  """ Generates ta features """

  prices = df.loc[:, [close, open, high, low, volume]].sort_index(inplace=True)

  # own definition
  def cmo(close_prices, window=14):
      delta = close_prices.diff()
      gain = delta.clip(lower=0)
      loss = -delta.clip(upper=0)
      sum_gain = gain.rolling(window=window, min_periods=1).sum()
      sum_loss = loss.rolling(window=window, min_periods=1).sum()
      return ((sum_gain - sum_loss) / (sum_gain + sum_loss)).abs() * 100
    
  calculations = {
    'kama': lambda: ta.momentum.KAMAIndicator(prices[close]).kama(),
    'ppo': lambda: ta.momentum.PercentagePriceOscillator(prices[close]).ppo(),
    'pvo': lambda: ta.momentum.PercentageVolumeOscillator(prices[volume]).pvo(),
    'roc': lambda: ta.momentum.ROCIndicator(prices[close]).roc(),
    'rsi': lambda: ta.momentum.RSIIndicator(prices[close]).rsi(),
    'srsi': lambda: ta.momentum.StochRSIIndicator(prices[close]).stochrsi(),
    'stoch': lambda: ta.momentum.StochasticOscillator(prices[high], prices[low], prices[close]).stoch(),
    'tsi': lambda: ta.momentum.TSIIndicator(prices[close]).tsi(),
    'uo': lambda: ta.momentum.UltimateOscillator(prices[high], prices[low], prices[close]).ultimate_oscillator(),
    'willr': lambda: ta.momentum.WilliamsRIndicator(prices[high], prices[low], prices[close]).williams_r(),
    'ao': lambda: ta.momentum.AwesomeOscillatorIndicator(prices[high], prices[low]).awesome_oscillator(),
    'ppo_hist': lambda: ta.momentum.PercentagePriceOscillator(prices[close]).ppo_hist(),
    'ppo_signal': lambda: ta.momentum.PercentagePriceOscillator(prices[close]).ppo_signal(),
    'aci': lambda: ta.volume.AccDistIndexIndicator(prices[high], prices[low], prices[close], prices[volume]).acc_dist_index(),
    'chaikin': lambda: ta.volume.ChaikinMoneyFlowIndicator(prices[high], prices[low], prices[close], prices[volume]).chaikin_money_flow(),
    'fi': lambda: ta.volume.ForceIndexIndicator(prices[close], prices[volume]).force_index(),
    'mfi': lambda: ta.volume.MFIIndicator(prices[high], prices[low], prices[close], prices[volume]).money_flow_index(),
    'nvi': lambda: ta.volume.NegativeVolumeIndexIndicator(prices[close], prices[volume]).negative_volume_index(),
    'obv': lambda: ta.volume.OnBalanceVolumeIndicator(prices[close], prices[volume]).on_balance_volume(),
    'vpt': lambda: ta.volume.VolumePriceTrendIndicator(prices[close], prices[volume]).volume_price_trend(),
    'vi': lambda: ta.volume.VolumeWeightedAveragePrice(prices[high], prices[low], prices[close], prices[volume]).volume_weighted_average_price(),
    'atr': lambda: ta.volatility.AverageTrueRange(prices[high], prices[low], prices[close]).average_true_range(),
    'bb_bbm': lambda: ta.volatility.BollingerBands(prices[close]).bollinger_mavg(),
    'bb_bbh': lambda: ta.volatility.BollingerBands(prices[close]).bollinger_hband(),
    'bb_bbl': lambda: ta.volatility.BollingerBands(prices[close]).bollinger_lband(),
    'dc': lambda: ta.volatility.DonchianChannel(prices[high], prices[low], prices[close]).donchian_channel_lband(),
    'kc': lambda: ta.volatility.KeltnerChannel(prices[high], prices[low], prices[close]).keltner_channel_lband(),
    'ui': lambda: ta.volatility.UlcerIndex(prices[close]).ulcer_index(),
    'adx': lambda: ta.trend.ADXIndicator(prices[high], prices[low], prices[close]).adx(),
    'ai': lambda: ta.trend.AroonIndicator(prices[high], prices[low]).aroon_indicator(),
    'cci': lambda: ta.trend.CCIIndicator(prices[high], prices[low], prices[close]).cci(),
    'kst': lambda: ta.trend.KSTIndicator(prices[close]).kst(),
    'kst_sig': lambda: ta.trend.KSTIndicator(prices[close]).kst_sig(),
    'macd': lambda: ta.trend.MACD(prices[close]).macd(),
    'macd_signal': lambda: ta.trend.MACD(prices[close]).macd_signal(),
    'macd_diff': lambda: ta.trend.MACD(prices[close]).macd_diff(),
    'psar': lambda: ta.trend.PSARIndicator(prices[high], prices[low], prices[close]).psar(),
    'sma_30': lambda: ta.trend.SMAIndicator(prices[close], window=30).sma_indicator(),
    'sma_50': lambda: ta.trend.SMAIndicator(prices[close], window=50).sma_indicator(),
    'sma_100': lambda: ta.trend.SMAIndicator(prices[close], window=100).sma_indicator(),
    'sma_200': lambda: ta.trend.SMAIndicator(prices[close], window=200).sma_indicator(),
    'trix': lambda: ta.trend.TRIXIndicator(prices[close]).trix(),
    'ema': lambda: ta.trend.EMAIndicator(prices[close]).ema_indicator(),
    'ii': lambda: ta.trend.IchimokuIndicator(prices[high], prices[low]).ichimoku_a(),
    'mi': lambda: ta.trend.MassIndex(prices[high], prices[low]).mass_index(),
    'cmo': lambda: cmo(prices[close])
  }
  
  for name, calc in calculations.items():
    try:
        prices[name] = calc()
    except Exception as e:
        print(f"Skipping {name} due to error: {e}")
  
  return prices.drop(columns=[close, open, high, low, volume], inplace=True)
