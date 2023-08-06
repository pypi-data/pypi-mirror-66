from string import ascii_lowercase

class sql_query :
    # Generic assign methods
    def where(self, wh=None, attr=None, cond=None, eq='=', d=False, clear=False) :
        '''

        Add one or more items for the WHERE statement of the sql query or clear the 
        WHERE statement at all.

        Args :
          wh (dict, optional) : A dictionary containing the information to build the 
            WHERE statement of the query.
            
            The dict should be build up like this: {attr: (cond, eq, d)}.
            attr stands for attribute, cond for condition, eq for equation and d for denial.
            
            The parts of the dict can also be given separately through the other
            parameters of this method. Check the descriptions below to get a better
            understanding of the accepted data types within the dictionary and what they
            are used for. Note that these arguments only support adding one key/value pair 
            at a time.

          attr (str, tuple, optional) : The field by which the resulting table should be filtered.
            
            In case you need to filter on multiple fields with an OR dependency (WHERE FldX = 'a' 
            OR FldY = 'b'), insert the fields as a tuple like this : ('FldX', 'FldY')
            If you choose to use this option, the cond parameter should also be a tuple.
            The eq and d parameter can still be strings. They will be internally translated to 
            tuples of the same lenght as attr. If you need different eq/d values for each attr,
            just use a tuple here as well instead of a str.

          cond (str, int, list, tuple, sql_query object, optional) : The value to filter within the
            given attr.

            Multiple datatypes can be given and will return a slightly different result.
            Here are some examples where we assume that the value 'FldX' is given as the attr
            and the other parameters are left as their default values.

            str: 'ValX'
            returns : WHERE FldX = 'ValX'

            int: 5
            returns : WHERE FldX = 5

            list: ['ValX', 'ValY']
            returns : WHERE (FldX = 'ValX' OR FldX = 'ValX')

            sql_query object : qry
            returns : WHERE FldX IN (str(qry)) <--- refer to the 'returns' section of the different
                                                    sql_query subclasses for an explanation of what
                                                    str(qry) will return.
            
            In case you need to filter on multiple fields with an OR dependency (WHERE FldX = 'a' 
            OR FldY = 'b'), insert the values as a tuple like this : ('a', 'b')

          eq (str, tuple, optional) : The operator for the WHERE statement. Can be filled with any
            valid operator for the SQL variant you use. examples are '='(equals), '>'(higher then),
            '<='(lower then or equal to) etc. Default = '='

            In case you need to filter on multiple fields with an OR dependency (WHERE FldX = 'a' 
            OR FldY < 3), insert the values as a tuple like this : ('=', '<').
            If both operators should be the same, it's enough to insert it as a single string as usual.

          d (bool, tuple, optional) : d indicates whether the WHERE statement should be denied. 
            When True, >WHERE FldX = 'a'< will become >WHERE NOT FldX = 'a'<. Default = False

            In case you need to filter on multiple fields with an OR dependency (WHERE FldX = 'a' 
            OR NOT FldY < 3), insert the values as a tuple like this : (False, True).
            If both denials should be the same, it's enough to insert it as a single boolean as usual.

          clear (bool, optional) : If True, the existing information for the WHERE 
            statement will be cleared before the new information is inserted. 
            Default=False
        '''
        
        if clear : self.wh = {} 
        
        if wh :
            self.wh = sql_query.mergeDict(self.wh, wh)
        
        if isinstance(attr, tuple) :
            l = len(attr)
            if not isinstance(eq, tuple) : eq = tuple([eq for i in range(l)])
            if not isinstance(d, tuple) : d = tuple([d for i in range(l)])

            wh = {attr: tuple([(cond[i], eq[i], d[i]) for i in range(l)])}
            self.wh = sql_query.mergeDict(self.wh, wh)

        elif attr :
            wh = {attr: (cond, eq, d)}
            self.wh = sql_query.mergeDict(self.wh, wh)

    # To string methods
    @classmethod
    def prep_filter_for_str(cls, start, items):
        '''
        Routine used to convert wh and hv attributes to the WHERE
        and HAVING parts of the resulting SQL query. Function is only
        used internally by the __str__ conversion and therefore not 
        documented any further.
        '''
        
        output = ''
        kw = start                              # kw for keyword
        for k, v in items.items() :
            if isinstance(k, tuple) :
                l = len(k)
                kw += ' ('
                for i in range(l) :
                    output += cls.filter_to_str(kw, k[i], v[i])
                    kw = 'OR'
                output += ')'
                kw = 'AND'
            else :
                if isinstance(v, tuple) :
                    output += cls.filter_to_str(kw, k, v)
                    kw = 'AND'
                elif isinstance(v, list) :
                    for v_in_l in v :
                        output += cls.filter_to_str(kw, k, v_in_l)
                        kw = 'AND'
        
        return output

    @staticmethod
    def filter_to_str(t, k, v) :
        '''
        Routine used to convert wh and hv attributes to the WHERE
        and HAVING parts of the resulting SQL query. Function is only
        used internally by the __str__ conversion and therefore not 
        documented any further.
        '''
        
        c = v[0]                                # c for condition
        eq = v[1]                               # eq for equation
        d = ' NOT ' if v[2] else ' '            # d for denial

        if c == 'NULL' :
            return ' {0} {1}{2}{3}'.format(t, k, d, c)
        elif isinstance(c, int) :
            return ' {0}{1}{2} {3} {4}'.format(t, d, k, eq, str(c))
        elif isinstance(c, str) :
            return ' {0}{1}{2} {3} "{4}"'.format(t, d, k, eq, c)
        elif isinstance(c, list) :
            if isinstance(c[0], str) :
                cond = '" OR {0} {1} "'.format(k, eq).join(c)
                return ' {0}{1}({2} {3} "{4}")'.format(t, d, k, eq, cond)
            elif isinstance(c[0], int) :
                c_to_txt = [str(x) for x in c]
                cond = ' OR {0} {1} '.format(k, eq).join(c_to_txt)
                return ' {0}{1}({2} {3} {4})'.format(t, d, k, eq, cond)                
        elif isinstance(c, tuple) :
            r = ' AND ' if d == ' ' else ' OR '
            return ' {t}({d}{k} >= {c0}{r}{d}{k} <= {c1})'.format(t=t, d=d, k=k, c0=c[0], c1=c[1], r=r)
        elif isinstance(c, sql_select) :
            eq = 'IN'
            return ' {0} {1}{2}{3} ({4})'.format(t, k, d, eq, str(c))

    # Other methods
    @staticmethod
    def mergeDict(dict1, dict2):
        '''Merge dictionaries and keep values of common keys in list'''
        dict3 = {**dict1, **dict2}
        for k, v in dict3.items():
            if k in dict1 and k in dict2:
                if dict1[k] != dict2[k] :
                    dict3[k] = [v , dict1[k]]
    
        return dict3

