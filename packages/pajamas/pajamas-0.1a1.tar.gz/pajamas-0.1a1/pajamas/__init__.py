import json

class get_changed:
    def __init__(self):
        self._version = 0.1
        self._pajamas = {"cells": []}
        self._switch_mode = '\n"""#\n'
        self._newline = "\n###-\n"
        self._hideline = "###X"

    def read_py(self, filename):
        with open(filename, "r") as f:
            raw = f.read()
        
        raw_lines = raw.split("\n")        
        header = raw_lines[0]
        body="\n".join(raw_lines[1:])

        cm_split = body.split(self._switch_mode)
        current_type = "code"
        if cm_split[0] == "":
            current_type = "markdown"
            cm_split = cm_split[1:]
        else:
            if cm_split[0].startswith(self._newline):
                cm_split[0] = cm_split[0][len(self._newline) :]
        if cm_split[-1] == "":
            if (current_type == "markdown" and len(cm_split) % 2 == 0) or (
                current_type == "code" and len(cm_split) % 2 == 1
            ):
                cm_split = cm_split[:-1]
        for cm_block in cm_split:
            self._read_cm_block(cm_block, current_type)
            current_type = "markdown" if current_type == "code" else "code"

    def _read_cm_block(self, cm_block, block_type):
        if block_type == "markdown":
            for cell in cm_block.split(self._newline):
                this_cell = {"cell_type": block_type, "source": cell.splitlines(True)}
                self._pajamas["cells"].append(this_cell)

        if block_type == "code":
            for cell in cm_block.split(self._newline):
                this_cell = {"cell_type": block_type, "source": []}
                for src_line in cell.splitlines(True):
                    if src_line[0 : len(self._hideline)] == self._hideline:
                        this_cell["source"].append(src_line[len(self._hideline) :])
                    else:
                        this_cell["source"].append(src_line)
                self._pajamas["cells"].append(this_cell)

    def read_ipynb(self, filename):
        with open(filename, "r") as f:
            raw = json.loads(f.read())
        for cell in raw["cells"]:
            this_cell = {}
            if (cell["cell_type"] == "markdown") or (cell["cell_type"] == "raw"):
                this_cell["cell_type"] = "markdown"
            else:
                if cell["cell_type"] == "code":
                    this_cell["cell_type"] = "code"
                else:
                    print("ERROR")

            this_cell["source"] = cell["source"]
            self._pajamas["cells"].append(this_cell)

    def read_pajamas(self, filename):
        with open(filename, "r") as f:
            self._pajamas = json.loads(f.read())

    def write_ipynb(self, filename):
        cell_stuff = self._get_cell_stuff()
        ipynb_output = self._get_empty_notebook()
        for cell in self._pajamas["cells"]:
            new_cell = {}
            new_cell["cell_type"] = cell["cell_type"]
            new_cell.update(cell_stuff[cell["cell_type"]])
            new_cell["source"] = cell["source"]
            ipynb_output["cells"].append(new_cell)
        with open(filename, "w") as f:
            json.dump(ipynb_output, f, indent=1)

    def write_py(self, filename):
        py_source = ""
        current_type = "code"
        for cell in self._pajamas["cells"]:
            if current_type == cell["cell_type"]:
                py_source += self._newline
            else:
                current_type = cell["cell_type"]
                py_source += self._switch_mode
            if current_type == "code":
                for src_line in cell["source"]:
                    if src_line[0] == "%":
                        py_source += self._hideline + src_line
                    else:
                        py_source += src_line
            else:
                py_source += "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            py_source += self._switch_mode
        with open(filename, "w") as f:
            f.write(py_source)

    def write_pajamas(self, filename):
        with open(filename, "w") as f:
            json.dump(self._pajamas, f, indent=1)

    def _get_cell_stuff(self):
        cell_stuff = {
            "code": {"execution_count": None, "metadata": {}, "outputs": []},
            "markdown": {"metadata": {}},
        }
        return cell_stuff

    def _get_empty_notebook(self):
        empty_notebook = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.7.6",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }
        return empty_notebook

    def __str__(self):
        return json.dumps(self._pajamas, indent=4)