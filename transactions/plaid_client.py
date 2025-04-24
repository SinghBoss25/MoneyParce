from plaid2.client import PlaidClient
from plaid2.authenticator import PlaidAuthentication
from django.conf import settings

auth = PlaidAuthentication(
    client_id='6809fa09b830b6002197b559',
    secret='4541f61eadcb05731b4fd11e1ca927',
    plaid_version="2020-09-14"
)

client = PlaidClient(
    base_url="https://sandbox.plaid.com",
    authenticator=auth
)