import requests


class Services:
    base_url = "http://localhost:8000/api/"

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()

    def authorization(self, authorization_data: dict):
        url = f"{self.base_url}users/{authorization_data['username']}/authenticate/"
        response = requests.post(url, json={"password": authorization_data['password']})
        response.raise_for_status()
        return response.json()

    def create_user(self, user_data: dict):
        response = requests.post(f"{self.base_url}users/", json=user_data)
        response.raise_for_status()
        return response.json()

    def get_users(self, page=1):
        # query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}users/")
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int):
        response = requests.get(f"{self.base_url}users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_transaction(self, transaction_data: dict):
        response = requests.post(f"{self.base_url}transactions/", json=transaction_data)
        response.raise_for_status()
        return response.json()

    def get_currencies(self):
        response = requests.get(f"{self.base_url}currencies/")
        response.raise_for_status()
        return response.json()

    def get_categories(self, is_earning: bool):
        response = requests.get(f"{self.base_url}categories/", params={"is_earning": is_earning})
        response.raise_for_status()
        return response.json()

app_serv = Services()


# dict(limit=self.limit, offset=(page - 1) * self.limit)