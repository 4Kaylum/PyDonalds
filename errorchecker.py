class McDonaldsException(Exception): pass


class ErrorChecker(object):

    ERRORS = {
        -1004: 'Login failed',
        -1126: 'Store is closed',
        -6057: 'Invalid payment method ID',
        -6008: 'Invalid order items',
        -1000: 'Invalid payment method ID for pickup'
    }

    @classmethod
    def check(cls, site):
        result_code = site.json()['ResultCode']
        v = cls.ERRORS.get(result_code, None)
        if v:
            raise McDonaldsException(v) 
        return 


    @classmethod
    def iserror(cls, site):
        try:
            cls.check(site)
        except McDonaldsException as e:
            return e 
        return False
