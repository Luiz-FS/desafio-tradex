from utils.verify_process_area import verify_process_area
from market import settings


def test_create_dirs(mocker):
    # arrange
    mock_isdir = mocker.patch("os.path.isdir", return_value=False)
    mock_mkdirs = mocker.patch("utils.verify_process_area.makedirs")

    # act
    verify_process_area()

    # assert
    mock_isdir.assert_called_with(settings.PROCESS_AREA)
    mock_mkdirs.assert_called_with(settings.PROCESS_AREA)


def test_not_create_dirs(mocker):
    # arrange
    mock_isdir = mocker.patch("os.path.isdir", return_value=True)
    mock_mkdirs = mocker.patch("utils.verify_process_area.makedirs")

    # act
    verify_process_area()

    # assert
    mock_isdir.assert_called_with(settings.PROCESS_AREA)
    mock_mkdirs.assert_not_called()
