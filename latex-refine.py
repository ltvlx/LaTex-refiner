import codecs
from pathlib import Path


def __get_ref_list(tex_proj_root):
    """
    Finds all bibliography files in 'tex_proj_root' directory.
    Extracts all references from these bibliography files.
    """
    references = {}
    for fpath in tex_proj_root.glob('*.bib'):
        with codecs.open(fpath, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line.find('@') == 0:
                    k = line.find('{')
                    l = line.find(',')
                    ref_type = line[:k]
                    ref_name = line[k+1:l]
                    references[ref_name] = {'type': ref_type, 'count': 0}
    
    return references


def __count_reference_use(tex_proj_root, references):
    """
    Finds all .tex files and then calculates the occurence of each reference 
    from 'references' dictionary in these tex files.
    """
    for fpath in tex_proj_root.glob('*.tex'):
        with codecs.open(fpath, 'r',encoding='utf-8') as fin:
            doc = fin.read()
            for ref_name in references:
                references[ref_name]['count'] = doc.count(ref_name)
    
    return references


def analyse_references_usage(tex_proj_root):
    """
    Finds references in the .bib files at the root directory
    Counts their number of appearance in .tex files
    Prints out the unused references
    """
    references = __get_ref_list(tex_proj_root)
    references = __count_reference_use(tex_proj_root, references)

    print("Unused references from .bib file:")
    i = 1
    for key in references:
        if references[key]['count'] == 0:
            print("%2d, %8s: %25s, %2d"%(i, references[key]['type'], key, references[key]['count']))
            i += 1
    print()



def __find_figures(tex_proj_root, figure_formats=['.pdf', '.png']):
    """
    Finds all figures in 'tex_proj_root' directory.
    """
    figures = {}

    for _path in tex_proj_root.rglob('*'):
        if _path.is_file() and _path.suffix in figure_formats:
            # This can be used without parts, but the path will have slash or backslash, dependion on the OS used
            # In .tex files I usually use common slash (/), while the standard for Win paths is blackslash (\)
            # figpath = _path.relative_to(tex_proj_root)
            figpath = "/".join(_path.relative_to(tex_proj_root).parts)
            figures[figpath] = 0
    
    return figures


def __count_figures_use(tex_proj_root, figures):
    """
    Finds all .tex files and then calculates the occurence of each figure 
    from 'figures' dictionary in these tex files.
    """
    for fpath in tex_proj_root.glob('*.tex'):
        with codecs.open(fpath, 'r',encoding='utf-8') as fin:
            doc = fin.read()
            for ref_name in figures:
                figures[ref_name] += doc.count(ref_name)
    
    return figures


def analyse_figures_usage(tex_proj_root):
    """
    Recursively finds all figures (.pdf and .png files), starting from the root directory
    Counts the number of appearance of these figures in .tex files
    Prints out the unused figures
    """
    figures = __find_figures(tex_proj_root)
    figures = __count_figures_use(tex_proj_root, figures)

    print("Unused figures:")
    i = 1
    for x, v in figures.items():
        if v == 0:
            print(x, v)
            i += 1
    print()



# Path to a Latex project
tex_proj_root = Path("C:\\Users\\ltvlx\\Documents\\GitHub\\PNAS-manuscript")

if tex_proj_root.exists():
    analyse_references_usage(tex_proj_root)
    analyse_figures_usage(tex_proj_root)
else:
    print("The given path does not exist!")
