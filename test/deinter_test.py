import numpy as np

test_data_out = ""
test_data_out_ecc = ""
test_data = "AJS1BKT2CLU3DMV4ENW5FOX6GPY7HQZ8IR09agmsbhntcioudjpvekqwflrx"

for i in test_data:
    test_data_out += i + ", "
    test_data_out += i + ", "
    test_data_out += i + ", "
    test_data_out += i + ", "

array_data = np.array(test_data_out[:-2].split(", "))

raw = np.concatenate([np.reshape(array_data, (-1, 4))[i::4][:9] for i in range(4)], axis=None)
ecc = np.concatenate([np.reshape(array_data, (-1, 4))[i::4][9:] for i in range(4)], axis=None)

print(raw)
print(ecc)
