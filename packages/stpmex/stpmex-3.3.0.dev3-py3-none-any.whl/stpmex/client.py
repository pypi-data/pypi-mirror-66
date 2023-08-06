from typing import Any, ClassVar, Dict, List, Union

from OpenSSL import crypto
from requests import Response, Session

from .exc import (
    ClaveRastreoAlreadyInUse,
    InvalidAccountType,
    InvalidPassphrase,
    InvalidRfcOrCurp,
    NoOrdenesEncontradas,
    NoServiceResponse,
    PldRejected,
    SignatureValidationError,
    StpmexException,
)
from .resources import CuentaFisica, Orden, Resource, Saldo
from .version import __version__ as client_version

DEMO_BASE_URL = 'https://demo.stpmex.com:7024/speidemows/rest'
PROD_BASE_URL = 'https://prod.stpmex.com/speiws/rest'


class Client:
    base_url: str
    empresa: str
    demo: bool
    headers: Dict[str, str]
    session: Session
    verify_ssl: bool

    # resources
    cuentas: ClassVar = CuentaFisica
    ordenes: ClassVar = Orden

    def __init__(
        self,
        empresa: str,
        priv_key: str,
        priv_key_passphrase: str,
        demo: bool = False,
    ):
        self.session = Session()
        self.headers = {'User-Agent': f'stpmex-python/{client_version}'}
        if demo:
            self.base_url = DEMO_BASE_URL
            self.verify_ssl = False
        else:
            self.base_url = PROD_BASE_URL
            self.verify_ssl = True
        try:
            self.pkey = crypto.load_privatekey(
                crypto.FILETYPE_PEM,
                priv_key,
                priv_key_passphrase.encode('ascii'),
            )
        except crypto.Error:
            raise InvalidPassphrase
        self.empresa = empresa
        Resource.empresa = empresa
        Resource._client = self

    def consulta_saldos(self) -> List[Saldo]:
        return Saldo.consulta()

    def post(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Union[Dict[str, Any], List[Any]]:
        return self.request('post', endpoint, data)

    def put(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Union[Dict[str, Any], List[Any]]:
        return self.request('put', endpoint, data)

    def delete(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Union[Dict[str, Any], List[Any]]:
        return self.request('delete', endpoint, data)

    def request(
        self, method: str, endpoint: str, data: Dict[str, Any], **kwargs: Any
    ) -> Union[Dict[str, Any], List[Any]]:
        url = self.base_url + endpoint
        response = self.session.request(
            method,
            url,
            json=data,
            headers=self.headers,
            verify=self.verify_ssl,
            **kwargs,
        )
        self._check_response(response)
        resultado = response.json()
        if 'resultado' in resultado:  # Some responses are enveloped
            resultado = resultado['resultado']
        return resultado

    @staticmethod
    def _check_response(response: Response) -> None:
        if response.ok:
            resp = response.json()
            if isinstance(resp, dict):
                try:
                    if 'descripcionError' in resp['resultado']:
                        id = resp['resultado']['id']
                        error = resp['resultado']['descripcionError']
                        if id == -11:
                            raise InvalidAccountType(**resp['resultado'])
                        elif (
                            id == 0
                            and error == 'No se recibió respuesta del servicio'
                        ):
                            raise NoServiceResponse(**resp['resultado'])
                        elif id == 0 and error == 'Error validando la firma':
                            raise SignatureValidationError(**resp['resultado'])
                        elif id == -1:
                            raise ClaveRastreoAlreadyInUse(**resp['resultado'])
                        elif id == -100:
                            raise NoOrdenesEncontradas
                        elif id == -200:
                            raise PldRejected(**resp['resultado'])
                        else:
                            raise StpmexException(**resp['resultado'])
                except KeyError:
                    if 'descripcion' in resp and resp['descripcion']:
                        id = resp['id']
                        if id == 1:
                            raise InvalidRfcOrCurp(**resp)
                        else:
                            raise StpmexException(**resp)
        response.raise_for_status()
