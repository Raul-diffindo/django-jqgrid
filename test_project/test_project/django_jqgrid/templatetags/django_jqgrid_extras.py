from django import template
register = template.Library()

@register.filter("adjust_jqgrid_colmodel")
def adjust_jqgrid_colmodel(colmodel_line):
    STRINGS_TO_REPLACE = ["'index'", "'name'", "'search'", "'align'", "'editable'", "'width'",
                          "'searchoptions'", "'sopt'", "'key'", "'editoptions'", "'editrules'", "'edittype'",
                          "'formoptions'", "'formatoptions'", "'formatter'", "'label'", "'sortable'", "'sorttype'",
                          "'title'", "''", "'viewable'", "'stype'", "'surl'", "'false'", "'true'",
                          ]

    for option in STRINGS_TO_REPLACE:
        colmodel_line = str(colmodel_line).replace(option, option.replace("'",""))

    return colmodel_line
