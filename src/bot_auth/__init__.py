"""
Web Bot Auth Library

A library to check for AI Bot Authentication using the latest HTTP header Signature.
"""

__version__ = "0.1.0"

import base64
import requests
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from datetime import datetime, timedelta
from http_message_signatures import (
    HTTPMessageSigner,
    HTTPSignatureKeyResolver,
    algorithms,
)


class SingleKeyResolver(HTTPSignatureKeyResolver):
    """
    SingleKeyResolver(key)

    A simple key resolver that always returns the same key for any key ID.
    """

    def __init__(
        self,
        key,
    ):
        self.key = key

    def resolve_public_key(self, key_id: str):
        return self.key

    def resolve_private_key(self, key_id: str):
        return self.key


class BotAuth:
    """
    BotAuth(url)

    @PARAMS
    - LocalKeys : Path where the local keys are stored.  Format: list[dict[str, str]]

    @METHODS
    - get_local_keys() -> -> list[dict[str, str]]
    - get_remote_keys() -> list[dict[str, str]]
    - get_header()-> dict[str, str]

    @info:
    © 2025 Atish Joottun
    """

    def __init__(
        self,
        localKeys,
        signAgent="http-message-signatures-example.research.cloudflare.com",
    ):
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
        This function fetches the remote keys from the given URL.
        Using the /.well-known/http-message-signatures-directory endpoint.
        """
        domain = requests.utils.urlparse(url).netloc
        well_known_url = (
            f"https://{domain}/.well-known/http-message-signatures-directory"
        )
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

    def get_bot_signature_header(self, url) -> dict[str, str]:
        """
        This creates and build the signature of the bot based on the key provided.
        Append the result to the request Header before making the result.
        """
        local_keys = self.localKeys

        ## Get similar key in local repo
        selected_key = local_keys[0]

        resolver = SingleKeyResolver(self._jwt_to_private_key(selected_key))
        signer = HTTPMessageSigner(
            signature_algorithm=algorithms.ED25519, key_resolver=resolver
        )

        created = datetime.fromtimestamp(time.time())
        expires = created + timedelta(minutes=5)

        request = requests.Request(
            "GET",
            url,
            headers={
                "Signature-Agent": self.signAgent,
            },
        )
        signer.sign(
            request,
            key_id="compute-jwk-thumbprint",
            covered_component_ids=("@authority", "signature-agent"),
            created=created,
            expires=expires,
            tag="web-bot-auth",
        )

        header = {
            "Signature-Agent": request.headers["Signature-Agent"],
            "Signature-Input": request.headers["Signature-Input"],
            "Signature": request.headers["Signature"],
        }

        return header


# Export the main class and version
__all__ = ["BotAuth", "__version__"]
