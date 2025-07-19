import base64, requests, time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

class BotAuth:
    '''
    BotAuth(url)
    
    @PARAMS
    - LocalKeys : Path where the local keys are stored.  Format: list[dict[str, str]]
    
    @METHODS
    - get_local_keys() -> -> list[dict[str, str]]
    - get_remote_keys() -> list[dict[str, str]]
    - get_header()-> dict[str, str]
        
    @info:
    © 2025 Atish Joottun
    '''
    def __init__(self, localKeys, signAgent="http-message-signatures-example.research.cloudflare.com"):
        self.localKeys = localKeys
        self.signAgent = signAgent

    def get_local_keys(self) -> list[dict[str, str]]:
        """
        DUMMY MODULE: TEMPLATE FOR TESTING
        "Deprecated" - This function is a placeholder for local keys.
        It should return a list of dictionaries containing key information.
        """
        # return [
        #     {
        #         "kty": "OKP",
        #         "crv": "Ed25519",
        #         "kid": "poqkLGiymh_W0uP6PZFw-dvez3QJT5SolqXBCW38r0U",
        #         "d": "n4Ni-HpISpVObnQMW0wOhCKROaIKqKtW_2ZYb2p9KcU",
        #         "x": "JrQLj5P_89iXES9-vFgrIy29clF9CC_oPPsw3c5D0bs",
        #     }
        # ]
        return self.localKeys

    def get_remote_header(self, url) -> list[dict[str, str]]:
        """
        @Params:
        - url: str [URL of website]
        """
        res = requests.get(url)
        try:
            res_json = res.headers
            return res_json
        except Exception as e:
            print(e)
            return None
        
    def get_remote_keys(self, url) -> list[dict[str, str]]:
        """
        This function fetches the remote keys from the given URL. uisng the /.well-known/http-message-signatures-directory endpoint.
        """
        domain = requests.utils.urlparse(url).netloc
        well_known_url = f"https://{domain}/.well-known/http-message-signatures-directory"
        res = requests.get(well_known_url)
        try:
            res_json = res.json()
            return res_json
        except Exception as e:
            print(e)
            return None
        

    def _base64url_decode(self, val):
        return base64.urlsafe_b64decode(val + "=" * (-len(val) % 4))

    def _base64_encode_bytes(self, val):
        return base64.b64encode(val).decode("ascii")

    def _jwt_to_private_key(self, jwk):
        return Ed25519PrivateKey.from_private_bytes(self._base64url_decode(jwk["d"]))

    # def _jwk_to_public_key_bytes(self, jwk):
    #     private_key = self.jwk_to_private_key(jwk)
    #     public_key = private_key.public_key()
    #     return public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)

    def get_bot_signature_header(self) -> dict[str, str]:
        """
        This creates and build the signature of the bot based on the key provided. Append the result to the request Header before making the result.
        """
        remote_keys = self.get_remote_keys()
        local_keys = self.localKeys

        if remote_keys is None:
            return None

        ## Get similar key in local repo
        selected_key = None
        for local in local_keys:
            for remote in remote_keys.get("keys", []):
                if remote.get("kid") == local.get("kid") and remote.get("x") == local.get("x"):
                    selected_key = local
                    break
            if selected_key:
                break

        if not selected_key:
            return None

        private_key = self._jwt_to_private_key(selected_key)
        url_obj = requests.utils.urlparse(self.url)
        authority = url_obj.netloc
        now = int(time.time())
        created = now
        expires = now + 3600
        param = f'("@authority" "signature-agent");created={created};expires={expires};keyid="{selected_key["kid"]}";tag="web-bot-auth"'
        base = f'"@authority": {authority}\n"signature-agent": {self.signAgent}\n"@signature-params": {param}'

        signature_b64 = self._base64_encode_bytes(private_key.sign(base.encode("utf-8")))
        header = {
            "Signature-Agent": self.signAgent,
            "Signature-Input": f"sig={param}",
            "Signature": f"sig=:{signature_b64}",
        }

        return header