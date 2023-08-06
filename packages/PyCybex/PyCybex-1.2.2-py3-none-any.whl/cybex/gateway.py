import requests, json, re, time
from binascii import hexlify
from graphenebase.types import Signature
from graphenebase.ecdsa import sign_message

class CybexGateway(object):
    def __init__(self, gw_endpoint):
        self.endpoint = gw_endpoint

    def sign_query_req(self, name, wif):
        ts = int(time.time())
        sig = Signature(sign_message('{}{}'.format(ts, name).encode('UTF-8'), wif))
        sig_hex = hexlify(sig.data).decode('ascii')
        return 'Bearer {}.{}.{}'.format(ts, name, sig_hex)

    def get_deposit_address(self, name, symbol, wif):
        url = '{}/users/{}/assets/{}/address'.format(self.endpoint, name, symbol)
        sig = self.sign_query_req(name, wif)
        r = requests.get(
                url,
                headers = {'Authorization': sig})
        if r.status_code != 200:
            raise Exception('Cannot get deposit address from gateway')
        return json.loads(r.text)
        
    def get_gateway_asset(self, symbol):
        url = '{}/assets/{}'.format(self.endpoint, symbol)
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return json.loads(r.text)

    def validate_withdraw_address(self, symbol, address):
        asset = self.get_gateway_asset(symbol)
        if asset['useMemo']:
            address = re.match(r"(.*)\[.*\]", address).group(1)
            
        url = '{}/assets/{}/address/{}/verify'.format(self.endpoint, symbol, address)
        r = requests.get(url)
        if r.status_code != 200:
            return False
        return json.loads(r.text)['valid']

if __name__ == '__main__':
    gw_handler = CybexGateway('https://gateway.cybex.io/v1')
    print(gw_handler.get_gateway_asset('ETH'))
    print(gw_handler.validate_withdraw_address('ETH', '0x4675dc5fe44500eb6af616753c75d39c50be31c8'))
    print(gw_handler.validate_withdraw_address('ETH', '0x4675dc5fe44500eb6af616753c75d39c50b'))
    #assert not validate_withdraw_address('ETH', 'invalid_address', 'test-account')
    #assert validate_withdraw_address('ETH', '0x4675dc5fe44500eb6af616753c75d39c50be31c8', 'test-account')
