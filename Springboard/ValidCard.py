def card_valid(card):
    card_no = []
    last_digit = ''
    j = 0
    for i in range(len(card)):
        if card[i].isnumeric():
            card_no.append(card[i])
        else:
            if card[i] != '-':
                return False, 'unexpected character" "{}"'.format(card[i])
    if '-' in card:
        part_card = card.split('-')
        for item in part_card:
            if len(item) != 4:
                return False, 'each section must have 4 digits, but section "{}" has {} digits'.format(item, len(item))
    if len(card_no) != 16:
        return False
    if card[0] not in ['4', '5', '6']:
        return False, 'first digit must be either 4, 5 or 6, but it is {}.'.format(card[0])
    for d in card_no:
        if d == last_digit:
            j += 1
            if j == 3:
                return False, '"{}" is repeated 4 times'.format(d)
        else:
            j = 0
            last_digit = d
    return True


card_list = ['4123456789123456', '123-4567-8912-3456', '61234-567-8912-3456', '4123356789123456', '5133-3367-8912-3456', '5123 - 3567 - 8912 - 3456']
for n in card_list:
    print(card_valid(n))
