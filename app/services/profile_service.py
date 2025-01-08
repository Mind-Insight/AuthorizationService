from repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository):
        self.profile_repository = profile_repository
