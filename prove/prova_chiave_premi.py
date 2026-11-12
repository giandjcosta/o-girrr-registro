"""Nessun contatto con Supabase: chiavi finte e trasporto HTTP simulato."""
import base64
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

spec = importlib.util.spec_from_file_location('premi', Path(__file__).resolve().parents[1] / 'calcoli/premi/registra_premi.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

def jwt(role='service_role', ref='qmjqfgmvimsuxvghetgi'):
    body = base64.urlsafe_b64encode(json.dumps({'role': role, 'ref': ref}).encode()).decode().rstrip('=')
    return 'finto.' + body + '.firma-finta'

class ChiavePremi(unittest.TestCase):
    def test_chiavi_non_server_non_partono(self):
        with patch.object(p.urllib.request, 'urlopen') as http:
            for key in ('', 'sb_publishable_FINTA', 'non-una-chiave', jwt('anon'), jwt(ref='altro')):
                with self.subTest(key=key), self.assertRaises(SystemExit):
                    p.registra({'p_team': 'Squadra di prova'}, key)
            http.assert_not_called()

    def test_headers_e_risposte_server(self):
        for key, bearer in ((jwt(), True), ('sb_secret_FINTA', False)):
            for result in ('created', 'duplicate'):
                response = MagicMock()
                response.__enter__.return_value.read.return_value = json.dumps(result).encode()
                with patch.object(p.urllib.request, 'urlopen', return_value=response) as http:
                    self.assertEqual(p.registra({'p_team': 'Prova'}, key), result)
                    req = http.call_args.args[0]
                    self.assertEqual(req.get_header('Apikey'), key)
                    self.assertEqual(req.get_header('Authorization') is not None, bearer)

    def test_preferenza_chiave_nuova_e_fallback(self):
        with patch.dict(p.os.environ, {'SUPABASE_SECRET_KEY': 'sb_secret_FINTA', 'SUPABASE_SERVICE_ROLE_KEY': jwt()}, clear=True):
            self.assertEqual(p.chiave_server(), 'sb_secret_FINTA')
        with patch.dict(p.os.environ, {'SUPABASE_SERVICE_ROLE_KEY': jwt()}, clear=True):
            self.assertEqual(p.chiave_server(), jwt())

if __name__ == '__main__':
    unittest.main()
