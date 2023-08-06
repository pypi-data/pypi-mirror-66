from boo import available_years, file_length_mb


def test_rosstat_files_are_available_and_big_in_size():
    for year in available_years():
        assert file_length_mb(year) > 500
