def column_printer(sheet, column):
    for i in range(1, sheet.max_row+1):
        cell = sheet[f'{column}{i}']
        print(f'{column}{i} {cell.value}')


def tax_calculator(subtotal, taxrate):
    tax= round((subtotal*taxrate),2)
    total = subtotal + tax
    return subtotal, tax, total


