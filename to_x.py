from fields import NUMBER, CATEGORICAL, CATEGORICAL_MULTI

def force_float(value):
    try:
        return float(value)
    except:
        return -1

def to_x(row_dict:dict, index_to_field:dict[int, str], fields_classes:dict[str, list]):
    X = []
    for row in row_dict:
        new_row = []
        for table, fields in NUMBER.items():
            for field in fields:
                index_to_field[len(new_row)] = field
                new_row.append(force_float(row[field]))

        for table, fields in CATEGORICAL.items():
            for field in fields:
                for i in range(len(fields_classes[field])):
                    index_to_field[len(new_row)+i] = field
                new_row.extend([1 if row[field] == _class else 0
                                for _class in fields_classes[field]])
        
        for table, fields in CATEGORICAL_MULTI.items():
            for field in fields:
                for i in range(len(fields_classes[field])):
                    index_to_field[len(new_row)+i] = field
                # row[field] is a list of classes that the object belongs to
                new_row.extend([1 if _class in row[field] else 0
                                for _class in fields_classes[field]])
        X.append(new_row)

    return X