import aterm

"""
handle annonymous classes
"""

@aterm.transformation
def fix_annonclass(ast):
    for ni in ast.findall('NewInstance'):
        parents = [p for p in ni.parents()]
        print parents
        
        import sys
        sys.exit()
        
    return ast

    
def run(ast):
    return fix_annonclass(ast)

    
    
