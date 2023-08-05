import json
from typing import List, Tuple

from tokenizer_tools.conllz.sentence import SentenceX


def read_conllx_from_string(conllx_string):
    # default is -1 for there always +1 for block which is not right for start block
    last_block_line_num = -1

    raw_sentence_list = conllx_string.split("\n\n")

    for raw_sentence in raw_sentence_list:
        # +1 for there is a empty line between block
        last_block_line_num += 1

        cleaned_sentence = raw_sentence.strip()

        if not cleaned_sentence:
            # skip
            continue

        sentence = SentenceX()
        raw_line_list = raw_sentence.split("\n")
        for index, raw_line in enumerate(raw_line_list):
            if index == 0:
                meta_string = raw_line.strip("#\t\n ")
                try:
                    meta_data = json.loads(meta_string)
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(
                        "Head line JSON parsing failed at line {}: {}".format(
                            last_block_line_num + index + 1, e
                        )
                    )

                sentence.id = meta_data.pop("id")
                sentence.meta = meta_data

                continue  # read id is done

            # line = raw_line.strip()
            item = raw_line.split("\t")

            if not raw_line or not item:
                # skip
                continue

            sentence.write_as_row(item)

        # +1 for index start from 0
        last_block_line_num += index + 1

        yield sentence


def yield_block(conllx_string: str) -> List[Tuple[int, str]]:
    lines = conllx_string.splitlines()

    block = []
    for line_num, line_str in enumerate(lines, start=1):
        if not line_str:  # empty line
            yield block

            # reset
            block = []

            # skip this line
            continue

        block.append((line_num, line_str))

    # last block
    if block:
        yield block


# TODO: this func will be used to replace read_conllx_from_string
# but need careful test
def load_conllx(conllx_string: str) -> List[SentenceX]:
    blocks = yield_block(conllx_string)
    return [parse_lines_to_sentence(block) for block in blocks]


def parse_lines_to_sentence(raw_line_list: List[Tuple[int, str]]) -> SentenceX:
    sentence = SentenceX()
    for index, (line_num, raw_line) in enumerate(raw_line_list):
        if index == 0:
            meta_string = raw_line.strip("#\t\n ")
            try:
                meta_data = json.loads(meta_string)
            except json.decoder.JSONDecodeError as e:
                raise ValueError("{}. At line {}: {}".format(e, line_num, raw_line))

            sentence.id = meta_data.pop("id")
            sentence.meta = meta_data

            continue  # read head is done

        # line = raw_line.strip()
        item = raw_line.split("\t")

        if not raw_line or not item:
            # skip
            continue

        sentence.write_as_row(item)

    return sentence


def read_conllx(input_fd):
    sentence_list = []

    content = input_fd.read()

    for sentence in read_conllx_from_string(content):
        sentence_list.append(sentence)

    return sentence_list
