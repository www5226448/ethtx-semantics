from enum import Enum

def dydx_parse_signed_number(argument, decimals=None):
  is_plus = argument['value'][0]['value']
  number = argument['value'][1]['value']

  sign = 1 if is_plus == 'True' else -1
  if not decimals:
    decimals = 0

  return sign * number / 10 ** decimals

def dydx_parse_asset_amount(asset_amount):
  class AssetDenomination(Enum):
    Wei = 0
    Par = 1

  class AssetReference(Enum):
    Delta = 0
    Target = 1

  # (sign=True, denomination=1, ref=1, value=0),
  sign = 1 if asset_amount['value'][0]['value'] == 'True' else -1

  try:
    denomination = AssetDenomination(asset_amount['value'][1]['value'])
  except:
    denomination = "Unknown AssetDenomination"

  try:
    reference = AssetReference(asset_amount['value'][2]['value']).name
  except:
    reference = "Unknown AssetReference"

  value = asset_amount['value'][3]['value']

  if denomination == AssetDenomination.Wei:
    value = sign * value / 10 ** 18
  else:
    value = sign * value

  if reference == AssetReference.Delta.name:
    asset_amount['value'] = f"{value} ({reference})"
  else:
    asset_amount['value'] = value

  asset_amount['type'] = "string"
  return asset_amount

def dydx_parse_market(market_argument):
  class DyDxMarket(Enum):
    WETH = 0
    SAI = 1
    USDC = 2
    DAI = 3

  value = market_argument['value']
  try:
    market_argument['value'] = DyDxMarket(value).name
  except:
    market_argument['value'] = f"Unkown Market ({value})"

def dydx_parse_operate(actions):
  class ActionType(Enum):
    Deposit = 0
    Withdraw = 1
    Transfer = 2
    Buy = 3
    Sell = 4
    Trade = 5
    Liquidate = 6
    Vaporize = 7
    Call = 8

  def _parse_deposit_args():
    action[0]['value'] = ActionType.Deposit.name
    action[1]['name'] = "account"
    action[2]['name'] = "amount"
    action[3]['name'] = "market"
    action[4]['type'] = "ignore"
    action[5]['name'] = "from"
    action[6]['type'] = "ignore"
    action[7]['type'] = "ignore"

  def _parse_withdraw_args():
    action[0]['value'] = ActionType.Withdraw.name
    action[1]['name'] = "account"
    action[2]['name'] = "amount"
    action[3]['name'] = "market"
    action[4]['type'] = "ignore"
    action[5]['name'] = "to"
    action[6]['type'] = "ignore"
    action[7]['type'] = "ignore"

  def _parse_transfer_args():
    action[0]['value'] = ActionType.Transfer.name
    action[1]['name'] = "accountOne"
    action[2]['name'] = "amount"
    action[3]['name'] = "market"
    action[4]['type'] = "ignore"
    action[5]['name'] = "accountTwo"
    action[6]['type'] = "ignore"
    action[7]['type'] = "ignore"

  def _parse_buy_args():
    action[0]['value'] = ActionType.Buy.name
    action[1]['name'] = "account"
    action[2]['name'] = "amount"
    action[3]['name'] = "makerMarket"
    action[4]['name'] = "takerMarket"
    action[5]['name'] = "exchangeWrapper"
    action[6]['type'] = "ignore"
    action[7]['name'] = "orderData"


  def _parse_sell_args():
    action[0]['value'] = ActionType.Sell.name
    action[1]['name'] = "account"
    action[2]['name'] = "amount"
    action[3]['name'] = "takerMarket"
    action[4]['name'] = "makerMarket"
    action[5]['name'] = "exchangeWrapper"
    action[6]['type'] = "ignore"
    action[7]['name'] = "orderData"

  def _parse_trade_args():
    action[0]['value'] = ActionType.Trade.name
    action[1]['name'] = "takerAccount"
    action[2]['name'] = "amount"
    action[3]['name'] = "inputMarket"
    action[4]['name'] = "outputMarket"
    action[5]['name'] = "autoTrader"
    action[6]['name'] = "makerAccount"
    action[7]['name'] = "tradeData"

  def _parse_liquidate_args(action):
    action[0]['value'] = ActionType.Liquidate.name
    action[1]['name'] = "solidAccount"
    action[2]['name'] = "amount"
    action[3]['name'] = "owedMarket"
    action[4]['name'] = "heldMarket"
    action[5]['type'] = "ignore"
    action[6]['name'] = "liquidAccount"
    action[7]['type'] = "ignore"

  def _parse_vaporize_args():
    action[0]['value'] = ActionType.Vaporize.name
    action[1]['name'] = "solidAccount"
    action[2]['name'] = "amount"
    action[3]['name'] = "owedMarket"
    action[4]['name'] = "heldMarket"
    action[5]['type'] = "ignore"
    action[6]['name'] = "vaporAccount"
    action[7]['type'] = "ignore"


  def _parse_call_args():
    return None

  def _parse(action):
    action_type = action[0]['value']

    dydx_parse_asset_amount(action[2])
    dydx_parse_market(action[3])
    dydx_parse_market(action[4])

    if action_type == ActionType.Deposit.value:
      _parse_deposit_args()
    elif action_type == ActionType.Withdraw.value:
      _parse_withdraw_args()
    elif action_type == ActionType.Transfer.value:
      _parse_transfer_args()
    elif action_type == ActionType.Buy.value:
      _parse_buy_args()
    elif action_type == ActionType.Sell.value:
      _parse_sell_args()
    elif action_type == ActionType.Trade.value:
      _parse_trade_args()
    elif action_type == ActionType.Liquidate.value:
      _parse_liquidate_args(action)
    elif action_type == ActionType.Vaporize.value:
      _parse_vaporize_args()
    elif action_type == ActionType.Call.value:
      _parse_call_args()

  for action in actions:
    _parse(action)

  return actions
