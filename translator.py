import translators as ts
import json
import argparse


def translator(input_file, lang):
    with open(input_file, 'r') as _file:
        labels = json.loads(_file.read())
    final_labels = translate(labels, lang)
    print(final_labels)
    output = f'translateds/{input_file.split(".")[0]}_translated_{lang}.json'
    with open(output, "w") as final_labels_file:
        final_labels_file.write(json.dumps(final_labels, indent=4,
                                           ensure_ascii=False))


def translate(_dict, _lang):
    _labels = {}
    for k, v in _dict.items():
        if isinstance(v, str):
            entry = ts.translate_html(v, translator=ts.google, to_language=_lang,
                                      translator_params={})
            _labels.update({k: entry})
        elif isinstance(v, dict):
            _entry = {}
            for key, val in v.items():
                if isinstance(val, str):
                    entry = ts.translate_html(val, translator=ts.google,
                                              to_language=_lang,
                                              translator_params={})
                    _entry.update({key: entry})
                else:
                    # must run separated
                    _entry = {key: val}
            _labels.update({k: _entry})
    return _labels


parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', required=True, type=str, help='Name of json file with sentences.')
parser.add_argument('--lang', '-lg', required=True, type=str, help='Language will be translated.')
args = parser.parse_args()


if __name__ == '__main__':
    # Only sub level of dict is permitted
    in_file = args.file
    lang = args.lang
    print(f"Translating....{in_file}")
    translator(in_file, lang)
