#!/usr/bin/env python3

try:
    from sphinxcontrib.napoleon import Config
    from sphinxcontrib.napoleon.docstring import (GoogleDocstring,
                                                  NumpyDocstring)
except ImportError:
    def convert_docstring(docstring):
        return docstring

else:
    CONFIG = Config(napoleon_use_param=True, napoleon_use_rtype=True,
                    napoleon_use_ivar=True,
                    napoleon_include_special_with_doc=True)

    def convert_docstring(docstring):
        if is_google_style(docstring):
            return str(GoogleDocstring(docstring, CONFIG))
        elif is_numpy_style(docstring):
            return str(NumpyDocstring(docstring, CONFIG))
        return docstring

PARAGRAPHS = (
    'Args',
    'Arguments',
    'Attributes',
    'Example',
    'Examples',
    'Keyword Args',
    'Keyword Arguments',
    'Methods',
    'Note',
    'Notes',
    'Other Parameters',
    'Parameters',
    'Return',
    'Returns',
    'Raises',
    'References',
    'See Also',
    'Warning',
    'Warnings',
    'Warns',
    'Yield',
    'Yields'
)


def iter_paragraph_lines(ds_lines):
    for line_no, ds_line in enumerate(ds_lines):
        striped_line = ds_line.strip()
        for paragraph in PARAGRAPHS:
            if striped_line.startswith(paragraph):
                yield line_no, striped_line, paragraph


def is_google_style(docstring):
    ds_lines = docstring.split('\n')
    try:
        line_no, ds_line, paragraph = next(iter_paragraph_lines(ds_lines))
        if ds_line.startswith(paragraph + ':'):
            if len(ds_lines) > line_no + 1:
                return not ds_lines[line_no + 1].strip().startswith('-' * len(paragraph))
            else:
                return True
        else:
            return False
    except StopIteration:
        return False


def is_numpy_style(docstring):
    ds_lines = docstring.split('\n')
    try:
        line_no, ds_line, paragraph = next(iter_paragraph_lines(ds_lines))
        if not ds_line.startswith(paragraph + ':'):
            if len(ds_lines) < line_no + 1:
                return False
            else:
                return ds_lines[line_no + 1].strip().startswith(
                    '-' * len(paragraph))
        else:
            return False
    except StopIteration:
        return False
