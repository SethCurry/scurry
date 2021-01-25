import requests

from dataclasses import dataclass


@dataclass
class File:
    name: str
    origin: str
    size: int
    date: int


@dataclass
class JobProgress:
    completion: float
    filepos: int
    printTime: int
    printTimeLeft: int


@dataclass
class Job:
    """
    Attributes:
        estimatedPrintTime (int): The estimated seconds until the print is done
    """
    file: File
    estimatedPrintTime: int


@dataclass
class ListJobsResponse:
    """
    Attributes:
        state (str): The state of the job
        progress (JobProgress): How far the job is into printing
        job (Job): The currently executing job
    """

    state: str
    progress: JobProgress
    job: Job


class Client:
    def __init__(self, url: str, api_key: str):
        """
        Args:
            url (str): The URL of the Octoprint API server
            api_key (str): The API key to use

        Attributes:
            url (str): The URL of the Octoprint API server
            api_key (str): The API key to use
        """
        self.url = url
        self.api_key = api_key

    def jobs(self) -> ListJobsResponse:
        """List the currently executing jobs.

        Returns:
            ListJobsResponse: The list of jobs
        """
        resp = requests.get(
            self.url + "/api/job",
            headers={"X-Api-Key": self.api_key},
        )

        body = resp.json()

        return ListJobsResponse(
            state=body["state"],
            progress=JobProgress(
                completion=body["progress"]["completion"],
                filepos=body["progress"]["filepos"],
                printTime=body["progress"]["printTime"],
                printTimeLeft=body["progress"]["printTimeLeft"],
            ),
            job=Job(
                estimatedPrintTime=body["job"]["estimatedPrintTime"],
                file=File(
                    name=body["job"]["file"]["name"],
                    origin=body["job"]["file"]["origin"],
                    size=body["job"]["file"]["size"],
                    date=body["job"]["file"]["date"],
                ),
            ),
        )
