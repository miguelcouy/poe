import pandas as pd



class Usinas:
    
    def ConcatenarDados(auxDf):
        return

    def Filtrar(df, **kwargs):
        '''
        kwargs:
        \n
        - codUsina [int or list of int]: Filter dataframe column 'CodUsina'
        by values contained.\n
        If zero, returns with no filter.\n
        \t>> Usinas().Filtrar(codUsina = 1)\n
        \t>> Usinas().Filtrar(codUsina = [1, 2, 4])\n
        \n
        - nameUsina [str or list of str]: Filter dataframe column 'Usina' 
        by values contained.\n
        \t>> Usinas().Filtrar(nameUsina = 'CAMARGOS')]\n
        \t>> Usinas().Filtrar(nameUsina = ['CAMARGOS', 'ITUTINGA', 'FUNIL-GRANDE'])]\n
        \n
        - subSistema [str or list of str]: Filter dataframe column 'Sistema' 
        by values contained.\n
        Expected values: '1 - Sudeste', '2 - Sul', '3 - Nordeste' and '4 - Nordeste'\n
        \t>> Usinas().Filtrar(subSistema = '1 - Sudeste')\n
        \t>> Usinas().Filtrar(subSistema = ['3 - Nordeste', '4 - Norte'])\n
        \n
        - tipoReservatorio [str or list of str]: Filter dataframe column 'Reg'
        by values contained.\n
        Expected values: 'D', 'S', 'M'\n
        \t- D -> Hydraulic power plant without reservatory (fio d'água).\n
        \t- S -> Itaipu power plant, special reservatory.\n
        \t- M -> Hydraulic power plant with reservatory.
        \t>> Usinas().Filtrar(tipoReservatorio = ['D','S'])
        \t>> Usinas().Filtrar(tipoReservatorio = ['M'])
        More than one filter can be used at the same time.
        '''

        def Filtro(item: int | str | list, nameColumn: str):
            if type(item) == int:
                if item > 0: DataFrameFiltrado = df[df[nameColumn] == item]
                else: DataFrameFiltrado = df
            if type(item) == str:
                DataFrameFiltrado = df[df[nameColumn] == item]
            if type(item) == list: 
                DataFrameFiltrado = df[df[nameColumn].apply(lambda x: x in item)]
            
            return DataFrameFiltrado


        codUsina = kwargs.get('codUsina')
        if codUsina: df = Filtro(codUsina, 'CodUsina')
        
        nameUsina = kwargs.get('nameUsina')
        if nameUsina: df = Filtro(nameUsina, 'Usina')
        
        subSistema = kwargs.get('subSistema')
        if subSistema: df = Filtro(item = subSistema, nameColumn = 'Sistema')
        
        tipoReservatorio = kwargs.get('tipoReservatorio')
        if tipoReservatorio: df = Filtro(tipoReservatorio, 'Reg')

        return df
    
    def Jusante(df, **kwargs):
        codUsina = kwargs.get('codUsina')
        if codUsina: Usinas.Filtrar(df, codUsina, 'codUsina')

        nomeUsina = kwargs.get('nameUsina')
        if nomeUsina: Usinas.Filtrar(df, nomeUsina, 'Usina')

        return df['Jusante'].replace('0 - NÃO HÁ', None)

