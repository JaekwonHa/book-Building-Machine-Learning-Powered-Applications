import argparse
import nltk
import pyphen


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="수정할 텍스트를 입력합니다"
    )
    parser.add_argument(
        'text',
        metavar='input text',
        type=str
    )
    args = parser.parse_args()
    return args.text


def clean_input(text):
    """

    :param text:
    :return: ASCII 이외의 문자를 제거한 정제된 텍스트
    """
    return str(text.encode().decode('ascii', errors='ignore'))


def preprocess_input(text):
    sentences = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    return tokens


def count_words_per_sentence(sentence_tokens):
    punctuation = ".,!?/"
    return len([word for word in  sentence_tokens if word not in  punctuation])

def count_total_words(sentence_list):
    return sum(
        [count_words_per_sentence(sentence) for sentence in sentence_list]
    )

def count_word_usage(tokens, word_list):
    """
    주어진 단어 리스트의 등장 횟수
    :param sentence_list:
    :return:
    """
    return len([word for word in tokens if word.lower() in word_list])


def compute_total_unique_words_fraction(sentence_list):
    """
    고유한 단어의 비율을 계산합니다.
    :param sentence_list:
    :return:
    """
    all_words = [word for word_list in sentence_list for word in word_list]
    unique_words = set(all_words)
    return len(unique_words) / len(all_words)


def compute_average_word_length(tokens):
    """
    한 문장에 있는 단어의 길이를 계산합니다
    :param tokens:
    :return:
    """
    word_lengths = [len(word) for word in tokens]
    return sum(word_lengths) / len(word_lengths)


def compute_total_average_word_length(sentence_list):
    """
    여러 문장에 대해 단어의 평균 길이를 계산합니다
    :param sentence_list:
    :return:
    """
    lengths = [compute_average_word_length(tokens) for tokens in sentence_list]
    return sum(lengths) / len(lengths)


def get_reading_level_from_flesch(flesch_score):
    """
    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests 에서 가져온 임곗값
    :param flesch_score:
    :return: 플레시 점수에 대한 가독성 수준
    """
    if flesch_score < 30:
        return "매우 읽기 어려움"
    elif flesch_score < 50:
        return "읽기 어려움"
    elif flesch_score < 60:
        return "약간 읽기 어려움"
    elif flesch_score < 70:
        return "보통"
    elif flesch_score < 80:
        return "약간 읽기 쉬움"
    elif flesch_score < 90:
        return "읽기 쉬움"
    else:
        return "매우 읽기 쉬움"


def compute_flesch_reading_ease(total_syllables, total_words, total_sentences):
    """
    요약 통계로부터 가독성 점수를 계산합니다.
    :param total_syllables:
    :param total_words:
    :param total_sentences:
    :return:
    """
    return (
        206.85 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
    )


def count_word_syllables(word):
    """
    단어에 있는 음절 횟수
    :param word:
    :return:
    """
    dic = pyphen.Pyphen(lang="en_US")
    # 음절 사이에 하이픈을 추가한 단어를 반환합니다
    hyphenated = dic.inserted(word)
    return len(hyphenated.split("-"))


def count_sentence_syllables(tokens):
    """
    문장에 있는 음절 개수를 셉니다
    :param tokens:
    :return:
    """
    # 토큰화 객체는 구둣점을 별도의 단어로 인식하기 때문에 여기서는 이를 필터링합니다
    punctuation = ".,!?/"
    return sum(
        [
            count_word_syllables(word)
            for word in tokens
            if word not in punctuation
        ]
    )


def count_total_syllables(sentence_list):
    """
    문장 리스트에 있는 음절을 셉니다.
    :param sentence_list:
    :return:
    """
    return sum(
        [count_sentence_syllables(sentence) for sentence in sentence_list]
    )


def get_suggestions(sentence_list):
    told_said_usage = sum(
        (count_word_usage(tokens, ["told", "said"]) for tokens in sentence_list)
    )
    but_and_usage = sum(
        (count_word_usage(tokens, ["but", "and"]) for tokens in sentence_list)
    )
    wh_adverbs_usage = sum(
        (count_word_usage(
            tokens,
            [
                "when",
                "where",
                "why",
                "whence",
                "whereby",
                "wherein",
                "whereupon"
            ]
        )
        for tokens in sentence_list
        )
    )
    result_str = ""
    adverb_usage = "단어 사용량: %s told/said, %s but/and, %s wh- 접속사" % (
        told_said_usage,
        but_and_usage,
        wh_adverbs_usage
    )
    result_str += adverb_usage
    average_word_length = compute_total_average_word_length(sentence_list)
    unique_words_fraction = compute_total_unique_words_fraction(sentence_list)

    word_stats = "단어의 평균 길이 %.2f, 고유한 단어의 비율 %.2f" % (
        average_word_length,
        unique_words_fraction
    )
    # 나중에 웹 애플리케이션으로 출력하기 위해 HTML <br> 태그를 추가합니다.
    result_str += "<br/>"
    result_str += word_stats

    number_of_syllables = count_total_syllables(sentence_list)
    number_of_words = count_total_words(sentence_list)
    number_of_sentences = len(sentence_list)

    syllable_counts = "%d개 음절, %d개 단어, %d개 문장" % (
        number_of_syllables,
        number_of_words,
        number_of_sentences,
    )
    result_str += "<br/>"
    result_str += syllable_counts

    flesch_score = compute_flesch_reading_ease(
        number_of_syllables, number_of_words, number_of_sentences
    )

    flesch = "플레시 점수 %.2f: %s" % (
        flesch_score,
        get_reading_level_from_flesch(flesch_score)
    )

    result_str += "<br/>"
    result_str += flesch

    return result_str


input_text = parse_arguments()
processed = clean_input(input_text)
tokenized_sentences = preprocess_input(processed)
suggestions = get_suggestions(tokenized_sentences)


print(suggestions)