class sql_select(sql_query) :
    '''
    Use to build a basic SQL select query. 
    Supports the following elements of a SQL query:
    SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, JOIN

    args :
      sl (str, list) : The name of the field(s) to add to the SELECT statement 
        of the query.

      fr (str, sql_select object) : The name of the table to add to the FROM 
        statement of the query.
        
        Another sql_select object can be given. 
        The given object will be nested inside this query.

      wh (dict, optional) : A dictionary containing the information to build the 
        WHERE statement of the query.
        
        The dict should be build up like this: {attr: (cond, eq, d)}
        attr    : the field in the table to filter on.
        cond    : the value to filter.
        eq      : the comparison operator (=, >, <, etc.)
        d       : boolean indicating whether the statement should be True or False

        The sql_query.where() method provides an easier way to build up the WHERE 
        statement. It lets you insert all of the above elements separately and 
        has default values for the simplest queries. Refer to this method for more 
        information on what datatypes to use for different filtering purposes.

      gb (str, list, optional) : The name of the field(s) to add to the GROUP BY 
        statement of the query.

      hv (dict, optional) : A dictionary containing the information to build the 
        HAVING statement of the query.
        
        The dict should be build up like this: {attr: (cond, eq, d)}
        attr    : the field in the table to filter on.
        cond    : the value to filter.
        eq      : the comparison operator (=, >, <, etc.)
        d       : boolean indicating whether the statement should be True or False

        The sql_select.having() method provides an easier way to build up the HAVING 
        statement. It lets you insert all of the above elements separately and 
        has default values for the simplest queries. Refer to this method for more 
        information on what datatypes to use for different filtering purposes.

      ob (dict, optional) : A dictionary containing the information to build the 
        ORDER BY statement of the query. Insert the field(s) as key(s) and the 
        order (ASC, DESC) as value(s).

        The sql_select.order_by() method provides an easier way to build up the ORDER 
        BY statement. Refer to this method for more information on what datatypes to
        use.

      lm (int) : The maximum number of rows that should be loaded by the query. This
        value is used as the LIMIT statement of the query.
      
    returns :
      A sql_select object. Use the build-in str() function to turn this object into
        an actual SQL SELECT query which you can copy into your database browser or
        into query reader functions like pd.read_sql_query() or sqlalchemy's 
        engine.execute(text())

    notes :
      A JOIN statement can inserted through the sql_select.join() method. This 
        merges 2 sql_select objects together and uses one as the base and the other 
        one as JOIN statement.
    '''
    
    aliases = [letter1+letter2 for letter1 in ascii_lowercase for letter2 in ascii_lowercase]
    no_of_queries = 0
    
    def __init__(self, sl, fr, wh=None, gb=None, hv=None, ob=None, lm=None) :
        self.sl = sl if isinstance(sl, list) else [sl]
        self.fr = fr
        
        self.base = {self.fr: [self.sl, self.aliases[self.no_of_queries], 'FROM']}

        self.wh = {}
        if wh :
            self.where(wh)

        if gb :
            self.gb = gb if isinstance(gb, list) else [gb]

        self.hv = {}
        if hv :
            self.having(hv)
        
        self.ob = {}
        if ob :
            self.order_by(ob)

        if lm :
            self.lm = lm

        self.jn = {}
        
        sql_select.no_of_queries += 1

    def __str__(self) :
        if self.jn :  
            txt = 'SELECT {}'.format(', '.join(['{}.{}'.format(v[1], i) for k, v in self.base.items() for i in v[0]]))
            for k, v in self.base.items() :
                on = 'ON {}'.format(self.jn[k][1]) if v[2].endswith('JOIN') else ''
                if isinstance(k, sql_select) :
                    txt += ' {} ({}) AS {} {}'.format(v[2], str(k), v[1], on)
                else :
                    txt += ' {} {} AS {} {}'.format(v[2], k, v[1], on)
        else :
            if isinstance(self.fr, sql_select) :
                txt = 'SELECT {} FROM ({})'.format(', '.join(self.sl), str(self.fr))
            else :
                txt = 'SELECT {} FROM {}'.format(', '.join(self.sl), self.fr)

        if hasattr(self, 'wh') :
            txt += self.prep_filter_for_str('WHERE', self.wh)

        if hasattr(self, 'gb') :
            txt += ' GROUP BY {}'.format(','.join(self.gb))

        if hasattr(self, 'hv') :
            txt += self.prep_filter_for_str('HAVING', self.hv)

        if hasattr(self, 'ob') :
            o = 'ORDER BY'
            for k, v in self.ob.items() :
                txt += ' {0} {1} {2}'.format(o, k, v)
                o = ','
        
        if hasattr(self, 'lm') :
            txt += ' LIMIT {}'.format(self.lm)

        return txt
    
    # Select specific assign methods
    def select(self, sl, clear=False) :
        '''
        Change the SELECT statement of the sql query

        Args :
          sl (str, list) : Field(s) to at to the SELECT statement of the query.

          clear (bool, optional) : If True, the existing information for the SELECT statement 
            will be cleared before the new information is inserted. Default=False
        '''
        
        new = sl if isinstance(sl, list) else [sl]
        self.sl = new if clear else list(set(self.sl + new))
        self.base[self.fr][0] = self.sl
    
    def group_by(self, gb=None, clear=False) :
        '''
        Specify the GROUP BY statement of the sql query

        Args :
          gb (str, list, optional) : Field(s) to at to the GROUP BY statement of the query.
          
          clear (bool, optional) : If True, the existing information for the GROUP BY statement 
            will be cleared before the new information is inserted. Default=False
        
        Notes :
          If no argument is specified, the method will only clear the GROUP BY statement.
        '''
        
        if clear and hasattr(self, 'gb') : delattr(self, 'gb')
        
        if isinstance(gb, str) :
            if hasattr(self, 'gb') :
                self.gb.append(gb)
            else :
                self.gb = [gb]
        elif isinstance(gb, list) :
            if hasattr(self, 'gb') :
                for i in gb :
                    self.gb.append(gb)
            else :
                self.gb = gb
    
    def having(self, hv=None, attr=None, cond=None, eq='=', d=False, clear=False) :        
        '''
        Add one or more items for the HAVING statement of the sql query or clear the 
        HAVING statement at all. Refer to the sql_query.where() method for a more
        indepth description of the arguments, since these work exactly the same. 
        the hv argument is the same as the wh argument.

        Args :
          hv (dict, optional) : A dictionary containing the information to build the 
            HAVING statement of the query.

          attr (str, tuple, optional) : The field by which the resulting table should be filtered.

          cond (str, int, list, tuple, sql_query object, optional) : The value to filter within the
            given attr.

          eq (str, tuple, optional) : The operator for the HAVING statement. Can be filled with any
            valid operator for the SQL variant you use. examples are '='(equals), '>'(higher then),
            '<='(lower then or equal to) etc. Default = '='.

          d (bool, tuple, optional) : Indicates whether the HAVING statement should be denied. 
            When True, >HAVING FldX = 'a'< will become >HAVING NOT FldX = 'a'<. Default = False.

          clear (bool, optional) : If True, the existing information for the HAVING 
            statement will be cleared before the new information is inserted. 
            Default=False
        '''

        if clear : self.hv = {} 
        
        if hv :
            self.hv = sql_query.mergeDict(self.hv, hv)
        
        if isinstance(attr, tuple) :
            l = len(attr)
            if not isinstance(eq, tuple) : eq = tuple([eq for i in range(l)])
            if not isinstance(d, tuple) : d = tuple([d for i in range(l)])

            hv = {attr: tuple([(cond[i], eq[i], d[i]) for i in range(l)])}
            self.hv = sql_query.mergeDict(self.hv, hv)
        
        elif attr :
            hv = {attr: (cond, eq, d)}
            self.hv = sql_query.mergeDict(self.hv, hv)

    def order_by(self, ob=None, attr=None, asc=True, clear=False) :
        '''
        Specify the ORDER BY statement of the sql query

        Args :
          ob(dict, optional) : A dictionary with the fields as keys and the order (ASC/DESC) as values.
            if ob is specified, attr and asc parameters are ignored.
          
          attr(str, optional) : The field by which the resulting table should be ordered.

          asc(bool, optional) : True will order the field ascending, False will order descending. Default=True.

          clear(bool, optional) : If True, the existing information for the ORDER BY statement will be
            cleared before the new information is inserted. Default=False
        
        Notes :
          If no argument is specified, the method will only clear the ORDER BY statement.
        '''
        
        if clear : self.ob = {}
        if ob :
            self.ob.update(ob)
        elif attr :
            ordr = 'ASC' if asc else 'DESC'
            self.ob.update({attr: ordr})

    def limit(self, lm=None, clear=False) :
        '''
        Specify the LIMIT statement of the sql query

        Args :
          lm (int, optional) : Maximum number of rows to load with the sql query
          
          clear (bool, optional) : If True, the existing information for the LIMIT statement will be cleared 
            before the new information is inserted. Default=False
        
        Notes :
          If no argument is specified, the method will only clear the LIMIT statement.
        '''

        if clear and hasattr(self, 'lm') : delattr(self, 'lm')

        if lm : self.lm = lm
    
    def join(self, other, how, on, left_fr=None) :
        '''
        Combine two queries to create a JOIN statement.

        Args :
          other(sql_select object) : sql_select object to join upon the sql_select
            object this method is called upon. the table in the fr attribute will 
            become the table for the JOIN statement and the fields in the sl 
            attribute will be added to the sl attribute of the caller.

          how(str) : How the JOIN should be performed (LEFT, RIGHT, INNER, OUTER)

          on(tuple) : tuple containing the fields that should be matched. The first
            element should match a field in the caller sql_select object and the 
            second should match a field in the 'other' sql_select object.

          left_fr(str, sql_select object, optional) : This argument can be used in 
            the case where multiple joins have been performed on one sql_select object.
            Use this argument to specify the originating table of the field that is used
            as the first element of the tuple in the 'on' argument. By default, the caller
            is used.
        
        notes :
          The join method has only been tested properly with a sql_select object 
            that only contains a sl and fr attribute for the 'other' argument. Also 
            only single dimensional joins are supported in this version.
        '''

        other.base[other.fr][2] = f'{how.upper()} JOIN'
        self.base.update(other.base)

        if left_fr :
            left_on_prefix = self.base[left_fr][1]
        else :
            left_on_prefix = self.base[self.fr][1]

        on = f'{left_on_prefix}.{on[0]} = {other.base[other.fr][1]}.{on[1]}'
        self.jn.update({other.fr: [how, on]})

