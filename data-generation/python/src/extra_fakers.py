from faker import Faker
from faker.providers import DynamicProvider

company_participant_provider = DynamicProvider(
     provider_name="company_participant",
     elements=["OWNER", "BOARDMEMBER", "DIRECTOR"],
)

if __name__=="__main__":
     fake = Faker()
     # then add new provider to faker instance
     fake.add_provider(company_participant_provider)
     fake.company_participant()
