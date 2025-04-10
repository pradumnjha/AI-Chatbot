import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class Config:
    def __init__(self):
        self.vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, key):
        return self.client.get_secret(key).value

    @property
    def openai_api_key(self):
        return self.get_secret("OPENAI-API-KEY")

    @property
    def confluence_username(self):
        return self.get_secret("CONFLUENCE-USERNAME")

    @property
    def confluence_token(self):
        return self.get_secret("CONFLUENCE-TOKEN")

    @property
    def microsoft_app_id(self):
        return self.get_secret("MICROSOFT-APP-ID")

    @property
    def microsoft_app_password(self):
        return self.get_secret("MICROSOFT-APP-PASSWORD")