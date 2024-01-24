import unittest
from search import (
    keyword_to_titles,
    title_to_info,
    search,
    article_length,
    key_by_author,
    filter_to_author,
    filter_out,
    articles_from_year,
)
from search_tests_helper import (
    get_print,
    print_basic,
    print_advanced,
    print_advanced_option,
)
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main


class TestSearch(unittest.TestCase):
    maxDiff = None

    ##############
    # UNIT TESTS #
    ##############
    def test_keyword_to_title_unit_test(self):
        expected_empty_metadata = {}
        self.assertEqual(keyword_to_titles([]), expected_empty_metadata)
        expected_multiple_keywords = {
            "canadian": ["List of Canadian musicians"],
            "canada": ["List of Canadian musicians"],
            "lee": ["List of Canadian musicians"],
            "white": ["List of Canadian musicians"],
            "smith": ["List of Canadian musicians"],
            "french": ["French pop music"],
            "pop": ["French pop music"],
            "music": ["French pop music", "Noise (music)", "1922 in music"],
            "edogawa": ["Edogawa, Tokyo"],
            "the": ["Edogawa, Tokyo", "1922 in music"],
            "with": ["Edogawa, Tokyo"],
            "noise": ["Noise (music)"],
            "that": ["Noise (music)"],
            "1922": ["1922 in music"],
        }
        self.assertEqual(
            keyword_to_titles(
                [
                    [
                        "List of Canadian musicians",
                        "Jack Johnson",
                        1181623340,
                        21023,
                        ["canadian", "canada", "lee", "white", "smith"],
                    ],
                    [
                        "French pop music",
                        "Mack Johnson",
                        1172208041,
                        5569,
                        ["french", "pop", "music"],
                    ],
                    [
                        "Edogawa, Tokyo",
                        "jack johnson",
                        1222607041,
                        4526,
                        ["edogawa", "the", "with"],
                    ],
                    [
                        "Noise (music)",
                        "jack johnson",
                        1194207604,
                        15641,
                        ["noise", "music", "that"],
                    ],
                    [
                        "1922 in music",
                        "Gary King",
                        1242717698,
                        11576,
                        ["music", "the", "1922"],
                    ],
                ]
            ),
            expected_multiple_keywords,
        )
        expected_keyword_case_sensitive = {
            "music": ["French pop music"],
            "Music": ["List of Canadian musicians"],
        }
        self.assertEqual(
            keyword_to_titles(
                [
                    ["French pop music", "Mack Johnson", 1172208041, 5569, ["music"]],
                    [
                        "List of Canadian musicians",
                        "Jack Johnson",
                        1181623340,
                        21023,
                        ["Music"],
                    ],
                ]
            ),
            expected_keyword_case_sensitive,
        )

    def test_title_to_info_unit_test(self):
        expected_empty_metadata = {}
        self.assertEqual(title_to_info([]), expected_empty_metadata)
        expected_single_title = {
            "List of Canadian musicians": {
                "author": "Jack Johnson",
                "timestamp": 1181623340,
                "length": 21023,
            }
        }
        self.assertEqual(
            title_to_info(
                [
                    [
                        "List of Canadian musicians",
                        "Jack Johnson",
                        1181623340,
                        21023,
                        ["canadian", "canada", "lee", "white", "smith"],
                    ]
                ]
            ),
            expected_single_title,
        )
        expected_multiple_titles = {
            "List of Canadian musicians": {
                "author": "Jack Johnson",
                "timestamp": 1181623340,
                "length": 21023,
            },
            "French pop music": {
                "author": "Mack Johnson",
                "timestamp": 1172208041,
                "length": 5569,
            },
            "Edogawa, Tokyo": {
                "author": "jack johnson",
                "timestamp": 1222607041,
                "length": 4526,
            },
            "Noise (music)": {
                "author": "jack johnson",
                "timestamp": 1194207604,
                "length": 15641,
            },
        }
        self.assertEqual(
            title_to_info(
                [
                    [
                        "List of Canadian musicians",
                        "Jack Johnson",
                        1181623340,
                        21023,
                        ["canadian", "canada", "lee", "white", "smith"],
                    ],
                    [
                        "French pop music",
                        "Mack Johnson",
                        1172208041,
                        5569,
                        ["french", "pop", "music"],
                    ],
                    [
                        "Edogawa, Tokyo",
                        "jack johnson",
                        1222607041,
                        4526,
                        ["edogawa", "the", "with"],
                    ],
                    [
                        "Noise (music)",
                        "jack johnson",
                        1194207604,
                        15641,
                        ["noise", "music", "that"],
                    ],
                ]
            ),
            expected_multiple_titles,
        )

    def test_search_unit_test(self):
        expected_empty_search = []
        self.assertEqual(
            search("", keyword_to_titles(article_metadata())), expected_empty_search
        )
        expected_dance_search = [
            "List of Canadian musicians",
            "2009 in music",
            "Old-time music",
            "1936 in music",
            "Indian classical music",
        ]
        self.assertEqual(
            search("dance", keyword_to_titles(article_metadata())),
            expected_dance_search,
        )
        expected_dance_search_case_sensitive = []
        self.assertEqual(
            search("Dance", keyword_to_titles(article_metadata())),
            expected_dance_search_case_sensitive,
        )

    def test_article_length_unit_test(self):
        empty_article_title = []
        self.assertEqual(
            article_length(
                1000,
                search("", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_article_title,
        )
        invalid_article_length = []
        self.assertEqual(
            article_length(
                -10,
                search("music", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            invalid_article_length,
        )
        regular_article_length_search_music = [
            "Kevin Cadogan",
            "Tim Arnold (musician)",
            "List of gospel musicians",
            "Texture (music)",
        ]
        self.assertEqual(
            article_length(
                5000,
                search("music", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            regular_article_length_search_music,
        )

    def test_key_by_author_unit_test(self):
        empty_article_title = {}
        self.assertEqual(
            key_by_author(
                search("", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_article_title,
        )
        key_by_author_canada = {
            "Jack Johnson": ["List of Canadian musicians"],
            "Burna Boy": ["Lights (musician)", "Will Johnson (soccer)"],
            "Nihonjoe": ["Old-time music"],
        }
        self.assertEqual(
            key_by_author(
                search("canada", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            key_by_author_canada,
        )
        key_by_author_dance = {
            "Jack Johnson": ["List of Canadian musicians"],
            "RussBot": ["2009 in music", "1936 in music"],
            "Nihonjoe": ["Old-time music"],
            "Burna Boy": ["Indian classical music"],
        }
        self.assertEqual(
            key_by_author(
                search("dance", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            key_by_author_dance,
        )

    def test_filter_to_author_unit_test(self):
        empty_article_title = []
        self.assertEqual(
            filter_to_author(
                "Burna boy",
                search("", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_article_title,
        )
        empty_author_name = []
        self.assertEqual(
            filter_to_author(
                "",
                search("pop", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_author_name,
        )
        author_name_not_in_articles = []
        self.assertEqual(
            filter_to_author(
                "Erioluwa",
                search("pop", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            author_name_not_in_articles,
        )
        author_name_in_articles = [
            "Lights (musician)",
            "Indian classical music",
            "Tony Kaye (musician)",
            "2008 in music",
        ]
        self.assertEqual(
            filter_to_author(
                "Burna Boy",
                search("music", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            author_name_in_articles,
        )

    def test_filter_out_unit_test(self):
        empty_article_title = []
        self.assertEqual(
            filter_out(
                "music",
                search("", keyword_to_titles(article_metadata())),
                keyword_to_titles(article_metadata()),
            ),
            empty_article_title,
        )
        empty_extra_keyword_soccer = [
            "Spain national beach soccer team",
            "Will Johnson (soccer)",
            "Steven Cohen (soccer)",
        ]
        self.assertEqual(
            filter_out(
                "",
                search("soccer", keyword_to_titles(article_metadata())),
                keyword_to_titles(article_metadata()),
            ),
            empty_extra_keyword_soccer,
        )
        filter_out_dance_music_initial_search = [
            "French pop music",
            "Noise (music)",
            "1922 in music",
            "1986 in music",
            "Kevin Cadogan",
            "Rock music",
            "Lights (musician)",
            "Tim Arnold (musician)",
            "Arabic music",
            "Joe Becker (musician)",
            "Richard Wright (musician)",
            "Voice classification in non-classical music",
            "1962 in country music",
            "List of dystopian music, TV programs, and games",
            "Steve Perry (musician)",
            "David Gray (musician)",
            "Alex Turner (musician)",
            "List of gospel musicians",
            "1996 in music",
            "Traditional Thai musical instruments",
            "2006 in music",
            "Tony Kaye (musician)",
            "Texture (music)",
            "2007 in music",
            "2008 in music",
        ]
        self.assertEqual(
            filter_out(
                "dance",
                search("music", keyword_to_titles(article_metadata())),
                keyword_to_titles(article_metadata()),
            ),
            filter_out_dance_music_initial_search,
        )

    def test_articles_from_year_unit_test(self):
        empty_article_title = []
        self.assertEqual(
            articles_from_year(
                2009,
                search("", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_article_title,
        )
        empty_article_year = []
        self.assertEqual(
            articles_from_year(
                "",
                search("music", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            empty_article_year,
        )
        article_from_year_2009_music = [
            "1922 in music",
            "2009 in music",
            "Rock music",
            "1936 in music",
            "1962 in country music",
            "Steve Perry (musician)",
        ]
        self.assertEqual(
            articles_from_year(
                2009,
                search("music", keyword_to_titles(article_metadata())),
                title_to_info(article_metadata()),
            ),
            article_from_year_2009_music,
        )

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch("builtins.input")
    def test_basic_search_integration_test(self, input_mock):
        keyword = "Canada"
        advanced_option = 6
        advanced_response = ""

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = (
            print_basic()
            + keyword
            + "\n"
            + print_advanced()
            + str(advanced_option)
            + "\n\nNo articles found\n"
        )

        self.assertEqual(output, expected)

    @patch("builtins.input")
    def test_article_length_integration_test(self, input_mock):
        keyword = "music"
        advanced_option = 1
        advanced_response = 5100

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = (
            print_basic()
            + keyword
            + "\n"
            + print_advanced()
            + str(advanced_option)
            + "\n"
            + print_advanced_option(advanced_option)
            + str(advanced_response)
            + "\n\nHere are your articles: ['Kevin Cadogan', 'Tim Arnold (musician)', 'List of gospel musicians', 'Texture (music)']\n"
        )

        self.assertEqual(output, expected)

    @patch("builtins.input")
    def test_key_by_author_integration_test(self, input_mock):
        keyword = "dance"
        advanced_option = 2
        advanced_response = ""

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = (
            print_basic()
            + keyword
            + "\n"
            + print_advanced()
            + str(advanced_option)
            + "\n\nHere are your articles: {'Jack Johnson': ['List of Canadian musicians'], 'RussBot': ['2009 in music', '1936 in music'], 'Nihonjoe': ['Old-time music'], 'Burna Boy': ['Indian classical music']}\n"
        )

        self.assertEqual(output, expected)

    @patch("builtins.input")
    def test_filter_to_author_integration_test(self, input_mock):
        keyword = "pop"
        advanced_option = 3
        advanced_response = "Mack Johnson"

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = (
            print_basic()
            + keyword
            + "\n"
            + print_advanced()
            + str(advanced_option)
            + "\n"
            + print_advanced_option(advanced_option)
            + str(advanced_response)
            + "\n\nHere are your articles: ['French pop music', 'Rock music']\n"
        )

        self.assertEqual(output, expected)

    @patch("builtins.input")
    def test_filter_out_integration_test(self, input_mock):
        keyword = "dance"
        advanced_option = 4
        advanced_response = "pop"

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = (
            print_basic()
            + keyword
            + "\n"
            + print_advanced()
            + str(advanced_option)
            + "\n"
            + print_advanced_option(advanced_option)
            + str(advanced_response)
            + "\n\nHere are your articles: ['Old-time music', '1936 in music', 'Indian classical music']\n"
        )

        self.assertEqual(output, expected)


# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
