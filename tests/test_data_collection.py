"""
Test module to determine the correctness of the data_collection.py file.

The test case will take the current repository.

Unless that path variable is changed.
"""
import pytest
from src import data_collection
from src import json_handler


def test_collect_and_add_raw_data_to_json():
    """Check that raw data was collected from the repository and was written."""
    test_file = "raw_data_testfile"
    # retreive the dictionary from the test file
    data_from_file = json_handler.get_dict_from_json_file(test_file)
    # Makes sure that the default key is in the dicitionary
    # The key is called "Keep this file empty"
    assert "Keep this file empty" in data_from_file
    repository = "https://github.com/GatorCogitate/cogitate_tool"
    # Call collect and write funciton
    data_collection.collect_and_add_raw_data_to_json(repository, test_file)
    # Update dicitionary from the new data in the file
    data_from_file = json_handler.get_dict_from_json_file(test_file)
    # Make sure the correct key is added
    assert "RAW_DATA" in data_from_file
    # Start teardown process to put file in default state
    default_dict = {"Keep this file empty": []}
    json_handler.write_dict_to_json_file(default_dict, test_file)


def test_collect_and_add_individual_metrics_to_json():
    """Check that calculated data was collected from the repository and was written."""
    read_test_file = "individual_metrics_testfile"
    write_test_file = "calculated_metrics_testfile"
    # retreive the dictionaries from the test file
    calculated_data_from_file = json_handler.get_dict_from_json_file(write_test_file)
    raw_data_from_file = json_handler.get_dict_from_json_file(read_test_file)
    # Makes sure that the default values are in the dicitionaries
    # The key is called "Keep this file empty"
    assert "Keep this file empty" in calculated_data_from_file
    # makes sure RAW_DATA is a key in the individual_metrics_testfile
    assert "RAW_DATA" in raw_data_from_file
    # Call collect and write funciton
    data_collection.collect_and_add_individual_metrics_to_json(
        read_test_file, write_test_file
    )
    # Update dicitionary from the new data in the file
    calculated_data_from_file = json_handler.get_dict_from_json_file(write_test_file)
    # Make sure the correct keys are added
    expected_keys = [
        "schultzh",
        "WonjoonC",
        "Jordan-A",
        "noorbuchi",
        "Chris Stephenson",
    ]
    actual_keys = list(calculated_data_from_file.keys())
    assert actual_keys == expected_keys
    # Start teardown process to put file in default state
    default_dict = {"Keep this file empty": []}
    json_handler.write_dict_to_json_file(default_dict, write_test_file)


@pytest.mark.parametrize(
    "json_file_name", [("individual_metrics_testfile")],
)
def test_calculate_individual_metrics(json_file_name):
    """Check that the individual metrics have been calculated."""
    data = data_collection.calculate_individual_metrics(json_file_name)
    assert len(data) != 0
    # assert (data) != 0


@pytest.mark.parametrize(
    "repository_url", [("https://github.com/GatorCogitate/cogitate_tool")],
)
def test_collect_commits_user_hash(repository_url):
    """Check the collection of the commits hash."""
    dict = {}
    assert len(dict) == 0
    dict = data_collection.collect_commits_hash(repository_url)
    assert len(dict) != 0


@pytest.mark.parametrize(
    "repository_url", [("https://github.com/GatorCogitate/cogitate_tool")],
)
def test_collect_commits_hash(repository_url):
    """Check the commits hash has been gathered."""
    list = []
    assert len(list) == 0
    list = data_collection.collect_commits_hash(repository_url)
    assert len(list) != 0


def test_raw_data_exists_in_testfile():
    """Checks the existence of the key RAW_DATA in individual_metrics_testfile."""
    test_dict = json_handler.get_dict_from_json_file("individual_metrics_testfile")
    assert "RAW_DATA" in test_dict.keys()


def test_calculate_individual_metrics_populates_data():
    """Checks that the function retruns a populated dictionary."""
    test_dict = {}
    # pylint: disable=len-as-condition
    assert len(test_dict) == 0
    test_dict = data_collection.calculate_individual_metrics(
        "individual_metrics_testfile"
    )
    assert len(test_dict) != 0


def test_get_individual_metrics_accuracy():
    """Checks that individual_metrics data outputs correct values."""
    test_dict = data_collection.calculate_individual_metrics(
        "individual_metrics_testfile"
    )
    expected_dict = {
        "EMAIL": "buchin@allegheny.edu",
        "COMMITS": 1,
        "ADDED": 694,
        "REMOVED": 0,
        "TOTAL": 0,
        "MODIFIED": 0,
        "RATIO": 0,
        "FILES": ["Pipfile", "Pipfile.lock", "UsingPyGithub.py", "lint.sh", "test.sh"],
        "FORMAT": [],
    }
    assert test_dict["noorbuchi"] == expected_dict


def test_get_individual_metrics_populates_keys():
    """Checks that individual_metrics data hass correct keys."""
    test_dict = data_collection.calculate_individual_metrics(
        "individual_metrics_testfile"
    )
    assert "INDIVIDUAL_METRICS" in test_dict.keys()
    expected_keys = [
        "schultzh",
        "WonjoonC",
        "Jordan-A",
        "noorbuchi",
        "Chris Stephenson",
    ]
    internal_keys = list(test_dict["INDIVIDUAL_METRICS"].keys())
    assert internal_keys == expected_keys


@pytest.mark.parametrize(
    "input_lines,input_commits,expected_output", [(50, 50, 1), (1, 1, 1), (0, 0, 0)],
)
def test_get_commit_average(input_lines, input_commits, expected_output):
    """Checks that the function correctly calculates the ratio."""
    assert (
        data_collection.get_commit_average(input_lines, input_commits)
    ) == expected_output
