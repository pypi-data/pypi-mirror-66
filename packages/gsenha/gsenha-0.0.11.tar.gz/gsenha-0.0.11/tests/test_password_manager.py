import base64
from unittest import TestCase
try:
    from unittest.mock import patch, Mock
except ImportError:
    from mock import patch, Mock

from cryptography.hazmat.primitives.asymmetric import padding

from gsenha import PasswordManager
from gsenha.exceptions import TokenError


class PasswordManagerTest(TestCase):

    def test_invalid_key_raises_exception(self):
        with self.assertRaises(Exception) as context_manager:
            PasswordManager(key='')

        self.assertEqual(str(context_manager.exception), 'Error loading private key')

    def test_invalid_key_path_raises_exception(self):
        with self.assertRaises(ValueError) as context_manager:
            PasswordManager(key='/this/path/does/not/exists')

        self.assertEqual(str(context_manager.exception), 'Key File does not exist')

    @patch('requests.post')
    def test_response_to_get_token_is_not_ok(self, mock_post):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        with self.assertRaises(TokenError) as context_manager:
            PasswordManager(key='tests/fixtures/privkey.pem')

        self.assertEqual(
            str(context_manager.exception),
            'Response status code to get token is not ok. Status code was: 500'
        )

    @patch('requests.post')
    def test_response_to_get_token_returns_error(self, mock_post):
        mock_post.side_effect = Exception('Boom!')

        with self.assertRaises(Exception) as context_manager:
            PasswordManager(key='tests/fixtures/privkey.pem')

        self.assertEqual(
            str(context_manager.exception),
            'There was error requesting token. Error was: Boom!'
        )

    @patch('requests.post')
    def test_response_to_get_token_is_ok_but_there_is_no_token(self, mock_post):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        self.assertIsNone(pm._token)

    @patch('requests.post')
    def test_response_to_get_token_is_ok(self, mock_post):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {'token': 'my-fake-token'}
        mock_post.return_value = mock_response

        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        self.assertEqual(pm._token, 'my-fake-token')

    @patch.object(PasswordManager, '_get_token', new=lambda x: 'my-fake-token')
    def test_try_to_get_password_but_password_name_is_not_passed(self):
        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        passwords = pm.get_passwords('folder-name')

        self.assertDictEqual(passwords, {})

    @patch.object(PasswordManager, '_get_token', new=lambda x: 'my-fake-token')
    @patch('requests.post')
    def test_request_to_get_password_returns_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'error', 'password': ''}
        mock_post.return_value = mock_response
        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        passwords = pm.get_passwords('folder-name', 'password-name')

        self.assertDictEqual(passwords, {})

    @patch.object(PasswordManager, '_get_token', new=lambda x: 'my-fake-token')
    @patch('requests.post')
    def test_gets_passwords_correctly(self, mock_post):
        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        def encrypt_text(text):
            public_key = pm._rsa_verifier.public_key()
            encrypted_key = public_key.encrypt(text.encode('ascii'), padding.PKCS1v15())
            return base64.b64encode(bytes(encrypted_key))

        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'password': {
                'url': encrypt_text('a'),
                'login': encrypt_text('b'),
                'passwd': encrypt_text('c'),
                'description': encrypt_text('d'),
                'vault': False
            }
        }
        mock_post.return_value = mock_response

        passwords = pm.get_passwords('folder-name', 'password-name')

        self.assertEqual(passwords['password-name']['url'], 'a')
        self.assertEqual(passwords['password-name']['login'], 'b')
        self.assertEqual(passwords['password-name']['password'], 'c')
        self.assertEqual(passwords['password-name']['description'], 'd')

    @patch.object(PasswordManager, '_get_token', new=lambda x: 'my-fake-token')
    @patch('requests.post')
    def test_gets_passwords_correctly_vault_true(self, mock_post):
        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        def b64_encode(text):
            return base64.b64encode(bytes(text, 'utf-8')).decode()

        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'password': {
                'url': b64_encode('a'),
                'login': b64_encode('b'),
                'passwd': b64_encode('c'),
                'description': b64_encode('d'),
                'vault': True
            }
        }
        mock_post.return_value = mock_response

        passwords = pm.get_passwords('folder-name', 'password-name')
        self.assertEqual(passwords['password-name']['url'], 'a')
        self.assertEqual(passwords['password-name']['login'], 'b')
        self.assertEqual(passwords['password-name']['password'], 'c')
        self.assertEqual(passwords['password-name']['description'], 'd')

    @patch.object(PasswordManager, '_get_token', new=lambda x: 'my-fake-token')
    @patch('requests.post')
    def test_gets_passwords_correctly_vault_missing(self, mock_post):
        pm = PasswordManager(key='tests/fixtures/privkey.pem')

        def encrypt_text(text):
            public_key = pm._rsa_verifier.public_key()
            encrypted_key = public_key.encrypt(text.encode('ascii'), padding.PKCS1v15())
            return base64.b64encode(bytes(encrypted_key))

        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'password': {
                'url': encrypt_text('a'),
                'login': encrypt_text('b'),
                'passwd': encrypt_text('c'),
                'description': encrypt_text('d'),
            }
        }
        mock_post.return_value = mock_response

        passwords = pm.get_passwords('folder-name', 'password-name')
        self.assertEqual(passwords['password-name']['url'], 'a')
        self.assertEqual(passwords['password-name']['login'], 'b')
        self.assertEqual(passwords['password-name']['password'], 'c')
        self.assertEqual(passwords['password-name']['description'], 'd')
