from google.protobuf.json_format import MessageToDict

from .squareup_pb2 import _sym_db
from .squareup_pb2_twirp import InvoiceFrontendServiceClient


def get_client():
	return InvoiceFrontendServiceClient("https://squareup.com")


GetInvoiceRequest = _sym_db.GetSymbol("squareup.invoice.frontend.GetInvoiceRequest")


def get_invoice(token: str):
	client = get_client()
	ret = client.get_invoice(GetInvoiceRequest(invoice_token=token))
	return MessageToDict(ret)
