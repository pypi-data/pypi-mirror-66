from . import intercept_bitshares
from bitshares.bitshares import BitShares
from bitshares.account import Account
from bitshares.amount import Amount
from bitshares.storage import configStorage as config
from bitshares.instance import set_shared_bitshares_instance
from bitshares.utils import formatTimeFromNow
from bitsharesbase import operations
from bitsharesbase.chains import known_chains
from graphenebase.base58 import known_prefixes
from graphenebase.types import Set
from . import dice
from . import exchange as cybex_exchange
from . import nonfungible as cybex_nonfungible
from . import asset
from . import cybex_operations
from . import gateway
from . import custom

import bitsharesbase.objects as bsobjects
bsobjects.operations = intercept_bitshares.cybex_operations

def cybex_debug_config(chain_id):
    debug_chain = {
        'chain_id': chain_id,
        'core_symbol': 'CYB',
        'prefix': 'CYB'
    }
    known_chains['CYB'] = debug_chain 

CYBEX_PROD_CHAIN = {
    'chain_id': '90be01e82b981c8f201c9a78a3d31f655743b29ff3274727b1439b093d04aa23',
    'core_symbol': 'CYB',
    'prefix': 'CYB'
}

class Cybex(BitShares):
    def __init__(self, node="", rpcuser="", rpcpassword="", 
                debug=False, **kwargs):

        if 'CYB' not in known_chains: # else we must have set a debug chain id
            known_chains['CYB'] = CYBEX_PROD_CHAIN

        known_prefixes.append('CYB')
        config['prefix'] = 'CYB'
        config.config_defaults["node"] = node

        super(Cybex, self).__init__(node=node, rpcuser=rpcuser,
                 rpcpassword=rpcpassword, debug=debug, **kwargs)
        set_shared_bitshares_instance(self)

    def transfer(self, to, amount, asset, memo="", account=None, **kwargs):
        """ Transfer an asset to another account.

            :param str to: Recipient
            :param float amount: Amount to transfer
            :param str asset: Asset to transfer
            :param str memo: (optional) Memo, may begin with `#` for encrypted
                messaging
            :param str account: (optional) the source account for the transfer
                if not ``default_account``
        """
        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)
        amount = Amount(amount, asset, bitshares_instance=self)
        to = Account(to, bitshares_instance=self)

        memoObj = Memo(
            from_account=account,
            to_account=to,
            bitshares_instance=self
        )
    
        op = cybex_operations.Transfer(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "from": account["id"],
            "to": to["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj.encrypt(memo),
            "extensions": None if 'extensions' not in kwargs else kwargs['extensions'],
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def override_transfer(self, _from, to, amount, asset, memo = "", account = None, **kwargs):
        """ Transfer an asset from one account to another.
            Only issuer of asset can do this when asset flag of override_authority is opened.

            :param str _from: from account
            :param str to: Recipient
            :param float amount: Amount to transfer
            :param str asset: Asset to transfer
            :param str memo: (optional) Memo
            :param str account: (optional) the account to send the transfer, must be issuer of asset
        """
        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if memo != "":
            raise ValueError("Currently not supported to encrypt override memo")

        account = Account(account, bitshares_instance = self)
        amount = Amount(amount, asset, bitshares_instance = self)
        _from = Account(_from, bitshares_instance = self)
        to = Account(to, bitshares_instance = self)

        memoObj = Memo(
            from_account = _from,
            to_account = to, 
            bitshares_instance = self
        )

        op = cybex_operations.Override_transfer(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account["id"],
            "from": _from["id"],
            "to": to["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj.encrypt(memo),
            "extensions": None, 
            "prefix": self.prefix
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def get_deposit_address(self, asset, account = None, **kwargs):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance = self)

        if self.wallet.locked():
            raise Exception("Wallet locked, unlock wallet before query deposit address")

        active_keys = account['active']['key_auths']
        if len(active_keys) == 0:
            raise ValueError("Account {} does not have enough active key auth to query cybex gateway".format(account['name']))

        weight = account['active']['weight_threshold']
        wif = ''
        pubkeys = self.wallet.getPublicKeys()

        for k in active_keys:
            if k[1] < weight:
                continue
            if k[0] not in pubkeys:
                continue
            wif = self.wallet.getPrivateKeyForPublicKey(k[0])

        if wif == '':
            raise ValueError("Can not find key to sign request for account {}".format(account['name']))

        if 'gateway_symbol' in kwargs:
            extern_symbol = kwargs['gateway_symbol']
        elif '.' in asset:
            extern_symbol = asset.split('.')[-1]
        else:
            extern_symbol = asset

        if 'gateway_url' in kwargs:
            gw_url = kwargs['gateway_url']
        else:
            gw_url = 'https://gateway.cybex.io/v1'

        gw_handler = gateway.CybexGateway(gw_url)
        gw_asset = gw_handler.get_gateway_asset(extern_symbol)
        if gw_asset['cybname'] != asset:
            raise ValueError("asset name {} does not fit asset supported by gateway: {}".format(asset, gw_asset['cybname']))

        if not gw_asset['depositSwitch']:
            raise ValueError("Asset {} deposit is disabled by gateway".format(extern_symbol))

        deposit_addr = gw_handler.get_deposit_address(account['name'], extern_symbol, wif)
        if deposit_addr['cybName'] != asset:
            raise ValueError("asset name {} does not fit asset supported by gateway: {}".format(asset, deposit_addr['cybName']))
        return deposit_addr['address']

    def withdraw(self, to_addr, amount, asset, account = None, **kwargs):
        """ Withdraw asset to external address.

            :param str to_addr: Receipant address
                for assets like ETH and BTC, just set address here
                for assets like EOS and PCX, address should be in format username[memo]
            :param float amount: Amount to withdraw
            :param str asset: Asset to withdraw
            :param str account: (optional) the source account for the withdraw
                if not ``default_account``
        """
        if 'gateway_url' in kwargs:
            gw_url = kwargs['gateway_url']
        else:
            gw_url = 'https://gateway.cybex.io/v1'

        gw_handler = gateway.CybexGateway(gw_url)

        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if '.' in asset:
            extern_symbol = asset.split('.')[-1]
        else:
            extern_symbol = asset

        gw_asset = gw_handler.get_gateway_asset(extern_symbol)
        if gw_asset['cybname'] != asset:
            raise ValueError("Asset {} dost not fit which gateway supports {}".format(asset, gw_asset['cybname']))
 
        if gw_asset is None:
            raise ValueError("Asset {} not supported by gateway".format(extern_symbol))

        if not gw_asset['withdrawSwitch']:
            raise ValueError("Asset {} withdraw is disabled by gateway".format(extern_symbol))

        if not gw_handler.validate_withdraw_address(extern_symbol, to_addr):
            raise ValueError("Withdraw address {} invalid".format(to_addr))

        if float(amount) < float(gw_asset['minWithdraw']):
            raise ValueError("Withdraw amount {} less than minimum {}".format(amount, gw_asset['minWithdraw']))

        if float(amount) < float(gw_asset['minWithdraw']):
            raise ValueError("Withdraw amount [{}] for {} less than minimum [{}]".format(amount,extern_symbol,float(gw_asset['minWithdraw'])))

        if not gw_handler.validate_withdraw_address(extern_symbol, to_addr):
            raise ValueError("Invalid withdraw address for asset {}".format(extern_symbol))

        account = Account(account, bitshares_instance = self)
        amount = Amount(amount, asset, bitshares_instance=self)
        to = Account(gw_asset['gatewayAccount'], bitshares_instance = self)

        memo_str = '{}:{}:{}'.format(gw_asset['withdrawPrefix'], extern_symbol, to_addr)

        from bitshares.memo import Memo
        memoObj = Memo(
            from_account = account,
            to_account = to,
            bitshares_instance = self
        )

        op = cybex_operations.Transfer(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "from": account["id"],
            "to": to["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj.encrypt(memo_str),
            "extensions": None,
            "prefix": self.prefix
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def issue_asset(self, to, amount, asset, memo = "", account = None, **kwargs):
        """ Issue an asset to another account.

            :param str to: Recipient
            :param float amount: Amount to issue
            :param str asset: Asset to issue
            :param str memo: (optional) Memo
            :param str account: (optional) ths source account to issue
        """
        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, bitshares_instance = self)
        to = Account(to, bitshares_instance = self)
        amount = Amount(amount, asset, bitshares_instance = self)

        memoObj = Memo(
            from_account = account,
            to_account = to,
            bitshares_instance = self
        )

        op = cybex_operations.Asset_issue(**{
            'fee': {"amount": 0, "asset_id": "1.3.0"},
            'issuer': account["id"],
            'issue_to_account': to["id"],
            'asset_to_issue': {
                'amount': int(amount),
                'asset_id': amount.asset["id"],
            },
            'memo': memoObj.encrypt(memo),
            "extensions": None if 'extensions' not in kwargs else kwargs['extensions'],
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def call_order_update(self, delta_collateral, delta_debt, account=None):
        """ call_order_update 
    
            :param str account: the account to cancel
                to (defaults to default_account)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account)
    
        kwargs = {
            'fee':{"amount": 0, "asset_id": "1.3.0"},
            'funding_account':account["id"],
            'delta_collateral':delta_collateral,
            'delta_debt':delta_debt,
        }
    
        op = operations.Call_order_update(**kwargs)
    
        return self.finalizeOp(op, account, "active")

    def create_asset(self, 
        symbol,
        precision,
        max_supply,
        core_exchange_ratio,
        description = '',
        charge_market_fee = True,
        white_list = True,
        override_authority = True,
        transfer_restricted = True,
        is_prediction_market = False,
        account = None,
        **kwargs):
        """ Create asset.

            :param str symbol: symbol of asset 
            :param int precision: precision of asset
            :param int max_supply: max supply of asset
            :param core_exchange_ratio: dict like {'symbol': 1, 'CYB': 2000}
                    'symbol' and 'CYB' must be in key, value must be int
            :param str description: description of asset
            
            PERMISSION FLAGS FOR ASSET.
            Caution!!! this can not be updated after created.
            :param bool charge_market_fee: set to true if an issuer specific percentage of
                    all market trades in this asset is paid to the issuer
            :param bool white_list: accounts must be white listed to hold this asset
            :param bool override_authority: issuer has permission to transfer from any to any
            :param bool transfer_restricted: issuer should be on part in transfer operation
            END OF PERMISSION FLAGS

            :param bool is_prediction_market
            :param str account: creator of asset
        """

        if (len(core_exchange_ratio) != 2 or 
            symbol not in core_exchange_ratio or
            'CYB' not in core_exchange_ratio):
            raise ValueError("Invalid core exchange ratio")

        if precision < 0 or precision > 12:
            raise ValueError("Invalid precision, not in range [0, 12]")

        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        perm = {
            "charge_market_fee": 0x01,
            "white_list": 0x02,
            "override_authority": 0x04,
            "transfer_restricted": 0x08,
            "disable_force_settle": 0x10,
            "global_settle": 0x20,
            "disable_confidential": 0x40,
            "witness_fed_asset": 0x80,
            "committee_fed_asset": 0x100,
        }
        
        permissions = {"charge_market_fee" : charge_market_fee,
                       "white_list" : white_list,
                       "override_authority" : override_authority,
                       "transfer_restricted" : transfer_restricted,
                       "disable_force_settle" : False,
                       "global_settle" : False,
                       "disable_confidential" : True,
                       "witness_fed_asset" : False,
                       "committee_fed_asset" : False,
                       }
        flags       = {"charge_market_fee" : False,
                       "white_list" : False,
                       "override_authority" : False,
                       "transfer_restricted" : False,
                       "disable_force_settle" : False,
                       "global_settle" : False,
                       "disable_confidential" : False,
                       "witness_fed_asset" : False,
                       "committee_fed_asset" : False,
                       }

        permissions_int = sum(
            [perm[p] if v else 0
                for p, v in permissions.items()])

        flags_int = sum(
            [perm[p] if v else 0
                for p, v in flags.items()])
        
        core_asset = asset.Asset('CYB', cybex_instance = self)

        options = {"max_supply" : max_supply * (10 ** precision),
                   "market_fee_percent" : 0,
                   "max_market_fee" : 0,
                   "issuer_permissions" : permissions_int,
                   "flags" : flags_int,
                   "precision" : precision,
                   "core_exchange_rate" : {
                       "base": {
                           "amount": int(core_exchange_ratio['CYB'] * (10 ** core_asset.precision)),
                           "asset_id": core_asset['id']},
                       "quote": {
                           "amount": core_exchange_ratio[symbol] * (10 ** precision),
                           "asset_id": "1.3.1"}},
                   "whitelist_authorities" : [],
                   "blacklist_authorities" : [],
                   "whitelist_markets" : [],
                   "blacklist_markets" : [],
                   "description" : description,
                   "extensions" : [] 
                   }

        if 'common_options' in kwargs:
              common_options=kwargs['common_options']
        else:
              common_options=options
        
        if 'bitasset_options' in kwargs:
              bitasset_options=kwargs['bitasset_options']
        else:
              bitasset_options=None
        
        asset_options = {
                     'fee': {"amount": 0, "asset_id": "1.3.0"},
                     'issuer': account["id"],
                     'symbol': symbol,
                     'precision': precision,
                     'common_options': common_options,
                     'is_prediction_market': is_prediction_market
        }

        if bitasset_options:
             asset_options['bitasset_opts'] = bitasset_options 
        
        op = operations.Asset_create(**asset_options)

        return self.finalizeOp(op, account, "active", **kwargs)

    def balance_claim(self, account, balance_id, balance_owner_key, amount, asset, **kwargs):
        """ Claim balance.

            :param str account: account to deposit the balance
            :param str balance_id: object id of balance object
            :param str balance_owner_key: public key of balance owner
            :param int amount: amount to claim
            :param str asset: asset to claim
        """
        account = Account(account, bitshares_instance = self)
        amount = Amount(amount, asset, bitshares_instance = self)
        op = cybex_operations.Balance_claim(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "deposit_to_account": account["id"],
            "balance_to_claim": balance_id,
            "balance_owner_key": balance_owner_key,
            "total_claimed": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def cancel(self, orderNumber, account=None, **kwargs):
        """ Cancel order by order id.
            For bitshares users, multiple orders can be canceled in one transaction
            But in cybex, to support rte, user can only cancel one order in single trx
            :param str orderNumbers: The Order Object ide of the form ``1.7.xxxx``
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, full=False, bitshares_instance=self)

        if isinstance(orderNumber, (list, tuple, set)):
            raise ValueError("Cybex does not support cancel more than one order in single transaction")

        op = cybex_operations.Limit_order_cancel(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "fee_paying_account": account["id"],
            "order": orderNumber,
            "extensions": [],
            "prefix": self.prefix})
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def cancel_by_rte(self, transaction_id, account = None, **kwargs):
        """ Cancel order by transaction id.

            :param str transaction_id: transaction id of the order
            :param account: account to execute the cancel
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)
        
        op = cybex_operations.Limit_order_cancel(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "fee_paying_account": account["id"],
            "order": "1.7.0",
            "extensions": [[6, {"trx_id": transaction_id}]],
            "prefix": self.prefix})
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def cancel_trading_pair(self, sell_asset, recv_asset, account = None, **kwargs):
        """ Cancel by trading pair

            :param str sell_asset
            :param str recv_asset
            :param str account
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if sell_asset == 'CYB' and recv_asset == 'CYB':
            raise ValueError("You need to provide different asset to cancel by trading pair")

        account = Account(account, bitshares_instance=self)
        sell_asset = asset.Asset(sell_asset, cybex_instance = self)
        recv_asset = asset.Asset(recv_asset, cybex_instance = self)
        
        op = cybex_operations.Cancel_all(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "seller": account["id"],
            "sell_asset_id": sell_asset['id'],
            "receive_asset_id": recv_asset['id']
            })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def cancel_all(self, account = None, **kwargs):
        """ Cancel all orders by account
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)
        core_asset = asset.Asset('CYB', cybex_instance = self)
        
        op = cybex_operations.Cancel_all(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "seller": account["id"],
            "sell_asset_id": core_asset['id'],
            "receive_asset_id": core_asset['id']
            })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def cancel_vesting(self, balance_object, sender = None, **kwargs):
        """ cancel vesting balance.

            :param str balance_object_id: balance object id of balance
            :param sender 
        """
        if not sender:
            if "default_account" in config:
                sender = config["default_account"]
        if not sender:
            raise ValueError("You need to provide an account")

        account = Account(sender, bitshares_instance = self)
        op = cybex_operations.Cancel_vesting(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "payer": account["id"],
            "sender": account["id"],
            "balance_object": balance_object
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def custom(self, required_auths, id, data, to_hex = custom.convert_to_hex, account = None, **kwargs):
        """ send custom operation

            :param list required_auths: list of accounts
            :param int  id: user specified integer
            :param str data: user specified data
            :param str account: account to send this operation
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if id >= 65536 or id < 0:
            raise ValueError("id must be in range [0, 65535)")

        account = Account(account, bitshares_instance = self)
        op = cybex_operations.Custom(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "payer": account["id"],
            "required_auths": [Account(x, bitshares_instance = self)["id"] for x in required_auths],
            "id": id,
            "data": to_hex(data)
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def account_whitelist(
        self,
        account_to_whitelist,
        lists=["white"],   # set of 'white' and/or 'black'
        account=None,
        **kwargs
    ):
        """ Account whitelisting

            :param str account_to_whitelist: The account we want to add
                to either the white- or the blacklist
            :param set lists: (defaults to ``('white')``). Lists the
                user should be added to. Either empty set, 'black',
                'white' or both.
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, bitshares_instance = self)
        account_to_list = Account(
            account_to_whitelist, bitshares_instance = self)

        if not isinstance(lists, (set, list)) :
            raise ValueError('"lists" must be of instance list()')

        l = cybex_operations.Account_whitelist.no_listing
        if "white" in lists:
            l += cybex_operations.Account_whitelist.white_listed
        if "black" in lists:
            l += cybex_operations.Account_whitelist.black_listed

        op = cybex_operations.Account_whitelist(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "authorizing_account": account["id"],
            "account_to_list": account_to_list["id"],
            "new_listing": l,
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def proposal_delete(self, proposal_id, account, **kwargs):
        """ Proposal delete

            :param str proposal_id: The id of proposal we want to delete
            :param str account: The account who will do this operation
            
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, bitshares_instance = self)

        op = cybex_operations.Proposal_delete(**{
            "fee_paying_account": account["id"],
            "using_owner_authority": False,
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "proposal": proposal_id, 
            })
        return self.finalizeOp(op, account, "active", **kwargs)

    def initiate_dice_bet(
        self,
        asset_to_bet,
        initial_balance,
        clearing_threshold,
        min_amount,
        max_amount,
        pay_discount_percent,
        max_dice,
        account = None,
        **kwargs
    ): 
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance = self)
        asset_to_bet = asset.Asset(asset_to_bet, cybex_instance = self)
        precision = asset_to_bet['precision']

        op = cybex_operations.Initiate_dice_bet(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "asset_to_bet": asset_to_bet["id"],
            "initial_balance": initial_balance * 10 ** precision,
            "clearing_threshold": clearing_threshold * 10 ** precision,
            "min_amount": min_amount * 10 ** precision,
            "max_amount": max_amount * 10 ** precision,
            "pay_discount_percent": pay_discount_percent * 10000,
            "max_dice": max_dice
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def deposit_dice_bet(
        self,
        dice_bet_id,
        amount,
        account = None,
        **kwargs
    ):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance = self)
        dice_bet = dice.Dicebet(dice_bet_id, cybex_instance = self)
        amount = Amount(amount, dice_bet.asset_to_bet, bitshares_instance = self)
        op = cybex_operations.Deposit_dice_bet(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "dice_bet": dice_bet_id,
            "amount": int(amount)
        })

        return self.finalizeOp(op, account, "active", **kwargs)
        
    def withdraw_dice_bet(
        self,
        dice_bet_id,
        amount,
        account = None,
        **kwargs
    ):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance = self)
        dice_bet = dice.Dicebet(dice_bet_id, cybex_instance = self)
        amount = Amount(amount, dice_bet.asset_to_bet, bitshares_instance = self)
        op = cybex_operations.Withdraw_dice_bet(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "dice_bet": dice_bet_id,
            "amount": int(amount)
        })

        return self.finalizeOp(op, account, "active", **kwargs)
        
    def participate_dice_bet(
        self,
        dice_bet_id,
        amount,
        choice,
        account = None,
        **kwargs
    ):
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance = self)
        dice_bet = dice.Dicebet(dice_bet_id, cybex_instance = self)
        amount = Amount(amount, dice_bet.asset_to_bet, bitshares_instance = self)

        op = cybex_operations.Participate_dice_bet(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "dice_bet": dice_bet_id,
            "payer": account["id"],
            "amount": int(amount),
            "choice": choice
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def create_exchange(self,
        name,
        rate,
        description,
        extensions = [],
        whitelist = [],
        blacklist = [],
        allow_quote_to_base = False,
        allow_base_to_quote = False,
        allow_deposit_base = True,
        allow_withdraw_base = True,
        allow_deposit_quote = True,
        allow_withdraw_quote = True,
        allow_charge_market_fee = False,
        allow_modify_rate = True,
        allow_only_whitelist = True,
        account = None,
        **kwargs):
        """ Create exchange.

            :param str name: name of exchange 
            :param dict rate: like {'base': {'symbol': 'JADE.ETH', 'amount': 1}, 'quote': {'symbol': 'JADE.USDT', 'amount': 200}}
            :param str description: description of asset
            :param extensions: element like [1, {"asset_id": "1.3.2", "min": 20, "max": 30}]

            PERMISSION FLAGS FOR ASSET.
            :param bool allow_quote_to_base: set to true if one can participate with quote asset
            :param bool allow_base_to_quote: set to true if one can participate with base asset
            :param bool allow_deposit_base:  set to true if owner need to deposit base
            :param bool allow_withdraw_base: set to true if owner need to withdraw base
            :param bool allow_deposit_quote:  set to true if owner need to deposit quote 
            :param bool allow_withdraw_quote: set to true if owner need to withdraw quote 
            :param bool allow_charge_market_fee: set to true if market fee is charged
                ( market fee flag should also be set for asset )
            :param bool allow_modify_rate: set to true if owner need to modify rate
            :param allow_only_whitelist: set to true if only whitelist(blacklist) accounts are allowed
            END OF PERMISSION FLAGS

            :param str account: creator of exchange
        """

        if len(rate) != 2 or len(set(rate.keys())) != 2:
            raise ValueError("Invalid rate")

        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        permissions = {
            "allow_quote_to_base": True,
            "allow_base_to_quote": True,
            "allow_deposit_base": True,
            "allow_withdraw_base": True,
            "allow_deposit_quote": True,
            "allow_withdraw_quote": True,
            "allow_charge_market_fee": True,
            "allow_modify_rate": True,
            "allow_only_whitelist": True
        }

        flags       = {
            "allow_quote_to_base": allow_quote_to_base,
            "allow_base_to_quote": allow_base_to_quote,
            "allow_deposit_base": allow_deposit_base,
            "allow_withdraw_base": allow_withdraw_base,
            "allow_deposit_quote": allow_deposit_quote,
            "allow_withdraw_quote": allow_withdraw_quote,
            "allow_charge_market_fee": allow_charge_market_fee,
            "allow_modify_rate": allow_modify_rate,
            "allow_only_whitelist": allow_only_whitelist
        }

        permissions_int = sum(
            [cybex_exchange.Exchange.permission_flags[p] if v else 0
                for p, v in permissions.items()])

        flags_int = sum(
            [cybex_exchange.Exchange.permission_flags[p] if v else 0
                for p, v in flags.items()])

        base_asset = asset.Asset(rate['base']['symbol'], cybex_instance = self)
        quote_asset = asset.Asset(rate['quote']['symbol'], cybex_instance = self)
        options = {
            'rate': {
                'base': {'asset_id': base_asset['id'], 'amount':int(rate['base']['amount'] * (10 ** base_asset.precision))},
                'quote': {'asset_id': quote_asset['id'], 'amount':int(rate['quote']['amount'] * (10 ** quote_asset.precision))}
            },
            "owner_permissions": permissions_int,
            "flags": flags_int,
            "whitelist_authorities": [
                Account(acc, bitshares_instance = self)['id']
                for acc in whitelist],
            "blacklist_authorities": [
                Account(acc, bitshares_instance = self)['id']
                for acc in blacklist],
            "extensions" : extensions,
            "description": description
        }

        op = cybex_operations.Create_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": name,
            "owner": account["id"],
            "options": options
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def update_exchange(self,
        name,
        rate,
        description,
        extensions = [],
        whitelist = [],
        blacklist = [],
        allow_quote_to_base = False,
        allow_base_to_quote = True,
        allow_deposit_base = True,
        allow_withdraw_base = True,
        allow_deposit_quote = True,
        allow_withdraw_quote = True,
        allow_charge_market_fee = False,
        allow_modify_rate = True,
        allow_only_whitelist = True,
        new_options = False,
        new_owner = None,
        account = None,
        **kwargs):
        """ Update exchange.

            :param str name: name or id of exchange 
            :param str account: creator of exchange
            :param bool new_options: set to True if you want to change options
            :param str new_owner: set to "" indicates no ownership transfer, else, set to new owner name if need to transfer ownership
        """

        if rate:
            if len(rate) != 2 or len(set(rate.keys())) != 2:
                raise ValueError("Invalid rate")

        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        flags       = {
            "allow_quote_to_base": allow_quote_to_base,
            "allow_base_to_quote": allow_base_to_quote,
            "allow_deposit_base": allow_deposit_base,
            "allow_withdraw_base": allow_withdraw_base,
            "allow_deposit_quote": allow_deposit_quote,
            "allow_withdraw_quote": allow_withdraw_quote,
            "allow_charge_market_fee": allow_charge_market_fee,
            "allow_modify_rate": allow_modify_rate,
            "allow_only_whitelist": allow_only_whitelist
        }

        flags_int = sum(
            [cybex_exchange.Exchange.permission_flags[p] if v else 0
                for p, v in flags.items()])

        options = None

        base_asset = asset.Asset(rate['base']['symbol'], cybex_instance = self)
        quote_asset = asset.Asset(rate['quote']['symbol'], cybex_instance = self)
        exchange = cybex_exchange.Exchange(name, cybex_instance = self)

        if new_options:
            options = {
                'rate': {
                    'base': {'asset_id': base_asset['id'], 'amount':int(rate['base']['amount'] * (10 ** base_asset.precision))},
                    'quote': {'asset_id': quote_asset['id'], 'amount':int(rate['quote']['amount'] * (10 ** quote_asset.precision))}
                },
                "owner_permissions": exchange["options"]["owner_permissions"],
                "flags": flags_int,
                "whitelist_authorities": [
                    Account(acc, bitshares_instance = self)['id']
                    for acc in whitelist],
                "blacklist_authorities": [
                    Account(acc, bitshares_instance = self)['id']
                    for acc in blacklist],
                "extensions" : extensions,
                "description": description
            }

        if new_owner:
            new_owner = Account(new_owner, bitshares_instance = self)            
            new_owner_id = new_owner['id']
        else:
            new_owner_id = ""

        op = cybex_operations.Update_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "exchange_to_update": exchange['id'],
            "new_owner": new_owner_id,
            "new_options": options
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def deposit_exchange(self, exchange, amount, asset, account = None, **kwargs):
        """ deposite to exchange object
        
            :param str exchange: name or id of exchange 
            :param float amount: amount to deposit
            :param str asset: asset to deposit
            :param str account: owner of exchange
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        exchange = cybex_exchange.Exchange(exchange, cybex_instance = self)
        account = Account(account, bitshares_instance=self)
        amount = Amount(amount, asset, bitshares_instance=self)

        op = cybex_operations.Deposit_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "exchange_to_deposit": exchange['id'],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def withdraw_exchange(self, exchange, amount, asset, account = None, **kwargs):
        """ withdraw from exchange object
        
            :param str exchange: name or id of exchange 
            :param float amount: amount to withdraw 
            :param str asset: asset to withdraw
            :param str account: owner of exchange
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        exchange = cybex_exchange.Exchange(exchange, cybex_instance = self)
        account = Account(account, bitshares_instance=self)
        amount = Amount(amount, asset, bitshares_instance=self)

        op = cybex_operations.Withdraw_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "exchange_to_withdraw": exchange['id'],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def remove_exchange(self, exchange, account = None, **kwargs):
        """ remove exchange object
        
            :param str exchange: name or id of exchange 
            :param str account: owner of exchange
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        exchange = cybex_exchange.Exchange(exchange, cybex_instance = self)
        account = Account(account, bitshares_instance=self)

        op = cybex_operations.Remove_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "exchange_to_remove": exchange["id"]
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def participate_exchange(self, exchange, amount, asset, account = None, **kwargs):
        """ participate exchange
        
            :param str exchange: name or id of exchange 
            :param float amount: amount to withdraw 
            :param str asset: asset to withdraw
            :param str account: owner of exchange
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        exchange = cybex_exchange.Exchange(exchange, cybex_instance = self)
        account = Account(account, bitshares_instance=self)
        amount = Amount(amount, asset, bitshares_instance=self)

        op = cybex_operations.Participate_exchange(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "payer": account["id"],
            "exchange_to_pay": exchange["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def create_nonfungible(self, 
        symbol,
        max_supply,
        description,
        white_list = True,
        transfer_restricted = True,
        charge_market_fee = True,
        allow_trade = True,
        allow_override = True,
        account = None,
        **kwargs):
        """ Create nonfungible.

            :param str symbol: symbol of nonfungible
            :param int max_supply: max total amount of all tokens
            :param str description: description of asset

            PERMISSION FLAGS FOR ASSET.
            :param bool white_list: account should be whitelisted to hold the asset
            :param bool transfer_restricted: issuer should be one party of transfer operation
            :param bool charge_market_fee: charge market fee when order fills
            :param bool allow_trade: allow token holders to place order
            :param bool allow_override: issuer may override token
            END OF PERMISSION FLAGS

            :param str account: creator of nonfungible
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        perm = cybex_nonfungible.Nonfungible.permission_flags
        permissions = {
            "white_list": white_list,
            "transfer_restricted": transfer_restricted,
            "charge_market_fee": charge_market_fee,
            "allow_trade": allow_trade,
            "allow_override": allow_override
        }

        flags = {
            "white_list": False,
            "transfer_restricted": False,
            "charge_market_fee": False,
            "allow_trade": True,
            "allow_override": True
        }

        permissions_int = sum(
            [perm[p] if v else 0
                for p, v in permissions.items()])

        flags_int = sum(
            [perm[p] if v else 0
                for p, v in flags.items()])

        opt_ext = []
        if 'first_trade_fee_multi' in kwargs:
            FEE_MULTI_SHIFT_BITS = 10
            multi = kwargs['first_trade_fee_multi']
            assert isinstance(multi, int) and multi > 0
            multi <<= FEE_MULTI_SHIFT_BITS
            opt_ext.append([0, {"multiple": multi}])

        options = {
            "max_supply": max_supply,
            "issuer_permissions": permissions_int,
            "flags": flags_int,
            "whitelist_authorities": [],
            "blacklist_authorities": [],
            "whitelist_markets": [],
            "blacklist_markets": [],
            "description": description,
            "extensions": opt_ext
        }

        if 'common_options' in kwargs:
            common_options = kwargs['common_options']
        else:
            common_options = options

        create_op = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account["id"],
            "symbol": symbol,
            "common_options": common_options
        }

        op = cybex_operations.Create_nonfungible(**create_op)

        return self.finalizeOp(op, account, "active", **kwargs)

    def update_nonfungible(self,
        symbol,
        description,
        max_supply,
        whitelist_authorities = [],
        blacklist_authorities = [],
        whitelist_markets = [],
        blacklist_markets = [],
        white_list = True,
        transfer_restricted = True,
        charge_market_fee = True,
        allow_trade = True,
        allow_override = True,
        new_issuer = None,
        account = None,
        **kwargs):
        """ Update nonfungible

            :param str symbol: symbol or id of nonfungible
            :param str description: description string of nonfungible
            :param int max_supply: max supply of nonfungible
            :param str account: current issuer of nonfungible
        """

        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        flags = {
            "white_list": white_list,
            "transfer_restricted": transfer_restricted,
            "charge_market_fee": charge_market_fee,
            "allow_trade": allow_trade,
            "allow_override": allow_override
        }

        nonfungible = cybex_nonfungible.Nonfungible(symbol, cybex_instance = self)
        flags_int = sum(
            [cybex_nonfungible.Nonfungible.permission_flags[p] if v else 0
                for p, v in flags.items()])

        options = {
            'max_supply': max_supply,
            'issuer_permissions': nonfungible['options']['issuer_permissions'],
            'flags': flags_int,
            'whitelist_authorities': [
                Account(acc, bitshares_instance = self)['id']
                for acc in whitelist_authorities
            ],
            'blacklist_authorities': [
                Account(acc, bitshares_instance = self)['id']
                for acc in blacklist_authorities
            ],
            'whitelist_markets': [
                asset.Asset(ass, cybex_instance = self)['id']
                for ass in whitelist_markets
            ],
            'blacklist_markets': [
                asset.Asset(ass, cybex_instance = self)['id']
                for ass in blacklist_markets
            ],
            'description': description
        }

        if new_issuer:
            new_issuer = Account(new_issuer, bitshares_instance = self)["id"]
        else:
            new_issuer = None
    
        op = cybex_operations.Update_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account["id"],
            "nonfungible_to_update": nonfungible["id"],
            "new_issuer": new_issuer,
            "new_options": options
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def issue_token(self,
        to,
        nonfungible,
        amount,
        attributes,
        memo,
        account = None, **kwargs):
        """ Issue token

            :param str to: Recipient
            :param str nonfungible: Nonfungible to issue
            :param int amount: Amount to issue
            :param dict attributes: token attributes
            :param str memo: (optional) Memo, may begin with `#` for encrypted
                messaging
            :param str account: (optional) issuer name
                if not ``default_account``
        """
        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)
        to = Account(to, bitshares_instance=self)

        memoObj = Memo(
            from_account=account,
            to_account=to,
            bitshares_instance=self
        )
    
        nonfungible = cybex_nonfungible.Nonfungible(nonfungible, cybex_instance = self)

        op = cybex_operations.Issue_nonfungible(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account["id"],
            "nonfungible_to_issue": nonfungible["id"],
            "amount": int(amount),
            "attributes": attributes,
            "issue_to_account": to["id"],
            "memo": memoObj.encrypt(memo),
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    def transfer_token(self,
        to,
        nonfungible,
        selector,
        memo = "",
        account = None,
        **kwargs):
        """ Transfer token

            :param str to: Recipient
            :param str nonfungible: Nonfungible to issue
            :param selector dict or list: token selector
            list selector example:
            [ token_id1, token_id2, token_id3,... ]
            dict selector example:
            {
                "max_count": 1000,
                "max_amount": 10000,
                "filter": {
                    "op": "and",
                    "expr1": ["attr1", "gt", 100],
                    "expr2": {
                        "op": "or",
                        "expr1": ["attr2", "eq", "abc"],
                        "expr2": ["attr3", "le", 999 ]
                    }
                }
            }
            :param memo str: (Optional) memo str
        """
        from bitshares.memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)
        to = Account(to, bitshares_instance=self)

        memoObj = Memo(
            from_account=account,
            to_account=to,
            bitshares_instance=self
        )
    
        nonfungible = cybex_nonfungible.Nonfungible(nonfungible, cybex_instance = self)

        op = cybex_operations.Transfer_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "selector": cybex_nonfungible.generate_selector(nonfungible['id'], selector),
            "from": account["id"],
            "to": to["id"],
            "memo": memoObj.encrypt(memo),
            "prefix": self.prefix
        })

        return self.finalizeOp(op, account, "active", **kwargs)
    
    def reserve_token(self,
        nonfungible,
        selector,
        account = None,
        **kwargs):
        """ Reserve token

            :param str nonfungible: Nonfungible to reserve
            :param selector dict or list: token selector
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        nonfungible = cybex_nonfungible.Nonfungible(nonfungible, cybex_instance = self)

        op = cybex_operations.Reserve_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "owner": account["id"],
            "selector": cybex_nonfungible.generate_selector(nonfungible["id"], selector)
        })

        return self.finalizeOp(op, account, "active", **kwargs)
    
    def sell_token(self,
        nonfungible,
        selector,
        asset,
        price,
        expiration = 86400,
        fill_or_kill = False,
        account = None,
        **kwargs):
        """ Sell token

            :param str nonfungible: Nonfungible to sell
            :param selector dict or list: token selector
            :param str asset: asset to sell for
            :param float price: amount of asset to sell for
            :param int expiration: expiration of order in seconds
            :param bool fill_or_kill: order should be totally filled immediately
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        nonfungible = cybex_nonfungible.Nonfungible(nonfungible, cybex_instance = self)

        amount = Amount(price, asset, bitshares_instance=self)

        op = cybex_operations.Sell_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "seller": account['id'],
            "selector": cybex_nonfungible.generate_selector(nonfungible['id'], selector),
            "price": {"amount": int(amount), "asset_id": amount.asset['id']},
            "expiration": formatTimeFromNow(expiration),
            "fill_or_kill": fill_or_kill
        })

        return self.finalizeOp(op, account, "active", **kwargs)
    
    def buy_token(self,
        nonfungible,
        selector,
        asset,
        price,
        expiration = 86400,
        fill_or_kill = False,
        account = None,
        **kwargs):
        """ Buy token

            :param str nonfungible: Nonfungible to buy
            :param selector dict or list: token selector
            :param str asset: pay asset
            :param float price: pay amount
            :param int expiration: expiration of order in seconds
            :param bool fill_or_kill: order should be totally filled immediately
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        nonfungible = cybex_nonfungible.Nonfungible(nonfungible, cybex_instance = self)

        amount = Amount(price, asset, bitshares_instance=self)

        op = cybex_operations.Buy_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "buyer": account['id'],
            "selector": cybex_nonfungible.generate_selector(nonfungible['id'], selector),
            "price": {"amount": int(amount), "asset_id": amount.asset['id']},
            "expiration": formatTimeFromNow(expiration),
            "fill_or_kill": fill_or_kill
        })

        return self.finalizeOp(op, account, "active", **kwargs)
    
    def cancel_sell_token(self,
        order_id,
        account = None,
        **kwargs):
        """ Cancel sell token

            :param str order_id: Order id of Token sell order
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        op = cybex_operations.Cancel_sell_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "seller": account['id'],
            "order_id": order_id
        })

        return self.finalizeOp(op, account, "active", **kwargs)
        
    def cancel_buy_token(self,
        order_id,
        account = None,
        **kwargs):
        """ Cancel sell token

            :param str order_id: Order id of Token buy order
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        op = cybex_operations.Cancel_buy_token(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "buyer": account['id'],
            "order_id": order_id
        })

        return self.finalizeOp(op, account, "active", **kwargs)

    def override_token(self,
        token_id,
        new_owner = None,
        new_attributes = None,
        account = None,
        **kwargs):
        """ Override token

            params including new_owner, new_attributes are optional
        """
        if new_owner is None and new_attributes is None:
            raise ValueError("Nothing to override")
        
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, bitshares_instance=self)

        tok = self.rpc.get_objects([token_id])[0]
        op_dic = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account['id'],
            "token": token_id,
            "owner": tok['owner']
        }

        if new_owner:
            new_owner = Account(new_owner, bitshares_instance = self)
            op_dic['new_owner'] = new_owner['id']

        if new_attributes:
            op_dic['new_attributes'] = new_attributes
        
        op = cybex_operations.Override_token(**op_dic)
        return self.finalizeOp(op, account, "active", **kwargs)

    def asset_claim_fees(self,
        symbol,
        amount,
        account = None,
        **kwargs):
        """ Claim fee from asset fee pool
        """

        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, bitshares_instance=self)

        amount = Amount(amount, symbol, bitshares_instance=self)

        op = cybex_operations.Asset_claim_fees(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "issuer": account['id'],
            "amount_to_claim": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            }
        })

        return self.finalizeOp(op, account, "active", **kwargs)
