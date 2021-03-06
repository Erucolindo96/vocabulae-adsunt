from typing import List
import re
import morfeusz2

class TextPreprocessing:

    @staticmethod
    def remove_stopwords(words: List[str]):
        pass

    @staticmethod
    def to_lemmas(words: List[str]) -> List[str]:

        w_str = " ".join(words)
        morf = morfeusz2.Morfeusz()  # (praet='composite')
        analysis = []
        analysis = morf.analyse(words)

        # for word in words:
        #     analysis.append(morf.analyse(word))
        # # analysis = morf.analyse(words)

        prev = None
        result = []

        for i, j, (orth, base, tag, posp, kwal) in analysis:
            if i == prev:
                continue
            prev = i
            if i > 0:
                if i + 1 == i:
                    continue
            if ':' in base:
                result.append(re.findall('(.*):', base)[0])
            else:
                result.append(base)
        return result

    @staticmethod
    def remove_author_and_title(text):
        line = 0
        idx_to_remove = 0
        for idx, char in enumerate(text[:1000]):
            if char == '\n':
                line += 1
            if line == 4 and char == '\n':
                idx_to_remove = idx
        return text[idx_to_remove:]

    @staticmethod
    def only_normal_e(string_or_list: List[str]) -> List[str]:
        return ['e' if char == 'é' else char for char in string_or_list]
