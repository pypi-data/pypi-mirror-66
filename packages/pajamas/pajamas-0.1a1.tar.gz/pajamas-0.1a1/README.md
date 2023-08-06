# pajamas

Fancy light clothes for jupyter notebooks to sleep in.

## Motivation

We love [jupyter notebooks](https://jupyter.org): they allow visual, intuitive, and fast data analysis, code testing and development, as well as documentation and sharing of results.

However, when sharing jupyter notebooks via repositories, two drawbacks become painfully apparent:
- jupyter notebooks can get extremely large because they often include all of their output.
- jupyter notebooks change whenever they are being worked with, even without changes to the code.

Of course, the first drawback can be avoided by diligently cleaning the notebook before submitting to the repo, and the second by resetting the file before submitting. In practice, however, we find that this is rarely done consistently.

## Summary

In a nutshell, the pajamas package simply strips the jupyter notebook of its output. Additionally, it provides an output-less format using the `.pajamas` extension, which facilitates working with templates from which jupyter notebooks are created. This enables us to block any `.ipynb` files from being committed to a repository (by including the extension to `.gitignore`), which keeps repositories smaller.

We see jupyter notebooks as a worker having all tools, materials, and results in hand, while the pajamas format retains all of the knowledge and ability (the code) but removes all of the heavy tools, materials, and results (the output contained in the jupyter notebook). Just like the worker would not go to sleep with all of the tools, neither should a jupyter notebook. Both use pajamas.

