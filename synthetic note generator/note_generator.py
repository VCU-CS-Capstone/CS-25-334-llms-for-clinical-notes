from pprint import pprint
import json
from note import ConsultNote


def main():
    total_results = []
    num_notes = 1
    for _ in range(0, num_notes):
        current_note = ConsultNote()
        total_results.append({'text': current_note.get_text(), 'data': current_note.get_data_fields()})

    pprint(total_results)
    with open('training.json', 'w') as f:
        json.dump(total_results, f, indent=4)


if __name__ == '__main__':
    main()
