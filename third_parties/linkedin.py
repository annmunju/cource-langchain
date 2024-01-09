# import requests
import json


def load_linkedin_profile():
    with open("src/sample.json", "r") as f:
        sample_linkedin = json.load(f)

    return sample_linkedin


def scrape_linkedin_profile(linkedin_profile_url: str):
    sample_raw = load_linkedin_profile()

    data = {
        k: v
        for k, v in sample_raw.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
