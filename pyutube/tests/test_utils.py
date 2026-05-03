import pytest

from pyutube.utils import is_youtube_link, is_youtube_video


@pytest.mark.parametrize("link, expected_result, test_id", [
    # Happy path tests
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_standard"),
    ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_http"),
    ("https://youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_www"),
    ("https://youtu.be/dQw4w9WgXcQ", True, "happy_short"),
    ("www.youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_protocol"),
    ("youtube.com/watch?v=dQw4w9WgXcQ", True, "happy_no_protocol_www"),
    ("youtu.be/dQw4w9WgXcQ", True, "happy_short_no_protocol"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=100s",
     True, "happy_starts_at_100s"),

    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_standard"),
    ("https://youtu.be/dQw4w9WgXcQ", True, "video_id_short"),
    ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_http"),
    ("www.youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_no_protocol"),
    ("youtube.com/watch?v=dQw4w9WgXcQ", True, "video_id_no_subdomain"),
    ("https://www.youtube.com/embed/dQw4w9WgXcQ", True, "video_embed_standard"),
    ("https://www.youtube.com/v/dQw4w9WgXcQ", True, "video_v_standard"),

    # Edge cases
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be",
     True, "edge_with_params"),
    ("", False, "edge_empty_string"),
    ("https://www.youtube.com/watch?v=", False, "edge_no_video_id"),
    ("https://www.youtu.be/", False, "edge_short_no_video_id"),
    ("https://www.youtube.com/watch?", False, "edge_no_query_string"),

    ("", False, "empty_string"),
    ("https://www.youtube.com/watch?v=", False, "video_id_empty"),
    # ("https://www.youtube.com/playlist?list=", False, "playlist_id_empty"),
    ("https://www.youtu.be/", False, "short_domain_no_id"),
    ("https://youtube.com/watch?v=dQw4w9WgXcQ&feature=share",
     True, "video_id_with_query"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "video_and_playlist"),

    # Error cases
    ("https://www.notyoutube.com/watch?v=dQw4w9WgXcQ", False, "error_wrong_domain"),
    ("https://www.youtube.com/watchv=dQw4w9WgXcQ",
     False, "error_missing_question_mark"),
    ("https://youtu.be/dQw4w9WgXcQextra", True, "error_extra_characters"),
    ("https://www.youtube.com/watch?time_continue=1&v=dQw4w9WgXcQ",
     False, "error_unexpected_params"),

    ("https://example.com/watch?v=dQw4w9WgXcQ", False, "non_youtube_domain"),
    ("https://www.youtube.com/watchv=dQw4w9WgXcQ", False, "typo_in_query"),
    ("https://youtu.be/dQw4w9WgXcQ?list=PLA7no0L9zTk4Qp6LlDjFVCetW-sFw9r5I",
     True, "short_link_with_playlist"),
    ("https://www.youtub.com/watch?v=dQw4w9WgXcQ", False, "typo_in_domain"),
    ("https://www.youtube.com/watch?feature=share&v=dQw4w9WgXcQ",
     True, "video_id_with_other_query_first"),

])
def test_is_youtube_link(link, expected_result, test_id):
    # Act
    result = is_youtube_video(link)

    # Assert
    assert result == expected_result, f"Test failed for test_id: {test_id}"


@pytest.mark.parametrize("link, expected_result", [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     (True, "video")),
    ("https://youtu.be/dQw4w9WgXcQ", (True, "video")),
    # ("https://www.youtube.com/playlist?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
    #  (True, "playlist")),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ",
     (True, "short")),


    ("", (False, "unknown")),
    ("https://www.youtube.com/", (False, "unknown")),
    ("https://www.youtube.com/watch?v=", (False, "unknown")),
    ("https://www.youtu.be/", (False, "unknown")),
    ("https://www.youtube.com/playlist?list=",
     (False, "unknown")),
    ("https://www.youtube.com/shorts/", (False, "unknown")),


    ("https://www.google.com", (False, "unknown")),
    ("https://www.youtube.com/watch?list=dQw4w9WgXcQ",
     (False, "unknown")),
    ("https://www.youtu.be/dQw4w9WgXcQ?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
     (True, "video")),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ?list=PLynG8gQD-n8BMplEGyFBRVJFssMFo5x07",
     (True, "short")),
])
def test_is_youtube_link_error_cases(link, expected_result):
    # Act
    result = is_youtube_link(link)

    # Assert
    assert result == expected_result
