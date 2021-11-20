def convert_brl(val: str) -> float:
        value=0
        neg = bool('-' in val)
        _val= list(val.strip().replace('- ','').replace('-',''))
        comma = ',' in _val and _val.index(',') 
        point = '.' in _val and _val.index('.')

        if comma:
            _val[comma] = '.'
        if point:
            _val[point] = ''
        _val = ''.join(_val)
        try:
            value = float(_val[(3 if 'R$' in _val else 0):].strip().replace(',','.'))
            value = (-value if neg else value )
        except ValueError as e:
            raise ValueError(f'Não foi possível converter \'{_val}\' para float')
        return value