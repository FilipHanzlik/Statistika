

def validate_form_input(dict):

    # define the result variable (it will be a dict of dicts)
    result = {}
    passed = True  # This variable stores if the test passed

    # test Výška
    try:
        vyska = int(dict['vyska'])
        if vyska <= 220 and vyska >= 50:
            result['vyska'] = 'validate valid'
        else:
            result['vyska'] = 'validate invalid'
            passed = False
    except ValueError:
        result['vyska'] = 'validate invalid'
        passed = False

    # test pro délku spánku
    try:
        delka_spanku = float(dict['delka-spanku'])
        if delka_spanku < 2 or delka_spanku > 20:
            result['delka_spanku'] = 'validate invalid'
            passed = False
        else:
            result['delka_spanku'] = 'validate valid'
    except ValueError:
        result['delka_spanku'] = 'validate invalid'
        passed = False

    # test pro cas vstávaní
    cas_vstavani = dict['cas-vstavani']
    if not isinstance(cas_vstavani, str):
        result['cas_vstavani'] = 'validate invalid'
        passed = False
    else:
        casti = cas_vstavani.split(':')
        if len(casti) == 2 and len(casti[0]) == 2 and len(casti[1]) == 2:
            try:
                if int(casti[0]) > 23:
                    passed = False
                    result['cas_vstavani'] = 'validate invalid'
                elif int(casti[1]) > 59:
                    passed = False
                    result['cas_vstavani'] = 'validate invalid'
                else:
                    result['cas_vstavani'] = 'validate valid'
            except ValueError:
                passed = False
                result['cas_vstavani'] = 'validate invalid'
        else:
            passed = False
            result['cas_vstavani'] = 'validate invalid'

    # test času na sociálních sítích
    try:
        cas_na_soc = float(dict['socialni-site'])
        if cas_na_soc < 20:
            result['socialni_site'] = 'validate valid'
        else:
            result['socialni_site'] = 'validate valid'
    except ValueError:
        result['socialni_site'] = 'validate invalid'
        passed = False

    print(result)
    return (passed, result)


