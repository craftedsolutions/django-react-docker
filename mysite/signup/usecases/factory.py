from signup.usecases.get_user_details import GetUserDetails
from signup.persistence.account_repo import AccountRepo
from signup.confirmation import generate_code


class UsecaseFactory(object):
    user_details = None

    account_repo = None

    def user_details_usecase(self):
        if self.user_details is None:
            self.user_details = GetUserDetails(self.get_account_repo())

        return self.user_details

    def get_account_repo(self):
        if self.account_repo is None:
            self.account_repo = AccountRepo(token_generator=generate_code)

        return self.account_repo
