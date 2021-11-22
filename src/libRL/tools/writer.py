import csv
import itertools


def reflection_loss(data, filepath):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        f.write("".join((",", *(str(i) for i in data["d"]), "\n")))
        writer.writerows(zip(data["f"], *data["RL"]))


def characterization(data, filepath):
    keys = list(data.keys())
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        writer.writerows(zip(*(iter(data[i]) for i in keys)))


def band_analysis(d_set, data, filepath):
    m_set = data.keys()
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(itertools.chain("d", m_set))
        writer.writerows(
            ((d, *(data.get(m, {}).get(d, 0) for m in m_set)) for d in d_set)
        )