class sql_update(sql_query) :
    '''
    Use to build a basic SQL select query. 
    Supports the following elements of a SQL query:
    UPDATE, SET, WHERE

    args :
      up (str, list) : The name of the table to add to the UPDATE statement 
        of the query.

      st (dict, optional) : A dictionary containing the field(s) to update as key(s) 
        with the new value(s) as value(s)
        
        The sql_update.set_() method provides an easier way to build up the SET
        statement. Refer to this method for more information on what datatypes to 
        use.

      wh (dict, optional) : A dictionary containing the information to build the 
        WHERE statement of the query.
        
        The dict should be build up like this: {attr: (cond, eq, d)}
        attr    : the field in the table to filter on.
        cond    : the value to filter.
        eq      : the comparison operator (=, >, <, etc.)
        d       : boolean indicating whether the statement should be True or False

        The sql_query.where() method provides an easier way to build up the WHERE 
        statement. It lets you insert all of the above elements separately and 
        has default values for the simplest queries. Refer to this method for more 
        information on what datatypes to use for different filtering purposes.
      
    returns :
      A sql_update object. Use the build-in str() function to turn this object into
        an actual SQL UPDATE query which you can copy into your database browser or
        into query reader functions like sqlalchemy's engine.execute(text())
    '''

    def __init__(self, up, st=None, wh=None) :
        self.up = up

        self.st = {}
        if st :
            self.set_(st)

        self.wh = {}
        if wh :
            self.where(wh)
    
    def __str__(self):
        txt = 'UPDATE {} '.format(self.up)

        txt += 'SET {0} '.format(', '.join(['{0} = {1}'.format(k, '"{}"'.format(v) if isinstance(v, str) else v) for k,v in self.st.items()]))
        
        if hasattr(self, 'wh') :
            txt += self.prep_filter_for_str('WHERE', self.wh)

        return txt

    def set_(self, st=None, attr=None, val=None, clear=False) :
        '''
        Specify a SET statement of the sql query

        Args :
          st (dict, optional) : A dictionary with the field(s) to update as key(s) and the new
            value(s) to insert as value(s).

            The parts of the dict can also be given separately through the other
            parameters of this method. Note that these arguments only support 
            adding one key/value pair at a time.

          attr (str, optional) : The field to update

          val (str, int, optional) : The new value for the field to update.
         
          clear (bool, optional) : If True, the existing information for the SET statement will be cleared 
            before the new information is inserted. Default=False
        '''
        
        if clear : self.st = {} 

        if st :
            self.st.update(st)
        else :
            self.st.update({attr: val})        