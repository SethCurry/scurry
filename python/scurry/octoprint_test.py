import scurry.octoprint as octoprint


def test_list_jobs():
    client = octoprint.Client(os.environ["SCURRY_TEST_OCTOPRINT_URL", "SCURRY_TEST_OCTOPRINT_API_KEY")
    job = client.jobs()
